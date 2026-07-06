from services.database_manager import DatabaseManager
from collections import Counter

db = DatabaseManager()

players = db.get_players()

missing = Counter()

for player in players:
    if player.get("nationality_id") is None:
        missing[player.get("country")] += 1

print("Nazioni non riconosciute:", len(missing))

for country, count in missing.most_common(50):
    print(country, count)