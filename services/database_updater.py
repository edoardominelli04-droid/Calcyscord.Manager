from services.importers.country_importer import CountryImporter
from services.importers.competition_importer import CompetitionImporter
from services.importers.club_importer import ClubImporter
from services.importers.stadium_importer import StadiumImporter
from services.importers.player_importer import PlayerImporter


class DatabaseUpdater:
    """Aggiorna tutti i dataset del gioco."""

    def __init__(self):

        self.country_importer = CountryImporter()

        self.competition_importer = CompetitionImporter()

        self.club_importer = ClubImporter()

        self.stadium_importer = StadiumImporter()

        self.player_importer = PlayerImporter()

    def update_all(self):

        print("Aggiornamento nazioni...")
        self.country_importer.generate_countries()

        print("Aggiornamento competizioni...")
        self.competition_importer.import_competitions()

        print("Aggiornamento club...")
        self.club_importer.import_clubs()

        print("Aggiornamento stadi...")
        self.stadium_importer.import_stadiums()

        print("Collegamento stadi ai club...")
        self.club_importer.link_stadiums()

        print("Aggiornamento giocatori...")
        self.player_importer.import_players()

        print("✅ Database aggiornato con successo.")