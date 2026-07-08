import discord
from ui.formation.formation_selects import FormationSlotSelect


class SchieraButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Schiera",

            emoji="⚽",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        view = discord.ui.View(
            timeout=120
        )

        view.add_item(
            FormationSlotSelect(
                self.view_data
            )
        )

        await interaction.response.send_message(

            "⚽ Seleziona lo slot da modificare.",

            view=view,

            ephemeral=True

        )


class ModuloButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Modulo",

            emoji="📐",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Cambio modulo in sviluppo.",

            ephemeral=True

        )


class CapitanoButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Capitano",

            emoji="👑",

            style=discord.ButtonStyle.success,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione capitano in sviluppo.",

            ephemeral=True

        )


class RicostruisciButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Ricostruisci",

            emoji="🔄",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Ricostruzione formazione in sviluppo.",

            ephemeral=True

        )


class ClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Club",

            emoji="🏠",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Ritorno al Club in sviluppo.",

            ephemeral=True

        )