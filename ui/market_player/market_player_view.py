import discord

from ui.market_player.market_player_embed import MarketPlayerEmbedBuilder
from ui.market_player.market_player_buttons import (
    BuyButton,
    OwnerButton,
    StatisticsButton,
    ClubButton,
    MarketButton
)


class MarketPlayerView(discord.ui.View):

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

        self.market_player_embed_builder = MarketPlayerEmbedBuilder()

        self.message = None

        self.add_item(
            MarketButton(self)
        )

        self.add_item(
            BuyButton(self)
        )

        self.add_item(
            OwnerButton(self)
        )

        self.add_item(
            StatisticsButton(self)
        )

        self.add_item(
            ClubButton(self)
        )

    async def show_player(
        self,
        interaction: discord.Interaction
    ):

        embed = self.market_player_embed_builder.build(

            self.player

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_statistics(
        self,
        interaction: discord.Interaction
    ):

        from ui.market_statistics.market_statistics_view import MarketStatisticsView

        view = MarketStatisticsView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            self.player

        )

        await view.show_statistics(

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

    async def show_buy(
        self,
        interaction: discord.Interaction
    ):

        from ui.market_buy.market_buy_view import MarketBuyView

        view = MarketBuyView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            self.player

        )

        await view.show_buy(

            interaction

        )
    
    async def show_owner(
        self,
        interaction: discord.Interaction
    ):

        from ui.market_owner.market_owner_view import MarketOwnerView

        view = MarketOwnerView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            self.player

        )

        await view.show_owner(

            interaction

        )