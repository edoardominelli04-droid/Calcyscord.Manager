import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.formation_service import FormationService
from services.utils.position_utils import PositionUtils

from ui.formation.formation_view import FormationView
from ui.formation.formation_embed import FormationEmbedBuilder


class Formation(commands.Cog):
    """Visualizzazione della formazione."""

    def __init__(self, bot):

        self.bot = bot

        self.db = DatabaseManager()

        self.manager_service = ManagerService()

        self.formation_service = FormationService()

        self.position_utils = PositionUtils()

        self.formation_embed_builder = FormationEmbedBuilder(

            self.db,

            self.formation_service,

            self.position_utils

        )

    # ==========================================================
    # FORMAZIONE
    # ==========================================================

    @commands.command(name="formazione")
    async def formazione(
        self,
        ctx
    ):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:

            await ctx.send(
                "❌ Devi prima registrarti con `!start`."
            )

            return

        formation = self.formation_service.get_manager_formation(
            manager["id"]
        )

        if formation is None:

            await ctx.send(
                "❌ Nessuna formazione trovata."
            )

            return

        embed = self.formation_embed_builder.build(
            manager["id"]
        )

        view = FormationView(

            manager["id"],

            formation,

            self.formation_service,

            self.formation_embed_builder

        )

        message = await ctx.send(

            embed=embed,

            view=view

        )

        view.message = message

    # ==========================================================
    # SCHIERA (DEBUG TEMPORANEO)
    # ==========================================================

    @commands.command(name="schiera")
    async def schiera(
        self,
        ctx,
        slot,
        player_id: int
    ):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:

            await ctx.send(
                "❌ Devi prima registrarti con `!start`."
            )

            return

        result = self.formation_service.swap_player(

            manager["id"],

            slot.upper(),

            player_id

        )

        if not result["success"]:

            await ctx.send(
                f"❌ {result['error']['message']}"
            )

            return

        data = result["data"]

        await ctx.send(

            "✅ "
            f"{data['new_player']['name']} "
            "sostituisce "
            f"{data['old_player']['name']} "
            f"nel ruolo **{data['slot']}**."

        )


async def setup(bot):
    await bot.add_cog(
        Formation(bot)
    )
