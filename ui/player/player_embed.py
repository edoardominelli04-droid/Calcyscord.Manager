import discord
from datetime import datetime


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

        value = int(

            player.get("market_value") or 0

        )

        value = f"€{value:,}".replace(",", ".")

        embed.add_field(

            name="🌍 Nazionalità",

            value=player["country"],

            inline=True

        )

        embed.add_field(

            name="⚽ Ruolo",

            value=f"{player['position']} ({player['sub_position']})",

            inline=True

        )

        embed.add_field(

            name="💰 Valore",

            value=value,

            inline=False

        )

        embed.add_field(

            name="📅 Nato",

            value=birth.strftime("%d/%m/%Y"),

            inline=True

        )

        embed.add_field(

            name="🎂 Età",

            value=str(age),

            inline=True

        )

        embed.add_field(

            name="👣 Piede",

            value=player["preferred_foot"].capitalize(),

            inline=True

        )

        embed.add_field(

            name="📏 Altezza",

            value=f"{int(player['height_cm'])} cm",

            inline=True

        )

        return embed