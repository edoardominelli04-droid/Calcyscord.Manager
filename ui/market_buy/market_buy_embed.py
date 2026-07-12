import discord


class MarketBuyEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player,
        owner,
        budget
    ):

        embed = discord.Embed(

            title=f"🛒 Acquista - {player['name']}",

            color=discord.Color.green()

        )

        image = player.get("image")

        if image:

            embed.set_thumbnail(

                url=image

            )

        manager = (

            "🤖 Sistema"

            if owner["is_bot"]

            else owner["manager"]["username"]

        )

        embed.add_field(

            name="💰 Valore di mercato",

            value=f"€ {player['market_value']:,}".replace(",", "."),

            inline=True

        )

        embed.add_field(

            name="👤 Proprietario",

            value=manager,

            inline=True

        )

        embed.add_field(

            name="🏟️ Club",

            value=owner["club"]["name"],

            inline=True

        )

        embed.add_field(

            name="💳 Budget disponibile",

            value=f"€ {budget:,}".replace(",", "."),

            inline=True

        )

        embed.add_field(

            name="📋 Operazione",

            value="Seleziona una modalità tramite i pulsanti.",

            inline=False

        )

        embed.set_footer(

            text="Calcyscord.Manager • Acquisto"

        )

        return embed