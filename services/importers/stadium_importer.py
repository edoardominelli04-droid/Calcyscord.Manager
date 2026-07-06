from services.database_manager import DatabaseManager
from services.providers.transfermarkt_provider import TransfermarktProvider
from services.mappers.stadium_mapper import StadiumMapper


class StadiumImporter:
    """Importa gli stadi dal dataset Transfermarkt."""

    def __init__(self):
        self.db = DatabaseManager()
        self.provider = TransfermarktProvider()

    def import_stadiums(self):
        clubs_df = self.provider.get_clubs()
        clubs = self.db.get_clubs()

        enabled_club_ids = {
            club["external_id"]
            for club in clubs
        }

        stadiums = []
        seen_stadiums = set()
        next_id = 1

        for _, row in clubs_df.iterrows():
            if row["club_id"] not in enabled_club_ids:
                continue

            stadium_name = row["stadium_name"]

            if not stadium_name or str(stadium_name) == "nan":
                continue

            key = stadium_name.strip().lower()

            if key in seen_stadiums:
                continue

            stadiums.append(
                StadiumMapper.from_transfermarkt(
                    row,
                    next_id
                )
            )

            seen_stadiums.add(key)
            next_id += 1

        self.db.save_stadiums(stadiums)

        return stadiums