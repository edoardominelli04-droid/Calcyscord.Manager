import discord


class PurchaseOfferModal(discord.ui.Modal):

    def __init__(
        self,
        view
    ):

        self.view_data = view

        super().__init__(

            title="💰 Offerta di acquisto"

        )

        self.offer_amount = discord.ui.TextInput(

            label="Importo dell'offerta",

            placeholder="Es. 50000000",

            required=True,

            max_length=15

        )

        self.add_item(

            self.offer_amount

        )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        raw_amount = self.offer_amount.value.strip()

        try:

            amount = int(

                raw_amount.replace(".", "").replace(",", "")

            )

        except ValueError:

            await interaction.response.send_message(

                "❌ Inserisci un importo numerico valido.",

                ephemeral=True

            )

            return

        if amount <= 0:

            await interaction.response.send_message(

                "❌ L'offerta deve essere maggiore di zero.",

                ephemeral=True

            )

            return

        await self.view_data.submit_purchase_offer(

            interaction,

            amount

        )