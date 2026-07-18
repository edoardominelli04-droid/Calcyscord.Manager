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

        from ui.formation.formation_module_select import (
            FormationModuleSelect
        )

        view = discord.ui.View(
            timeout=120
        )

        view.add_item(
            FormationModuleSelect(
                self.view_data
            )
        )

        await interaction.response.send_message(

            "📐 Seleziona il nuovo modulo.",

            view=view,

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

        from ui.formation.formation_captain_select import (
            FormationCaptainSelect
        )

        view = discord.ui.View(
            timeout=120
        )

        view.add_item(
            FormationCaptainSelect(
                self.view_data
            )
        )

        await interaction.response.send_message(

            "👑 Seleziona il nuovo capitano.",

            view=view,

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

        await interaction.response.defer(ephemeral=True)

        result = self.view_data.formation_service.rebuild_random_formation(
            self.view_data.manager_id
        )

        if not result["success"]:
            await interaction.followup.send(
                f"❌ {result['error']['message']}",
                ephemeral=True
            )
            return

        self.view_data.formation = result["data"]["formation"]

        await interaction.message.edit(
            embed=self.view_data.formation_embed_builder.build(
                self.view_data.manager_id
            ),
            view=self.view_data
        )

        captain_note = (
            " Il capitano è stato mantenuto."
            if result["data"]["captain_preserved"]
            else " Se necessario, scegli un nuovo capitano."
        )

        await interaction.followup.send(
            "🔄 Formazione ricostruita casualmente usando il modulo "
            f"**{self.view_data.formation['module']}**."
            + captain_note,
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
