import discord


class TransferRequestDetailEmbedBuilder:
    """Embed di dettaglio di una richiesta di trasferimento."""

    def build(
        self,
        buyer,
        seller,
        player,
        request
    ):

        embed = discord.Embed(

            title="📨 Offerta di trasferimento",

            colour=discord.Colour.orange()

        )

        embed.add_field(

            name="⚽ Giocatore",

            value=player["name"],

            inline=False

        )

        embed.add_field(

            name="👤 Club acquirente",

            value=buyer["username"],

            inline=True

        )

        embed.add_field(

            name="💰 Offerta",

            value=f"€ {request['amount']:,}".replace(",", "."),

            inline=True

        )

        embed.set_footer(

            text=f"Richiesta #{request['id']}"

        )

        return embed