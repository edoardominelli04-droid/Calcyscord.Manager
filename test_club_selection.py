from services.game.registration_service import RegistrationService
from services.game.club_selection_service import ClubSelectionService


registration = RegistrationService()
club_selection = ClubSelectionService()

DISCORD_ID = 111111111
USERNAME = "Edoardo"

# Registrazione (se già esiste non succede nulla)
manager, finance, created = registration.register(
    DISCORD_ID,
    USERNAME
)

# Scegli il club (cambia l'ID se vuoi provarne un altro)
CLUB_ID = 1

try:

    manager, club = club_selection.choose_club(
        DISCORD_ID,
        CLUB_ID
    )

    print()
    print("=== CLUB ASSEGNATO ===")
    print()

    print("Manager:")
    print(manager)

    print()
    print("Club:")
    print(club)

except ValueError as e:

    print()
    print("ERRORE")
    print(e)