import discord

from ui.search.search_modal import SearchModal

# ==========================================================
# PORTIERI
# ==========================================================

class GoalkeepersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Portieri",

            emoji="🧤",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_goalkeepers(
            interaction
        )


# ==========================================================
# DIFENSORI
# ==========================================================

class DefendersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Difensori",

            emoji="🛡️",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_defenders(
            interaction
        )


# ==========================================================
# CENTROCAMPISTI
# ==========================================================

class MidfieldersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Centrocampisti",

            emoji="⚙️",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_midfielders(
            interaction
        )


# ==========================================================
# ATTACCANTI
# ==========================================================

class AttackersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Attaccanti",

            emoji="⚽",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_attackers(
            interaction
        )


# ==========================================================
# CERCA GIOCATORE
# ==========================================================

class SearchPlayerButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Cerca",

            emoji="🔍",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_modal(

            SearchModal(

                self.view_data.club_service,

                self.view_data.club_embed_builder,

                self.view_data.roster_embed_builder,

                self.view_data.data

            )

        )

# ==========================================================
# TORNA AL CLUB
# ==========================================================

class BackClubButton(discord.ui.Button):

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