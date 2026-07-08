import discord

from ui.roster.roster_buttons import (
    GoalkeepersButton,
    DefendersButton,
    MidfieldersButton,
    AttackersButton,
    SearchPlayerButton,
    BackClubButton
)


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