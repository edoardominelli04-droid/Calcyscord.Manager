import discord

from ui.club.club_buttons import (
    RosaButton,
    FormazioneButton,
    MercatoButton,
    ContrattiButton,
    ClassificaButton,
    NotificheButton
)

from ui.roster.roster_view import RosterView

class ClubView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data
    ):

        print("CV1")

        super().__init__(
            timeout=300
        )

        print("CV2")

        self.club_service = club_service
        self.club_embed_builder = club_embed_builder
        self.roster_embed_builder = roster_embed_builder
        self.data = data
        self.message = None

        print("CV3")

        self.add_item(
            RosaButton(self)
        )

        print("CV4")

        self.add_item(
            FormazioneButton(self)
        )

        print("CV5")

        self.add_item(
            MercatoButton(self)
        )

        print("CV6")

        self.add_item(
            ContrattiButton(self)
        )

        print("CV7")

        self.add_item(
            ClassificaButton(self)
        )

        print("CV8")

        self.add_item(
            NotificheButton(self)
        )

        print("CV9")
        
    async def show_roster(
        self,
        interaction: discord.Interaction
    ):

        embed = self.roster_embed_builder.build(
            self.data
        )

        view = RosterView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await interaction.response.edit_message(

            embed=embed,

            view=view

        )

        view.message = await interaction.original_response()