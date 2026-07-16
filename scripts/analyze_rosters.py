from collections import Counter

from services.database_manager import DatabaseManager


def main():

    db = DatabaseManager()

    players = db.get_players()
    rosters = db.get_current_rosters()
    clubs = db.get_clubs()

    players_by_id = {
        player["id"]: player
        for player in players
    }

    clubs_by_id = {
        club["id"]: club["name"]
        for club in clubs
    }

    print("=" * 80)

    for roster in rosters:

        counter = Counter()

        for player_id in roster["players"]:

            player = players_by_id.get(player_id)

            if player is None:
                continue

            counter[player["position"]] += 1

        print(
            f"{clubs_by_id.get(roster['club_id'], roster['club_id']):30}"
            f" GK:{counter['Goalkeeper']:2}"
            f" DEF:{counter['Defender']:2}"
            f" MID:{counter['Midfield']:2}"
            f" ATT:{counter['Attack']:2}"
        )

    print("=" * 80)


if __name__ == "__main__":
    main()