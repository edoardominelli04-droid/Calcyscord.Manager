from datetime import datetime, timezone

import discord
from discord.ext import commands

from database.database import fetch_one, execute_query


class Club(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createclub(self, ctx, *, team_name: str):
        user_id = str(ctx.author.id)
        now = datetime.now(timezone.utc).isoformat()
        default_formation = "4-3-3"

        existing_team = fetch_one(
            "SELECT team_name FROM manager_teams WHERE user_id = ?",
            (user_id,)
        )

        if existing_team:
            await ctx.send(f"❌ Hai già una squadra: **{existing_team['team_name']}**.")
            return

        name_taken = fetch_one(
            "SELECT team_name FROM manager_teams WHERE LOWER(team_name) = LOWER(?)",
            (team_name,)
        )

        if name_taken:
            await ctx.send("❌ Questo nome squadra è già stato utilizzato.")
            return

        execute_query(
            """
            INSERT INTO manager_teams (
                user_id,
                team_name,
                formation,
                pending_formation,
                created_at,
                last_active_at,
                active
            )
            VALUES (?, ?, ?, NULL, ?, ?, 1)
            """,
            (user_id, team_name, default_formation, now, now)
        )

        embed = discord.Embed(
            title="🏟️ Club creato!",
            description=f"Benvenuto in **Calcyscord.Manager**, {ctx.author.mention}.",
            color=0x22C55E
        )

        embed.add_field(name="🏛️ Nome squadra", value=team_name, inline=False)
        embed.add_field(name="👤 Allenatore", value=ctx.author.display_name, inline=True)
        embed.add_field(name="📐 Modulo", value=default_formation, inline=True)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Club(bot))