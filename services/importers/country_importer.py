import pycountry

from services.database_manager import DatabaseManager


class CountryImporter:
    """Importa e aggiorna il database delle nazioni."""

    def __init__(self):
        self.db = DatabaseManager()

    def load_countries(self):
        return self.db.get_countries()

    def save_countries(self, countries):
        self.db.save_countries(countries)

    def generate_countries(self):
        countries = []

        for index, country in enumerate(pycountry.countries, start=1):
            countries.append({
                "id": index,
                "name": country.name,
                "code": country.alpha_2,
                "continent_id": None,
                "flag": self._country_code_to_flag(country.alpha_2)
            })

        self.save_countries(countries)
        return countries

    def _country_code_to_flag(self, code):
        return "".join(chr(127397 + ord(char)) for char in code.upper())