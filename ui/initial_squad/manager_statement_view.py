import os

import discord

from services.database_manager import DatabaseManager
from services.game.formation_service import FormationService
from services.game.initial_squad_service import InitialSquadService
from services.game.manager_statement_service import ManagerStatementService


PRESS_ROOM_CHANNEL_ID = int(
    os.getenv(
        "PRESS_ROOM_CHANNEL_ID",
        "1527694721173028985"
    )
)


class ManagerStatementEmbedBuilder:
    """Embed del percorso successivo alla conferma della rosa."""

    def __init__(self):
        self.db = DatabaseManager()
        self.initial_squad_service = InitialSquadService()

    def build_preview(self, manager, club, text, user):
        embed = discord.Embed(
            title="🎙️ Presentazione ufficiale",
            description=(
                f"**{manager['username']} è il nuovo manager "
                f"del {club['name']}**\n\n"
                f"“{text}”"
            ),
            colour=discord.Colour.gold()
        )

        embed.add_field(
            name="👤 Manager",
            value=manager["username"],
            inline=True
        )

        embed.add_field(
            name="🏟️ Club",
            value=club["name"],
            inline=True
        )

        avatar = getattr(user, "display_avatar", None)

        if avatar:
            embed.set_author(
                name=getattr(user, "display_name", manager["username"]),
                icon_url=avatar.url
            )

        if club.get("logo"):
            embed.set_thumbnail(url=club["logo"])

        embed.set_footer(
            text="Controlla il testo prima della pubblicazione."
        )

        return embed

    def build_public(self, manager, club, text, user):
        embed = self.build_preview(
            manager,
            club,
            text,
            user
        )

        embed.colour = discord.Colour.dark_green()
        embed.set_footer(
            text="Calcyscord.Manager • Sala stampa"
        )

        return embed

    def build_neutral(self, manager, club, user):
        embed = discord.Embed(
            title="📣 Nuovo incarico",
            description=(
                f"**{manager['username']} è ufficialmente il nuovo "
                f"manager del {club['name']}.**"
            ),
            colour=discord.Colour.dark_green()
        )

        avatar = getattr(user, "display_avatar", None)

        if avatar:
            embed.set_author(
                name=getattr(user, "display_name", manager["username"]),
                icon_url=avatar.url
            )

        if club.get("logo"):
            embed.set_thumbnail(url=club["logo"])

        embed.set_footer(
            text="Calcyscord.Manager • Sala stampa"
        )

        return embed

    def build_preparation(self, manager_id):
        manager = self.db.get_manager_by_id(manager_id)
        club = self.db.get_club_by_id(manager["club_id"])

        formation = next(
            (
                item
                for item in self.db.get_formations()
                if item["manager_id"] == manager_id
            ),
            None
        )

        starters = formation.get("starting", {}) if formation else {}

        formation_ready = (
            formation is not None
            and len(starters) == 11
        )

        captain_ready = any(
            data.get("captain")
            for data in starters.values()
        )

        formation_icon = "✅" if formation_ready else "⬜"
        captain_icon = "✅" if captain_ready else "⬜"

        embed = discord.Embed(
            title="🚦 Preparazione del club",
            description=(
                f"Il **{club['name']}** è stato affidato a "
                f"**{manager['username']}**. Ora prepara la squadra "
                "per le partite."
            ),
            colour=discord.Colour.blurple()
        )

        embed.add_field(
            name="📋 Checklist iniziale",
            value=(
                "✅ Club scelto\n"
                "✅ Rosa iniziale confermata\n"
                f"{formation_icon} Formazione iniziale\n"
                f"{captain_icon} Capitano"
            ),
            inline=False
        )

        if formation_ready and captain_ready:
            embed.add_field(
                name="🎉 Club pronto",
                value="La preparazione iniziale è completa.",
                inline=False
            )
        else:
            embed.add_field(
                name="⚠️ Prossimo passo",
                value=(
                    "La formazione iniziale è già stata generata. "
                    "Scegli il capitano per completare la preparazione."
                ),
                inline=False
            )

        if club.get("logo"):
            embed.set_thumbnail(url=club["logo"])

        embed.set_footer(
            text="Scegli il capitano adesso oppure continua più tardi."
        )

        return embed

    def build_later(self, manager_id):
        manager = self.db.get_manager_by_id(manager_id)
        club = self.db.get_club_by_id(manager["club_id"])

        return discord.Embed(
            title="🏠 Preparazione rimandata",
            description=(
                f"Il **{club['name']}** è stato registrato correttamente.\n\n"
                "Quando vuoi potrai riprendere la scelta del capitano "
                "usando `!riprendi`."
            ),
            colour=discord.Colour.green()
        )


async def get_press_room(client):
    channel = client.get_channel(PRESS_ROOM_CHANNEL_ID)

    if channel is None:
        try:
            channel = await client.fetch_channel(PRESS_ROOM_CHANNEL_ID)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            return None

    return channel


