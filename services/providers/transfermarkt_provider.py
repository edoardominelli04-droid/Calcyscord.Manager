from pathlib import Path
import pandas as pd


class TransfermarktProvider:
    """Provider per leggere i dataset Transfermarkt."""

    def __init__(self):
        self.base_path = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "source"
            / "transfermarkt"
        )

    def _read_csv(self, filename):
        file_path = self.base_path / filename

        return pd.read_csv(
            file_path,
            low_memory=False
        )

    # ==========================================================
    # DATASETS
    # ==========================================================

    def get_players(self):
        return self._read_csv("players.csv")

    def get_clubs(self):
        return self._read_csv("clubs.csv")

    def get_competitions(self):
        return self._read_csv("competitions.csv")

    def get_countries(self):
        return self._read_csv("countries.csv")

    def get_games(self):
        return self._read_csv("games.csv")

    def get_transfers(self):
        return self._read_csv("transfers.csv")

    def get_player_valuations(self):
        return self._read_csv("player_valuations.csv")

    def get_appearances(self):
        return self._read_csv("appearances.csv")

    def get_club_games(self):
        return self._read_csv("club_games.csv")

    def get_game_events(self):
        return self._read_csv("game_events.csv")

    def get_game_lineups(self):
        return self._read_csv("game_lineups.csv")

    def get_national_teams(self):
        return self._read_csv("national_teams.csv")