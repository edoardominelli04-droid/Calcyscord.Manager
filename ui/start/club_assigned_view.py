import discord

from ui.start.club_assigned_embed import (
    ClubAssignedEmbedBuilder
)

from ui.initial_squad.initial_squad_view import (
    InitialSquadView
)


class ClubAssignedView(discord.ui.View):
    """Schermata mostrata dopo l'assegnazione del club."""

    def __init__(
        self,
        manager,
        club,
        competition
    ):

        super().__init__(
            timeout=600
        )

        self.manager = manager

        self.club = club

        self.competition = competition

        self.embed_builder = ClubAssignedEmbedBuilder()

        self.message = None

        self.add_item(
            StartInitialSquadButton()
        )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build(

            self.club,

            self.competition

        )

        await interaction.edit_original_response(

            content=None,

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()


class StartInitialSquadButton(discord.ui.Button):

    def __init__(self):

        super().__init__(

            label="Inizia a costruire la tua rosa",

            emoji="⚽",

            style=discord.ButtonStyle.success

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        parent = self.view

        view = InitialSquadView(

            parent.manager["id"]

        )

        await view.show(

            interaction

        )