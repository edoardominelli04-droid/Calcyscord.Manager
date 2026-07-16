import discord

from services.game.player_service import PlayerService
from services.game.manager_service import ManagerService
from services.game.initial_squad_service import (
    InitialSquadService
)

from ui.initial_squad.player_list_embed import (
    PlayerListEmbedBuilder
)

from ui.initial_squad.player_list_select import (
    PlayerListSelect
)


class PlayerListView(discord.ui.View):
    """Visualizza la lista dei giocatori di un reparto."""

    def __init__(
        self,
        manager_id,
        role,
        parent_view
    ):

        super().__init__(
            timeout=600
        )

        self.manager_id = manager_id

        self.role = role

        self.parent_view = parent_view

        self.player_service = PlayerService()

        self.manager_service = ManagerService()

        self.initial_squad_service = InitialSquadService()

        self.embed_builder = PlayerListEmbedBuilder()

        self.message = None

        manager = self.manager_service.get_by_id(
            manager_id
        )

        if manager is None:

            raise ValueError(
                f"Manager {manager_id} non trovato."
            )

        self.club_id = manager["club_id"]

        self.players = self._load_players()

        if self.players:

            self.add_item(

                PlayerListSelect(

                    self,

                    self.players

                )

            )

    # ==========================================================
    # CARICAMENTO GIOCATORI
    # ==========================================================

    def _load_players(self):

        draft = self.initial_squad_service.get_draft(
            self.manager_id
        )

        selected = set()

        if draft is not None:

            selected = set(
                draft["players"]
            )

        if self.role == "Goalkeeper":

            players = self.player_service.get_goalkeepers(
                self.club_id
            )

        elif self.role == "Defender":

            players = self.player_service.get_defenders(
                self.club_id
            )

        elif self.role == "Midfield":

            players = self.player_service.get_midfielders(
                self.club_id
            )

        elif self.role == "Attack":

            players = self.player_service.get_forwards(
                self.club_id
            )

        else:

            players = []

        return [

            player

            for player in players

            if player["id"] not in selected

        ]

    # ==========================================================
    # VISUALIZZAZIONE
    # ==========================================================

    async def show(
        self,
        interaction: discord.Interaction
    ):

        embed = self.embed_builder.build(

            self.role,

            self.players

        )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    # ==========================================================
    # SELEZIONE GIOCATORE
    # ==========================================================

    async def select_player(
        self,
        interaction,
        player_id
    ):

        added = self.initial_squad_service.add_player(

            self.manager_id,

            player_id

        )

        if not added:

            await interaction.response.send_message(

                "❌ Giocatore già selezionato.",

                ephemeral=True

            )

            return

        await self.parent_view.show(
            interaction
        )