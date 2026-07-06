import pycountry

from services.database_manager import DatabaseManager


class CountryImporter:
    """Importa e aggiorna il database delle nazioni."""

    CONTINENT_MAP = {
        "EU": 1,
        "SA": 2,
        "NA": 3,
        "AF": 4,
        "AS": 5,
        "OC": 6
    }

    MANUAL_CONTINENTS = {
        "IT": 1,
        "FR": 1,
        "DE": 1,
        "ES": 1,
        "GB": 1,
        "PT": 1,
        "NL": 1,
        "BE": 1,
        "CH": 1,
        "TR": 1,

        "AR": 2,
        "BR": 2,
        "UY": 2,
        "CL": 2,
        "CO": 2,

        "US": 3,
        "CA": 3,
        "MX": 3,

        "MA": 4,
        "SN": 4,
        "NG": 4,
        "CI": 4,
        "GH": 4,

        "JP": 5,
        "KR": 5,
        "SA": 5,

        "AU": 6,
        "NZ": 6
    }

    def __init__(self):
        self.db = DatabaseManager()

    def load_countries(self):
        return self.db.get_countries()

    def save_countries(self, countries):
        self.db.save_countries(countries)

    def generate_countries(self):
        countries = []

        for index, country in enumerate(pycountry.countries, start=1):
            code = country.alpha_2

            countries.append({
                "id": index,
                "name": country.name,
                "code": code,
                "continent_id": self.MANUAL_CONTINENTS.get(code),
                "flag": self._country_code_to_flag(code)
            })

        self.save_countries(countries)
        return countries

    def _country_code_to_flag(self, code):
        return "".join(chr(127397 + ord(char)) for char in code.upper())