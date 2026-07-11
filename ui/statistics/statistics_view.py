import discord

from ui.statistics.statistics_embed import StatisticsEmbedBuilder

from ui.statistics.statistics_buttons import (
    ClubButton
)


class StatisticsView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data,
        player
    ):

        super().__init__(
            timeout=300
        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.player = player

        self.statistics_embed_builder = StatisticsEmbedBuilder()

        self.message = None

        self.add_item(
            ClubButton(self)
        )

    async def show_statistics(
        self,
        interaction: discord.Interaction
    ):

        embed = self.statistics_embed_builder.build(

            self.player

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_club(
        self,
        interaction: discord.Interaction
    ):

        from ui.club.club_view import ClubView

        embed = self.club_embed_builder.build(

            self.data

        )

        view = ClubView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await interaction.response.edit_message(

            embed=embed,

            view=view

        )

        view.message = await interaction.original_response()