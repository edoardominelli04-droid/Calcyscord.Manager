import discord

from ui.market.market_search_modal import MarketSearchModal
from ui.market.market_search_utils import find_player
from ui.market.market_embed import MarketEmbedBuilder
from ui.market.market_buttons import (
    SearchButton,
    BuyButton,
    SellButton,
    TransfersButton,
    ClubButton
)
from ui.market_player.market_player_view import MarketPlayerView


class MarketView(discord.ui.View):

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

        self.market_embed_builder = MarketEmbedBuilder()

        self.data = data

        self.message = None

        self.add_item(
            SearchButton(self)
        )

        self.add_item(
            BuyButton(self)
        )

        self.add_item(
            SellButton(self)
        )

        self.add_item(
            TransfersButton(self)
        )

        self.add_item(
            ClubButton(self)
        )

    async def show_market(
        self,
        interaction: discord.Interaction
    ):

        embed = self.market_embed_builder.build(

            self.data

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_search(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_modal(

            MarketSearchModal(

                self

            )

        )

    async def search_player(
        self,
        interaction: discord.Interaction,
        name: str
    ):

        players = self.club_service.get_all_players()

        player = find_player(

            players,

            name

        )

        if player is None:

            await interaction.response.send_message(

                "❌ Nessun giocatore trovato.",

                ephemeral=True

            )

            return

        view = MarketPlayerView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            player

        )

        await view.show_player(

            interaction

        )

    async def show_buy(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Sistema acquisti in sviluppo.",

            ephemeral=True

        )

    async def show_sell(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Sistema vendite in sviluppo.",

            ephemeral=True

        )

    async def show_transfers(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Trasferimenti in sviluppo.",

            ephemeral=True

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