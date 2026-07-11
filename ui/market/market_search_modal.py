import discord


class MarketSearchModal(discord.ui.Modal):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            title="🔍 Cerca giocatore"

        )

        self.player_name = discord.ui.TextInput(

            label="Nome giocatore",

            placeholder="Es. Lautaro, Bellingham, Yamal...",

            required=True,

            max_length=50

        )

        self.add_item(

            self.player_name

        )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.search_player(

            interaction,

            self.player_name.value

        )