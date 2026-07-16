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

        rules = self.service.get_rules()

        all_completed = True

        for item in self.children:

            # --------------------------------------------------
            # Pulsanti reparti
            # --------------------------------------------------

            if hasattr(item, "role"):

                completed = self.service.is_role_complete(

                    self.manager_id,

                    item.role

                )

                item.disabled = completed

                if not completed:

                    all_completed = False

            # --------------------------------------------------
            # Pulsante conferma
            # --------------------------------------------------

            elif isinstance(item, ConfirmSquadButton):

                item.disabled = not all_completed

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