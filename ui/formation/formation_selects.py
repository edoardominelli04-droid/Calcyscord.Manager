import asyncio
import discord


class FormationSlotSelect(discord.ui.Select):
    """
    Menu per la scelta dello slot da modificare.
    """

    def __init__(
        self,
        view
    ):

        self.view_data = view

        options = []

        for slot in view.formation["starting"].keys():

            options.append(

                discord.SelectOption(

                    label=slot,

                    value=slot

                )

            )

        super().__init__(

            placeholder="Seleziona lo slot da modificare...",

            min_values=1,

            max_values=1,

            options=options

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        slot = self.values[0]

        self.view_data.selected_slot = slot

        view = discord.ui.View(
            timeout=120
        )

        view.add_item(
            FormationPlayerSelect(
                self.view_data
            )
        )

        await interaction.response.send_message(

            f"⚽ Slot selezionato: **{slot}**.\n"
            "Ora scegli il giocatore.",

            view=view,

            ephemeral=True

        )


class FormationPlayerSelect(discord.ui.Select):
    """
    Menu per la scelta del nuovo titolare.
    Mostra solo i giocatori compatibili presenti in panchina.
    """

    def __init__(
        self,
        view
    ):

        self.view_data = view

        result = (
            self.view_data.formation_service
            .get_compatible_bench_players(
                self.view_data.manager_id,
                self.view_data.selected_slot
            )
        )

        options = []

        if result["success"]:

            for player in result["data"]["players"]:

                role = player.get(
                    "sub_position",
                    "-"
                )

                options.append(

                    discord.SelectOption(

                        label=player["name"],

                        value=str(
                            player["id"]
                        ),

                        description=role

                    )

                )

        if not options:

            options.append(

                discord.SelectOption(

                    label="Nessun giocatore compatibile",

                    value="none"

                )

            )

        super().__init__(

            placeholder="Seleziona il giocatore...",

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

        player_id = self.values[0]

        if player_id == "none":

            await interaction.followup.send(

                "❌ Nessun giocatore compatibile.",

                ephemeral=True

            )

            return

        result = (
            self.view_data.formation_service
            .swap_player(

                self.view_data.manager_id,

                self.view_data.selected_slot,

                int(player_id)

            )
        )

        if not result["success"]:

            await interaction.followup.send(

                f"❌ {result['error']['message']}",

                ephemeral=True

            )

            return

        data = result["data"]

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

        msg = await interaction.followup.send(

            "✅ "
            f"{data['new_player']['name']} "
            "sostituisce "
            f"{data['old_player']['name']} "
            f"nel ruolo **{data['slot']}**.",

            ephemeral=True,

            wait=True

        )

        await asyncio.sleep(10)

        await msg.delete()