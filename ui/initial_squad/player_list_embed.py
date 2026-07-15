import discord


class PlayerListEmbedBuilder:
    """Embed che visualizza una lista di giocatori."""

    def build(
        self,
        title,
        players
    ):

        embed = discord.Embed(
            title=title,
            colour=discord.Colour.blurple()
        )

        if not players:

            embed.description = (
                "Nessun giocatore disponibile."
            )

            return embed

        lines = []

        for index, player in enumerate(players, start=1):

            value = player.get("market_value") or 0

            lines.append(

                f"**{index}.** {player['name']}\n"
                f"💰 {value:,.0f} €".replace(",", ".")

            )

        embed.description = "\n\n".join(lines)

        embed.set_footer(

            text=f"{len(players)} giocatori disponibili"

        )

        return embed