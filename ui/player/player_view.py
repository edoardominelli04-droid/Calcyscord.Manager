import discord

from ui.player.player_embed import PlayerEmbedBuilder


class PlayerView(discord.ui.View):

    def __init__(
        self,
        player
    ):

        super().__init__(
            timeout=300
        )

        self.player = player

        self.player_embed_builder = PlayerEmbedBuilder()

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