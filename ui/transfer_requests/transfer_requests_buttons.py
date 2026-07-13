import discord


class TransferRequestSelect(discord.ui.Select):

    def __init__(
        self,
        view,
        requests
    ):

        self.view_data = view

        options = []

        for item in requests:

            request = item["request"]

            buyer = item["buyer"]

            player = item["player"]

            options.append(

                discord.SelectOption(

                    label=player["name"][:100],

                    description=(
                        f"{buyer['username']} • "
                        f"€ {request['amount']:,}"
                    ).replace(",", "."),

                    value=str(request["id"])

                )

            )

        if not options:

            options.append(

                discord.SelectOption(

                    label="Nessuna offerta",

                    value="none"

                )

            )

        super().__init__(

            placeholder="Seleziona una trattativa...",

            options=options,

            row=0

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        if self.values[0] == "none":

            await interaction.response.defer()

            return

        await self.view_data.show_request(

            interaction,

            int(self.values[0])

        )


class BackButton(discord.ui.Button):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            label="Mercato",

            emoji="💰",

            style=discord.ButtonStyle.secondary,

            row=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        await self.view_data.show_market(

            interaction

        )