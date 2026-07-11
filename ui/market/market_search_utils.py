def find_player(
    players,
    name
):

    name = name.lower().strip()

    for player in players:

        if name in player["name"].lower():

            return player

    return None