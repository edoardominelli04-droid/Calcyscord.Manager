import discord

from ui.start.start_embed import StartEmbedBuilder
from ui.start.start_browse_buttons import CompetitionSelect


class StartBrowseView(discord.ui.View):
    """Visualizza le competizioni disponibili."""

    def __init__(
        self,
        parent_view,
        competitions
    ):

        super().__init__(
            timeout=300
        )

        self.parent_view = parent_view

        self.competitions = competitions

        self.embed_builder = StartEmbedBuilder()

        self.message = None

        if competitions:

            self.add_item(

                CompetitionSelect(

                    self,

                    competitions

                )

            )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build_competition_list(

            self.competitions

        )

        await interaction.response.send_message(

            embed=embed,

            view=self,

            ephemeral=True

        )

        self.message = await interaction.original_response()

    async def select_competition(
        self,
        interaction: discord.Interaction,
        competition_id
    ):

        clubs = (

            self.parent_view.start_service
            .get_clubs_by_competition(

                competition_id

            )

        )

        from ui.start.start_search_view import (
            StartSearchView
        )

        view = StartSearchView(

            self.parent_view,

            clubs

        )

        await view.show(

            interaction

        )