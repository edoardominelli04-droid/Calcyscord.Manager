import math

from services.database_manager import DatabaseManager


class PlayerService:
    """Gestisce la ricerca dei giocatori appartenenti alla rosa attuale."""

    def __init__(self):

        self.db = DatabaseManager()

        # ======================================================
        # CACHE GIOCATORI
        # ======================================================

        self.players_by_id = {

            player["id"]: player

            for player in self.db.get_players()

        }

        # ======================================================
        # CACHE ROSE
        # ======================================================

        self.rosters_by_club = {

            roster["club_id"]: roster

            for roster in self.db.get_current_rosters()

        }

    # ==========================================================
    # ROSA ATTUALE
    # ==========================================================

    def get_current_players(
        self,
        club_id
    ):

        roster = self.rosters_by_club.get(
            club_id
        )

        if roster is None:
            return []

        current_players = []

        for player_id in roster["players"]:

            player = self.players_by_id.get(
                player_id
            )

            if player is None:
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

            market_value = player.get(
                "market_value"
            )

            if (
                isinstance(market_value, float)
                and math.isnan(market_value)
            ):
                player["market_value"] = 0

            current_players.append(
                player
            )

        return current_players

    # ==========================================================
    # REPARTI
    # ==========================================================

    def get_goalkeepers(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_current_players(
                club_id
            )

            if player["position"] == "Goalkeeper"

        ]

    def get_defenders(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_current_players(
                club_id
            )

            if player["position"] == "Defender"

        ]

    def get_midfielders(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_current_players(
                club_id
            )

            if player["position"] == "Midfield"

        ]

    def get_forwards(
        self,
        club_id
    ):

        return [

            player

            for player in self.get_current_players(
                club_id
            )

            if player["position"] == "Attack"

        ]