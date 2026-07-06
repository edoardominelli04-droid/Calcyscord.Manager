import json
from pathlib import Path


class DatabaseManager:
    """Gestisce la lettura e la scrittura dei file JSON del progetto."""

    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent / "data"

        self.datasets_path = base_path / "datasets"
        self.config_path = base_path / "config"

    def _load_json(self, folder, filename):
        file_path = folder / filename

        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, folder, filename, data):
        file_path = folder / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ==========================================================
    # LOAD DATASETS
    # ==========================================================

    def get_players(self):
        return self._load_json(self.datasets_path, "players.json")

    def get_clubs(self):
        return self._load_json(self.datasets_path, "clubs.json")

    def get_competitions(self):
        return self._load_json(self.datasets_path, "competitions.json")

    def get_countries(self):
        return self._load_json(self.datasets_path, "countries.json")

    def get_stadiums(self):
        return self._load_json(self.datasets_path, "stadiums.json")

    def get_continents(self):
        return self._load_json(self.datasets_path, "continents.json")

    def get_config(self):
        return self._load_json(self.datasets_path, "config.json")

    def get_managers(self):
        return self._load_json(self.datasets_path, "managers.json")

    # ==========================================================
    # LOAD CONFIG
    # ==========================================================

    def get_competitions_config(self):
        return self._load_json(self.config_path, "competitions.json")

    def get_config_file(self, filename):
        """Carica un qualsiasi file dalla cartella config."""
        return self._load_json(self.config_path, filename)

    # ==========================================================
    # SAVE DATASETS
    # ==========================================================

    def save_players(self, data):
        self._save_json(self.datasets_path, "players.json", data)

    def save_clubs(self, data):
        self._save_json(self.datasets_path, "clubs.json", data)

    def save_competitions(self, data):
        self._save_json(self.datasets_path, "competitions.json", data)

    def save_countries(self, data):
        self._save_json(self.datasets_path, "countries.json", data)

    def save_stadiums(self, data):
        self._save_json(self.datasets_path, "stadiums.json", data)

    def save_continents(self, data):
        self._save_json(self.datasets_path, "continents.json", data)

    def save_config(self, data):
        self._save_json(self.datasets_path, "config.json", data)

    def save_managers(self, data):
        self._save_json(self.datasets_path, "managers.json", data)

    # ==========================================================
    # SAVE CONFIG
    # ==========================================================

    def save_config_file(self, filename, data):
        """Salva un qualsiasi file nella cartella config."""
        self._save_json(self.config_path, filename, data)