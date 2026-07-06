from collections import Counter
from services.database_manager import DatabaseManager


class DatabaseValidator:
    """Controlla la coerenza del database."""

    def __init__(self):
        self.db = DatabaseManager()
        self.errors = []

    def validate(self):
        self.errors = []

        # -----------------------------
        # DUPLICATI
        # -----------------------------
        self.check_duplicate_player_external_ids()
        self.check_duplicate_club_external_ids()
        self.check_duplicate_competition_external_ids()

        # -----------------------------
        # INTEGRITÀ
        # -----------------------------
        self.check_players_without_club()
        self.check_clubs_without_competition()
        self.check_clubs_without_stadium()

        # -----------------------------
        # RELAZIONI
        # -----------------------------
        self.check_player_club_links()
        self.check_club_competition_links()
        self.check_club_stadium_links()

        return self.errors

    # ======================================================
    # DUPLICATI
    # ======================================================

    def check_duplicate_player_external_ids(self):
        players = self.db.get_players()

        ids = Counter(
            player["external_id"]
            for player in players
            if player.get("external_id") is not None
        )

        for external_id, count in ids.items():
            if count > 1:
                self.errors.append(
                    f"Player external_id duplicato: {external_id}"
                )

    def check_duplicate_club_external_ids(self):
        clubs = self.db.get_clubs()

        ids = Counter(
            club["external_id"]
            for club in clubs
            if club.get("external_id") is not None
        )

        for external_id, count in ids.items():
            if count > 1:
                self.errors.append(
                    f"Club external_id duplicato: {external_id}"
                )

    def check_duplicate_competition_external_ids(self):
        competitions = self.db.get_competitions()

        ids = Counter(
            competition["external_id"]
            for competition in competitions
            if competition.get("external_id") is not None
        )

        for external_id, count in ids.items():
            if count > 1:
                self.errors.append(
                    f"Competition external_id duplicato: {external_id}"
                )

    # ======================================================
    # INTEGRITÀ
    # ======================================================

    def check_players_without_club(self):
        for player in self.db.get_players():
            if player.get("club_id") is None:
                self.errors.append(
                    f"Giocatore senza club: {player['name']}"
                )

    def check_clubs_without_competition(self):
        for club in self.db.get_clubs():
            if club.get("competition_id") is None:
                self.errors.append(
                    f"Club senza competizione: {club['name']}"
                )

    def check_clubs_without_stadium(self):
        for club in self.db.get_clubs():
            if club.get("stadium_id") is None:
                self.errors.append(
                    f"Club senza stadio: {club['name']}"
                )

    # ======================================================
    # RELAZIONI
    # ======================================================

    def check_player_club_links(self):
        clubs = {
            club["id"]
            for club in self.db.get_clubs()
        }

        for player in self.db.get_players():
            if player["club_id"] not in clubs:
                self.errors.append(
                    f"Club inesistente per il giocatore: {player['name']}"
                )

    def check_club_competition_links(self):
        competitions = {
            competition["id"]
            for competition in self.db.get_competitions()
        }

        for club in self.db.get_clubs():
            if club["competition_id"] not in competitions:
                self.errors.append(
                    f"Competizione inesistente per il club: {club['name']}"
                )

    def check_club_stadium_links(self):
        stadiums = {
            stadium["id"]
            for stadium in self.db.get_stadiums()
        }

        for club in self.db.get_clubs():
            if club["stadium_id"] not in stadiums:
                self.errors.append(
                    f"Stadio inesistente per il club: {club['name']}"
                )