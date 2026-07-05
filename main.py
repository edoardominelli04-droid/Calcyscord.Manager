import os
from datetime import datetime, timezone

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.schema import create_tables
from database.database import fetch_one, execute_query

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    create_tables()

    print("=" * 40)
    print(f"✅ {bot.user} è online!")
    print("Calcyscord.Manager avviato correttamente.")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Game(name="⚽ Calcyscord.Manager")
    )


@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


@bot.command()
async def createclub(ctx, *, team_name: str):
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
        color=0x22c55e
    )
    embed.add_field(name="🏛️ Nome squadra", value=team_name, inline=False)
    embed.add_field(name="👤 Allenatore", value=ctx.author.display_name, inline=True)
    embed.add_field(name="📐 Modulo iniziale", value=default_formation, inline=True)
    embed.set_footer(text="Prossimo passo: gestione rosa e comando !club")

    await ctx.send(embed=embed)


bot.run(TOKEN)