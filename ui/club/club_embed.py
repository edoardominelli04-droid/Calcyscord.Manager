import discord


class ClubEmbedBuilder:

    def __init__(
        self
    ):
        pass

    def build(
        self,
        data
    ):

        club = data["club"]
        manager = data["manager"]
        finance = data["finance"]
        competition = data["competition"]
        stadium = data["stadium"]

        embed = discord.Embed(

            title=f"🏟 {club['name']}",

            color=discord.Color.dark_green()

        )

        embed.add_field(

            name="👔 Allenatore",

            value=manager["username"],

            inline=True

        )

        embed.add_field(

            name="🏆 Competizione",

            value=competition["name"] if competition else "-",

            inline=True

        )

        embed.add_field(

            name="📍 Stadio",

            value=stadium["name"] if stadium else club.get(
                "stadium_name",
                "-"
            ),

            inline=True

        )

        embed.add_field(

            name="👥 Rosa",

            value=data["players_count"],

            inline=True

        )

        embed.add_field(

            name="📈 Età media",

            value=data["average_age"],

            inline=True

        )

        embed.add_field(

            name="💰 Budget",

            value=f"{finance['balance']:,} €".replace(
                ",",
                "."
            ),

            inline=True

        )

        embed.add_field(

            name="💎 Valore rosa",

            value=f"{int(data['market_value']):,} €".replace(
                ",",
                "."
            ),

            inline=True

        )

        if data["most_valuable_player"]:

            player = data["most_valuable_player"]

            embed.add_field(

                name="⭐ Giocatore più prezioso",

                value=(
                    f"{player['name']}\n"
                    f"{int(player.get('market_value', 0) or 0):,} €".replace(",", ".")
                ),

                inline=False

            )

        return embed