from services.database_manager import DatabaseManager
from services.providers.transfermarkt_provider import TransfermarktProvider
from services.mappers.club_mapper import ClubMapper


class ClubImporter:
    """Importa i club dal dataset Transfermarkt."""

    def __init__(self):
        self.db = DatabaseManager()
        self.provider = TransfermarktProvider()

    def import_clubs(self):
        competitions = self.db.get_competitions()
        enabled_competition_ids = {
            competition["external_id"]: competition["id"]
            for competition in competitions
        }

        clubs_df = self.provider.get_clubs()

        clubs = []
        next_id = 1

        for _, row in clubs_df.iterrows():
            competition_external_id = row["domestic_competition_id"]

            if competition_external_id not in enabled_competition_ids:
                continue

            club = ClubMapper.from_transfermarkt(row, next_id)
            club["competition_id"] = enabled_competition_ids[competition_external_id]

            clubs.append(club)
            next_id += 1

        self.db.save_clubs(clubs)

        return clubs
    
    def link_stadiums(self):
        clubs = self.db.get_clubs()
        stadiums = self.db.get_stadiums()

        stadium_by_name = {
            stadium["name"].strip().lower(): stadium["id"]
            for stadium in stadiums
            if stadium.get("name")
        }

        for club in clubs:
            stadium_name = club.get("stadium_name")

            if not stadium_name:
                club["stadium_id"] = None
                continue

            club["stadium_id"] = stadium_by_name.get(
                stadium_name.strip().lower()
            )

        self.db.save_clubs(clubs)

        return clubs