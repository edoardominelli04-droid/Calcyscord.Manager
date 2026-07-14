import random

from services.database_manager import DatabaseManager
from services.game.club_selection_service import ClubSelectionService


class StartService:
    """Gestisce la ricerca e la selezione dei club nell'onboarding."""

    def __init__(self):

        self.db = DatabaseManager()

        self.club_selection_service = ClubSelectionService()

    # ==========================================================
    # CLUB DISPONIBILI
    # ==========================================================

    def get_available_clubs(self):

        clubs = self.db.get_clubs()

        ownership = self.db.get_club_ownership()

        taken_club_ids = {

            record["club_id"]

            for record in ownership

            if record.get("manager_id") is not None

        }

        return [

            club

            for club in clubs

            if (
                club.get("active", True)
                and club["id"] not in taken_club_ids
            )

        ]

    # ==========================================================
    # RICERCA PER NOME
    # ==========================================================

    def search_clubs(
        self,
        name
    ):

        query = name.strip().lower()

        if not query:

            return []

        matches = [

            club

            for club in self.get_available_clubs()

            if query in club["name"].lower()

        ]

        return sorted(

            matches,

            key=lambda club: (

                not club["name"].lower().startswith(query),

                club["name"].lower()

            )

        )

    # ==========================================================
    # CLUB SUGGERITI
    # ==========================================================

    def get_suggested_clubs(
        self,
        limit=5
    ):

        clubs = self.get_available_clubs()

        if not clubs:

            return []

        limit = min(
            limit,
            len(clubs)
        )

        return random.sample(
            clubs,
            limit
        )

    # ==========================================================
    # COMPETIZIONI DISPONIBILI
    # ==========================================================

    def get_available_competitions(self):

        clubs = self.get_available_clubs()

        competition_ids = {

            club.get("competition_id")

            for club in clubs

            if club.get("competition_id") is not None

        }

        competitions = []

        for competition_id in competition_ids:

            competition = self.db.get_competition_by_id(
                competition_id
            )

            if competition is not None:

                competitions.append(
                    competition
                )

        return sorted(

            competitions,

            key=lambda competition: competition["name"].lower()

        )

    # ==========================================================
    # CLUB PER COMPETIZIONE
    # ==========================================================

    def get_clubs_by_competition(
        self,
        competition_id
    ):

        return sorted(

            [

                club

                for club in self.get_available_clubs()

                if club.get("competition_id") == competition_id

            ],

            key=lambda club: club["name"].lower()

        )

    # ==========================================================
    # CONTROLLO DISPONIBILITÀ
    # ==========================================================

    def is_club_available(
        self,
        club_id
    ):

        return any(

            club["id"] == club_id

            for club in self.get_available_clubs()

        )

    # ==========================================================
    # CONFERMA SCELTA
    # ==========================================================

    def confirm_club(
        self,
        discord_id,
        club_id
    ):

        if not self.is_club_available(
            club_id
        ):

            raise ValueError(
                "Il club non è più disponibile."
            )

        return self.club_selection_service.choose_club(

            discord_id,

            club_id

        )