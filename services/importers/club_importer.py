from services.database_manager import DatabaseManager
from services.identity.club_identity_service import ClubIdentityService
from services.mappers.club_mapper import ClubMapper
from services.providers.football_data_provider import FootballDataProvider
from services.providers.transfermarkt_provider import TransfermarktProvider


class ClubImporter:
    """Importa i club attuali collegando Transfermarkt e football-data.org."""
    def __init__(self):
        self.db, self.tm, self.fd = DatabaseManager(), TransfermarktProvider(), FootballDataProvider()
        self.identity = ClubIdentityService()

    def import_clubs(self):
        competitions = {str(c["external_id"]): c for c in self.db.get_competitions()}
        links = [x for x in self.db.get_config_file("provider_competitions.json") if x.get("playable") and x.get("football_data_code")]
        overrides = self.db.get_config_file("club_provider_overrides.json") or {}
        existing = self.db.get_clubs()
        existing_by_tm = {int(c.get("transfermarkt_id", c.get("external_id"))): c for c in existing}
        next_id = max((int(c["id"]) for c in existing), default=0) + 1
        frame = self.tm.get_clubs()
        season = int(frame["last_season"].max())
        imported = []
        for link in links:
            tm_code = link["transfermarkt_id"]
            competition = competitions.get(tm_code)
            if competition is None: raise RuntimeError(f"Competizione Transfermarkt {tm_code} non importata")
            rows = frame[(frame["domestic_competition_id"] == tm_code) & (frame["last_season"] == season)]
            tm_clubs = [row for _, row in rows.iterrows()]
            teams = self.fd.get_teams_by_competition(link["football_data_code"], season).get("teams", [])
            if not teams: raise RuntimeError(f"Football-data non ha restituito squadre per {tm_code}")
            matches = self.identity.match(tm_clubs, teams, overrides.get(tm_code, {}))
            for row, team, _ in matches:
                tm_id = int(row["club_id"]); old = existing_by_tm.get(tm_id)
                internal_id = int(old["id"]) if old else next_id
                if old is None: next_id += 1
                club = ClubMapper.from_providers(row, team, internal_id)
                club["competition_id"] = competition["id"]
                club["football_data_competition_code"] = link["football_data_code"]
                imported.append(club)
        current = {c["transfermarkt_id"] for c in imported}
        for old in existing:
            tm_id = int(old.get("transfermarkt_id", old.get("external_id")))
            if tm_id not in current:
                archived = dict(old); archived.update({"transfermarkt_id":tm_id,"active":False,"playable":False}); imported.append(archived)
        imported.sort(key=lambda c: int(c["id"]))
        self.db.save_clubs(imported); return imported

    def link_stadiums(self):
        clubs, stadiums = self.db.get_clubs(), self.db.get_stadiums()
        by_name = {s["name"].strip().lower():s["id"] for s in stadiums if s.get("name")}
        for club in clubs:
            name = club.get("stadium_name"); club["stadium_id"] = by_name.get(name.strip().lower()) if name else None
        self.db.save_clubs(clubs); return clubs
