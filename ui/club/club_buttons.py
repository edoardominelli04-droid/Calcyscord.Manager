import discord


class RosaButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Rosa",

            emoji="👥",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_roster(
            interaction
        )

class FormazioneButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Formazione",

            emoji="📋",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione formazione in sviluppo.",

            ephemeral=True

        )

class MercatoButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Mercato",

            emoji="💰",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_market(

            interaction

        )

class ContrattiButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Contratti",

            emoji="📜",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione contratti in sviluppo.",

            ephemeral=True

        )

class ClassificaButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Classifica",

            emoji="📊",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione classifica in sviluppo.",

            ephemeral=True

        )

class NotificheButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Notifiche",

            emoji="🔔",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione notifiche in sviluppo.",

            ephemeral=True

        )