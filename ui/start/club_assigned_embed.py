import discord


class ClubAssignedEmbedBuilder:
    """Embed mostrato dopo l'assegnazione del club."""

    def build(
        self,
        club,
        competition
    ):

        embed = discord.Embed(

            title="🎉 Complimenti!",

            description=(

                f"Sei il nuovo manager del **{club['name']}**.\n\n"

                "La tua avventura in **Calcyscord.Manager** può finalmente iniziare."

            ),

            colour=discord.Colour.green()

        )

        embed.add_field(

            name="🏆 Competizione",

            value=competition["name"],

            inline=True

        )

        embed.add_field(

            name="🏟️ Stadio",

            value=club["stadium_name"],

            inline=True

        )

        embed.add_field(

            name="💰 Budget iniziale",

            value="100 punti",

            inline=False

        )

        embed.add_field(

            name="📢 Prossimo obiettivo",

            value=(
                "La stagione è alle porte.\n"
                "Prima dell'esordio dovrai costruire la tua rosa iniziale "
                "scegliendo i giocatori che vestiranno la maglia del club."
            ),

            inline=False

        )

        embed.set_footer(

            text="Premi il pulsante qui sotto per iniziare la tua carriera."

        )

        return embed