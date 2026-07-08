import discord


class FormationModuleSelect(discord.ui.Select):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        modules = [

            "4-3-3",
            "4-2-3-1",
            "4-4-2",
            "4-1-4-1",
            "3-5-2",
            "3-4-3",
            "5-3-2",
            "5-4-1"

        ]

        options = []

        for module in modules:

            options.append(

                discord.SelectOption(

                    label=module,

                    value=module

                )

            )

        super().__init__(

            placeholder="Seleziona il modulo...",

            min_values=1,

            max_values=1,

            options=options

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        module = self.values[0]

        result = (
            self.view_data.formation_service
            .change_module(

                self.view_data.manager_id,

                module

            )
        )

        if not result["success"]:

            await interaction.followup.send(

                f"❌ {result['error']['message']}",

                ephemeral=True

            )

            return

        embed = (
            self.view_data
            .formation_embed_builder
            .build(
                self.view_data.manager_id
            )
        )

        await self.view_data.message.edit(

            embed=embed,

            view=self.view_data

        )

        await interaction.delete_original_response()

        await interaction.followup.send(

            f"✅ Modulo cambiato in **{module}**.",

            ephemeral=True

        )