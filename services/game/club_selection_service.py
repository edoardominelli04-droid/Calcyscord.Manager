from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.club_ownership_service import ClubOwnershipService
from services.game.initial_squad_service import InitialSquadService


class ClubSelectionService:
    def __init__(self):
        self.db, self.manager_service = DatabaseManager(), ManagerService()
        self.ownership_service, self.initial_squad_service = ClubOwnershipService(), InitialSquadService()
    @staticmethod
    def searchable_text(club):
        values = [club.get("name"),club.get("official_name"),club.get("code"),*club.get("aliases",[])]
        return " ".join(str(v) for v in values if v).lower()
    def get_playable_clubs(self): return [c for c in self.db.get_clubs() if c.get("active") and c.get("playable",True)]
    def search_clubs(self, query):
        query = str(query or "").strip().lower(); return [c for c in self.get_playable_clubs() if query in self.searchable_text(c)]
    def choose_club(self, discord_id, club_id):
        manager = self.manager_service.get_by_discord_id(discord_id)
        if manager is None: raise ValueError("Manager non trovato.")
        if manager["club_id"] is not None: raise ValueError("Hai già scelto un club.")
        club = self.db.get_club_by_id(club_id)
        if club is None: raise ValueError("Club inesistente.")
        if not club.get("active") or not club.get("playable",True): raise ValueError("Questo club non partecipa a un campionato supportato nella stagione corrente.")
        if self.ownership_service.club_is_taken(club_id): raise ValueError("Questo club è già occupato.")
        self.ownership_service.assign_club(manager["id"],club_id)
        manager["club_id"], manager["onboarding_status"] = club_id,"initial_squad"
        self.manager_service.save(manager); self.initial_squad_service.create_draft(manager["id"],club_id)
        return manager,club
