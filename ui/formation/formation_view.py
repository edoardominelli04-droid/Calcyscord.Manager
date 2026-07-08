import discord

from ui.formation.formation_buttons import (
    SchieraButton,
    ModuloButton,
    CapitanoButton,
    RicostruisciButton,
    ClubButton
)


class FormationView(discord.ui.View):
    """
    View principale della schermata Formazione.
    """

    def __init__(
        self,
        manager_id,
        formation,
        formation_service
    ):

        super().__init__(
            timeout=300
        )

        self.manager_id = manager_id
        self.formation = formation
        self.formation_service = formation_service

        self.add_item(
            SchieraButton(self)
        )

        self.add_item(
            ModuloButton(self)
        )

        self.add_item(
            CapitanoButton(self)
        )

        self.add_item(
            RicostruisciButton(self)
        )

        self.add_item(
            ClubButton(self)
        )