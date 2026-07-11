import discord


class StatisticsEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player
    ):

        embed = discord.Embed(

            title=f"📊 Statistiche - {player['name']}",

            color=discord.Color.orange()

        )

        embed.set_thumbnail(

            url=player["image"]

        )

        embed.add_field(

            name="⚽ Gol",

            value="---",

            inline=True

        )

        embed.add_field(

            name="🎯 Assist",

            value="---",

            inline=True

        )

        embed.add_field(

            name="⏱️ Minuti",

            value="---",

            inline=True

        )

        embed.add_field(

            name="🏟️ Presenze",

            value="---",

            inline=True

        )

        embed.add_field(

            name="⭐ Media voto",

            value="---",

            inline=True

        )

        embed.add_field(

            name="🟨 Ammonizioni",

            value="---",

            inline=True

        )

        embed.add_field(

            name="🟥 Espulsioni",

            value="---",

            inline=True

        )

        embed.set_footer(

            text="Calcyscord.Manager • Statistiche"

        )

        return embed