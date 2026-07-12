import discord

from ui.market_buy.market_buy_embed import MarketBuyEmbedBuilder
from ui.market_buy.market_buy_modal import PurchaseOfferModal
from services.game.market_service import MarketService
from ui.market_buy.market_buy_buttons import (
    PurchaseButton,
    LoanButton,
    PlayerButton,
    MarketButton,
    ClubButton
)


class MarketBuyView(discord.ui.View):

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

        self.market_service = MarketService()

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.player = player

        self.market_buy_embed_builder = MarketBuyEmbedBuilder()

        self.message = None

        self.add_item(
            PurchaseButton(self)
        )

        self.add_item(
            LoanButton(self)
        )

        self.add_item(
            PlayerButton(self)
        )

        self.add_item(
            MarketButton(self)
        )

        self.add_item(
            ClubButton(self)
        )

    async def show_buy(
        self,
        interaction: discord.Interaction
    ):

        owner = self.club_service.get_player_owner(

            self.player["id"]

        )

        budget = self.data["finance"]["transfer_budget"]

        embed = self.market_buy_embed_builder.build(

            self.player,

            owner,

            budget

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_purchase(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_modal(

            PurchaseOfferModal(

                self

            )

        )

    async def submit_purchase_offer(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        buyer_manager_id = self.data["manager"]["id"]

        result = self.market_service.submit_offer(

            buyer_manager_id,

            self.player["id"],

            amount

        )

        if result["success"]:

            self.data = self.club_service.get_manager_club(
                interaction.user.id
        )

        await interaction.response.send_message(

            result["message"],

            ephemeral=True

        )

    async def show_loan(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Sistema prestiti in sviluppo.",

            ephemeral=True

        )

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