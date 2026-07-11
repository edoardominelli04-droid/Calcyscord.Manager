import discord

from ui.player.player_view import PlayerView


class SearchModal(discord.ui.Modal):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data
    ):

        super().__init__(

            title="🔍 Cerca giocatore della tua rosa"

        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.player_name = discord.ui.TextInput(

            label="Nome giocatore",

            placeholder="Es. Immobile, Trapp, Barella...",

            required=True,

            max_length=50

        )

        self.add_item(

            self.player_name

        )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        query = str(

            self.player_name

        ).lower().strip()

        player = next(

            (

                p

                for p in self.data["players"]

                if query in p["name"].lower()

            ),

            None

        )

        if player is None:

            await interaction.response.send_message(

                "❌ Nessun giocatore trovato.",

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