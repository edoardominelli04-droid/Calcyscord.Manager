import discord

from services.game.player_service import PlayerService
from services.game.manager_service import ManagerService

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

    def _load_players(self):

        if self.role == "Goalkeeper":

            return self.player_service.get_goalkeepers(

                self.club_id

            )

        if self.role == "Defender":

            return self.player_service.get_defenders(

                self.club_id

            )

        if self.role == "Midfield":

            return self.player_service.get_midfielders(

                self.club_id

            )

        if self.role == "Attack":

            return self.player_service.get_forwards(

                self.club_id

            )

        return []

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

    async def select_player(
        self,
        interaction: discord.Interaction,
        player_id
    ):

        await interaction.response.send_message(

            f"Hai selezionato il giocatore {player_id}",

            ephemeral=True

        )