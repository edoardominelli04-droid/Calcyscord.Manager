from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.club_ownership_service import ClubOwnershipService
from services.game.initial_squad_service import InitialSquadService


class ClubSelectionService:
    """Gestisce la scelta del club da parte del manager."""

    def __init__(self):
        self.db = DatabaseManager()
        self.manager_service = ManagerService()
        self.ownership_service = ClubOwnershipService()
        self.initial_squad_service = InitialSquadService()

    def choose_club(self, discord_id, club_id):

        manager = self.manager_service.get_by_discord_id(discord_id)

        if manager is None:
            raise ValueError("Manager non trovato.")

        if manager["club_id"] is not None:
            raise ValueError("Hai già scelto un club.")

        club = self.db.get_club_by_id(club_id)

        if club is None:
            raise ValueError("Club inesistente.")

        if self.ownership_service.club_is_taken(club_id):
            raise ValueError("Questo club è già occupato.")

        self.ownership_service.assign_club(
            manager["id"],
            club_id
        )

        manager["club_id"] = club_id

        manager["onboarding_status"] = "initial_squad"

        self.manager_service.save(manager)

        self.initial_squad_service.create_draft(

            manager["id"],

            club_id

        )

        return manager, club
