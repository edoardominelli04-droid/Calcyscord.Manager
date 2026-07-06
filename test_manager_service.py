from services.game.manager_service import ManagerService

service = ManagerService()

DISCORD_ID = 123456789
USERNAME = "Edoardo"

manager = service.get_by_discord_id(DISCORD_ID)

if manager is None:
    manager = service.create_manager(DISCORD_ID, USERNAME)

    print("Manager creato!")
    print(manager)

else:
    print("Manager già esistente!")
    print(manager)