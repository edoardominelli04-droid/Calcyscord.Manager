from services.database_manager import DatabaseManager


class FinanceService:
    """Gestisce le finanze dei manager."""

    STARTING_BALANCE = 50_000_000

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db._load_json(
            self.db.save_path,
            "finances.json"
        )

    def save_all(self, finances):
        self.db._save_json(
            self.db.save_path,
            "finances.json",
            finances
        )

    def get_finance(self, manager_id):
        finances = self.get_all()

        for finance in finances:
            if finance["manager_id"] == manager_id:
                return finance

        return None

    def create_finance(self, manager_id):
        finances = self.get_all()

        if self.get_finance(manager_id):
            return None

        finance = {
            "manager_id": manager_id,

            "balance": self.STARTING_BALANCE,

            "transfer_budget": self.STARTING_BALANCE,

            "salary_budget": 0,

            "income_total": 0,

            "expense_total": 0
        }

        finances.append(finance)

        self.save_all(finances)

        return finance

    def save(self, finance):
        finances = self.get_all()

        for index, current in enumerate(finances):
            if current["manager_id"] == finance["manager_id"]:
                finances[index] = finance
                break

        self.save_all(finances)