import discord

from ui.player.player_embed import PlayerEmbedBuilder


class MarketPlayerEmbedBuilder:

    def __init__(
        self
    ):

        self.player_embed_builder = PlayerEmbedBuilder()

    def build(
        self,
        player
    ):

        embed = self.player_embed_builder.build(

            player

        )

        return embed