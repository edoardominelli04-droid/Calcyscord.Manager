import discord

from ui.roster.roster_buttons import (
    GoalkeepersButton,
    DefendersButton,
    MidfieldersButton,
    AttackersButton,
    SearchPlayerButton,
    BackClubButton
)

from ui.roster.role_view import RoleView


class RosterView(discord.ui.View):

    def __init__(
        self,
        club_service,
        club_embed_builder,
        roster_embed_builder,
        data
    ):

        super().__init__(
            timeout=300
        )

        self.club_service = club_service

        self.club_embed_builder = club_embed_builder

        self.roster_embed_builder = roster_embed_builder

        self.data = data

        self.message = None

        self.add_item(
            GoalkeepersButton(self)
        )

        self.add_item(
            DefendersButton(self)
        )

        self.add_item(
            MidfieldersButton(self)
        )

        self.add_item(
            AttackersButton(self)
        )

        self.add_item(
            SearchPlayerButton(self)
        )

        self.add_item(
            BackClubButton(self)
        )

    async def _open_role(
        self,
        interaction: discord.Interaction,
        role: str
    ):

        players = [

            player

            for player in self.data["players"]

            if player["position"] == role

        ]

        view = RoleView(

            self.roster_embed_builder,

            self.data,

            players,

            role

        )

        await view.show(

            interaction

        )

    async def show_goalkeepers(
        self,
        interaction: discord.Interaction
    ):

        await self._open_role(

            interaction,

            "Goalkeeper"

        )

    async def show_defenders(
        self,
        interaction: discord.Interaction
    ):

        await self._open_role(

            interaction,

            "Defender"

        )

    async def show_midfielders(
        self,
        interaction: discord.Interaction
    ):

        await self._open_role(

            interaction,

            "Midfield"

        )

    async def show_attackers(
        self,
        interaction: discord.Interaction
    ):

        await self._open_role(

            interaction,

            "Attack"

        )