import copy
import math
from datetime import datetime

from services.database_manager import DatabaseManager
from services.game.player_service import PlayerService
from services.game.manager_service import ManagerService
from services.game.formation_service import FormationService


class InitialSquadService:
    """Gestisce la composizione della rosa iniziale."""

    DEFAULT_BUDGET = 100

    PRICING_VERSION = 3

    MAX_GOALKEEPERS = 2

    TIER_COSTS = {
        "S": 10,
        "A": 7,
        "B": 5,
        "C": 3,
        "D": 1
    }

    MAX_S_PLAYERS = 2
    MAX_PREMIUM_PLAYERS = 6

    def __init__(self):

        self.db = DatabaseManager()

        self.player_service = PlayerService()

        self.manager_service = ManagerService()

        self.formation_service = FormationService()

    # ==========================================================
    # DATABASE
    # ==========================================================

    def get_all(self):

        return self.db.get_initial_squad_drafts()

    def save_all(self, drafts):

        self.db.save_initial_squad_drafts(drafts)

    # ==========================================================
    # BOZZA
    # ==========================================================

    def get_draft(self, manager_id):

        for draft in self.get_all():

            if draft["manager_id"] == manager_id:

                self._ensure_pricing_snapshot(
                    draft
                )

                return draft

        return None

    def create_draft(self, manager_id, club_id):

        if self.get_draft(manager_id):

            return self.get_draft(manager_id)

        draft = {

            "manager_id": manager_id,

            "club_id": club_id,

            "budget": self.DEFAULT_BUDGET,

            "points_used": 0,

            "players": [],

            "pricing": self._build_pricing_snapshot(
                club_id
            ),

            "pricing_version": self.PRICING_VERSION,

            "confirmed": False

        }

        drafts = self.get_all()

        drafts.append(draft)

        self.save_all(drafts)

        return draft

    # ==========================================================
    # FASCE E COSTI CONGELATI
    # ==========================================================

    def _safe_market_value(self, player):

        value = player.get("market_value") or 0

        if isinstance(value, float) and math.isnan(value):
            return 0

        return max(0, int(value))

    def _build_pricing_snapshot(self, club_id):

        club_players = self.player_service.get_current_players(
            club_id
        )

        by_role = {
            "Goalkeeper": [],
            "Defender": [],
            "Midfield": [],
            "Attack": []
        }

        for player in club_players:

            role = player.get("position")

            if role not in by_role:
                continue

            by_role[role].append(
                player
            )

        ranked_players = []

        for role, players in by_role.items():

            role_ranking = sorted(
                players,
                key=self._safe_market_value,
                reverse=True
            )

            total = len(role_ranking)

            for index, player in enumerate(role_ranking):

                if total <= 1:
                    role_score = 1.0
                else:
                    role_score = 1 - (index / (total - 1))

                ranked_players.append((
                    role_score,
                    self._safe_market_value(player),
                    player
                ))

        ranked_players.sort(
            key=lambda item: (item[0], item[1]),
            reverse=True
        )

        extra_b_slots = min(
            4,
            max(0, len(ranked_players) - 20)
        )

        b_limit = 12 + extra_b_slots

        c_limit = b_limit + 6

        pricing = {}

        for index, (_, _, player) in enumerate(ranked_players):

            if index < 2:
                tier = "S"
            elif index < 6:
                tier = "A"
            elif index < b_limit:
                tier = "B"
            elif index < c_limit:
                tier = "C"
            else:
                tier = "D"

            pricing[str(player["id"])] = {
                "tier": tier,
                "cost": self.TIER_COSTS[tier]
            }

        return pricing

    def _ensure_pricing_snapshot(self, draft):

        changed = False

        if (
            not draft.get("pricing")
            or draft.get("pricing_version") != self.PRICING_VERSION
        ):

            draft["pricing"] = self._build_pricing_snapshot(
                draft["club_id"]
            )

            draft["pricing_version"] = self.PRICING_VERSION

            changed = True

        if draft.get("budget") != self.DEFAULT_BUDGET:

            draft["budget"] = self.DEFAULT_BUDGET

            changed = True

        points_used = sum(
            draft["pricing"].get(str(player_id), {}).get("cost", 0)
            for player_id in draft.get("players", [])
        )

        if draft.get("points_used") != points_used:

            draft["points_used"] = points_used

            changed = True

        if changed:

            self.save(
                draft
            )

    def get_player_pricing(self, manager_id, player_id):

        draft = self.get_draft(
            manager_id
        )

        if draft is None:
            return {"tier": "D", "cost": 1}

        return draft["pricing"].get(
            str(player_id),
            {"tier": "D", "cost": 1}
        )

    def get_tier_counts(self, manager_id):

        draft = self.get_draft(
            manager_id
        )

        counts = {
            "S": 0,
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0
        }

        if draft is None:
            return counts

        for player_id in draft.get("players", []):

            pricing = self.get_player_pricing(
                manager_id,
                player_id
            )

            counts[pricing["tier"]] += 1

        return counts

    def save(self, draft):

        drafts = self.get_all()

        for index, current in enumerate(drafts):

            if current["manager_id"] == draft["manager_id"]:

                drafts[index] = draft

                break

        self.save_all(drafts)

    # ==========================================================
    # AGGIUNTA GIOCATORE
    # ==========================================================

    def add_player(
        self,
        manager_id,
        player_id
    ):

        added, _ = self.try_add_player(
            manager_id,
            player_id
        )

        return added

    def try_add_player(
        self,
        manager_id,
        player_id
    ):

        draft = self.get_draft(
            manager_id
        )

        if draft is None:

            raise ValueError(
                "Bozza non trovata."
            )

        if draft.get("confirmed"):

            return False, "La rosa è già stata confermata."

        if player_id in draft["players"]:

            return False, "Giocatore già selezionato."

        player = self.player_service.players_by_id.get(
            player_id
        )

        if player is None:

            return False, "Giocatore non trovato."

        current_player_ids = {

            current_player["id"]

            for current_player in self.player_service.get_current_players(
                draft["club_id"]
            )

        }

        if player_id not in current_player_ids:

            return False, "Il giocatore non appartiene alla rosa attuale del club."

        role = player.get("position")

        rules = self.get_rules()

        valid_roles = (
            "Goalkeeper",
            "Defender",
            "Midfield",
            "Attack"
        )

        if role not in valid_roles:

            return False, "Ruolo del giocatore non valido."

        counts = self.get_role_counts(
            manager_id
        )

        if role == "Goalkeeper" and (
            counts.get(role, 0) >= self.MAX_GOALKEEPERS
        ):

            return False, "Puoi selezionare al massimo 2 portieri."

        total_required = sum(
            rules.values()
        )

        total_selected = sum(
            counts.values()
        )

        if total_selected >= total_required:

            return False, "Hai già raggiunto il limite di 20 giocatori."

        projected_counts = dict(
            counts
        )

        projected_counts[role] += 1

        remaining_slots = total_required - total_selected - 1

        minimums_still_needed = sum(

            max(
                0,
                rules[required_role] - projected_counts[required_role]
            )

            for required_role in valid_roles

        )

        if minimums_still_needed > remaining_slots:

            return (
                False,
                "Devi conservare gli ultimi posti per completare gli altri reparti."
            )

        pricing = self.get_player_pricing(
            manager_id,
            player_id
        )

        projected_points = (
            draft["points_used"] + pricing["cost"]
        )

        if projected_points > draft["budget"]:

            return False, "Non hai abbastanza stelle disponibili."

        tier_counts = self.get_tier_counts(
            manager_id
        )

        if (
            pricing["tier"] == "S"
            and tier_counts["S"] >= self.MAX_S_PLAYERS
        ):

            return False, "Puoi selezionare al massimo 2 giocatori di fascia S."

        premium_count = (
            tier_counts["S"] + tier_counts["A"]
        )

        if (
            pricing["tier"] in ("S", "A")
            and premium_count >= self.MAX_PREMIUM_PLAYERS
        ):

            return False, "Puoi selezionare al massimo 6 giocatori tra fascia S e A."

        draft["players"].append(
            player_id
        )

        draft["points_used"] = projected_points

        self.save(
            draft
        )

        return True, None

    # ==========================================================
    # RIMOZIONE GIOCATORE
    # ==========================================================

    def remove_player(
        self,
        manager_id,
        player_id
    ):

        draft = self.get_draft(
            manager_id
        )

        if draft is None or draft.get("confirmed"):

            return False

        if player_id not in draft["players"]:

            return False

        draft["players"].remove(
            player_id
        )

        pricing = self.get_player_pricing(
            manager_id,
            player_id
        )

        draft["points_used"] = max(
            0,
            draft["points_used"] - pricing["cost"]
        )

        self.save(
            draft
        )

        return True

    def get_selected_players(
        self,
        manager_id,
        role=None
    ):

        draft = self.get_draft(
            manager_id
        )

        if draft is None:

            return []

        players = []

        for player_id in draft["players"]:

            player = self.player_service.players_by_id.get(
                player_id
            )

            if player is None:
                continue

            if role is not None and player.get("position") != role:
                continue

            players.append(
                player
            )

        return players
    
    # ==========================================================
    # STATISTICHE BOZZA
    # ==========================================================

    def get_role_counts(
        self,
        manager_id
    ):

        draft = self.get_draft(manager_id)

        if draft is None:

            return {
                "Goalkeeper": 0,
                "Defender": 0,
                "Midfield": 0,
                "Attack": 0
            }

        counts = {

            "Goalkeeper": 0,
            "Defender": 0,
            "Midfield": 0,
            "Attack": 0

        }

        players = {

            player["id"]: player

            for player in self.db.get_players()

        }

        for player_id in draft["players"]:

            player = players.get(player_id)

            if player is None:
                continue

            role = player["position"]

            if role in counts:

                counts[role] += 1

        return counts
    
    # ==========================================================
    # REGOLE ROSA
    # ==========================================================

    def get_rules(self):

        return self.db.get_config_file(
            "initial_squad_rules.json"
        )
    
    # ==========================================================
    # REPARTO COMPLETATO
    # ==========================================================

    def is_role_complete(
        self,
        manager_id,
        role
    ):

        counts = self.get_role_counts(
            manager_id
        )

        rules = self.get_rules()

        required = rules.get(
            role,
            0
        )

        return counts.get(
            role,
            0
        ) >= required

    # ==========================================================
    # ROSA COMPLETA
    # ==========================================================

    def is_squad_complete(
        self,
        manager_id
    ):

        counts = self.get_role_counts(
            manager_id
        )

        rules = self.get_rules()

        total_required = sum(
            rules.values()
        )

        total_selected = sum(
            counts.values()
        )

        required_roles = (
            "Goalkeeper",
            "Defender",
            "Midfield",
            "Attack"
        )

        minimums_completed = all(

            counts[role] >= rules[role]

            for role in required_roles

        )

        return (
            total_selected == total_required
            and minimums_completed
        )

    # ==========================================================
    # CONFERMA DEFINITIVA
    # ==========================================================

    def _build_contract(self, player, manager_id, contract_id):

        market_value = self._safe_market_value(
            player
        )

        salary = max(
            50000,
            int(market_value * 0.08)
        )

        current_year = datetime.now().year

        return {
            "id": contract_id,
            "player_id": player["id"],
            "manager_id": manager_id,
            "type": "professional",
            "is_loan": False,
            "signed_at": datetime.now().isoformat(),
            "expires_at": None,
            "start_season": current_year,
            "end_season": current_year + 3,
            "salary": salary,
            "transfer_fee": 0,
            "release_clause": None,
            "origin_club_id": player.get("club_id"),
            "contract_version": 1,
            "contract_notes": "Rosa iniziale",
            "renewable": True,
            "status": "active"
        }

    def _validate_confirmation(self, manager_id):

        draft = self.get_draft(
            manager_id
        )

        if draft is None:
            return False, "Bozza della rosa non trovata."

        if draft.get("confirmed"):
            return False, "La rosa è già stata confermata."

        if not self.is_squad_complete(manager_id):
            return False, "La rosa deve contenere 20 giocatori validi."

        if draft["points_used"] > draft["budget"]:
            return False, "Il budget di 100 punti è stato superato."

        tier_counts = self.get_tier_counts(
            manager_id
        )

        if tier_counts["S"] > self.MAX_S_PLAYERS:
            return False, "Sono presenti più di 2 giocatori di fascia S."

        if (
            tier_counts["S"] + tier_counts["A"]
            > self.MAX_PREMIUM_PLAYERS
        ):
            return False, "Sono presenti più di 6 giocatori tra fascia S e A."

        if len(set(draft["players"])) != len(draft["players"]):
            return False, "La rosa contiene giocatori duplicati."

        current_player_ids = {
            player["id"]
            for player in self.player_service.get_current_players(
                draft["club_id"]
            )
        }

        unavailable = [
            player_id
            for player_id in draft["players"]
            if player_id not in current_player_ids
        ]

        if unavailable:
            return False, "Uno o più giocatori non sono più disponibili nel club."

        assigned_to_others = {
            member["player_id"]
            for member in self.db.get_squads()
            if (
                member["manager_id"] != manager_id
                and member.get("status") == "active"
            )
        }

        if any(
            player_id in assigned_to_others
            for player_id in draft["players"]
        ):
            return False, "Uno dei giocatori è già assegnato a un altro manager."

        return True, None

    def confirm_squad(self, manager_id):

        valid, error = self._validate_confirmation(
            manager_id
        )

        if not valid:
            return False, error

        draft = self.get_draft(
            manager_id
        )

        manager = self.manager_service.get_by_id(
            manager_id
        )

        if manager is None:
            return False, "Manager non trovato."

        snapshots = {
            "squads": copy.deepcopy(self.db.get_squads()),
            "contracts": copy.deepcopy(self.db.get_contracts()),
            "formations": copy.deepcopy(self.db.get_formations()),
            "managers": copy.deepcopy(self.db.get_managers()),
            "drafts": copy.deepcopy(self.get_all())
        }

        try:

            selected_players = [
                self.player_service.players_by_id[player_id]
                for player_id in draft["players"]
            ]

            contracts = [
                contract
                for contract in snapshots["contracts"]
                if contract["manager_id"] != manager_id
            ]

            next_contract_id = max(
                (contract["id"] for contract in contracts),
                default=0
            ) + 1

            new_contracts = []

            for player in selected_players:

                contract = self._build_contract(
                    player,
                    manager_id,
                    next_contract_id
                )

                next_contract_id += 1

                contracts.append(contract)
                new_contracts.append(contract)

            squads = [
                member
                for member in snapshots["squads"]
                if member["manager_id"] != manager_id
            ]

            for player, contract in zip(
                selected_players,
                new_contracts
            ):

                squads.append({
                    "manager_id": manager_id,
                    "club_id": draft["club_id"],
                    "player_id": player["id"],
                    "contract_id": contract["id"],
                    "status": "active"
                })

            self.db.save_contracts(contracts)
            self.db.save_squads(squads)

            formations = [
                formation
                for formation in snapshots["formations"]
                if formation["manager_id"] != manager_id
            ]

            self.db.save_formations(formations)

            self.formation_service.create_initial_formation(
                manager_id
            )

            manager["onboarding_status"] = "active"
            self.manager_service.save(manager)

            draft["confirmed"] = True
            draft["confirmed_at"] = datetime.now().isoformat()
            draft["points_remaining"] = 0
            draft["statement_status"] = "pending"

            self.save(draft)

        except Exception as exception:

            self.db.save_squads(snapshots["squads"])
            self.db.save_contracts(snapshots["contracts"])
            self.db.save_formations(snapshots["formations"])
            self.db.save_managers(snapshots["managers"])
            self.db.save_initial_squad_drafts(snapshots["drafts"])

            return False, f"Conferma non riuscita: {exception}"

        return True, "Rosa confermata correttamente."
