from services.database_manager import DatabaseManager
from services.game.module_service import ModuleService
from services.game.data.position_rules import POSITION_RULES
from services.utils.slot_utils import SlotUtils


class FormationService:
    """Gestisce le formazioni dei manager."""

    def __init__(self):
        self.db = DatabaseManager()
        self.module_service = ModuleService()

    # ==========================================================
    # DATABASE
    # ==========================================================

    def get_all(self):
        return self.db.get_formations()

    def save_all(self, formations):
        self.db.save_formations(formations)

    # ==========================================================
    # GET
    # ==========================================================

    def get_manager_formation(self, manager_id):

        for formation in self.get_all():

            if formation["manager_id"] == manager_id:
                return formation

        return None
    
    # ==========================================================
    # BUILD FORMAZIONE
    # ==========================================================

    def _build_formation(
        self,
        manager_id,
        module_name
    ):

        slots = self.module_service.get_slots(
            module_name
       )

        squad = [

            player

            for player in self.db.get_squads()

            if player["manager_id"] == manager_id

        ]

        players = []

        for squad_player in squad:

            player = self.db.get_player_by_id(
                squad_player["player_id"]
            )

            if player is not None:
                players.append(player)

        starting = {}

        used_players = set()

        for slot in slots:

            family = SlotUtils.family(slot)

            wanted_positions = POSITION_RULES[family]

            selected = None

            # Cerca prima il sottoruolo ideale

            for player in players:

                if player["id"] in used_players:
                    continue

                if (
                    player.get("sub_position")
                    in wanted_positions
                ):
                    selected = player
                    break

            # Fallback sul ruolo principale

            if selected is None:

                category = SlotUtils.department(
                    slot
                )

                for player in players:

                    if player["id"] in used_players:
                        continue

                    if (
                        player.get("position")
                        == category
                    ):
                        selected = player
                        break

            if selected is None:
                continue

            starting[slot] = {

                "player_id": selected["id"],

                "captain": False,

                "vice_captain": False

            }

            used_players.add(
                selected["id"]
            )

        bench = []

        for player in players:

            if player["id"] not in used_players:
                bench.append(player["id"])

        formation = {

            "manager_id": manager_id,

            "module": module_name,

            "starting": starting,

            "bench": bench

        }

        return formation

    # ==========================================================
    # CREAZIONE FORMAZIONE
    # ==========================================================

    def create_initial_formation(
        self,
        manager_id,
        module_name=None
    ):

        if self.get_manager_formation(manager_id):
            raise ValueError(
                "La formazione esiste già."
            )

        if module_name is None:
            module_name = (
                self.module_service.DEFAULT_MODULE
            )

        formation = self._build_formation(
            manager_id,
            module_name
        )

        formations = self.get_all()

        formations.append(
            formation
        )

        self.save_all(
            formations
        )

        return formation

    # ==========================================================
    # STARTING
    # ==========================================================

    def get_starting_players(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return {}

        return formation["starting"]

    # ==========================================================
    # PANCHINA
    # ==========================================================

    def get_bench_players(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return []

        return formation["bench"]

    # ==========================================================
    # CREAZIONE FORMAZIONE
    # ==========================================================

    def create_initial_formation(
        self,
        manager_id,
        module_name=None
    ):

        if self.get_manager_formation(manager_id):
            raise ValueError(
                "La formazione esiste già."
            )

        if module_name is None:
            module_name = (
                self.module_service.DEFAULT_MODULE
            )

        formation = self._build_formation(
            manager_id,
            module_name
        )

        formations = self.get_all()

        formations.append(
            formation
        )

        self.save_all(
            formations
        )

        return formation

    # ==========================================================
    # CAMBIO MODULO
    # ==========================================================

    def change_module(
        self,
        manager_id,
        module_name
    ):

        current = self.get_manager_formation(
            manager_id
        )

        if current is None:
            raise ValueError(
                "Formazione non trovata."
            )

        # Verifica che il modulo esista
        self.module_service.get_module(
            module_name
        )

        new_formation = self._build_formation(
            manager_id,
            module_name
        )

        # Mantiene capitano e vicecapitano
        # se il giocatore resta titolare

        for slot, data in new_formation["starting"].items():

            player_id = data["player_id"]

            for old_slot, old_data in current[
                "starting"
            ].items():

                if (
                    old_data["player_id"]
                    == player_id
                ):

                    data["captain"] = old_data[
                        "captain"
                    ]

                    data["vice_captain"] = old_data[
                        "vice_captain"
                    ]

                    break

        formations = self.get_all()

        for index, formation in enumerate(
            formations
        ):

            if (
                formation["manager_id"]
                == manager_id
            ):

                formations[index] = new_formation
                break

        self.save_all(
            formations
        )

        return new_formation

    # ==========================================================
    # SLOT
    # ==========================================================

    def get_slot_player(
        self,
        manager_id,
        slot
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return None

        return formation["starting"].get(slot)

    def set_slot_player(
        self,
        manager_id,
        slot,
        player_id
    ):

        formations = self.get_all()

        for formation in formations:

            if formation["manager_id"] != manager_id:
                continue

            formation["starting"][slot] = {

                "player_id": player_id,

                "captain": False,

                "vice_captain": False

            }

            self.save_all(
                formations
            )

            return formation

        return None
    
    # ==========================================================
    # PLAYER HELPERS
    # ==========================================================

    def get_starting_players_full(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return {}

        players = {}

        for slot, data in formation["starting"].items():

            player = self.db.get_player_by_id(
                data["player_id"]
            )

            if player is None:
                continue

            players[slot] = {
                "player": player,
                "captain": data["captain"],
                "vice_captain": data["vice_captain"]
            }

        return players

    def get_bench_players_full(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return []

        bench = []

        for player_id in formation["bench"]:

            player = self.db.get_player_by_id(
                player_id
            )

            if player is not None:
                bench.append(player)

        return bench