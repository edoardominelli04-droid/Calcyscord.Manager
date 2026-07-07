import discord
from discord.ext import commands

from services.database_manager import DatabaseManager


class Dev(commands.Cog):
    """Comandi di sviluppo."""

    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()

    @commands.command(name="resetme")
    async def resetme(self, ctx):

        discord_id = str(ctx.author.id)

        # ==========================
        # MANAGER
        # ==========================

        managers = self.db.get_managers()

        manager = next(
            (m for m in managers if m["discord_id"] == discord_id),
            None
        )

        if manager is None:
            await ctx.send("❌ Nessun manager trovato.")
            return

        manager_id = manager["id"]

        managers = [
            m
            for m in managers
            if m["id"] != manager_id
        ]

        self.db.save_managers(managers)

        # ==========================
        # FINANZE
        # ==========================

        finances = [
            f
            for f in self.db.get_finances()
            if f["manager_id"] != manager_id
        ]

        self.db.save_finances(finances)

        # ==========================
        # CLUB OWNERSHIP
        # ==========================

        ownership = [
            o
            for o in self.db.get_club_ownership()
            if o["manager_id"] != manager_id
        ]

        self.db.save_club_ownership(ownership)

        # ==========================
        # ROSA
        # ==========================

        squads = [
            s
            for s in self.db.get_squads()
            if s["manager_id"] != manager_id
        ]

        self.db.save_squads(squads)

        # ==========================
        # CONTRATTI
        # ==========================

        contracts = [
            c
            for c in self.db.get_contracts()
            if c["manager_id"] != manager_id
        ]

        self.db.save_contracts(contracts)

        # ==========================
        # FORMAZIONI
        # ==========================

        formations = [
            f
            for f in self.db.get_formations()
            if f["manager_id"] != manager_id
        ]

        self.db.save_formations(formations)

        # ==========================
        # MESSAGGIO
        # ==========================

        embed = discord.Embed(
            title="🗑️ Reset completato",
            description=(
                "Il tuo profilo è stato eliminato.\n\n"
                "Sono stati rimossi:\n"
                "• Manager\n"
                "• Finanze\n"
                "• Club assegnato\n"
                "• Rosa\n"
                "• Contratti\n"
                "• Formazione"
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="Puoi ricominciare con !start"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dev(bot))