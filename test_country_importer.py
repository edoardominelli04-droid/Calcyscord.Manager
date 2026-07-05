from services.importers.country_importer import CountryImporter

importer = CountryImporter()

countries = importer.generate_countries()

print("Nazioni generate:", len(countries))
print("Prima nazione:", countries[0])