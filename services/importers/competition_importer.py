from services.database_manager import DatabaseManager
from services.mappers.competition_mapper import CompetitionMapper
from services.providers.transfermarkt_provider import TransfermarktProvider


class CompetitionImporter:
    """Importa competizioni senza modificare gli ID interni già assegnati."""
    def __init__(self):
        self.db, self.provider = DatabaseManager(), TransfermarktProvider()
    def import_competitions(self):
        enabled = {x["external_id"] for x in self.db.get_config_file("competitions.json") if x["enabled"]}
        existing = self.db.get_competitions()
        old_by_external = {str(c["external_id"]):c for c in existing}
        next_id = max((int(c["id"]) for c in existing), default=0)+1
        competitions=[]
        for _,row in self.provider.get_competitions().iterrows():
            external=str(row["competition_id"])
            if external not in enabled: continue
            old=old_by_external.get(external); internal_id=int(old["id"]) if old else next_id
            if old is None: next_id+=1
            competition=CompetitionMapper.from_transfermarkt(row,internal_id)
            competitions.append(competition)
        competitions.sort(key=lambda c:int(c["id"]))
        self.db.save_competitions(competitions); return competitions
