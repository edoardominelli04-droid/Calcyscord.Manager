from config.game_config import CURRENT_SEASON

from services.database_manager import DatabaseManager
from services.providers.transfermarkt_provider import (
    TransfermarktProvider
)


class RosterImporter:
    """Costruisce le rose attuali dei club."""

    def __init__(self):

        self.db = DatabaseManager()

        self.provider = TransfermarktProvider()

    # ======================================================
    # STAGIONE DATASET
    # ======================================================

    def get_latest_dataset_season(self):

        games = self.provider.get_games()

        return int(
            games["season"].max()
        )

    # ======================================================
    # IMPORTAZIONE ROSE
    # ======================================================

    def import_rosters(self):

        dataset_season = self.get_latest_dataset_season()

        print(
            f"Importazione rose dal dataset stagione {dataset_season}..."
        )

        # ==================================================
        # MAPPING ID INTERNI
        # ==================================================

        clubs = self.db.get_clubs()

        players = self.db.get_players()

        club_map = {

            club["external_id"]: club["id"]

            for club in clubs

        }

        player_map = {

            player["external_id"]: player["id"]

            for player in players

        }

        # ==================================================
        # PARTITE DELL'ULTIMA STAGIONE
        # ==================================================

        games = self.provider.get_games()

        games = games[
            games["season"] == dataset_season
        ]

        print(
            f"Partite trovate: {len(games)}"
        )

        # ==================================================
        # PRESENZE
        # ==================================================

        appearances = self.provider.get_appearances()

        game_ids = set(
            games["game_id"]
        )

        appearances = appearances[
            appearances["game_id"].isin(game_ids)
        ]

        print(
            f"Presenze trovate: {len(appearances)}"
        )

        # ==================================================
        # COSTRUZIONE ROSE
        # ==================================================

        rosters = {}

        for _, appearance in appearances.iterrows():

            club_external_id = int(
                appearance["player_current_club_id"]
            )

            player_external_id = int(
                appearance["player_id"]
            )

            if club_external_id not in club_map:
                continue

            if player_external_id not in player_map:
                continue

            club_id = club_map[
                club_external_id
            ]

            player_id = player_map[
                player_external_id
            ]

            if club_id not in rosters:

                rosters[club_id] = set()

            rosters[club_id].add(
                player_id
            )

        # ==================================================
        # CONVERSIONE JSON
        # ==================================================

        current_rosters = []

        for club_id, players in rosters.items():

            current_rosters.append({

                "club_id": club_id,

                "season": CURRENT_SEASON,

                "players": sorted(
                    list(players)
                )

            })

        self.db.save_current_rosters(
            current_rosters
        )

        print(
            f"Rose salvate: {len(current_rosters)}"
        )

        return current_rosters