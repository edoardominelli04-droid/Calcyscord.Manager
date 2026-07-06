from services.importers.country_importer import CountryImporter
from services.importers.competition_importer import CompetitionImporter
from services.importers.stadium_importer import StadiumImporter
from services.importers.club_importer import ClubImporter


class DatabaseUpdater:
    """Aggiorna tutti i dataset del gioco."""

    def __init__(self):
        self.country_importer = CountryImporter()
        self.competition_importer = CompetitionImporter()
        self.stadium_importer = StadiumImporter()
        self.club_importer = ClubImporter()

    def update_all(self):
        print("Aggiornamento nazioni...")
        self.country_importer.generate_countries()

        print("Aggiornamento competizioni...")
        self.competition_importer.generate_default_competitions()

        print("Aggiornamento stadi...")
        self.stadium_importer.generate_default_stadiums()

        print("Aggiornamento club...")
        self.club_importer.generate_default_clubs()

        print("Database aggiornato con successo.")