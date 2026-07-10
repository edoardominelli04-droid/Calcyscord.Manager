import discord

from ui.player.player_embed import PlayerEmbedBuilder

from ui.player.player_buttons import (
    ContractButton,
    StatisticsButton,
    ClubButton
)


class PlayerView(discord.ui.View):

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

        self.player_embed_builder = PlayerEmbedBuilder()

        self.message = None

        self.add_item(
            ContractButton(self)
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

        embed = self.player_embed_builder.build(

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