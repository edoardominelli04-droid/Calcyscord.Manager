from services.importers.player_importer import PlayerImporter

importer = PlayerImporter()

player = importer.find_player("Lautaro")

if player:
    print("Giocatore trovato:")
    print(player)
else:
    print("Giocatore non trovato")