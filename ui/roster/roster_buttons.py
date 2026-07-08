import discord


# ==========================================================
# PORTIERI
# ==========================================================

class GoalkeepersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Portieri",

            emoji="🧤",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione portieri in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# DIFENSORI
# ==========================================================

class DefendersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Difensori",

            emoji="🛡",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione difensori in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# CENTROCAMPISTI
# ==========================================================

class MidfieldersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Centrocampisti",

            emoji="⚙️",

            style=discord.ButtonStyle.primary,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione centrocampisti in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# ATTACCANTI
# ==========================================================

class AttackersButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Attaccanti",

            emoji="⚽",

            style=discord.ButtonStyle.primary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Gestione attaccanti in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# CERCA
# ==========================================================

class SearchPlayerButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Cerca",

            emoji="🔍",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Ricerca giocatore in sviluppo.",

            ephemeral=True

        )


# ==========================================================
# TORNA AL CLUB
# ==========================================================

class BackClubButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Club",

            emoji="⬅️",

            style=discord.ButtonStyle.success,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🚧 Ritorno al Club in sviluppo.",

            ephemeral=True

        )