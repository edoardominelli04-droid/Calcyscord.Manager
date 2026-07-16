import discord

from services.game.initial_squad_service import (
    InitialSquadService
)


class InitialSquadEmbedBuilder:
    """Embed della composizione della rosa iniziale."""

    def __init__(self):

        self.service = InitialSquadService()

    # ==========================================================
    # BARRA DI AVANZAMENTO
    # ==========================================================

    def _build_progress_bar(
        self,
        current,
        maximum
    ):

        length = 30

        if maximum == 0:

            return "░" * length

        filled = int(

            (current / maximum) * length

        )

        filled = min(
            filled,
            length
        )

        return (

            "█" * filled +

            "░" * (length - filled)

        )

    # ==========================================================
    # HOME
    # ==========================================================

    def build_home(
        self,
        draft,
        counts
    ):

        budget = draft["budget"]

        used = draft["points_used"]

        rules = self.service.get_rules()

        total_required = sum(
            rules.values()
        )

        total_selected = sum(
            counts.values()
        )

        percentage = int(
            total_selected / total_required * 100
        )

        progress = self._build_progress_bar(
            total_selected,
            total_required
        )

        # ======================================================
        # STATO REPARTI
        # ======================================================

        goalkeeper_status = (
            " ✅"
            if counts["Goalkeeper"] >= rules["Goalkeeper"]
            else ""
        )

        defender_status = (
            " ✅"
            if counts["Defender"] >= rules["Defender"]
            else ""
        )

        midfield_status = (
            " ✅"
            if counts["Midfield"] >= rules["Midfield"]
            else ""
        )

        attack_status = (
            " ✅"
            if counts["Attack"] >= rules["Attack"]
            else ""
        )

        # ======================================================
        # FOOTER
        # ======================================================

        if percentage == 100:

            footer = (
                "🎉 La tua rosa è pronta. Premi 'Conferma rosa' per iniziare la tua carriera."
            )

        else:

            footer = (
                "Completa tutti i reparti per confermare la rosa."
            )

        # ======================================================
        # EMBED
        # ======================================================

        embed = discord.Embed(

            title="👥 Componi la rosa iniziale",

            colour=discord.Colour.blurple()

        )

        embed.description = (

            "Costruisci la tua rosa iniziale selezionando i giocatori del club.\n"

            "Quando tutti i reparti saranno completi potrai confermarla."

        )

        embed.add_field(

            name="📈 Avanzamento",

            value=(

                f"{progress}\n\n"

                f"**{total_selected}/{total_required} giocatori**\n"

                f"**{percentage}% completato**"

            ),

            inline=False

        )

        embed.add_field(

            name="👥 Reparti",

            value=(

                f"🥅 Portieri: **{counts['Goalkeeper']}/{rules['Goalkeeper']}**{goalkeeper_status}\n"

                f"🛡️ Difensori: **{counts['Defender']}/{rules['Defender']}**{defender_status}\n"

                f"🎯 Centrocampisti: **{counts['Midfield']}/{rules['Midfield']}**{midfield_status}\n"

                f"⚽ Attaccanti: **{counts['Attack']}/{rules['Attack']}**{attack_status}"

            ),

            inline=False

        )

        embed.add_field(

            name="💰 Budget",

            value=f"**{used}/{budget} punti**",

            inline=False

        )

        embed.set_footer(

            text=footer

        )

        return embed