import discord

from services.game.initial_squad_service import InitialSquadService

from ui.initial_squad.initial_squad_embed import (
    InitialSquadEmbedBuilder
)

from ui.initial_squad.initial_squad_buttons import (
    GoalkeepersButton,
    DefendersButton,
    MidfieldersButton,
    ForwardsButton,
    ConfirmSquadButton
)

from ui.initial_squad.player_list_view import (
    PlayerListView
)


class InitialSquadView(discord.ui.View):

    def __init__(
        self,
        manager_id
    ):

        super().__init__(
            timeout=600
        )

        self.manager_id = manager_id

        self.service = InitialSquadService()

        self.embed_builder = InitialSquadEmbedBuilder()

        self.message = None

        self.add_item(GoalkeepersButton())
        self.add_item(DefendersButton())
        self.add_item(MidfieldersButton())
        self.add_item(ForwardsButton())
        self.add_item(ConfirmSquadButton())

    # ==========================================================
    # AGGIORNA STATO PULSANTI
    # ==========================================================

    def _update_buttons(self):

        draft = self.service.get_draft(
            self.manager_id
        )

        squad_confirmed = bool(
            draft and draft.get("confirmed")
        )

        squad_completed = self.service.is_squad_complete(
            self.manager_id
        )

        for item in self.children:

            # --------------------------------------------------
            # Pulsanti reparti
            # --------------------------------------------------

            if hasattr(item, "role"):

                completed = self.service.is_role_complete(

                    self.manager_id,

                    item.role

                )

                item.disabled = squad_confirmed

                item.style = (
                    discord.ButtonStyle.success
                    if completed
                    else discord.ButtonStyle.secondary
                )

            # --------------------------------------------------
            # Pulsante conferma
            # --------------------------------------------------

            elif isinstance(item, ConfirmSquadButton):

                item.disabled = (
                    not squad_completed
                    or squad_confirmed
                )

    # ==========================================================
    # APERTURA LISTA GIOCATORI
    # ==========================================================

    def open_player_list(
        self,
        role
    ):

        return PlayerListView(
            self.manager_id,
            role,
            self
        )

    # ==========================================================
    # VISUALIZZAZIONE
    # ==========================================================

    async def show(
        self,
        interaction: discord.Interaction
    ):

        draft = self.service.get_draft(
            self.manager_id
        )

        counts = self.service.get_role_counts(
            self.manager_id
        )

        self._update_buttons()

        embed = self.embed_builder.build_home(

            draft,

            counts

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    # ==========================================================
    # REFRESH
    # ==========================================================

    async def refresh(self):

        if self.message is None:

            return

        draft = self.service.get_draft(
            self.manager_id
        )

        counts = self.service.get_role_counts(
            self.manager_id
        )

        self._update_buttons()

        embed = self.embed_builder.build_home(

            draft,

            counts

        )

        await self.message.edit(

            embed=embed,

            view=self

        )
