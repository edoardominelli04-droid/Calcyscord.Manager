from services.game.squad_service import SquadService

service = SquadService()

MANAGER_ID = 3
CLUB_ID = 1

try:

    squad = service.create_initial_squad(
        MANAGER_ID,
        CLUB_ID
    )

    print()

    print("Giocatori creati:", len(squad))

    if squad:
        print()
        print("Primo giocatore:")
        print(squad[0])

except ValueError as e:

    print(e)