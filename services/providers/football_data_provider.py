import os
import requests

from .base_provider import BaseProvider


class FootballDataProvider(BaseProvider):
    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY")

        self.headers = {
            "X-Auth-Token": self.api_key
        }

    def get_player(self, player_id):
        raise NotImplementedError("Football-data.org non supporta ancora questo metodo.")

    def get_team(self, team_id):
        response = requests.get(
            f"{self.BASE_URL}/teams/{team_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_matches(self, competition_id):
        response = requests.get(
            f"{self.BASE_URL}/competitions/{competition_id}/matches",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_competitions(self):
        response = requests.get(
            f"{self.BASE_URL}/competitions",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()