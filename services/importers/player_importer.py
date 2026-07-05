import json

from services.database_manager import DatabaseManager


class PlayerImporter:
    """Importa e ricerca i giocatori dal database."""

    def __init__(self):
        self.db = DatabaseManager()

    def load_players(self):
        return self.db.get_players()

    def find_player(self, query):
        query = query.lower().strip()

        for player in self.load_players():
            if query in player["name"].lower():
                return player

        return None