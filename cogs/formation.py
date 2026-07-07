import discord
from discord.ext import commands

from services.database_manager import DatabaseManager
from services.game.manager_service import ManagerService
from services.game.formation_service import FormationService
from services.utils.position_utils import PositionUtils
from services.utils.slot_utils import SlotUtils


class Formation(commands.Cog):
    """Visualizzazione della formazione."""

    def __init__(self, bot):
        self.bot = bot

        self.db = DatabaseManager()
        self.manager_service = ManagerService()
        self.formation_service = FormationService()
        self.position_utils = PositionUtils()

    @commands.command(name="formazione")
    async def formazione(self, ctx):

        manager = self.manager_service.get_by_discord_id(
            ctx.author.id
        )

        if manager is None:
            await ctx.send("❌ Devi prima registrarti con `!start`.")
            return

        formation = self.formation_service.get_manager_formation(
            manager["id"]
        )

        if formation is None:
            await ctx.send("❌ Nessuna formazione trovata.")
            return

        club = self.db.get_club_by_id(manager["club_id"])

        starting = self.formation_service.get_starting_players_full(
            manager["id"]
        )

        bench = self.formation_service.get_bench_players_full(
            manager["id"]
        )

        portiere = []
        difensori = []
        centrocampisti = []
        attaccanti = []

        for slot, data in starting.items():

            player = data["player"]

            ruolo = self.position_utils.translate(
                player.get("sub_position")
            )

            nome = player["name"]

            if data["captain"]:
                nome += " ©"

            elif data["vice_captain"]:
                nome += " (VC)"

            riga = f"{slot:<4}• {nome} ({ruolo})"

            department = SlotUtils.department(slot)

            if department == "Goalkeeper":

                portiere.append(
                    riga
                )

            elif department == "Defence":

                difensori.append(
                    riga
                )

            elif department == "Midfield":

                centrocampisti.append(
                    riga
               )

            elif department == "Attack":

                attaccanti.append(
                    riga
                )

        portieri_panchina = []
        difensori_panchina = []
        centrocampisti_panchina = []
        attaccanti_panchina = []

        for player in bench:

            ruolo = self.position_utils.translate(
                player.get("sub_position")
            )

            riga = f"{player['name']} ({ruolo})"

            department = self.position_utils.get_department(player)

            if department == "goalkeeper":
                portieri_panchina.append(riga)

            elif department == "defence":
                difensori_panchina.append(riga)

            elif department == "midfield":
                centrocampisti_panchina.append(riga)

            elif department == "attack":
                attaccanti_panchina.append(riga)

        embed = discord.Embed(
            title="📋 Formazione",
            description="La tua formazione attuale",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🏟 Club",
            value=club["name"],
            inline=True
        )

        embed.add_field(
            name="👔 Allenatore",
            value=manager["username"],
            inline=True
        )

        embed.add_field(
            name="📐 Modulo",
            value=formation["module"],
            inline=True
        )

        embed.add_field(
            name="👥 Rosa",
            value=f"{11 + len(bench)} giocatori",
            inline=True
        )

        embed.add_field(
            name="🧤 Portiere",
            value="\n".join(portiere) if portiere else "-",
            inline=False
        )

        embed.add_field(
            name="🛡 Difensori",
            value="\n".join(difensori) if difensori else "-",
            inline=False
        )

        embed.add_field(
            name="⚙️ Centrocampisti",
            value="\n".join(centrocampisti) if centrocampisti else "-",
            inline=False
        )

        embed.add_field(
            name="⚽ Attaccanti",
            value="\n".join(attaccanti) if attaccanti else "-",
            inline=False
        )

        panchina_text = ""

        if portieri_panchina:
            panchina_text += (
                "**🧤 Portieri**\n"
                + "\n".join(portieri_panchina)
                + "\n\n"
            )

        if difensori_panchina:
            panchina_text += (
                "**🛡 Difensori**\n"
                + "\n".join(difensori_panchina)
                + "\n\n"
            )

        if centrocampisti_panchina:
            panchina_text += (
                "**⚙️ Centrocampisti**\n"
                + "\n".join(centrocampisti_panchina)
                + "\n\n"
            )

        if attaccanti_panchina:
            panchina_text += (
                "**⚽ Attaccanti**\n"
                + "\n".join(attaccanti_panchina)
            )

        if not panchina_text.strip():
            panchina_text = "-"

        embed.add_field(
            name="🪑 Panchina",
            value=panchina_text,
            inline=False
        )

        embed.set_footer(
            text="Usa i pulsanti qui sotto per gestire la formazione."
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Formation(bot))