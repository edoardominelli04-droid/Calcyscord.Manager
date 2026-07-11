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


SUBPOSITION_TRANSLATIONS = {

    "Goalkeeper": "Portiere",
    "Centre-Back": "Difensore Centrale",
    "Left-Back": "Terzino Sinistro",
    "Right-Back": "Terzino Destro",
    "Defensive Midfield": "Mediano",
    "Central Midfield": "Centrocampista Centrale",
    "Attacking Midfield": "Trequartista",
    "Left Midfield": "Centrocampista Sinistro",
    "Right Midfield": "Centrocampista Destro",
    "Left Winger": "Ala Sinistra",
    "Right Winger": "Ala Destra",
    "Centre-Forward": "Attaccante Centrale",
    "Second Striker": "Seconda Punta"

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

        market_value = player.get(

            "market_value"

        ) or 0

        market_value = (

            f"€{int(market_value):,}"

            .replace(",", ".")

        )

        country = COUNTRIES.get(

            player["country"],

            player["country"]

        )

        sub_position = SUBPOSITION_TRANSLATIONS.get(

            player["sub_position"],

            player["sub_position"]

        )

        foot = FEET.get(

            player["preferred_foot"],

            player["preferred_foot"]

        )

        height = player.get(

            "height_cm"

        )

        height = (

            f"{int(height)} cm"

            if height

            else "---"

        )

        embed.add_field(

            name="🌍 Nazionalità",

            value=country,

            inline=True

        )

        embed.add_field(

            name="⚽ Ruolo",

            value=sub_position,

            inline=True

        )

        embed.add_field(

            name="💰 Valore",

            value=market_value,

            inline=False

        )

        embed.add_field(

            name="📅 Data di nascita",

            value=birth_date,

            inline=False

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

            value=height,

            inline=True

        )

        return embed