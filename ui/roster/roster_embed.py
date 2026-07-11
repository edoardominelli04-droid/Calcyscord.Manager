import discord


class RosterEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        data
    ):

        club = data["club"]

        embed = discord.Embed(

            title=f"👥 Rosa - {club['name']}",

            color=discord.Color.blue()

        )

        embed.add_field(
            name="🧤 Portieri",
            value="2",
            inline=True
        )

        embed.add_field(
            name="🛡 Difensori",
            value="8",
            inline=True
        )

        embed.add_field(
            name="⚙️ Centrocampisti",
            value="7",
            inline=True
        )

        embed.add_field(
            name="⚽ Attaccanti",
            value="5",
            inline=True
        )

        embed.set_footer(
            text="Seleziona un reparto tramite i pulsanti."
        )

        return embed

    def _build_role_embed(
        self,
        data,
        players,
        title,
        emoji
    ):

        club = data["club"]

        embed = discord.Embed(

            title=f"{emoji} {title} - {club['name']}",

            color=discord.Color.blue()

        )

        if not players:

            embed.description = (
                f"Nessun {title.lower()} presente in rosa."
            )

        else:

            for player in players:

                value = int(player.get("market_value") or 0)

                market_value = (
                    f"€{value:,}"
                    .replace(",", ".")
                )

                embed.add_field(

                    name=player["name"],

                    value=(
                        f"🌍 {player['country']}\n"
                        f"💰 {market_value}"
                    ),

                    inline=False

                )

        embed.set_footer(
            text="Calcyscord.Manager • Rosa"
        )

        return embed

    def build_goalkeepers(
        self,
        data,
        players
    ):

        return self._build_role_embed(
            data,
            players,
            "Portieri",
            "🧤"
        )

    def build_defenders(
        self,
        data,
        players
    ):

        return self._build_role_embed(
            data,
            players,
            "Difensori",
            "🛡️"
        )

    def build_midfielders(
        self,
        data,
        players
    ):

        return self._build_role_embed(
            data,
            players,
            "Centrocampisti",
            "⚙️"
        )

    def build_attackers(
        self,
        data,
        players
    ):

        return self._build_role_embed(
            data,
            players,
            "Attaccanti",
            "⚽"
        )
    
    def build_search(
        self
    ):

        embed = discord.Embed(

            title="🔍 Cerca giocatore",

            description="Seleziona un giocatore della tua rosa.",

            color=discord.Color.blue()

        )

        embed.set_footer(

            text="Calcyscord.Manager • Rosa"

        )

        return embed