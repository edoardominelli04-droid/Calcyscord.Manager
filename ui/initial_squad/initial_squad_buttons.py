import discord


class RoleButton(discord.ui.Button):
    """Pulsante generico per un reparto."""

    def __init__(
        self,
        label,
        emoji,
        role,
        row
    ):

        self.role = role

        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.secondary,
            row=row
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        view = self.view

        player_list = view.open_player_list(
            self.role
        )

        await player_list.show(
            interaction
        )


class GoalkeepersButton(RoleButton):

    def __init__(self):

        super().__init__(

            label="Portieri",

            emoji="🥅",

            role="Goalkeeper",

            row=0

        )


class DefendersButton(RoleButton):

    def __init__(self):

        super().__init__(

            label="Difensori",

            emoji="🛡️",

            role="Defender",

            row=0

        )


class MidfieldersButton(RoleButton):

    def __init__(self):

        super().__init__(

            label="Centrocampisti",

            emoji="🎯",

            role="Midfield",

            row=1

        )


class ForwardsButton(RoleButton):

    def __init__(self):

        super().__init__(

            label="Attaccanti",

            emoji="⚽",

            role="Attack",

            row=1

        )


class ConfirmSquadButton(discord.ui.Button):

    def __init__(self):

        super().__init__(

            label="Conferma rosa",

            emoji="✅",

            style=discord.ButtonStyle.success,

            row=2,

            disabled=True

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "🎉 La conferma della rosa sarà implementata nel prossimo step.",

            ephemeral=True

        )