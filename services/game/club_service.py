from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.finance_service import FinanceService
from services.game.squad_service import SquadService
from datetime import datetime


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
    
    def get_player_owner(
        self,
        player_id
    ):

        squads = self.db.get_squads()

        ownership = self.db.get_club_ownership()

        for member in squads:

            if member["player_id"] != player_id:
                continue

            manager = self.db.get_manager_by_id(

                member["manager_id"]

            )

            if manager is None:
                break

            club = self.db.get_club_by_id(

                manager["club_id"]

            )

            return {

                "manager": manager,

                "club": club,

                "is_bot": False

            }

        player = self.db.get_player_by_id(

            player_id

        )

        if player is None:

            return None

        club = self.db.get_club_by_id(

            player["club_id"]

        )

        manager = None

        for record in ownership:

            if record["club_id"] == club["id"]:

                manager = self.db.get_manager_by_id(

                    record["manager_id"]

                )

                break

        return {

            "manager": manager,

            "club": club,

            "is_bot": manager is None

        }
    
    def is_player_owned_by_manager(
        self,
        manager_id,
        player_id
    ):

        squad = self.db.get_squads()

        for member in squad:

            if (
                member["manager_id"] == manager_id
                and member["player_id"] == player_id
            ):

                return True

        return False
    
    # ==========================================================
    # GESTIONE CLUB
    # ==========================================================

    def get_club_owner(
        self,
        club_id
    ):

        ownership = self.db.get_club_ownership()

        for record in ownership:

            if record["club_id"] != club_id:
                continue

            if record["manager_id"] is None:

                return None

            return self.db.get_manager_by_id(

                record["manager_id"]

            )

        return None

    def is_bot_controlled(
        self,
        club_id
    ):

        return self.get_club_owner(

            club_id

        ) is None

    def assign_club_to_manager(
        self,
        club_id,
        manager_id
    ):

        ownership = self.db.get_club_ownership()

        for record in ownership:

            if record["club_id"] == club_id:

                if record["manager_id"] != manager_id:

                    record["last_manager_id"] = record["manager_id"]

                record["manager_id"] = manager_id

                record["assigned_at"] = datetime.utcnow().isoformat()

                self.db.save_club_ownership(

                    ownership

                )

                return

    def release_club(
        self,
        club_id
    ):

        ownership = self.db.get_club_ownership()

        for record in ownership:

            if record["club_id"] == club_id:

                record["last_manager_id"] = record["manager_id"]
                
                record["manager_id"] = None

                record["assigned_at"] = None

                self.db.save_club_ownership(

                    ownership

                )

                return

    def initialize_club_ownership(
        self
    ):

        clubs = self.db.get_clubs()

        ownership = self.db.get_club_ownership()

        existing = {

            record["club_id"]

            for record in ownership

        }

        changed = False

        for club in clubs:

            if club["id"] in existing:

                continue

            ownership.append(

                {

                    "club_id": club["id"],

                    "manager_id": None,

                    "assigned_at": None,

                    "last_manager_id": None

                }

            )

            changed = True

        if changed:

            self.db.save_club_ownership(

                ownership

            )