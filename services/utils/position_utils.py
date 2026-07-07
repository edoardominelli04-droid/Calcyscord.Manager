class PositionUtils:
    """Utility per la gestione dei ruoli dei calciatori."""

    # ==========================================================
    # TRADUZIONE RUOLI
    # ==========================================================

    TRANSLATIONS = {

        "Goalkeeper": "Portiere",

        "Left-Back": "Terzino Sinistro",
        "Right-Back": "Terzino Destro",
        "Centre-Back": "Difensore Centrale",

        "Defensive Midfield": "Mediano",
        "Central Midfield": "Centrocampista Centrale",
        "Attacking Midfield": "Trequartista",

        "Left Midfield": "Centrocampista Sinistro",
        "Right Midfield": "Centrocampista Destro",

        "Left Winger": "Ala Sinistra",
        "Right Winger": "Ala Destra",

        "Second Striker": "Seconda Punta",
        "Centre-Forward": "Prima Punta",

        "Unknown": "Sconosciuto"
    }

    # ==========================================================
    # REPARTI
    # ==========================================================

    GOALKEEPERS = {
        "Goalkeeper"
    }

    DEFENDERS = {
        "Left-Back",
        "Right-Back",
        "Centre-Back"
    }

    MIDFIELDERS = {
        "Defensive Midfield",
        "Central Midfield",
        "Attacking Midfield",
        "Left Midfield",
        "Right Midfield"
    }

    ATTACKERS = {
        "Left Winger",
        "Right Winger",
        "Second Striker",
        "Centre-Forward"
    }

    # ==========================================================
    # TRADUZIONE
    # ==========================================================

    def translate(self, position):

        return self.TRANSLATIONS.get(
            position,
            position
        )

    # ==========================================================
    # REPARTO
    # ==========================================================

    def get_department(self, player):

        role = player.get("sub_position")

        if role in self.GOALKEEPERS:
            return "goalkeeper"

        if role in self.DEFENDERS:
            return "defence"

        if role in self.MIDFIELDERS:
            return "midfield"

        if role in self.ATTACKERS:
            return "attack"

        # Fallback sul ruolo principale

        position = player.get("position")

        if position == "Goalkeeper":
            return "goalkeeper"

        if position == "Defence":
            return "defence"

        if position == "Midfield":
            return "midfield"

        if position == "Attack":
            return "attack"

        return "unknown"

    # ==========================================================
    # CONTROLLI
    # ==========================================================

    def is_goalkeeper(self, player):
        return self.get_department(player) == "goalkeeper"

    def is_defender(self, player):
        return self.get_department(player) == "defence"

    def is_midfielder(self, player):
        return self.get_department(player) == "midfield"

    def is_attacker(self, player):
        return self.get_department(player) == "attack"