from datetime import datetime

from services.database_manager import DatabaseManager


class ManagerService:
    """Gestisce i manager del gioco."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.get_managers()

    def get_by_discord_id(self, discord_id):
        managers = self.db.get_managers()

        for manager in managers:
            if str(manager["discord_id"]) == str(discord_id):
                return manager

        return None

    def manager_exists(self, discord_id):
        return self.get_by_discord_id(discord_id) is not None

    def create_manager(self, discord_id, username):
        managers = self.db.get_managers()

        if self.manager_exists(discord_id):
            return None

        manager = {
            "id": max(
                (
                    manager["id"]
                    for manager in managers
                ),
                default=0
            ) + 1,

            "discord_id": str(discord_id),
            "username": username,

            "club_id": None,

            "onboarding_status": "club_selection",
            
            "is_bot": False,

            "created_at": datetime.utcnow().isoformat(),

            "level": 1,
            "experience": 0,

            "reputation": 0,

            "wins": 0,
            "draws": 0,
            "losses": 0,

            "trophies": [],

            "theme": "standard",

            "notifications": True,

            "active": True
        }

        managers.append(manager)

        self.db.save_managers(managers)

        return manager

    def save(self, manager):
        managers = self.db.get_managers()

        for index, current in enumerate(managers):
            if current["id"] == manager["id"]:
                managers[index] = manager
                break

        self.db.save_managers(managers)