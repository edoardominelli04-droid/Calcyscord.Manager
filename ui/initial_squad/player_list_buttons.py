import discord


class PlayerRemoveSelect(discord.ui.Select):
    """Menu per rimuovere un giocatore già scelto nel reparto."""

    def __init__(self, view, players):

        self.view_data = view

        options = [
            discord.SelectOption(
                label=(
                    f"{player['name']} ⭐ {player.get('initial_cost', 1)}"
                )[:100],
                description=(
                    "Rimuovi e recupera "
                    f"⭐ {player.get('initial_cost', 1)}"
                ),
                value=str(player["id"]),
                emoji="➖"
            )
            for player in players[:25]
        ]

        super().__init__(
            placeholder="Rimuovi un giocatore selezionato...",
            options=options,
            row=1
        )

    async def callback(self, interaction: discord.Interaction):

        await self.view_data.remove_player(
            interaction,
            int(self.values[0])
        )


class BackToInitialSquadButton(discord.ui.Button):
    """Ritorna alla schermata principale della rosa iniziale."""

    def __init__(self, view):

        self.view_data = view

        super().__init__(
            label="Torna alla rosa",
            emoji="↩️",
            style=discord.ButtonStyle.secondary,
            row=2
        )

    async def callback(self, interaction: discord.Interaction):

        await self.view_data.parent_view.show(
            interaction
        )
