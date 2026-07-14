import discord


class CompetitionSelect(discord.ui.Select):

    def __init__(
        self,
        view,
        competitions
    ):

        self.view_data = view

        options = []

        for competition in competitions[:25]:

            options.append(

                discord.SelectOption(

                    label=competition["name"][:100],

                    value=str(competition["id"])

                )

            )

        super().__init__(

            placeholder="Seleziona una competizione...",

            options=options,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.select_competition(

            interaction,

            int(self.values[0])

        )