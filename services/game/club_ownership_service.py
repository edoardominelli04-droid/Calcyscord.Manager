from datetime import datetime

from services.database_manager import DatabaseManager


class ClubOwnershipService:
    """Gestisce l'assegnazione dei club ai manager."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.get_club_ownership()

    def save_all(self, ownerships):
        self.db.save_club_ownership(ownerships)

    def get_by_manager(self, manager_id):
        for ownership in self.get_all():
            if ownership["manager_id"] == manager_id:
                return ownership

        return None

    def get_by_club(self, club_id):
        for ownership in self.get_all():
            if ownership["club_id"] == club_id:
                return ownership

        return None

    def manager_has_club(self, manager_id):
        return self.get_by_manager(manager_id) is not None

    def club_is_taken(self, club_id):
        return self.get_by_club(club_id) is not None

    def assign_club(self, manager_id, club_id):

        if self.manager_has_club(manager_id):
            raise ValueError("Il manager possiede già un club.")

        if self.club_is_taken(club_id):
            raise ValueError("Il club è già assegnato.")

        ownership = {
            "manager_id": manager_id,
            "club_id": club_id,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }

        ownerships = self.get_all()
        ownerships.append(ownership)

        self.save_all(ownerships)

        return ownership

    def remove_club(self, manager_id):
        ownerships = self.get_all()

        ownerships = [
            ownership
            for ownership in ownerships
            if ownership["manager_id"] != manager_id
        ]

        self.save_all(ownerships)