import discord


class MarketOwnerEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player,
        owner
    ):

        embed = discord.Embed(

            title=f"👤 Proprietario - {player['name']}",

            color=discord.Color.blue()

        )

        image = player.get("image")

        if image:

            embed.set_thumbnail(

                url=image

            )

        if owner["is_bot"]:

            manager_name = "🤖 Sistema"

            status = "🤖 Gestito dal sistema"

        else:

            manager_name = owner["manager"]["username"]
        

            status = "🟢 Gestito da un manager"

        embed.add_field(

            name="👤 Manager",

            value=manager_name,

            inline=True

        )

        embed.add_field(

            name="🏟️ Club",

            value=owner["club"]["name"],

            inline=True

        )

        embed.add_field(

            name="📄 Stato sul mercato",

            value=status,

            inline=False

        )

        embed.set_footer(

            text="Calcyscord.Manager • Proprietario"

        )

        return embed