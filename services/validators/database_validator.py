from services.database_manager import DatabaseManager


class DatabaseValidator:
    """Controlla la coerenza dei dataset."""

    def __init__(self):
        self.db = DatabaseManager()

    def validate(self):
        clubs = self.db.get_clubs()
        players = self.db.get_players()
        stadiums = self.db.get_stadiums()
        competitions = self.db.get_competitions()
        countries = self.db.get_countries()

        errors = []

        club_ids = {club["id"] for club in clubs}
        stadium_ids = {stadium["id"] for stadium in stadiums}
        competition_ids = {competition["id"] for competition in competitions}
        country_ids = {country["id"] for country in countries}

        for club in clubs:
            if club.get("competition_id") not in competition_ids:
                errors.append(f"Club senza competizione valida: {club.get('name')}")

            if club.get("stadium_id") not in stadium_ids:
                errors.append(f"Club senza stadio valido: {club.get('name')}")

        for player in players:
            if player.get("club_id") not in club_ids:
                errors.append(f"Giocatore senza club valido: {player.get('name')}")

            if player.get("competition_id") not in competition_ids:
                errors.append(f"Giocatore senza competizione valida: {player.get('name')}")

            if player.get("nationality_id") not in country_ids:
                errors.append(f"Giocatore senza nazionalità valida: {player.get('name')}")

        return errors