import json
from pathlib import Path


class DatabaseManager:
    """Gestisce la lettura e la scrittura dei dataset JSON."""

    def __init__(self):
        self.data_path = Path(__file__).resolve().parent.parent / "data" / "datasets"

    def _load_json(self, filename):
        file_path = self.data_path / filename

        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, filename, data):
        file_path = self.data_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ---------- LOAD ----------

    def get_players(self):
        return self._load_json("players.json")

    def get_clubs(self):
        return self._load_json("clubs.json")

    def get_competitions(self):
        return self._load_json("competitions.json")

    def get_countries(self):
        return self._load_json("countries.json")

    def get_stadiums(self):
        return self._load_json("stadiums.json")

    def get_continents(self):
        return self._load_json("continents.json")

    def get_config(self):
        return self._load_json("config.json")

    # ---------- SAVE ----------

    def save_players(self, data):
        self._save_json("players.json", data)

    def save_clubs(self, data):
        self._save_json("clubs.json", data)

    def save_competitions(self, data):
        self._save_json("competitions.json", data)

    def save_countries(self, data):
        self._save_json("countries.json", data)

    def save_stadiums(self, data):
        self._save_json("stadiums.json", data)

    def save_continents(self, data):
        self._save_json("continents.json", data)

    def save_config(self, data):
        self._save_json("config.json", data)