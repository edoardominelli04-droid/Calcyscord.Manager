import discord


class FormationCaptainSelect(discord.ui.Select):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        starting = (
            self.view_data
            .formation_service
            .get_starting_players_full(
                self.view_data.manager_id
            )
        )

        options = []

        for slot, data in starting.items():

            player = data["player"]

            options.append(

                discord.SelectOption(

                    label=player["name"],

                    value=str(
                        player["id"]
                    ),

                    description=slot

                )

            )

        super().__init__(

            placeholder="Seleziona il capitano...",

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

        player_id = int(
            self.values[0]
        )

        result = (
            self.view_data
            .formation_service
            .set_captain(

                self.view_data.manager_id,

                player_id

            )
        )

        if not result["success"]:

            await interaction.followup.send(

                f"❌ {result['error']['message']}",

                ephemeral=True

            )

            return

        player = result["data"]["player"]

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

            f"👑 **{player['name']}** è il nuovo capitano.",

            ephemeral=True

        )