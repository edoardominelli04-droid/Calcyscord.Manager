from services.database_manager import DatabaseManager
from services.providers.transfermarkt_provider import TransfermarktProvider
from services.mappers.competition_mapper import CompetitionMapper


class CompetitionImporter:
    """Importa le competizioni dal dataset Transfermarkt."""

    def __init__(self):
        self.db = DatabaseManager()
        self.provider = TransfermarktProvider()

    def import_competitions(self):
        config = self.db.get_config_file("competitions.json")
        enabled_ids = {
            item["external_id"]
            for item in config
            if item["enabled"]
        }

        competitions_df = self.provider.get_competitions()

        competitions = []
        next_id = 1

        for _, row in competitions_df.iterrows():

            if row["competition_id"] not in enabled_ids:
                continue

            competitions.append(
                CompetitionMapper.from_transfermarkt(
                    row,
                    next_id
                )
            )

            next_id += 1

        self.db.save_competitions(competitions)

        return competitions