import json
from pathlib import Path


class DatabaseManager:
    """Gestisce la lettura e la scrittura dei database JSON."""

    def __init__(self):

        base_path = Path(__file__).resolve().parent.parent / "data"

        self.datasets_path = base_path / "datasets"
        self.save_path = base_path / "save"
        self.config_path = base_path / "config"

    # ==========================================================
    # METODI GENERICI
    # ==========================================================

    def _sanitize_json_data(self, value):
        """
        Converte automaticamente valori non validi
        (NaN, Infinity, -Infinity) in None.
        """

        if isinstance(value, float):

            if value != value:
                return None

            if value in (
                float("inf"),
                float("-inf")
            ):
                return None

        if isinstance(value, list):

            return [

                self._sanitize_json_data(item)

                for item in value

            ]

        if isinstance(value, dict):

            return {

                key: self._sanitize_json_data(item)

                for key, item in value.items()

            }

        return value

    def _load_json(self, folder, filename):

        file_path = folder / filename

        if not file_path.exists():
            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

        if not content:
            return []

        data = json.loads(

            content,

            parse_constant=lambda value: None

        )

        return self._sanitize_json_data(

            data

        )

    def _save_json(self, folder, filename, data):

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = folder / filename

        clean_data = self._sanitize_json_data(

            data

        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(

                clean_data,

                file,

                ensure_ascii=False,

                indent=4,

                allow_nan=False

            )

    # ==========================================================
    # DATASETS
    # ==========================================================

    def get_players(self):
        return self._load_json(self.datasets_path, "players.json")

    def save_players(self, data):
        self._save_json(self.datasets_path, "players.json", data)

    def get_clubs(self):
        return self._load_json(self.datasets_path, "clubs.json")

    def save_clubs(self, data):
        self._save_json(self.datasets_path, "clubs.json", data)

    def get_competitions(self):
        return self._load_json(self.datasets_path, "competitions.json")

    def save_competitions(self, data):
        self._save_json(self.datasets_path, "competitions.json", data)

    def get_countries(self):
        return self._load_json(self.datasets_path, "countries.json")

    def save_countries(self, data):
        self._save_json(self.datasets_path, "countries.json", data)

    def get_continents(self):
        return self._load_json(self.datasets_path, "continents.json")

    def save_continents(self, data):
        self._save_json(self.datasets_path, "continents.json", data)

    def get_stadiums(self):
        return self._load_json(self.datasets_path, "stadiums.json")

    def save_stadiums(self, data):
        self._save_json(self.datasets_path, "stadiums.json", data)

    # ==========================================================
    # SAVE GAME
    # ==========================================================

    def get_managers(self):
        return self._load_json(self.save_path, "managers.json")

    def save_managers(self, data):
        self._save_json(self.save_path, "managers.json", data)

    def get_finances(self):
        return self._load_json(self.save_path, "finances.json")

    def save_finances(self, data):
        self._save_json(self.save_path, "finances.json", data)

    def get_club_ownership(self):
        return self._load_json(self.save_path, "club_ownership.json")

    def save_club_ownership(self, data):
        self._save_json(self.save_path, "club_ownership.json", data)

    def get_squads(self):
        return self._load_json(self.save_path, "squads.json")

    def save_squads(self, data):
        self._save_json(self.save_path, "squads.json", data)

    def get_contracts(self):
        return self._load_json(self.save_path, "contracts.json")

    def save_contracts(self, data):
        self._save_json(self.save_path, "contracts.json", data)

    def get_transfer_requests(self):
        return self._load_json(
            self.save_path,
            "transfer_requests.json"
        )

    def save_transfer_requests(self, data):
        self._save_json(
            self.save_path,
            "transfer_requests.json",
            data
        )

    def get_formations(self):
        return self._load_json(
            self.save_path,
            "formations.json"
        )

    def save_formations(self, data):
        self._save_json(
            self.save_path,
            "formations.json",
            data
        )

    def get_initial_squad_drafts(self):
        return self._load_json(
            self.save_path,
            "initial_squad_drafts.json"
        )

    def save_initial_squad_drafts(self, data):
        self._save_json(
            self.save_path,
            "initial_squad_drafts.json",
            data
        )

    def get_manager_statements(self):
        return self._load_json(
            self.save_path,
            "manager_statements.json"
        )

    def save_manager_statements(self, data):
        self._save_json(
            self.save_path,
            "manager_statements.json",
            data
        )

    def get_current_rosters(self):
        return self._load_json(
            self.save_path,
            "current_rosters.json"
        )

    def save_current_rosters(self, data):
        self._save_json(
            self.save_path,
            "current_rosters.json",
            data
        )

    # ==========================================================
    # CONFIG
    # ==========================================================

    def get_competitions_config(self):
        return self._load_json(
            self.config_path,
            "competitions.json"
        )

    def get_config_file(self, filename):
        return self._load_json(
            self.config_path,
            filename
        )

    def save_config_file(self, filename, data):
        self._save_json(
            self.config_path,
            filename,
            data
        )

    # ==========================================================
    # FINDERS
    # ==========================================================

    def get_player_by_id(self, player_id):
        return next(
            (
                p
                for p in self.get_players()
                if p["id"] == player_id
            ),
            None
        )

    def get_manager_by_id(self, manager_id):
        return next(
            (
                m
                for m in self.get_managers()
                if m["id"] == manager_id
            ),
            None
        )

    def get_club_by_id(self, club_id):
        return next(
            (
                c
                for c in self.get_clubs()
                if c["id"] == club_id
            ),
            None
        )

    def get_competition_by_id(self, competition_id):
        return next(
            (
                c
                for c in self.get_competitions()
                if c["id"] == competition_id
            ),
            None
        )

    def get_stadium_by_id(self, stadium_id):
        return next(
            (
                s
                for s in self.get_stadiums()
                if s["id"] == stadium_id
            ),
            None
        )

    def get_contract_by_id(self, contract_id):
        return next(
            (
                c
                for c in self.get_contracts()
                if c["id"] == contract_id
            ),
            None
        )
