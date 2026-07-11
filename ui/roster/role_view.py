import discord

from ui.player.player_select import PlayerSelect
from ui.player.player_view import PlayerView


class RoleView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data,
        players,
        role
    ):

        super().__init__(
            timeout=300
        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.players = players

        self.role = role

        self.message = None

        self.add_item(

            PlayerSelect(

                self,

                players

            )

        )

    async def show(
        self,
        interaction: discord.Interaction
    ):

        if self.role == "Goalkeeper":

            embed = self.roster_embed_builder.build_goalkeepers(

                self.data,

                self.players

            )

        elif self.role == "Defender":

            embed = self.roster_embed_builder.build_defenders(

                self.data,

                self.players

            )

        elif self.role == "Midfield":

            embed = self.roster_embed_builder.build_midfielders(

                self.data,

                self.players

            )

        elif self.role == "Attack":

            embed = self.roster_embed_builder.build_attackers(

                self.data,

                self.players

            )

        elif self.role == "Search":

            embed = self.roster_embed_builder.build_search()

        else:

            embed = discord.Embed(

                title="❌ Errore",

                description="Ruolo non riconosciuto.",

                color=discord.Color.red()

            )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

        self.message = await interaction.original_response()

    async def show_player(
        self,
        interaction: discord.Interaction,
        player_id: int
    ):

        player = next(

            (
                p
                for p in self.players
                if p["id"] == player_id
            ),

            None

        )

        if player is None:

            await interaction.response.send_message(

                "❌ Giocatore non trovato.",

                ephemeral=True

            )

            return

        view = PlayerView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            self.data,

            player

        )

        await view.show_player(

            interaction

        )