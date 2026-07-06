from services.importers.player_importer import PlayerImporter

importer = PlayerImporter()

players = importer.import_players()

print("Giocatori importati:", len(players))

for player in players[:10]:
    print(
        player["id"],
        player["name"],
        player["position"],
        "nationality_id:",
        player.get("nationality_id"),
        "market_value:",
        player["market_value"]
    )