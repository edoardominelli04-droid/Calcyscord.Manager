import discord


# ==========================================================
# CERCA
# ==========================================================

class SearchClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Cerca per nome",

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
# SFOGLIA
# ==========================================================

class BrowseClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Sfoglia",

            emoji="🧭",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_browse(

            interaction

        )


# ==========================================================
# SUGGERITI
# ==========================================================

class SuggestedClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Club suggeriti",

            emoji="🎲",

            style=discord.ButtonStyle.success,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_suggestions(

            interaction

        )


# ==========================================================
# CHIUDI
# ==========================================================

class CloseButton(discord.ui.Button):

    def __init__(
        self
    ):

        super().__init__(

            label="Chiudi",

            emoji="❌",

            style=discord.ButtonStyle.danger,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.edit_message(

            content="Procedura annullata.",

            embed=None,

            view=None

        )