class ManagerOnlyView(discord.ui.View):

    def __init__(self, manager_id, timeout=600):
        super().__init__(timeout=timeout)

        self.manager_id = manager_id
        self.db = DatabaseManager()
        self.embed_builder = ManagerStatementEmbedBuilder()
        self.statement_service = ManagerStatementService()

        self.manager = self.db.get_manager_by_id(manager_id)
        self.club = self.db.get_club_by_id(self.manager["club_id"])
        self.discord_id = str(self.manager["discord_id"])

    async def interaction_check(self, interaction):
        if str(interaction.user.id) == self.discord_id:
            return True

        await interaction.response.send_message(
            "❌ Questa schermata appartiene a un altro manager.",
            ephemeral=True
        )

        return False


class ManagerStatementModal(discord.ui.Modal):

    def __init__(self, parent_view, original_message, initial_text=""):
        super().__init__(title="Prima dichiarazione da manager")

        self.parent_view = parent_view
        self.original_message = original_message

        self.statement = discord.ui.TextInput(
            label="La tua dichiarazione",
            placeholder=(
                "Presentati alla community e racconta le tue ambizioni..."
            ),
            style=discord.TextStyle.paragraph,
            required=True,
            min_length=1,
            max_length=ManagerStatementService.MAX_LENGTH,
            default=initial_text or None
        )

        self.add_item(self.statement)

    async def on_submit(self, interaction):
        valid, error, clean_text = (
            self.parent_view.statement_service.validate_text(
                self.statement.value
            )
        )

        if not valid:
            await interaction.response.send_message(
                f"❌ {error}",
                ephemeral=True
            )
            return

        preview_view = ManagerStatementPreviewView(
            manager_id=self.parent_view.manager_id,
            text=clean_text,
            original_message=self.original_message
        )

        embed = preview_view.embed_builder.build_preview(
            preview_view.manager,
            preview_view.club,
            clean_text,
            interaction.user
        )

        await interaction.response.send_message(
            embed=embed,
            view=preview_view,
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions.none()
        )


class WriteStatementButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Scrivi dichiarazione",
            emoji="✍️",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction):
        allowed, error = self.view.statement_service.can_complete(
            self.view.manager_id
        )

        if not allowed:
            await interaction.response.send_message(
                f"❌ {error}",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            ManagerStatementModal(
                self.view,
                interaction.message
            )
        )


class SkipStatementButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Salta",
            emoji="⏭️",
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction):
        await interaction.response.defer()

        allowed, error = self.view.statement_service.can_complete(
            self.view.manager_id
        )

        if not allowed:
            await interaction.followup.send(
                f"❌ {error}",
                ephemeral=True
            )
            return

        channel = await get_press_room(interaction.client)

        if channel is None:
            await interaction.followup.send(
                "❌ Il canale `🎙️ sala stampa` non è accessibile al bot.",
                ephemeral=True
            )
            return

        public_embed = self.view.embed_builder.build_neutral(
            self.view.manager,
            self.view.club,
            interaction.user
        )

        try:
            public_message = await channel.send(
                embed=public_embed,
                allowed_mentions=discord.AllowedMentions.none()
            )
        except (discord.Forbidden, discord.HTTPException):
            await interaction.followup.send(
                "❌ Non riesco a pubblicare in `🎙️ sala stampa`.",
                ephemeral=True
            )
            return

        completed, result = self.view.statement_service.skip(
            self.view.manager_id,
            channel.id,
            public_message.id
        )

        if not completed:
            await interaction.followup.send(
                f"❌ {result}",
                ephemeral=True
            )
            return

        preparation_view = ClubPreparationView(self.view.manager_id)

        await interaction.edit_original_response(
            embed=preparation_view.embed_builder.build_preparation(
                self.view.manager_id
            ),
            view=preparation_view
        )


class ManagerStatementView(ManagerOnlyView):

    def __init__(self, manager_id):
        super().__init__(manager_id)

        self.add_item(WriteStatementButton())
        self.add_item(SkipStatementButton())


class PublishStatementButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Pubblica",
            emoji="✅",
            style=discord.ButtonStyle.success
        )

    async def callback(self, interaction):
        await interaction.response.defer()

        allowed, error = self.view.statement_service.can_complete(
            self.view.manager_id
        )

        if not allowed:
            await interaction.followup.send(
                f"❌ {error}",
                ephemeral=True
            )
            return

        channel = await get_press_room(interaction.client)

        if channel is None:
            await interaction.followup.send(
                "❌ Il canale `🎙️ sala stampa` non è accessibile al bot.",
                ephemeral=True
            )
            return

        public_embed = self.view.embed_builder.build_public(
            self.view.manager,
            self.view.club,
            self.view.text,
            interaction.user
        )

        try:
            public_message = await channel.send(
                embed=public_embed,
                allowed_mentions=discord.AllowedMentions.none()
            )
        except (discord.Forbidden, discord.HTTPException):
            await interaction.followup.send(
                "❌ Non riesco a pubblicare in `🎙️ sala stampa`.",
                ephemeral=True
            )
            return

        completed, result = self.view.statement_service.publish(
            self.view.manager_id,
            self.view.text,
            channel.id,
            public_message.id
        )

        if not completed:
            await interaction.followup.send(
                f"❌ {result}",
                ephemeral=True
            )
            return

        preparation_view = ClubPreparationView(self.view.manager_id)
        preparation_embed = (
            preparation_view.embed_builder.build_preparation(
                self.view.manager_id
            )
        )

        await interaction.edit_original_response(
            embed=preparation_embed,
            view=preparation_view
        )

        if self.view.original_message is not None:
            try:
                await self.view.original_message.edit(
                    embed=preparation_embed,
                    view=ClubPreparationView(self.view.manager_id)
                )
            except discord.HTTPException:
                pass


class ModifyStatementButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Modifica",
            emoji="✏️",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction):
        await interaction.response.send_modal(
            ManagerStatementModal(
                self.view,
                self.view.original_message,
                initial_text=self.view.text
            )
        )


class CancelStatementButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Annulla",
            emoji="❌",
            style=discord.ButtonStyle.danger
        )

    async def callback(self, interaction):
        await interaction.response.edit_message(
            content=(
                "Anteprima annullata. Puoi tornare al messaggio precedente "
                "per scrivere una nuova dichiarazione oppure saltare."
            ),
            embed=None,
            view=None
        )


class ManagerStatementPreviewView(ManagerOnlyView):

    def __init__(self, manager_id, text, original_message):
        super().__init__(manager_id)

        self.text = text
        self.original_message = original_message

        self.add_item(PublishStatementButton())
        self.add_item(ModifyStatementButton())
        self.add_item(CancelStatementButton())


class InitialCaptainSelect(discord.ui.Select):

    def __init__(self, manager_id, preparation_message):
        self.manager_id = manager_id
        self.preparation_message = preparation_message
        self.formation_service = FormationService()
        self.embed_builder = ManagerStatementEmbedBuilder()

        starting = self.formation_service.get_starting_players_full(
            manager_id
        )

        options = []

        for slot, data in starting.items():
            player = data["player"]

            options.append(
                discord.SelectOption(
                    label=player["name"],
                    value=str(player["id"]),
                    description=f"Titolare • {slot}"
                )
            )

        super().__init__(
            placeholder="Seleziona il capitano...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)

        player_id = int(self.values[0])

        result = self.formation_service.set_captain(
            self.manager_id,
            player_id
        )

        if not result["success"]:
            await interaction.followup.send(
                f"❌ {result['error']['message']}",
                ephemeral=True
            )
            return

        player = result["data"]["player"]

        if self.preparation_message is not None:
            try:
                await self.preparation_message.edit(
                    embed=self.embed_builder.build_preparation(
                        self.manager_id
                    ),
                    view=None
                )
            except discord.HTTPException:
                pass

        try:
            await interaction.delete_original_response()
        except discord.HTTPException:
            pass

        await interaction.followup.send(
            (
                f"👑 **{player['name']}** è il capitano.\n"
                "✅ Preparazione completata: ora puoi iniziare a giocare."
            ),
            ephemeral=True
        )


class ChooseCaptainButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Scegli capitano",
            emoji="👑",
            style=discord.ButtonStyle.success
        )

    async def callback(self, interaction):
        formation_service = FormationService()
        starting = formation_service.get_starting_players_full(
            self.view.manager_id
        )

        if len(starting) != 11:
            await interaction.response.send_message(
                "❌ La formazione iniziale non contiene 11 titolari.",
                ephemeral=True
            )
            return

        selection_view = discord.ui.View(timeout=180)
        selection_view.add_item(
            InitialCaptainSelect(
                self.view.manager_id,
                interaction.message
            )
        )

        await interaction.response.send_message(
            "👑 Scegli il capitano tra gli undici titolari.",
            view=selection_view,
            ephemeral=True
        )


class ContinueLaterButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Continua più tardi",
            emoji="🏠",
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction):
        await interaction.response.defer()

        try:
            self.view.stop()

            await interaction.message.edit(
                embed=self.view.embed_builder.build_later(
                    self.view.manager_id
                ),
                view=None
            )

        except Exception as error:
            print(
                "ERRORE PULSANTE CONTINUA PIU TARDI:",
                repr(error)
            )

            await interaction.followup.send(
                "❌ Impossibile chiudere la preparazione: "
                f"`{type(error).__name__}: {error}`",
                ephemeral=True
            )


class ClubPreparationView(ManagerOnlyView):

    def __init__(self, manager_id):
        super().__init__(manager_id)

        self.add_item(ChooseCaptainButton())
        self.add_item(ContinueLaterButton())
