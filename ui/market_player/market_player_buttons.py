import discord


# ==========================================================
# MERCATO
# ==========================================================

class MarketButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Mercato",

            emoji="💰",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_market(

            interaction

        )


# ==========================================================
# ACQUISTA
# ==========================================================

class BuyButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Acquista",

            emoji="🛒",

            style=discord.ButtonStyle.success,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Sistema acquisti in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# PROPRIETARIO
# ==========================================================

class OwnerButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Proprietario",

            emoji="👤",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Informazioni proprietario in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# STATISTICHE
# ==========================================================

class StatisticsButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Statistiche",

            emoji="📊",

            style=discord.ButtonStyle.primary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_statistics(

            interaction

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

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_club(

            interaction

        )