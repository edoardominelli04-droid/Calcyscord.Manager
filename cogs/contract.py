import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.squad_service import SquadService
from services.utils.text_utils import normalize_text


class Contract(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = DatabaseManager()
        self.manager_service = ManagerService()
        self.squad_service = SquadService()

    @commands.command(name="contratto")
    async def contratto(self, ctx, *, player_name: str):

        manager = self.manager_service.get_by_discord_id(ctx.author.id)

        if manager is None:
            await ctx.send("❌ Devi prima registrarti con `!start`.")
            return

        squad = self.squad_service.get_manager_players(manager["id"])

        if not squad:
            await ctx.send("❌ Non hai ancora una rosa.")
            return

        search = normalize_text(player_name)

        matches = []

        for squad_member in squad:
            player = self.db.get_player_by_id(squad_member["player_id"])

            if player is None:
                continue

            if search in normalize_text(player.get("name", "")):
                matches.append((player, squad_member))

        if not matches:
            await ctx.send("❌ Giocatore non trovato nella tua rosa.")
            return

        if len(matches) > 1:
            names = "\n".join(
                f"• {player['name']}"
                for player, _ in matches[:10]
            )

            embed = discord.Embed(
                title="🔎 Più giocatori trovati",
                description="Sii più specifico.\n\n" + names,
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)
            return

        player, squad_member = matches[0]

        contract_id = squad_member.get("contract_id")

        if contract_id is None:
            await ctx.send("❌ Questo giocatore non ha ancora un contratto collegato.")
            return

        contract = self.db.get_contract_by_id(contract_id)

        if contract is None:
            await ctx.send("❌ Contratto non trovato.")
            return

        salary = int(contract.get("salary") or 0)
        release_clause = contract.get("release_clause")

        embed = discord.Embed(
            title="📄 Contratto",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="👤 Giocatore",
            value=str(player.get("name", "-")),
            inline=False
        )

        embed.add_field(
            name="📑 Tipo contratto",
            value=str(contract.get("type", "-")).capitalize(),
            inline=True
        )

        embed.add_field(
            name="🤝 Prestito",
            value="Sì" if contract.get("is_loan") else "No",
            inline=True
        )

        embed.add_field(
            name="💰 Stipendio",
            value=f"{salary:,} €".replace(",", "."),
            inline=True
        )

        embed.add_field(
            name="📅 Inizio",
            value=str(contract.get("start_season", "-")),
            inline=True
        )

        embed.add_field(
            name="📅 Scadenza",
            value=str(contract.get("end_season", "-")),
            inline=True
        )

        embed.add_field(
            name="📜 Clausola",
            value=(
                "-"
                if release_clause is None
                else f"{int(release_clause):,} €".replace(",", ".")
            ),
            inline=True
        )

        embed.add_field(
            name="🔄 Rinnovabile",
            value="✅ Sì" if contract.get("renewable") else "❌ No",
            inline=True
        )

        embed.add_field(
            name="📌 Stato",
            value=str(contract.get("status", "-")).capitalize(),
            inline=True
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Contract(bot))