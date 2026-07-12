class BotNegotiationService:
    """
    Gestisce tutte le decisioni dei club controllati dal sistema.
    """

    def __init__(self):
        pass

    # ==========================================================
    # VALUTAZIONE OFFERTA
    # ==========================================================

    def evaluate_offer(
        self,
        player,
        amount
    ):

        market_value = player.get(
            "market_value",
            0
        )

        if amount >= market_value:

            return {

                "accepted": True,

                "message": (
                    "✅ Il club ha accettato "
                    "l'offerta."
                )

            }

        return {

            "accepted": False,

            "message": (
                "❌ Il club ritiene "
                "l'offerta insufficiente."
            )

        }