import discord
from discord.ext import commands

from services.game.manager_service import ManagerService
from services.game.module_service import ModuleService
from services.game.formation_service import FormationService


class Module(commands.Cog):
    """Gestione dei moduli tattici."""

    def __init__(self, bot):
        self.bot = bot

        self.manager_service = ManagerService()
        self.module_service = ModuleService()
        self.formation_service = FormationService()

    @commands.command(name="modulo")
    async def modulo(self, ctx, *, module_name=None):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send(
                "❌ Devi prima registrarti con `!start`."
            )
            return

        # ======================================================
        # MOSTRA ELENCO MODULI
        # ======================================================

        if module_name is None:

            modules = self.module_service.get_available_modules()

            embed = discord.Embed(
                title="📐 Moduli disponibili",
                description=(
                    "Per cambiare modulo usa:\n"
                    "`!modulo <nome modulo>`"
                ),
                color=discord.Color.blue()
            )

            embed.add_field(
                name="Moduli",
                value="\n".join(
                    f"• {module}"
                    for module in modules
                ),
                inline=False
            )

            embed.set_footer(
                text="In futuro potrai selezionare il modulo con un pulsante."
            )

            await ctx.send(embed=embed)
            return

        # ======================================================
        # CAMBIO MODULO
        # ======================================================

        try:

            formation = (
                self.formation_service.change_module(
                    manager["id"],
                    module_name
                )
            )

        except ValueError as e:

            await ctx.send(
                f"❌ {e}"
            )
            return

        embed = discord.Embed(
            title="✅ Modulo aggiornato",
            description=(
                "La formazione è stata aggiornata "
                "automaticamente."
            ),
            color=discord.Color.green()
        )

        embed.add_field(
            name="📐 Nuovo modulo",
            value=formation["module"],
            inline=False
        )

        embed.set_footer(
            text="Usa !formazione per visualizzare la nuova disposizione."
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Module(bot))