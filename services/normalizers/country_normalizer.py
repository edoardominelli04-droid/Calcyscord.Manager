class CountryNormalizer:
    """Normalizza i nomi delle nazioni tra Transfermarkt e countries.json."""

    COUNTRY_NAME_MAP = {
        # Regno Unito
        "England": "United Kingdom",
        "Scotland": "United Kingdom",
        "Wales": "United Kingdom",
        "Northern Ireland": "United Kingdom",

        # Europa
        "Czech Republic": "Czechia",
        "Bosnia-Herzegovina": "Bosnia and Herzegovina",
        "Bosnia and Herzegovina": "Bosnia and Herzegovina",
        "Turkey": "Türkiye",
        "Russia": "Russian Federation",
        "Moldova": "Moldova, Republic of",

        # Asia
        "South Korea": "Korea, Republic of",
        "Korea, South": "Korea, Republic of",
        "North Korea": "Korea, Democratic People's Republic of",
        "Korea, North": "Korea, Democratic People's Republic of",
        "Iran": "Iran, Islamic Republic of",
        "Syria": "Syrian Arab Republic",
        "Laos": "Lao People's Democratic Republic",
        "Vietnam": "Viet Nam",

        # America
        "USA": "United States",
        "Venezuela": "Venezuela, Bolivarian Republic of",
        "Bolivia": "Bolivia, Plurinational State of",

        # Africa
        "Ivory Coast": "Côte d'Ivoire",
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Cape Verde": "Cabo Verde",
        "The Gambia": "Gambia",
        "Tanzania": "Tanzania, United Republic of",

        # Caraibi
        "Curacao": "Curaçao",
        "St. Kitts & Nevis": "Saint Kitts and Nevis",
        "St. Lucia": "Saint Lucia",

        # Congo
        "DR Congo": "Congo, The Democratic Republic of the",
        "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
        "Congo DR": "Congo, The Democratic Republic of the",

        # Altri
        "Neukaledonien": "New Caledonia",
        "Palestine": "Palestine",
        "Bonaire": "Bonaire",

        # Temporaneo (finché non avremo Kosovo come nazione separata)
        "Kosovo": "Serbia",
    }

    @classmethod
    def normalize(cls, name):
        if name is None:
            return None

        name = str(name).strip()

        if not name or name.lower() == "nan":
            return None

        return cls.COUNTRY_NAME_MAP.get(name, name)