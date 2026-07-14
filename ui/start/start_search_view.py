import discord

from ui.start.start_embed import StartEmbedBuilder

from ui.start.start_search_buttons import (
    ClubSearchSelect
)

from ui.start.start_confirm_view import (
    StartConfirmView
)

class StartSearchView(discord.ui.View):
    """Visualizza i risultati della ricerca dei club."""

    def __init__(
        self,
        parent_view,
        clubs
    ):

        super().__init__(
            timeout=300
        )

        self.parent_view = parent_view

        self.clubs = clubs

        self.embed_builder = StartEmbedBuilder()

        self.message = None

        if clubs:

            self.add_item(

                ClubSearchSelect(

                    self,

                    clubs

                )

            )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build_club_list(

            self.clubs

        )

        await interaction.response.send_message(

            embed=embed,

            view=self,

            ephemeral=True

        )

        self.message = await interaction.original_response()

    async def select_club(
        self,
        interaction: discord.Interaction,
        club_id
    ):

        club = next(

            (

                c

                for c in self.clubs

                if c["id"] == club_id

            ),

            None

        )

        if club is None:

            await interaction.response.send_message(

                "❌ Club non trovato.",

                ephemeral=True

            )

            return

        view = StartConfirmView(

            self.parent_view,

            club

        )

        await view.show(

            interaction

        )