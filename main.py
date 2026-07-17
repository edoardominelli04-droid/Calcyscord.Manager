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
        activity=discord.Game(
            name="⚽ Calcyscord.Manager"
        )
    )


@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        commands.CommandNotFound
    ):

        print(
            f"COMANDO NON TROVATO: {ctx.message.content}"
        )

        return

    raise error


@bot.command()
async def ping(
    ctx
):

    await ctx.send(
        "🏓 Pong!"
    )


@bot.command(name="riprendi")
async def riprendi(
    ctx
):
    """Riapre nei DM il percorso successivo alla rosa confermata."""

    try:
        from services.game.manager_service import ManagerService
        from services.game.initial_squad_service import InitialSquadService

        manager = ManagerService().get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send(
                "❌ Manager non trovato. Usa prima `!start`."
            )
            return

        initial_squad_service = InitialSquadService()
        draft = initial_squad_service.get_draft(
            manager["id"]
        )

        if draft is None:
            await ctx.send(
                "❌ Non esiste una composizione della rosa da riprendere."
            )
            return

        if not draft.get("confirmed"):
            await ctx.send(
                "❌ La rosa iniziale non è stata ancora confermata."
            )
            return

        statement_status = draft.get(
            "statement_status",
            "pending"
        )

        if statement_status != "pending":
            from services.game.manager_statement_service import (
                ManagerStatementService
            )

            if ManagerStatementService().is_preparation_complete(
                manager["id"]
            ):
                await ctx.send(
                    "✅ La preparazione iniziale è già completata. "
                    "Usa `!club` e `!formazione` per gestire la squadra."
                )
                return

        dm = await ctx.author.create_dm()

        if statement_status == "pending":
            from ui.initial_squad.initial_squad_embed import (
                InitialSquadEmbedBuilder
            )
            from ui.initial_squad.manager_statement_view import (
                ManagerStatementView
            )

            counts = initial_squad_service.get_role_counts(
                manager["id"]
            )

            embed = InitialSquadEmbedBuilder().build_confirmed(
                draft,
                counts
            )

            view = ManagerStatementView(
                manager["id"]
            )

        else:
            from ui.initial_squad.manager_statement_view import (
                ClubPreparationView
            )

            view = ClubPreparationView(
                manager["id"]
            )

            embed = view.embed_builder.build_preparation(
                manager["id"]
            )

        message = await dm.send(
            embed=embed,
            view=view
        )

        view.message = message

        await ctx.send(
            "📩 Percorso riaperto nei messaggi privati."
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ Non posso inviarti messaggi privati. "
            "Abilita i DM del server e riprova."
        )

    except Exception as error:
        print(
            "ERRORE COMANDO !riprendi:",
            repr(error)
        )

        await ctx.send(
            "❌ Impossibile riaprire il percorso: "
            f"`{type(error).__name__}: {error}`"
        )


async def load_extensions():

    await bot.load_extension(
        "cogs.manager"
    )

    await bot.load_extension(
        "cogs.dev"
    )

    await bot.load_extension(
        "cogs.roster"
    )

    await bot.load_extension(
        "cogs.player"
    )

    await bot.load_extension(
        "cogs.club_dashboard"
    )

    await bot.load_extension(
        "cogs.contract"
    )

    await bot.load_extension(
        "cogs.formation"
    )

    await bot.load_extension(
        "cogs.module"
    )


async def main():

    async with bot:

        await load_extensions()

        await bot.start(
            TOKEN
        )


asyncio.run(
    main()
)
