import discord


# ==========================================================
# CERCA
# ==========================================================

class SearchButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Cerca",

            emoji="🔍",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_search(

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

        await self.view_data.show_buy(

            interaction

        )


# ==========================================================
# VENDI
# ==========================================================

class SellButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Vendi",

            emoji="💸",

            style=discord.ButtonStyle.danger,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_sell(

            interaction

        )


# ==========================================================
# TRASFERIMENTI
# ==========================================================

class TransfersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Trasferimenti",

            emoji="📋",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_transfers(

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