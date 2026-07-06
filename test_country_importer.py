from services.importers.country_importer import CountryImporter

importer = CountryImporter()

countries = importer.generate_countries()

print("Nazioni generate:", len(countries))
print("Prima nazione:", countries[0])

italy = next(country for country in countries if country["code"] == "IT")
argentina = next(country for country in countries if country["code"] == "AR")

print("Italia:", italy)
print("Argentina:", argentina)