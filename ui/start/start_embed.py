import discord


class StartEmbedBuilder:
    """Costruisce gli embed del sistema di onboarding."""

    def build_welcome(self):

        embed = discord.Embed(

            title="👋 Benvenuto in Calcyscord.Manager",

            description=(
                "Benvenuto nel tuo nuovo ruolo di manager.\n\n"
                "Scegli come trovare il club da allenare."
            ),

            colour=discord.Colour.green()

        )

        embed.add_field(

            name="🔍 Cerca per nome",

            value=(
                "Trova rapidamente un club "
                "digitandone il nome."
            ),

            inline=False

        )

        embed.add_field(

            name="🧭 Sfoglia club",

            value=(
                "Esplora i club disponibili "
                "per competizione."
            ),

            inline=False

        )

        embed.add_field(

            name="🎲 Club suggeriti",

            value=(
                "Ricevi una selezione casuale "
                "di club ancora liberi."
            ),

            inline=False

        )

        embed.set_footer(

            text="Potrai scegliere un solo club."

        )

        return embed

    def build_confirmation(
        self,
        club,
        competition=None
    ):

        embed = discord.Embed(

            title="🏟️ Conferma scelta",

            description=(
                "Controlla i dati del club "
                "prima della conferma."
            ),

            colour=discord.Colour.gold()

        )

        embed.add_field(

            name="Club",

            value=club["name"],

            inline=False

        )

        if competition:

            embed.add_field(

                name="Competizione",

                value=competition["name"],

                inline=True

            )

        embed.add_field(

            name="Stadio",

            value=club.get("stadium_name", "-"),

            inline=True

        )

        embed.add_field(

            name="Età media",

            value=str(
                club.get("average_age", "-")
            ),

            inline=True

        )

        embed.set_footer(

            text="Il club verrà assegnato solo dopo la conferma."

        )

        return embed

    def build_completed(
        self,
        club
    ):

        embed = discord.Embed(

            title="✅ Club assegnato",

            description=(
                f"Ora sei il nuovo manager di **{club['name']}**."
            ),

            colour=discord.Colour.green()

        )

        embed.add_field(

            name="Prossimo passo",

            value=(
                "Usa `!club` per iniziare "
                "la tua carriera."
            ),

            inline=False

        )

        return embed
    
    def build_club_list(
        self,
        clubs
    ):

        embed = discord.Embed(

            title="🏟️ Seleziona un club",

            description="Seleziona uno dei club disponibili.",

            colour=discord.Colour.blurple()

        )

        if not clubs:

            embed.description = (

                "Nessun club disponibile."

            )

            return embed

        for club in clubs[:25]:

            embed.add_field(

                name=club["name"],

                value=club.get(

                    "competition_external_id",

                    "-"

                ),

                inline=False

            )

        return embed
    
    def build_competition_list(
        self,
        competitions
    ):

        embed = discord.Embed(

            title="🧭 Sfoglia competizioni",

            description="Seleziona una competizione.",

            colour=discord.Colour.blurple()

        )

        if not competitions:

            embed.description = (

                "Nessuna competizione disponibile."

            )

            return embed

        for competition in competitions:

            embed.add_field(

                name=competition["name"],

                value="",

                inline=False

            )

        return embed