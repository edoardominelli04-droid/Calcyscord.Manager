import discord


# ==========================================================
# ACQUISTO DEFINITIVO
# ==========================================================

class PurchaseButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Acquisto",

            emoji="💰",

            style=discord.ButtonStyle.success,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_purchase(

            interaction

        )


# ==========================================================
# PRESTITO
# ==========================================================

class LoanButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Prestito",

            emoji="🤝",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_loan(

            interaction

        )


# ==========================================================
# GIOCATORE
# ==========================================================

class PlayerButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Giocatore",

            emoji="👤",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_player(

            interaction

        )


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

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_market(

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

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_club(

            interaction

        )