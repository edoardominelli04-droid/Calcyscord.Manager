import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.schema import create_tables

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


async def load_extensions():
    await bot.load_extension("cogs.club")
    await bot.load_extension("cogs.manager")
    await bot.load_extension("cogs.dev")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())