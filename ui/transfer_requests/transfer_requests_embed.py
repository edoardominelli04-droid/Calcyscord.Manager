import discord


class TransferRequestsEmbedBuilder:
    """Costruisce l'embed delle offerte ricevute."""

    def build(
        self,
        requests
    ):

        embed = discord.Embed(

            title="📨 Offerte ricevute",

            description=(
                "Seleziona una trattativa da valutare."
            ),

            colour=discord.Colour.orange()

        )

        if not requests:

            embed.description = (

                "Non hai offerte di mercato in attesa."

            )

            return embed

        for item in requests:

            request = item["request"]

            buyer = item["buyer"]

            player = item["player"]

            embed.add_field(

                name=player["name"],

                value=(

                    f"👤 **{buyer['username']}**\n"

                    f"💰 **€ {request['amount']:,}**".replace(",", ".")

                ),

                inline=False

            )

        embed.set_footer(

            text=f"{len(requests)} offerte pendenti"

        )

        return embed