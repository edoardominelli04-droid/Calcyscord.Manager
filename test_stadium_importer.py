from services.importers.stadium_importer import StadiumImporter

importer = StadiumImporter()

stadiums = importer.import_stadiums()

print("Stadi importati:", len(stadiums))

for stadium in stadiums[:10]:
    print(stadium["id"], stadium["name"], stadium["capacity"])