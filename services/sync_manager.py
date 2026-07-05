from services.providers.football_data_provider import FootballDataProvider


class SyncManager:
    """Gestisce la sincronizzazione dei dati esterni."""

    def __init__(self):
        self.provider = FootballDataProvider()

    def sync_competitions(self):
        return self.provider.get_competitions()

    def sync_team(self, team_id):
        return self.provider.get_team(team_id)

    def sync_matches(self, competition_id):
        return self.provider.get_matches(competition_id)