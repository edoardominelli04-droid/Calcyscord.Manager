import discord

from ui.player.player_select import PlayerSelect


class RoleView(discord.ui.View):

    def __init__(
        self,
        roster_embed_builder,
        data,
        players,
        role
    ):

        super().__init__(
            timeout=300
        )

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

        else:

            embed = self.roster_embed_builder.build_attackers(

                self.data,

                self.players

            )

        await interaction.response.edit_message(

            embed=embed,

            view=self

        )

    async def show_player(
        self,
        interaction: discord.Interaction,
        player_id: int
    ):

        await interaction.response.send_message(

            f"👤 Giocatore selezionato: {player_id}",

            ephemeral=True

        )