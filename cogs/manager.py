import discord
from discord.ext import commands

from services.game.registration_service import RegistrationService
from services.game.club_selection_service import ClubSelectionService
from services.game.finance_service import FinanceService

from ui.start.start_view import StartView


class Manager(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.registration = RegistrationService()

        self.club_selection = ClubSelectionService()

        self.finance = FinanceService()

    # ==========================================================
    # START
    # ==========================================================

    @commands.command(name="start")
    async def start(self, ctx):

        manager, finance, created = self.registration.register(

            ctx.author.id,

            ctx.author.display_name

        )

        # ======================================================
        # MANAGER GIÀ REGISTRATO CON CLUB
        # ======================================================

        if manager["club_id"] is not None:

            # Permette di riprendere il percorso successivo alla
            # conferma anche dopo un riavvio o un messaggio scaduto.
            from services.game.initial_squad_service import (
                InitialSquadService
            )

            initial_squad_service = InitialSquadService()
            draft = initial_squad_service.get_draft(manager["id"])

            if draft and draft.get("confirmed"):

                try:
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
                                "Usa `!club` e `!formazione` per gestire "
                                "la squadra."
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

                        view = ManagerStatementView(manager["id"])

                    else:
                        from ui.initial_squad.manager_statement_view import (
                            ClubPreparationView
                        )

                        view = ClubPreparationView(manager["id"])
                        embed = view.embed_builder.build_preparation(
                            manager["id"]
                        )

                    message = await dm.send(
                        embed=embed,
                        view=view
                    )

                    view.message = message

                    await ctx.send(
                        "📩 Ho riaperto nei messaggi privati "
                        "la preparazione del tuo club."
                    )

                except discord.Forbidden:
                    await ctx.send(
                        "❌ Non posso inviarti messaggi privati. "
                        "Abilita i DM e riprova."
                    )

                return

            embed = discord.Embed(

                title="👔 Bentornato!",

                description=(
                    "Hai già iniziato la tua carriera.\n\n"
                    "Usa `!club` per continuare a gestire la tua squadra."
                ),

                colour=discord.Colour.blurple()

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

            await ctx.send(

                embed=embed

            )

            return

        # ======================================================
        # MANAGER SENZA CLUB
        # ======================================================

        if created:

            description = (

                "Il tuo profilo manageriale è stato creato.\n\n"
                "Controlla i messaggi privati.\n"
                "Ti guiderò nella scelta del tuo club."

            )

            colour = discord.Colour.green()

            title = "🎉 Benvenuto in Calcyscord.Manager!"

        else:

            description = (

                "Riprendiamo la procedura di scelta del club.\n\n"
                "Controlla i tuoi messaggi privati."

            )

            colour = discord.Colour.blurple()

            title = "👋 Bentornato!"

        embed = discord.Embed(

            title=title,

            description=description,

            colour=colour

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

        await ctx.send(

            embed=embed

        )

        try:

            dm = await ctx.author.create_dm()

            view = StartView(

                ctx.author.id

            )

            embed = view.embed_builder.build_welcome()

            message = await dm.send(

                embed=embed,

                view=view

            )

            view.message = message

        except discord.Forbidden:

            await ctx.send(

                "❌ Non posso inviarti messaggi privati.\n"
                "Abilita i DM del server e riprova."

            )

    # ==========================================================
    # MANAGER
    # ==========================================================

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

            colour=discord.Colour.blurple()

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

        await ctx.send(

            embed=embed

        )

    # ==========================================================
    # CHOOSECLUB (TEMPORANEO)
    # ==========================================================

    @commands.command(name="chooseclub")
    async def chooseclub(self, ctx, club_id: int):

        await ctx.send(

            "ℹ️ Questo comando è temporaneamente mantenuto "
            "solo per test e debug.\n\n"
            "Per gli utenti normali la scelta del club avviene "
            "tramite `!start` nei messaggi privati."

        )


async def setup(bot):

    await bot.add_cog(

        Manager(bot)

    )
