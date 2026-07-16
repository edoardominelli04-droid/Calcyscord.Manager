import discord

from ui.initial_squad.player_list_view import (
    PlayerListView
)


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

        draft = view.service.get_draft(
            view.manager_id
        )

        player_list = PlayerListView(

            manager_id=view.manager_id,

            role=self.role,

            parent_view=view

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

            row=2

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(

            "La conferma sarà disponibile quando la rosa sarà completa.",

            ephemeral=True

        )