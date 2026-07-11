import discord

from ui.club.club_buttons import (
    RosaButton,
    FormazioneButton,
    MercatoButton,
    ContrattiButton,
    ClassificaButton,
    NotificheButton
)

from ui.roster.roster_view import RosterView
from ui.market.market_view import MarketView


class ClubView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data
    ):

        super().__init__(
            timeout=300
        )

        self.club_service = club_service
        self.club_embed_builder = club_embed_builder
        self.roster_embed_builder = roster_embed_builder
        self.data = data
        self.message = None

        self.add_item(
            RosaButton(self)
        )

        self.add_item(
            FormazioneButton(self)
        )

        self.add_item(
            MercatoButton(self)
        )

        self.add_item(
            ContrattiButton(self)
        )

        self.add_item(
            ClassificaButton(self)
        )

        self.add_item(
            NotificheButton(self)
        )

    async def show_roster(
        self,
        interaction: discord.Interaction
    ):

        embed = self.roster_embed_builder.build(

            self.data

        )

        view = RosterView(

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

    async def show_market(
        self,
        interaction: discord.Interaction
    ):

        view = MarketView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await view.show_market(

            interaction

        )