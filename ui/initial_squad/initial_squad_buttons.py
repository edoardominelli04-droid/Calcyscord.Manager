import discord


class GoalkeepersButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Portieri",
            emoji="🥅",
            style=discord.ButtonStyle.secondary,
            row=0
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "Funzione in sviluppo.",
            ephemeral=True
        )


class DefendersButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Difensori",
            emoji="🛡️",
            style=discord.ButtonStyle.secondary,
            row=0
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "Funzione in sviluppo.",
            ephemeral=True
        )


class MidfieldersButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Centrocampisti",
            emoji="🎯",
            style=discord.ButtonStyle.secondary,
            row=1
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "Funzione in sviluppo.",
            ephemeral=True
        )


class ForwardsButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Attaccanti",
            emoji="⚽",
            style=discord.ButtonStyle.secondary,
            row=1
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "Funzione in sviluppo.",
            ephemeral=True
        )


class ConfirmSquadButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Conferma rosa",
            emoji="✅",
            style=discord.ButtonStyle.success,
            row=2
        )

    async def callback(self, interaction):

        await interaction.response.send_message(
            "La conferma sarà disponibile quando la rosa sarà completa.",
            ephemeral=True
        )