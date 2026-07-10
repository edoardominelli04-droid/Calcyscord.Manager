import discord


class PlayerSelect(discord.ui.Select):

    def __init__(
        self,
        view,
        players
    ):

        self.view_data = view

        options = []

        for player in players:

            options.append(

                discord.SelectOption(

                    label=player["name"],

                    description=player["country"],

                    emoji="⚽",

                    value=str(player["id"])

                )

            )

        super().__init__(

            placeholder="Seleziona un giocatore...",

            min_values=1,

            max_values=1,

            options=options

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_player(

            interaction,

            int(self.values[0])

        )