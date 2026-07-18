import os
import time
from pathlib import Path
import requests
from dotenv import load_dotenv
from .base_provider import BaseProvider

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class FootballDataProvider(BaseProvider):
    BASE_URL = "https://api.football-data.org/v4"
    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY")
        if not self.api_key:
            raise RuntimeError("FOOTBALL_DATA_API_KEY non configurata nel file .env")
        self.headers = {"X-Auth-Token": self.api_key}
    def _get(self, path, params=None):
        last_response = None
        for attempt in range(5):
            response = requests.get(
                f"{self.BASE_URL}{path}", headers=self.headers,
                params=params, timeout=30
            )
            last_response = response
            if response.status_code != 429:
                response.raise_for_status()
                return response.json()

            retry_after = response.headers.get("Retry-After")
            try:
                wait_seconds = max(1, int(float(retry_after)))
            except (TypeError, ValueError):
                wait_seconds = min(60, 12 * (attempt + 1))
            print(
                f"⏳ Limite football-data raggiunto. "
                f"Nuovo tentativo tra {wait_seconds} secondi..."
            )
            time.sleep(wait_seconds)

        last_response.raise_for_status()
        raise RuntimeError("football-data non disponibile dopo 5 tentativi")
    def get_player(self, player_id): return self._get(f"/persons/{player_id}")
    def get_team(self, team_id): return self._get(f"/teams/{team_id}")
    def get_matches(self, competition_id, season=None): return self._get(f"/competitions/{competition_id}/matches", {"season": season} if season is not None else None)
    def get_competitions(self): return self._get("/competitions")
    def get_teams_by_competition(self, competition_id, season=None): return self._get(f"/competitions/{competition_id}/teams", {"season": season} if season is not None else None)
    def get_team_players(self, team_id): return self.get_team(team_id)
