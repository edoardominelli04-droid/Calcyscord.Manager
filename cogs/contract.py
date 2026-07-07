import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.squad_service import SquadService
from services.game.contract_service import ContractService
from services.utils.text_utils import normalize_text


class Contract(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = DatabaseManager()

        self.manager_service = ManagerService()
        self.squad_service = SquadService()
        self.contract_service = ContractService()

    @commands.command(name="contratto")
    async def contratto(self, ctx, *, player_name: str):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send("❌ Devi prima registrarti con `!start`.")
            return

        squad = self.squad_service.get_manager_players(
            manager["id"]
        )

        matches = []

        for member in squad:

            player = self.db.get_player_by_id(
                member["player_id"]
            )

            if player is None:
                continue

            if normalize_text(player_name) in normalize_text(player["name"]):
                matches.append((player, member))

        if not matches:
            await ctx.send("❌ Giocatore non trovato nella tua rosa.")
            return

        if len(matches) > 1:

            embed = discord.Embed(
                title="🔎 Più giocatori trovati",
                description="\n".join(
                    f"• {player['name']}"
                    for player, _ in matches[:10]
                ),
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)
            return

        player, squad_member = matches[0]

        await ctx.send("DEBUG 1")

        contract = self.db.get_contract_by_id(
            squad_member["contract_id"]
        )

        await ctx.send("DEBUG 2")

        if contract is None:
            await ctx.send("❌ Contratto non trovato.")
            return

        embed = discord.Embed(
            title="📄 Contratto",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="👤 Giocatore",
            value=player["name"],
            inline=False
        )

        embed.add_field(
            name="📑 Tipo contratto",
            value=contract["type"].capitalize(),
            inline=True
        )

        embed.add_field(
            name="🤝 Prestito",
            value="Sì" if contract["is_loan"] else "No",
            inline=True
        )

        embed.add_field(
            name="💰 Stipendio",
            value=f"{contract['salary']:,} €".replace(",", "."),
            inline=True
        )

        embed.add_field(
            name="📅 Inizio",
            value=str(contract["start_season"]),
            inline=True
        )

        embed.add_field(
            name="📅 Scadenza",
            value=str(contract["end_season"]),
            inline=True
        )

        embed.add_field(
            name="📜 Clausola",
            value=(
                "-"
                if contract["release_clause"] is None
                else f"{contract['release_clause']:,} €".replace(",", ".")
            ),
            inline=True
        )

        embed.add_field(
            name="🔄 Rinnovabile",
            value="✅ Sì" if contract["renewable"] else "❌ No",
            inline=True
        )

        embed.add_field(
            name="📌 Stato",
            value=contract["status"].capitalize(),
            inline=True
        )

        await ctx.send("DEBUG 3")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Contract(bot))