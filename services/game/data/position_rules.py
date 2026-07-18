POSITION_RULES = {
    "GK": ["Goalkeeper"],

    # Gli esterni di centrocampo possono arretrare sulla stessa fascia.
    # È necessario per club che giocano abitualmente con quinti, come
    # l'Atalanta, dove Transfermarkt li classifica come Midfield.
    "LB": ["Left-Back", "Left Wing-Back", "Left Midfield"],
    "LWB": ["Left Wing-Back", "Left-Back", "Left Midfield"],
    "CB": ["Centre-Back"],
    "RB": ["Right-Back", "Right Wing-Back", "Right Midfield"],
    "RWB": ["Right Wing-Back", "Right-Back", "Right Midfield"],

    "DM": ["Defensive Midfield"],
    "CM": ["Central Midfield"],
    "AM": ["Attacking Midfield"],
    "LM": ["Left Midfield", "Left Wing-Back", "Left-Back"],
    "RM": ["Right Midfield", "Right Wing-Back", "Right-Back"],
    "LW": ["Left Winger"],
    "RW": ["Right Winger"],
    "ST": ["Centre-Forward", "Second Striker"]
}
