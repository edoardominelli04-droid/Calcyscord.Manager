from services.database_manager import DatabaseManager
from services.game.contract_service import ContractService


class SquadService:
    """Gestisce le rose dei club."""

    def __init__(self):
        self.db = DatabaseManager()
        self.contract_service = ContractService()

    def get_all(self):
        return self.db.get_squads()

    def save_all(self, squads):
        self.db.save_squads(squads)

    def get_manager_players(self, manager_id):
        return [
            player
            for player in self.get_all()
            if player["manager_id"] == manager_id
        ]

    def create_initial_squad(self, manager_id, club_id):

        if self.get_manager_players(manager_id):
            raise ValueError("Il manager possiede già una rosa.")

        players = self.db.get_players()

        squad = []

        for player in players:

            if player["club_id"] != club_id:
                continue

            contract = self.contract_service.create_contract(
                player,
                manager_id
            )

            contract_id = None

            if contract is not None:
                contract_id = contract["id"]

            squad.append({
                "manager_id": manager_id,
                "club_id": club_id,
                "player_id": player["id"],
                "contract_id": contract_id,
                "status": "active"
            })

        squads = self.get_all()
        squads.extend(squad)

        self.save_all(squads)

        return squad