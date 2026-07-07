import discord
from discord.ext import commands

from services.game.club_service import ClubService


class ClubDashboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.club_service = ClubService()

    @commands.command(name="club")
    async def club(self, ctx):

        try:

            data = self.club_service.get_manager_club(
                ctx.author.id
            )

        except ValueError as e:
            await ctx.send(f"❌ {e}")
            return

        club = data["club"]
        manager = data["manager"]
        finance = data["finance"]
        competition = data["competition"]
        stadium = data["stadium"]

        embed = discord.Embed(
            title=f"🏟️ {club['name']}",
            color=discord.Color.dark_green()
        )

        embed.add_field(
            name="👔 Manager",
            value=manager["username"],
            inline=True
        )

        embed.add_field(
            name="🏆 Competizione",
            value=competition["name"] if competition else "-",
            inline=True
        )

        embed.add_field(
            name="📍 Stadio",
            value=stadium["name"] if stadium else club.get("stadium_name", "-"),
            inline=True
        )

        embed.add_field(
            name="👥 Rosa",
            value=data["players_count"],
            inline=True
        )

        embed.add_field(
            name="📈 Età media",
            value=data["average_age"],
            inline=True
        )

        embed.add_field(
            name="💰 Budget",
            value=f"{finance['balance']:,} €".replace(",", "."),
            inline=True
        )

        embed.add_field(
            name="💎 Valore rosa",
            value=f"{int(data['market_value']):,} €".replace(",", "."),
            inline=True
        )

        if data["most_valuable_player"]:

            player = data["most_valuable_player"]

            embed.add_field(
                name="⭐ Giocatore più prezioso",
                value=(
                    f"{player['name']}\n"
                    f"{int(player.get('market_value', 0) or 0):,} €".replace(",", ".")
                ),
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ClubDashboard(bot))