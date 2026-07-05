from services.importers.player_importer import PlayerImporter

importer = PlayerImporter()

players = importer.load_players()

print("Giocatori caricati:", len(players))

print("Primo giocatore:", players[0])