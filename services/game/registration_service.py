from services.game.manager_service import ManagerService
from services.game.finance_service import FinanceService


class RegistrationService:
    """Gestisce la registrazione di un nuovo manager."""

    def __init__(self):
        self.manager_service = ManagerService()
        self.finance_service = FinanceService()

    def register(self, discord_id, username):
        """
        Registra un nuovo manager.

        Restituisce:
            (manager, finance, created)

        created = True  -> nuovo manager creato
        created = False -> manager già esistente
        """

        manager = self.manager_service.get_by_discord_id(discord_id)

        if manager is not None:

            finance = self.finance_service.get_finance(
                manager["id"]
            )

            if finance is None:
                finance = self.finance_service.create_finance(
                    manager["id"]
                )

            return manager, finance, False

        manager = self.manager_service.create_manager(
            discord_id,
            username
        )

        finance = self.finance_service.create_finance(
            manager["id"]
        )

        return manager, finance, True