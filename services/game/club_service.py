from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.finance_service import FinanceService
from services.game.squad_service import SquadService


class ClubService:
    """Gestisce tutte le informazioni del club."""

    def __init__(self):
        self.db = DatabaseManager()

        self.manager_service = ManagerService()
        self.finance_service = FinanceService()
        self.squad_service = SquadService()

    def get_manager_club(self, discord_id):

        manager = self.manager_service.get_by_discord_id(discord_id)

        if manager is None:
            raise ValueError("Manager non trovato.")

        if manager["club_id"] is None:
            raise ValueError("Non possiedi ancora un club.")

        finance = self.finance_service.get_finance(
            manager["id"]
        )

        club = self.db.get_club_by_id(
            manager["club_id"]
        )

        competition = self.db.get_competition_by_id(
            club["competition_id"]
        )

        stadium = self.db.get_stadium_by_id(
            club["stadium_id"]
        )

        squad = self.squad_service.get_manager_players(
            manager["id"]
        )

        squad_players = []

        for member in squad:

            player = self.db.get_player_by_id(
                member["player_id"]
            )

            if player:
                squad_players.append(player)

        market_value = sum(
            p.get("market_value", 0) or 0
            for p in squad_players
        )

        average_age = (
            round(
                sum(
                    p.get("age", 0) or 0
                    for p in squad_players
                ) / len(squad_players),
                1
            )
            if squad_players else 0
        )

        most_valuable = None

        if squad_players:
            most_valuable = max(
                squad_players,
                key=lambda p: p.get("market_value", 0) or 0
            )

        return {
            "manager": manager,
            "finance": finance,
            "club": club,
            "competition": competition,
            "stadium": stadium,
            "players": squad_players,
            "players_count": len(squad_players),
            "average_age": average_age,
            "market_value": market_value,
            "most_valuable_player": most_valuable
        }

    def get_all_players(
        self
    ):

        return self.db.get_players()