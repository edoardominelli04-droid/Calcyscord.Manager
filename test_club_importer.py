from services.importers.club_importer import ClubImporter

importer = ClubImporter()

clubs = importer.link_stadiums()

print("Club aggiornati:", len(clubs))

for club in clubs[:10]:
    print(club["id"], club["name"], "stadium_id:", club.get("stadium_id"))