import discord

from ui.start.start_embed import StartEmbedBuilder


class StartConfirmView(discord.ui.View):
    """Conferma finale della scelta del club."""

    def __init__(
        self,
        parent_view,
        club
    ):

        super().__init__(
            timeout=300
        )

        self.parent_view = parent_view

        self.club = club

        self.embed_builder = StartEmbedBuilder()

        self.message = None

        self.add_item(
            ConfirmButton(self)
        )

        self.add_item(
            BackButton(self)
        )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        competition = (

            self.parent_view
            .start_service
            .db
            .get_competition_by_id(

                self.club["competition_id"]

            )

        )

        embed = self.embed_builder.build_confirmation(

            self.club,

            competition

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def confirm(
        self,
        interaction: discord.Interaction
    ):

        try:

            manager, club = (

                self.parent_view.start_service.confirm_club(

                    self.parent_view.discord_id,

                    self.club["id"]

                )

            )

        except ValueError as e:

            await interaction.response.send_message(

                f"❌ {e}",

                ephemeral=True

            )

            return

        embed = self.embed_builder.build_completed(

            club

        )

        await interaction.response.edit_message(

            embed=embed,

            view=None

        )

    async def back(
        self,
        interaction: discord.Interaction
    ):

        await self.parent_view.show(

            interaction

        )


class ConfirmButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Conferma",

            emoji="✅",

            style=discord.ButtonStyle.success,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.confirm(

            interaction

        )


class BackButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Indietro",

            emoji="◀️",

            style=discord.ButtonStyle.secondary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.back(

            interaction

        )