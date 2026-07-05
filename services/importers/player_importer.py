import json
from pathlib import Path


class PlayerImporter:
    def __init__(self):
        self.players_dataset = Path("data/datasets/players.json")
        self.teams_dataset = Path("data/datasets/teams.json")

    def load_players(self):
        with open(self.players_dataset, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def find_player(self, query):
        query = query.lower().strip()

        for player in self.load_players():
            if query in player["name"].lower():
                return player

        return None

    def load_teams(self):
        with open(self.teams_dataset, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_player(self, player_id):
        for player in self.load_players():
            if player["id"] == player_id:
                return player
        return None

    def get_team(self, team_id):
        for team in self.load_teams():
            if team["id"] == team_id:
                return team
        return None

    def get_players_by_team(self, team_id):
        return [
            player
            for player in self.load_players()
            if player["team_id"] == team_id
        ]

    def get_players_by_competition(self, competition_code):
        return [
            player
            for player in self.load_players()
            if player["competition"] == competition_code
        ]