import discord
from discord.ext import commands

from services.game.club_service import ClubService

from ui.club.club_embed import ClubEmbedBuilder
from ui.club.club_view import ClubView

from ui.roster.roster_embed import RosterEmbedBuilder


class ClubDashboard(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

        self.club_service = ClubService()

        self.club_embed_builder = ClubEmbedBuilder()

        self.roster_embed_builder = RosterEmbedBuilder()

    @commands.command(name="club")
    async def club(
        self,
        ctx
    ):

        try:

            data = self.club_service.get_manager_club(
                ctx.author.id
            )

        except ValueError as e:

            await ctx.send(
                f"❌ {e}"
            )

            return

        embed = self.club_embed_builder.build(
            data
        )

        view = ClubView(

            self.club_service,

            self.club_embed_builder,

            self.roster_embed_builder,

            data

        )

        message = await ctx.send(

            embed=embed,

            view=view

        )

        view.message = message


async def setup(bot):

    await bot.add_cog(
        ClubDashboard(bot)
    )