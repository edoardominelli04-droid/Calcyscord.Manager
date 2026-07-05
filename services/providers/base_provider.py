from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Classe base per tutti i provider dati."""

    @abstractmethod
    def get_player(self, player_id):
        pass

    @abstractmethod
    def get_team(self, team_id):
        pass

    @abstractmethod
    def get_matches(self, competition_id):
        pass

    @abstractmethod
    def get_competitions(self):
        pass