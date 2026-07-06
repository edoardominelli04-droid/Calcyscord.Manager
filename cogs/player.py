import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.squad_service import SquadService
from services.utils.text_utils import normalize_text


class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = DatabaseManager()
        self.manager_service = ManagerService()
        self.squad_service = SquadService()

    @commands.command(name="giocatore")
    async def giocatore(self, ctx, *, player_name: str):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send("❌ Devi prima registrarti con `!start`.")
            return

        squad = self.squad_service.get_manager_players(
            manager["id"]
        )

        players = self.db.get_players()

        squad_players = []

        for member in squad:

            player = next(
                (
                    p
                    for p in players
                    if p["id"] == member["player_id"]
                ),
                None
            )

            if player is not None:
                squad_players.append(player)

        # ==========================
        # Ricerca normalizzata
        # ==========================

        search = normalize_text(player_name)

        matches = [
            p
            for p in squad_players
            if search in normalize_text(p["name"])
        ]

        if len(matches) == 0:
            await ctx.send("❌ Giocatore non trovato nella tua rosa.")
            return

        if len(matches) > 1:

            names = "\n".join(
                f"• {p['name']}"
                for p in matches[:10]
            )

            embed = discord.Embed(
                title="🔎 Più giocatori trovati",
                description="Sii più specifico.\n\n" + names,
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)
            return

        player = matches[0]

        # ==========================
        # Embed
        # ==========================

        embed = discord.Embed(
            title=f"👤 {player['name']}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Ruolo",
            value=player.get("position", "-"),
            inline=True
        )

        embed.add_field(
            name="Età",
            value=player.get("age", "-"),
            inline=True
        )

        embed.add_field(
            name="Nazionalità",
            value=player.get("country_name", "-"),
            inline=True
        )

        embed.add_field(
            name="Altezza",
            value=player.get("height", "-"),
            inline=True
        )

        embed.add_field(
            name="Piede",
            value=player.get("foot", "-"),
            inline=True
        )

        embed.add_field(
            name="Valore di mercato",
            value=player.get("market_value", "-"),
            inline=True
        )

        embed.add_field(
            name="Club",
            value=player.get("club_name", "-"),
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Player(bot))