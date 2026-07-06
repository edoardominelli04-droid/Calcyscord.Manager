from services.sync_manager import SyncManager
import json

sync = SyncManager()

data = sync.sync_competitions()

print(json.dumps(data, indent=4, ensure_ascii=False))

print("\n=== ELENCO COMPETIZIONI ===")
for c in data["competitions"]:
    print(c["id"], "-", c["name"])