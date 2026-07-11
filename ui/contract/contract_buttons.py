import discord


# ==========================================================
# RINNOVA
# ==========================================================

class RenewButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Rinnova",

            emoji="✍️",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Sistema rinnovi in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# CLUB
# ==========================================================

class ClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Club",

            emoji="🏟️",

            style=discord.ButtonStyle.success,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_club(

            interaction

        )