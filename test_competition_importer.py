from services.importers.competition_importer import CompetitionImporter

importer = CompetitionImporter()

competitions = importer.import_competitions()

print("Competizioni importate:", len(competitions))

for competition in competitions:
    print(competition["id"], competition["external_id"], competition["name"])