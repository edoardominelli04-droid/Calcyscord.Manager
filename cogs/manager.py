import discord
from discord.ext import commands

from services.game.registration_service import RegistrationService
from services.game.club_selection_service import ClubSelectionService
from services.game.finance_service import FinanceService


class Manager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.registration = RegistrationService()
        self.club_selection = ClubSelectionService()
        self.finance = FinanceService()

    @commands.command(name="start")
    async def start(self, ctx):

        manager, finance, created = self.registration.register(
            ctx.author.id,
            ctx.author.display_name
        )

        if created:

            embed = discord.Embed(
                title="🎉 Benvenuto in Calcyscord.Manager!",
                description=(
                    "Il tuo profilo manageriale è stato creato.\n\n"
                    "Ora scegli il tuo club con:\n"
                    "`!chooseclub <id_club>`"
                ),
                color=discord.Color.green()
            )

        else:

            embed = discord.Embed(
                title="✅ Sei già registrato",
                description="Il tuo profilo esiste già.",
                color=discord.Color.blue()
            )

        embed.add_field(
            name="Manager",
            value=manager["username"],
            inline=True
        )

        embed.add_field(
            name="Livello",
            value=manager["level"],
            inline=True
        )

        embed.add_field(
            name="Saldo",
            value=f"{finance['balance']:,} €".replace(",", "."),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="manager")
    async def manager(self, ctx):

        manager = self.registration.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send(
                "❌ Non sei registrato. Usa `!start`."
            )
            return

        finance = self.finance.get_finance(
            manager["id"]
        )

        embed = discord.Embed(
            title="👔 Profilo Manager",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Nome",
            value=manager["username"],
            inline=False
        )

        embed.add_field(
            name="Livello",
            value=manager["level"],
            inline=True
        )

        embed.add_field(
            name="Esperienza",
            value=manager["experience"],
            inline=True
        )

        embed.add_field(
            name="Reputazione",
            value=manager["reputation"],
            inline=True
        )

        embed.add_field(
            name="Saldo",
            value=f"{finance['balance']:,} €".replace(",", "."),
            inline=False
        )

        if manager["club_id"] is None:
            club = "Nessun club"
        else:
            clubs = self.club_selection.db.get_clubs()

            club = next(
                (
                    c["name"]
                    for c in clubs
                    if c["id"] == manager["club_id"]
                ),
                "Sconosciuto"
            )

        embed.add_field(
            name="Club",
            value=club,
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="chooseclub")
    async def chooseclub(self, ctx, club_id: int):

        try:

            manager, club = self.club_selection.choose_club(
                ctx.author.id,
                club_id
            )

            embed = discord.Embed(
                title="🏟️ Club assegnato",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="Club",
                value=club["name"],
                inline=False
            )

            embed.add_field(
                name="Competizione",
                value=club.get("competition_external_id", "-"),
                inline=True
            )

            embed.add_field(
                name="Stadio",
                value=club.get("stadium_name", "-"),
                inline=True
            )

            await ctx.send(embed=embed)

        except ValueError as e:

            await ctx.send(f"❌ {e}")


async def setup(bot):
    await bot.add_cog(Manager(bot))