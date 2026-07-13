import discord

from services.game.transfer_request_service import TransferRequestService

from ui.transfer_requests.transfer_requests_embed import (
    TransferRequestsEmbedBuilder
)

from ui.transfer_requests.transfer_requests_buttons import (
    TransferRequestSelect,
    BackButton
)

from ui.transfer_requests.transfer_request_detail_view import (
    TransferRequestDetailView
)


class TransferRequestsView(
    discord.ui.View
):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data
    ):

        super().__init__(

            timeout=300

        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.transfer_request_service = (

            TransferRequestService()

        )

        self.embed_builder = (

            TransferRequestsEmbedBuilder()

        )

        self.message = None

    async def show_requests(
        self,
        interaction: discord.Interaction
    ):

        requests = (

            self.transfer_request_service
           .get_manager_requests_details(

                self.data["manager"]["id"]

            )

        )

        embed = self.embed_builder.build(

            requests

        )

        self.clear_items()

        self.add_item(

            TransferRequestSelect(

                self,

                requests

            )

        )

        self.add_item(

            BackButton(self)

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = (

            await interaction.original_response()

        )

    async def show_request(
        self,
        interaction: discord.Interaction,
        request_id
    ):

        requests = self.transfer_request_service.get_manager_requests_details(

            self.data["manager"]["id"]

        )

        selected = None

        for item in requests:

            if item["request"]["id"] == request_id:

                selected = item

                break

        if selected is None:

            await interaction.response.send_message(

                "❌ Richiesta non trovata.",

                ephemeral=True

            )

            return

        view = TransferRequestDetailView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            selected

        )

        await view.show_request(

            interaction

        )