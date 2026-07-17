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

            tier = player.get("initial_tier", "D")

            cost = player.get("initial_cost", 1)

            options.append(

                discord.SelectOption(

                    label=(
                        f"{player['name']} ⭐ {cost}"
                    )[:100],

                    description=(
                        f"Fascia {tier} • "
                        f"{value:,.0f} €"
                    ).replace(",", ".")[:100],

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
