from services.database_manager import DatabaseManager
from services.game.player_service import PlayerService


class InitialSquadService:
    """Gestisce la composizione della rosa iniziale."""

    DEFAULT_BUDGET = 100

    def __init__(self):

        self.db = DatabaseManager()

        self.player_service = PlayerService()

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

            "confirmed": False

        }

        drafts = self.get_all()

        drafts.append(draft)

        self.save_all(drafts)

        return draft

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

        draft = self.get_draft(
            manager_id
        )

        if draft is None:

            raise ValueError(
                "Bozza non trovata."
            )

        if player_id in draft["players"]:

            return False

        draft["players"].append(
            player_id
        )

        self.save(
            draft
        )

        return True
    
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