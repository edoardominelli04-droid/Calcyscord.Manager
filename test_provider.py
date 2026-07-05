from services.sync_manager import SyncManager

sync = SyncManager()

competitions = sync.sync_competitions()

for competition in competitions["competitions"][:10]:
    print(f"{competition['code']} - {competition['name']}")