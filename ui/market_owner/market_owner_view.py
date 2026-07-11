import discord

from ui.market_owner.market_owner_embed import MarketOwnerEmbedBuilder
from ui.market_owner.market_owner_buttons import (
    PlayerButton,
    MarketButton,
    ClubButton
)


class MarketOwnerView(discord.ui.View):

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

        self.market_owner_embed_builder = MarketOwnerEmbedBuilder()

        self.message = None

        self.add_item(
            PlayerButton(self)
        )

        self.add_item(
            MarketButton(self)
        )

        self.add_item(
            ClubButton(self)
        )

    async def show_owner(
        self,
        interaction: discord.Interaction
    ):

        owner = self.club_service.get_player_owner(

            self.player["id"]

        )

        embed = self.market_owner_embed_builder.build(

            self.player,

            owner

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_player(
        self,
        interaction: discord.Interaction
    ):

        from ui.market_player.market_player_view import MarketPlayerView

        view = MarketPlayerView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            self.player

        )

        await view.show_player(

            interaction

        )

    async def show_market(
        self,
        interaction: discord.Interaction
    ):

        from ui.market.market_view import MarketView

        view = MarketView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await view.show_market(

            interaction

        )

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