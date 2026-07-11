import discord


class MarketEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        data
    ):

        club = data["club"]
        finance = data.get("finance") or {}
        players = data.get("players") or []

        balance = (
            finance.get("balance")
            or finance.get("budget")
            or finance.get("credits")
            or 0
        )

        balance = (
            f"€{int(balance):,}"
            .replace(",", ".")
        )

        embed = discord.Embed(

            title=f"💰 Mercato - {club['name']}",

            color=discord.Color.gold()

        )

        embed.add_field(

            name="💵 Budget",

            value=balance,

            inline=False

        )

        embed.add_field(

            name="👥 Giocatori in rosa",

            value=str(len(players)),

            inline=False

        )

        embed.add_field(

            name="📋 Trasferimenti attivi",

            value="0",

            inline=False

        )

        embed.add_field(

            name="📨 Offerte ricevute",

            value="0",

            inline=True

        )

        embed.add_field(

            name="📤 Offerte inviate",

            value="0",

            inline=True

        )

        embed.set_footer(

            text="Calcyscord.Manager • Mercato"

        )

        return embed