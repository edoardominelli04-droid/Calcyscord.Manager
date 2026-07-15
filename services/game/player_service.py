import math

from services.database_manager import DatabaseManager


class PlayerService:
    """Gestisce la ricerca e il filtraggio dei giocatori."""

    def __init__(self):

        self.db = DatabaseManager()

    # ==========================================================
    # STAGIONE
    # ==========================================================

    def get_latest_season(self):

        clubs = self.db.get_clubs()

        seasons = [

            club["last_season"]

            for club in clubs

            if club.get("last_season") is not None

        ]

        if not seasons:

            return None

        return max(seasons)

    # ==========================================================
    # GIOCATORI ELEGGIBILI
    # ==========================================================

    def get_eligible_players(
        self,
        club_id
    ):

        latest_season = self.get_latest_season()

        players = self.db.get_players()

        eligible = []

        for player in players:

            if player.get("club_id") != club_id:
                continue

            if player.get("last_season") != latest_season:
                continue

            if not player.get("active", True):
                continue

            if player.get("status") != "available":
                continue

            position = player.get("position")

            if position not in (
                "Goalkeeper",
                "Defender",
                "Midfield",
                "Attack"
            ):
                continue

            market_value = player.get("market_value")

            if isinstance(market_value, float):

                if math.isnan(market_value):

                    player["market_value"] = 0

            eligible.append(player)

        return eligible

    # ==========================================================
    # REPARTI
    # ==========================================================

    def get_goalkeepers(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_eligible_players(club_id)

            if player["position"] == "Goalkeeper"

        ]

    def get_defenders(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_eligible_players(club_id)

            if player["position"] == "Defender"

        ]

    def get_midfielders(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_eligible_players(club_id)

            if player["position"] == "Midfield"

        ]

    def get_forwards(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_eligible_players(club_id)

            if player["position"] == "Attack"

        ]