import discord

from services.game.transfer_request_service import TransferRequestService

from ui.transfer_requests.transfer_request_detail_embed import (
    TransferRequestDetailEmbedBuilder
)

from ui.transfer_requests.transfer_request_detail_buttons import (
    AcceptButton,
    RejectButton,
    BackButton
)

from ui.transfer_requests.transfer_requests_view import (
    TransferRequestsView
)

class TransferRequestDetailView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data,
        request_details
    ):

        super().__init__(

            timeout=300

        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.request_details = request_details

        self.transfer_request_service = (

            TransferRequestService()

        )

        self.embed_builder = (

            TransferRequestDetailEmbedBuilder()

        )

        self.message = None

        self.add_item(

            AcceptButton(self)

        )

        self.add_item(

            RejectButton(self)

        )

        self.add_item(

            BackButton(self)

        )

    async def show_request(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build(

            self.request_details["buyer"],

            self.request_details["seller"],

            self.request_details["player"],

            self.request_details["request"]

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = (

            await interaction.original_response()

        )

    async def accept_request(
        self,
        interaction: discord.Interaction
    ):

        result = self.transfer_request_service.accept_request(

            self.request_details["request"]["id"]

        )

        view = TransferRequestsView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await view.show_requests(

            interaction

        )


    async def reject_request(
        self,
        interaction: discord.Interaction
    ):

        result = self.transfer_request_service.reject_request(

            self.request_details["request"]["id"]

        )

        view = TransferRequestsView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await view.show_requests(

            interaction

        )


    async def show_requests(
        self,
        interaction: discord.Interaction
    ):

        from ui.transfer_requests.transfer_requests_view import (
            TransferRequestsView
        )

        view = TransferRequestsView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data

        )

        await view.show_requests(

            interaction

        )