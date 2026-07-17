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

        tier_counts = self.service.get_tier_counts(
            draft["manager_id"]
        )

        rules = self.service.get_rules()

        total_required = sum(
            rules.values()
        )

        total_selected = sum(
            counts.values()
        )

        flexible_used = (
            max(0, counts["Goalkeeper"] - rules["Goalkeeper"])
            + max(0, counts["Defender"] - rules["Defender"])
            + max(0, counts["Midfield"] - rules["Midfield"])
            + max(0, counts["Attack"] - rules["Attack"])
        )

        goalkeeper_required = min(
            counts["Goalkeeper"],
            rules["Goalkeeper"]
        )

        defender_required = min(
            counts["Defender"],
            rules["Defender"]
        )

        midfield_required = min(
            counts["Midfield"],
            rules["Midfield"]
        )

        attack_required = min(
            counts["Attack"],
            rules["Attack"]
        )

        defender_flexible = max(
            0,
            counts["Defender"] - rules["Defender"]
        )

        goalkeeper_flexible = max(
            0,
            counts["Goalkeeper"] - rules["Goalkeeper"]
        )

        midfield_flexible = max(
            0,
            counts["Midfield"] - rules["Midfield"]
        )

        attack_flexible = max(
            0,
            counts["Attack"] - rules["Attack"]
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

        if draft.get("confirmed"):

            footer = (
                "✅ Rosa confermata. Le scelte sono ora definitive."
            )

        elif percentage == 100:

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

        if draft.get("confirmed"):

            embed.title = "✅ Rosa iniziale confermata"

            embed.colour = discord.Colour.green()

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

                f"🥅 Portieri: **{goalkeeper_required}/{rules['Goalkeeper']} obbligatori** "
                f"+ **{goalkeeper_flexible} flessibili**{goalkeeper_status}\n"

                f"🛡️ Difensori: **{defender_required}/{rules['Defender']} obbligatori** "
                f"+ **{defender_flexible} flessibili**{defender_status}\n"

                f"🎯 Centrocampisti: **{midfield_required}/{rules['Midfield']} obbligatori** "
                f"+ **{midfield_flexible} flessibili**{midfield_status}\n"

                f"⚽ Attaccanti: **{attack_required}/{rules['Attack']} obbligatori** "
                f"+ **{attack_flexible} flessibili**{attack_status}\n"

                f"🔄 Posti flessibili: **{flexible_used}/{rules['Flexible']}**"

            ),

            inline=False

        )

        if not draft.get("confirmed"):

            embed.add_field(

                name="💰 Budget",

                value=(
                    f"Utilizzato: ⭐ **{used}/{budget}**\n"
                    f"Disponibile: ⭐ **{max(0, budget - used)}**\n"
                    f"Fascia S: **{tier_counts['S']}/2** • "
                    f"Fasce S+A: **{tier_counts['S'] + tier_counts['A']}/6**"
                ),

                inline=False

            )

        embed.set_footer(

            text=footer

        )

        return embed
