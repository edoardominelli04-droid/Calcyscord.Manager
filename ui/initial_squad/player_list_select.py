import discord


class PlayerListSelect(discord.ui.Select):
    """Select per scegliere un giocatore dalla lista."""

    def __init__(
        self,
        view,
        players
    ):

        self.view_data = view

        options = []

        for player in players[:25]:

            value = player.get("market_value") or 0

            options.append(

                discord.SelectOption(

                    label=player["name"][:100],

                    description=f"{value:,.0f} €".replace(",", "."),

                    value=str(player["id"])

                )

            )

        super().__init__(

            placeholder="Seleziona un giocatore...",

            options=options,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.select_player(

            interaction,

            int(self.values[0])

        )