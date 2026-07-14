import discord

from services.game.start_service import StartService

from ui.start.start_embed import (
    StartEmbedBuilder
)

from ui.start.start_search_modal import (
    StartSearchModal
)

from ui.start.start_search_view import (
    StartSearchView
)

from ui.start.start_buttons import (
    SearchClubButton,
    BrowseClubButton,
    SuggestedClubButton,
    CloseButton
)


class StartView(discord.ui.View):
    """View principale dell'onboarding."""

    def __init__(
        self,
        discord_id
    ):

        super().__init__(
            timeout=300
        )

        self.discord_id = discord_id

        self.start_service = StartService()

        self.embed_builder = StartEmbedBuilder()

        self.message = None

        self.add_item(
            SearchClubButton(self)
        )

        self.add_item(
            BrowseClubButton(self)
        )

        self.add_item(
            SuggestedClubButton(self)
        )

        self.add_item(
            CloseButton()
        )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build_welcome()

        await interaction.response.send_message(

            embed=embed,

            view=self,

            ephemeral=True

        )

        self.message = await interaction.original_response()

    # ==========================================================
    # PULSANTI
    # ==========================================================

    async def show_search(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_modal(

            StartSearchModal(

                self

            )

        )

    async def search_club(
        self,
        interaction: discord.Interaction,
        name
    ):

        clubs = self.start_service.search_clubs(

            name

        )

        view = StartSearchView(

            self,

            clubs

        )

        await view.show(

            interaction

        )

    async def show_browse(
        self,
        interaction: discord.Interaction
    ):

        from ui.start.start_browse_view import (
            StartBrowseView
        )

        competitions = (

            self.start_service
            .get_available_competitions()

        )

        view = StartBrowseView(

            self,

            competitions

        )

        await view.show(

            interaction

        )

    async def show_suggestions(
        self,
        interaction: discord.Interaction
    ):

        from ui.start.start_search_view import (
            StartSearchView
        )

        clubs = self.start_service.get_suggested_clubs()

        view = StartSearchView(

            self,

            clubs

        )

        await view.show(

            interaction

        )