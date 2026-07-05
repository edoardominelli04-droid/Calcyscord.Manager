from services.sync_manager import SyncManager


class TeamImporter:
    """Importa dati squadra da football-data.org."""

    def __init__(self):
        self.sync = SyncManager()

    def get_team_data(self, team_id):
        team = self.sync.sync_team(team_id)

        return {
            "external_id": team.get("id"),
            "name": team.get("name"),
            "short_name": team.get("shortName"),
            "tla": team.get("tla"),
            "crest": team.get("crest"),
            "venue": team.get("venue"),
            "squad": team.get("squad", [])
        }