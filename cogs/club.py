from datetime import datetime, timezone

import discord
from discord.ext import commands

from database.database import fetch_one, fetch_all, execute_query


class ClubView(discord.ui.View):
    def __init__(self, author_id, team):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.team = team

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Questa schermata non è tua.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Home", emoji="🏟️", style=discord.ButtonStyle.primary)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=build_club_home_embed(interaction.user, self.team), view=self)

    @discord.ui.button(label="Rosa", emoji="👥", style=discord.ButtonStyle.secondary)
    async def roster_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="👥 Rosa",
            description="La gestione completa della rosa verrà implementata nei prossimi step.",
            color=0x2563EB
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Formazione", emoji="⚽", style=discord.ButtonStyle.secondary)
    async def lineup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚽ Formazione",
            description="La gestione di titolari, panchina e modulo verrà implementata nei prossimi step.",
            color=0x22C55E
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Calciomercato", emoji="🔄", style=discord.ButtonStyle.secondary)
    async def market_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔄 Calciomercato",
            description="Vendite, acquisti e trattative verranno implementati nei prossimi step.",
            color=0xF59E0B
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Aste", emoji="🔨", style=discord.ButtonStyle.secondary)
    async def auction_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔨 Aste",
            description="L'interfaccia delle aste settimanali verrà implementata nei prossimi step.",
            color=0x8B5CF6
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Classifica", emoji="📊", style=discord.ButtonStyle.secondary)
    async def ranking_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 Classifica",
            description="La classifica stagionale verrà implementata nei prossimi step.",
            color=0x38BDF8
        )
        await interaction.response.edit_message(embed=embed, view=self)


def get_roster_count(user_id):
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM manager_rosters WHERE user_id = ?",
        (str(user_id),)
    )
    return row["total"] if row else 0


def build_club_home_embed(user, team):
    roster_count = get_roster_count(user.id)

    embed = discord.Embed(
        title=f"🏟️ {team['team_name']}",
        description="Centro di controllo del tuo club.",
        color=0x22C55E
    )

    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    embed.add_field(name="👤 Allenatore", value=user.display_name, inline=True)
    embed.add_field(name="📐 Modulo", value=team["formation"], inline=True)
    embed.add_field(name="👥 Giocatori in rosa", value=str(roster_count), inline=True)

    embed.add_field(name="💰 Crediti", value="Economia condivisa non ancora collegata", inline=False)
    embed.add_field(name="🏆 Trofei", value="Nessun trofeo", inline=True)
    embed.add_field(name="📬 Notifiche", value="Nessuna notifica", inline=True)

    embed.set_footer(text="Calcyscord.Manager • Club Hub")

    return embed


class Club(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createclub(self, ctx, *, team_name: str):
        user_id = str(ctx.author.id)
        now = datetime.now(timezone.utc).isoformat()
        default_formation = "4-3-3"

        existing_team = fetch_one(
            "SELECT team_name FROM manager_teams WHERE user_id = ?",
            (user_id,)
        )

        if existing_team:
            await ctx.send(f"❌ Hai già una squadra: **{existing_team['team_name']}**.")
            return

        name_taken = fetch_one(
            "SELECT team_name FROM manager_teams WHERE LOWER(team_name) = LOWER(?)",
            (team_name,)
        )

        if name_taken:
            await ctx.send("❌ Questo nome squadra è già stato utilizzato.")
            return

        execute_query(
            """
            INSERT INTO manager_teams (
                user_id,
                team_name,
                formation,
                pending_formation,
                created_at,
                last_active_at,
                active
            )
            VALUES (?, ?, ?, NULL, ?, ?, 1)
            """,
            (user_id, team_name, default_formation, now, now)
        )

        embed = discord.Embed(
            title="🏟️ Club creato!",
            description=f"Benvenuto in **Calcyscord.Manager**, {ctx.author.mention}.",
            color=0x22C55E
        )

        embed.add_field(name="🏛️ Nome squadra", value=team_name, inline=False)
        embed.add_field(name="👤 Allenatore", value=ctx.author.display_name, inline=True)
        embed.add_field(name="📐 Modulo", value=default_formation, inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def club(self, ctx):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

        user_id = str(ctx.author.id)

        team = fetch_one(
            "SELECT * FROM manager_teams WHERE user_id = ? AND active = 1",
            (user_id,)
        )

        if not team:
            embed = discord.Embed(
                title="🏟️ Nessun club trovato",
                description="Non hai ancora creato una squadra.\n\nUsa:\n`!createclub Nome Squadra`",
                color=0xEF4444
            )
            await ctx.send(embed=embed)
            return

        embed = build_club_home_embed(ctx.author, team)
        view = ClubView(ctx.author.id, team)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Club(bot))