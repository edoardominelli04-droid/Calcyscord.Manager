import discord


class ClubSearchSelect(discord.ui.Select):

    def __init__(
        self,
        view,
        clubs
    ):

        self.view_data = view

        options = []

        for club in clubs[:25]:

            options.append(

                discord.SelectOption(

                    label=club["name"][:100],

                    description=club.get(
                        "competition_external_id",
                        "-"
                    ),

                    value=str(club["id"])

                )

            )

        super().__init__(

            placeholder="Seleziona un club...",

            options=options,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.select_club(

            interaction,

            int(self.values[0])

        )