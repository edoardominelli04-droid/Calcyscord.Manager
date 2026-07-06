from services.database_manager import DatabaseManager


class BaseImporter:
    """Classe base per tutti gli importer."""

    def __init__(self):
        self.db = DatabaseManager()

    # ==========================================================
    # CONFIG
    # ==========================================================

    def load_config(self, filename):
        return self.db.get_config_file(filename)

    def save_config(self, filename, data):
        self.db.save_config_file(filename, data)

    # ==========================================================
    # UTILITIES
    # ==========================================================

    def get_enabled_items(self, config):
        """Restituisce solo gli elementi abilitati."""
        return [
            item for item in config
            if item.get("enabled", False)
        ]

    def sort_by_priority(self, items):
        """Ordina gli elementi per priorità."""
        return sorted(
            items,
            key=lambda item: item.get("priority", 999)
        )