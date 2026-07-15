from services.database_manager import DatabaseManager
from services.providers.transfermarkt_provider import TransfermarktProvider
from services.mappers.player_mapper import PlayerMapper
from services.normalizers.country_normalizer import CountryNormalizer


class PlayerImporter:
    """Importa i giocatori dal dataset Transfermarkt."""

    def __init__(self):
        self.db = DatabaseManager()
        self.provider = TransfermarktProvider()

    def import_players(self):

        clubs = self.db.get_clubs()
        countries = self.db.get_countries()

        enabled_club_ids = {
            club["external_id"]: club
            for club in clubs
        }

        country_by_name = {
            country["name"].strip().lower(): country["id"]
            for country in countries
            if country.get("name")
        }

        players_df = self.provider.get_players()

        players = []

        next_id = 1

        for _, row in players_df.iterrows():

            club_external_id = row["current_club_id"]

            if club_external_id not in enabled_club_ids:
                continue

            player = PlayerMapper.from_transfermarkt(
                row,
                next_id
            )

            club = enabled_club_ids[club_external_id]

            # ======================================================
            # COLLEGAMENTI INTERNI
            # ======================================================

            player["club_id"] = club["id"]

            player["competition_id"] = club["competition_id"]

            # ======================================================
            # ULTIMA STAGIONE DISPONIBILE
            # ======================================================

            player["last_season"] = club.get(
                "last_season"
            )

            # ======================================================
            # NAZIONALITÀ
            # ======================================================

            country_name = CountryNormalizer.normalize(
                player.get("country")
            )

            country_key = str(
                country_name
            ).strip().lower()

            player["nationality_id"] = country_by_name.get(
                country_key
            )

            players.append(player)

            next_id += 1

        self.db.save_players(players)

        return players