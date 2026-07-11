import discord
from datetime import date


class ContractEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        player
    ):

        # ======================================================
        # DATI CONTRATTO (temporanei)
        # ======================================================

        salary = "€ ---"

        expiry_date = None

        duration = "---"

        negotiation = False

        renewed = False

        released = False

        # ======================================================
        # STATO CONTRATTO
        # ======================================================

        if released:

            status = "⚫ Svincolato"

        elif renewed:

            status = "🔵 Rinnovato"

        elif negotiation:

            status = "🟠 In trattativa"

        elif expiry_date is None:

            status = "🟢 In vigore"

        else:

            today = date.today()

            months_left = (

                (expiry_date.year - today.year) * 12
                + (expiry_date.month - today.month)

            )

            if months_left < 0:

                status = "🔴 Scaduto"

            elif months_left <= 6:

                status = "🟡 In scadenza"

            else:

                status = "🟢 In vigore"

        # ======================================================
        # EMBED
        # ======================================================

        embed = discord.Embed(

            title=f"📜 Contratto - {player['name']}",

            color=discord.Color.green()

        )

        embed.set_thumbnail(

            url=player["image"]

        )

        embed.add_field(

            name="💰 Stipendio",

            value=salary,

            inline=True

        )

        embed.add_field(

            name="📅 Scadenza",

            value="Da definire" if expiry_date is None else expiry_date.strftime("%d/%m/%Y"),

            inline=True

        )

        embed.add_field(

            name="⌛ Durata",

            value=duration,

            inline=True

        )

        embed.add_field(

            name="📄 Stato",

            value=status,

            inline=True

        )

        embed.set_footer(

            text="Calcyscord.Manager • Contratto"

        )

        return embed