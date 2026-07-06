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

        finances = self.db.get_finances()

        finances = [
            f
            for f in finances
            if f["manager_id"] != manager_id
        ]

        self.db.save_finances(finances)

        # ==========================
        # CLUB OWNERSHIP
        # ==========================

        ownership = self.db.get_club_ownership()

        ownership = [
            o
            for o in ownership
            if o["manager_id"] != manager_id
        ]

        self.db.save_club_ownership(ownership)

        # ==========================
        # SQUAD
        # ==========================

        squads = self.db._load_json(
            self.db.save_path,
            "squads.json"
        )

        squads = [
            s
            for s in squads
            if s["manager_id"] != manager_id
        ]

        self.db._save_json(
            self.db.save_path,
            "squads.json",
            squads
        )

        embed = discord.Embed(
            title="🗑️ Reset completato",
            description="Il tuo profilo di sviluppo è stato eliminato.",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dev(bot))