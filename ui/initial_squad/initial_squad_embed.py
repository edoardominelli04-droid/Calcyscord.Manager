import discord


class InitialSquadEmbedBuilder:
    """Embed della composizione della rosa iniziale."""

    def build_home(
        self,
        draft,
        counts
    ):

        budget = draft["budget"]

        used = draft["points_used"]

        embed = discord.Embed(

            title="👥 Componi la rosa iniziale",

            description=(
                "Seleziona i giocatori della tua rosa iniziale.\n\n"

                f"💰 **Budget:** {used} / {budget} punti\n\n"

                f"🥅 **Portieri:** {counts['Goalkeeper']}/2\n"

                f"🛡️ **Difensori:** {counts['Defender']}/6\n"

                f"🎯 **Centrocampisti:** {counts['Midfield']}/7\n"

                f"⚽ **Attaccanti:** {counts['Attack']}/5"
            ),

            colour=discord.Colour.blurple()

        )

        embed.set_footer(

            text=(
                "Completa la rosa per poter confermare."
            )

        )

        return embed