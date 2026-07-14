import discord


class StartSearchModal(discord.ui.Modal):

    def __init__(
        self,
        view
    ):

        super().__init__(

            title="Cerca un club"

        )

        self.view_data = view

        self.club_name = discord.ui.TextInput(

            label="Nome del club",

            placeholder="Es. Inter, Roma, Ajax...",

            required=True,

            max_length=50

        )

        self.add_item(

            self.club_name

        )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.search_club(

            interaction,

            str(self.club_name)

        )