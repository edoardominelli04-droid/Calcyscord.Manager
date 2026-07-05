from services.importers.team_importer import TeamImporter

importer = TeamImporter()

team = importer.get_team_data(108)

print(team["name"])
print(team["short_name"])
print(team["tla"])
print(team["venue"])
print("Giocatori trovati:", len(team["squad"]))

for player in team["squad"][:10]:
    print(player.get("name"), "-", player.get("position"))