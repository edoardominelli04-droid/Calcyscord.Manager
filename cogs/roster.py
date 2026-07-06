import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.squad_service import SquadService
from services.game.finance_service import FinanceService


class Roster(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = DatabaseManager()
        self.manager_service = ManagerService()
        self.squad_service = SquadService()
        self.finance_service = FinanceService()

    @commands.command(name="rosa")
    async def rosa(self, ctx):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send("❌ Usa prima `!start`.")
            return

        if manager["club_id"] is None:
            await ctx.send("❌ Devi prima scegliere un club.")
            return

        squad = self.squad_service.get_manager_players(
            manager["id"]
        )

        players = self.db.get_players()

        finance = self.finance_service.get_finance(
            manager["id"]
        )

        club = next(
            c
            for c in self.db.get_clubs()
            if c["id"] == manager["club_id"]
        )

        embed = discord.Embed(
            title=f"🏟️ {club['name']}",
            color=discord.Color.green()
        )

        embed.add_field(
            name="👔 Manager",
            value=manager["username"],
            inline=True
        )

        embed.add_field(
            name="💰 Budget",
            value=f"{finance['balance']:,} €".replace(",", "."),
            inline=True
        )

        goalkeepers = []
        defenders = []
        midfielders = []
        forwards = []

        for member in squad:

            player = next(
                p
                for p in players
                if p["id"] == member["player_id"]
            )

            position = player.get("position", "")

            if position == "Goalkeeper":
                goalkeepers.append(player["name"])

            elif position == "Defender":
                defenders.append(player["name"])

            elif position == "Midfield":
                midfielders.append(player["name"])

            else:
                forwards.append(player["name"])

        embed.add_field(
            name="🧤 Portieri",
            value="\n".join(goalkeepers) or "-",
            inline=False
        )

        embed.add_field(
            name="🛡 Difensori",
            value="\n".join(defenders) or "-",
            inline=False
        )

        embed.add_field(
            name="⚙ Centrocampisti",
            value="\n".join(midfielders) or "-",
            inline=False
        )

        embed.add_field(
            name="🎯 Attaccanti",
            value="\n".join(forwards) or "-",
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Roster(bot))