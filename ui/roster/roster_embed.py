import discord


COUNTRIES = {

    "Italy": "🇮🇹",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Spain": "🇪🇸",
    "England": "🏴",
    "Portugal": "🇵🇹",
    "Brazil": "🇧🇷",
    "Argentina": "🇦🇷",
    "Belgium": "🇧🇪",
    "Netherlands": "🇳🇱"

}


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

        goalkeepers = sum(

            1

            for p in data["players"]

            if p["position"] == "Goalkeeper"

        )

        defenders = sum(

            1

            for p in data["players"]

            if p["position"] == "Defender"

        )

        midfielders = sum(

            1

            for p in data["players"]

            if p["position"] == "Midfield"

        )

        attackers = sum(

            1

            for p in data["players"]

            if p["position"] == "Attack"

        )

        total = len(

            data["players"]

        )

        embed = discord.Embed(

            title=f"👥 Rosa - {club['name']}",

            color=discord.Color.blue()

        )

        embed.add_field(

            name="🧤 Portieri",

            value=str(goalkeepers),

            inline=False

        )

        embed.add_field(

            name="🛡️ Difensori",

            value=str(defenders),

            inline=False

        )

        embed.add_field(

            name="⚙️ Centrocampisti",

            value=str(midfielders),

            inline=False

        )

        embed.add_field(

            name="⚽ Attaccanti",

            value=str(attackers),

            inline=False

        )

        embed.add_field(

            name="👥 Totale giocatori",

            value=str(total),

            inline=False

        )

        embed.set_footer(

            text="Calcyscord.Manager • Rosa"

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

                value = int(

                    player.get(

                        "market_value"

                    ) or 0

                )

                market_value = (

                    f"€{value:,}"

                    .replace(",", ".")

                )

                country = COUNTRIES.get(

                    player["country"],

                    "🌍"

                )

                embed.add_field(

                    name=f"{country} {player['name']}",

                    value=f"💰 {market_value}",

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

            title="🔎 Cerca giocatori nella tua rosa",

            description="Inserisci il nome del giocatore da cercare.",

            color=discord.Color.blue()

        )

        embed.set_footer(

            text="Calcyscord.Manager • Rosa"

        )

        return embed