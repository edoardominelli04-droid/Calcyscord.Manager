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

        view = self.view

        await interaction.response.defer()

        confirmed, message = view.service.confirm_squad(
            view.manager_id
        )

        if not confirmed:

            await interaction.followup.send(
                f"❌ {message}",
                ephemeral=True
            )

            return

        draft = view.service.get_draft(
            view.manager_id
        )

        counts = view.service.get_role_counts(
            view.manager_id
        )

        view._update_buttons()

        embed = view.embed_builder.build_home(
            draft,
            counts
        )

        from ui.initial_squad.manager_statement_view import (
            ManagerStatementView
        )

        statement_view = ManagerStatementView(
            view.manager_id
        )

        # Arresta esplicitamente la vecchia InitialSquadView:
        # in questo modo Discord non puo ripubblicare i pulsanti dei reparti
        # dopo che la rosa e stata confermata.
        view.stop()

        message = interaction.message

        if message is not None:

            await message.edit(
                embed=embed,
                view=statement_view
            )

            statement_view.message = message

        else:

            await interaction.edit_original_response(
                embed=embed,
                view=statement_view
            )

            statement_view.message = await interaction.original_response()
