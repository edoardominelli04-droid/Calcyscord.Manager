import discord

from datetime import datetime


COUNTRIES = {

    "Italy": "🇮🇹 Italia",
    "France": "🇫🇷 Francia",
    "Germany": "🇩🇪 Germania",
    "Spain": "🇪🇸 Spagna",
    "England": "🏴 Inghilterra",
    "Portugal": "🇵🇹 Portogallo",
    "Brazil": "🇧🇷 Brasile",
    "Argentina": "🇦🇷 Argentina",
    "Belgium": "🇧🇪 Belgio",
    "Netherlands": "🇳🇱 Paesi Bassi"

}


POSITIONS = {

    "Goalkeeper": "Portiere",
    "Defender": "Difensore",
    "Midfield": "Centrocampista",
    "Attack": "Attaccante"

}


SUB_POSITIONS = {

    "Centre-Forward": "Punta centrale",
    "Second Striker": "Seconda punta",

    "Left Winger": "Ala sinistra",
    "Right Winger": "Ala destra",

    "Attacking Midfield": "Trequartista",
    "Central Midfield": "Centrocampista centrale",
    "Defensive Midfield": "Mediano",

    "Centre-Back": "Difensore centrale",
    "Left-Back": "Terzino sinistro",
    "Right-Back": "Terzino destro"

}


FEET = {

    "right": "Destro",
    "left": "Sinistro",
    "both": "Ambidestro"

}


MONTHS = {

    1: "gennaio",
    2: "febbraio",
    3: "marzo",
    4: "aprile",
    5: "maggio",
    6: "giugno",
    7: "luglio",
    8: "agosto",
    9: "settembre",
    10: "ottobre",
    11: "novembre",
    12: "dicembre"

}


class PlayerEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player
    ):

        embed = discord.Embed(

            title=f"👤 {player['name']}",

            color=discord.Color.blue()

        )

        embed.set_thumbnail(

            url=player["image"]

        )

        birth = datetime.strptime(

            player["date_of_birth"],

            "%Y-%m-%d %H:%M:%S"

        )

        today = datetime.today()

        age = (

            today.year
            - birth.year
            - (
                (today.month, today.day)
                <
                (birth.month, birth.day)
            )

        )

        birth_date = (

            f"{birth.day} "
            f"{MONTHS[birth.month]} "
            f"{birth.year}"

        )

        market_value = int(

            player.get("market_value") or 0

        )

        market_value = (

            f"€{market_value:,}"

            .replace(",", ".")

        )

        country = COUNTRIES.get(

            player["country"],

            player["country"]

        )

        position = POSITIONS.get(

            player["position"],

            player["position"]

        )

        sub_position = SUB_POSITIONS.get(

            player["sub_position"],

            player["sub_position"]

        )

        foot = FEET.get(

            player["preferred_foot"],

            player["preferred_foot"]

        )

        embed.add_field(

            name="🌍 Nazionalità",

            value=country,

            inline=True

        )

        embed.add_field(

            name="⚽ Ruolo",

            value=f"{position} ({sub_position})",

            inline=True

        )

        embed.add_field(

            name="💰 Valore",

            value=market_value,

            inline=False

        )

        embed.add_field(

            name="📅 Nato",

            value=birth_date,

            inline=True

        )

        embed.add_field(

            name="🎂 Età",

            value=f"{age} anni",

            inline=True

        )

        embed.add_field(

            name="👣 Piede",

            value=foot,

            inline=True

        )

        embed.add_field(

            name="📏 Altezza",

            value=f"{int(player['height_cm'])} cm",

            inline=True

        )

        return embed