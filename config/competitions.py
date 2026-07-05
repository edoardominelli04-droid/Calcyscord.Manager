"""
Configurazione centralizzata delle competizioni supportate
da Calcyscord.Manager.
"""

SUPPORTED_COMPETITIONS = {

    "SA": {
        "name": "Serie A",
        "country": "Italy",
        "priority": 1,
        "logo": "assets/leagues/serie_a.png",
        "color": 0x008FD5
    },

    "PL": {
        "name": "Premier League",
        "country": "England",
        "priority": 2,
        "logo": "assets/leagues/premier_league.png",
        "color": 0x3D195B
    },

    "PD": {
        "name": "LaLiga",
        "country": "Spain",
        "priority": 3,
        "logo": "assets/leagues/laliga.png",
        "color": 0xFF4B44
    },

    "BL1": {
        "name": "Bundesliga",
        "country": "Germany",
        "priority": 4,
        "logo": "assets/leagues/bundesliga.png",
        "color": 0xD20515
    },

    "FL1": {
        "name": "Ligue 1",
        "country": "France",
        "priority": 5,
        "logo": "assets/leagues/ligue1.png",
        "color": 0x091C3E
    },

    "DED": {
        "name": "Eredivisie",
        "country": "Netherlands",
        "priority": 6,
        "logo": "assets/leagues/eredivisie.png",
        "color": 0xFF7F00
    },

    "PPL": {
        "name": "Primeira Liga",
        "country": "Portugal",
        "priority": 7,
        "logo": "assets/leagues/primeira_liga.png",
        "color": 0x046A38
    },

    "ELC": {
        "name": "Championship",
        "country": "England",
        "priority": 8,
        "logo": "assets/leagues/championship.png",
        "color": 0x0057B8
    },

    "BSA": {
        "name": "Brasileirão Série A",
        "country": "Brazil",
        "priority": 9,
        "logo": "assets/leagues/brasileirao.png",
        "color": 0x009739
    }
}

ACTIVE_COMPETITION_CODES = [
    "SA",
    "PL",
    "PD",
    "BL1",
    "FL1"
]