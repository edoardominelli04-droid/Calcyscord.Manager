import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.schema import create_tables

# Carica le variabili dal file .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot
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


bot.run(TOKEN)