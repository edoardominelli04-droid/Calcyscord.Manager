import discord


class ContractEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player
    ):

        embed = discord.Embed(

            title=f"📜 Contratto - {player['name']}",

            color=discord.Color.green()

        )

        embed.set_thumbnail(

            url=player["image"]

        )

        embed.add_field(

            name="💰 Stipendio",

            value="€ ---",

            inline=True

        )

        embed.add_field(

            name="📅 Scadenza",

            value="Da definire",

            inline=True

        )

        embed.add_field(

            name="⏳ Durata residua",

            value="---",

            inline=True

        )

        embed.set_footer(

            text="Calcyscord.Manager • Contratto"

        )

        return embed