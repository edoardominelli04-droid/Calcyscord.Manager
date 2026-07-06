from services.game.manager_service import ManagerService
from services.game.finance_service import FinanceService


manager_service = ManagerService()
finance_service = FinanceService()

DISCORD_ID = 987654321
USERNAME = "TestManager"

manager = manager_service.get_by_discord_id(DISCORD_ID)

if manager is None:
    manager = manager_service.create_manager(
        DISCORD_ID,
        USERNAME
    )

finance = finance_service.get_finance(manager["id"])

if finance is None:
    finance = finance_service.create_finance(
        manager["id"]
    )

print("=== MANAGER ===")
print(manager)

print()
print("=== FINANZE ===")
print(finance)