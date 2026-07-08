import discord


class RosterEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        data
    ):

        club = data["club"]

        embed = discord.Embed(

            title=f"👥 Rosa - {club['name']}",

            color=discord.Color.blue()

        )

        embed.add_field(

            name="🧤 Portieri",

            value="2",

            inline=True

        )

        embed.add_field(

            name="🛡 Difensori",

            value="8",

            inline=True

        )

        embed.add_field(

            name="⚙️ Centrocampisti",

            value="7",

            inline=True

        )

        embed.add_field(

            name="⚽ Attaccanti",

            value="5",

            inline=True

        )

        embed.set_footer(

            text="Seleziona un reparto tramite i pulsanti."

        )

        return embed