from services.database_manager import DatabaseManager
from services.game.finance_service import FinanceService
from services.game.club_service import ClubService
from services.game.bot_negotiation_service import BotNegotiationService
from services.game.transfer_service import TransferService
from services.game.transfer_request_service import TransferRequestService


class MarketService:
    """
    Gestisce tutte le operazioni di mercato di Calcyscord.Manager.

    - offerte di acquisto
    - prestiti
    - vendite al bot
    - trasferimenti tra manager
    - aste
    - controlli finestre di mercato
    - negoziazione automatica dei club gestiti dal sistema
    """

    def __init__(
        self
    ):

        self.db = DatabaseManager()

        self.finance_service = FinanceService()

        self.club_service = ClubService()

        self.bot_negotiation_service = BotNegotiationService()

        self.transfer_service = TransferService()

        self.transfer_request_service = TransferRequestService()

    # ==========================================================
    # ACQUISTO
    # ==========================================================

    def submit_offer(
        self,
        buyer_manager_id,
        player_id,
        amount
    ):

        # ==========================================
        # OFFERTA VALIDA
        # ==========================================

        if amount <= 0:

            return {

                "success": False,

                "message": "❌ L'offerta deve essere maggiore di zero."

            }

        # ==========================================
        # GIOCATORE ESISTE
        # ==========================================

        player = self.db.get_player_by_id(

            player_id

        )

        if player is None:

            return {

                "success": False,

                "message": "❌ Giocatore non trovato."

            }

        # ==========================================
        # GIOCATORE GIÀ IN ROSA
        # ==========================================

        if self.club_service.is_player_owned_by_manager(

            buyer_manager_id,

            player_id

        ):

            return {

                "success": False,

                "message": "❌ Il giocatore appartiene già alla tua rosa."

            }

        # ==========================================
        # BUDGET
        # ==========================================

        finance = self.finance_service.get_finance(

            buyer_manager_id

        )

        if finance is None:

            return {

                "success": False,

                "message": "❌ Dati finanziari non trovati."

            }

        if amount > finance["transfer_budget"]:

            return {

                "success": False,

                "message": "❌ Budget trasferimenti insufficiente."

            }
        
        # ==========================================
        # PROPRIETARIO
        # ==========================================

        owner = self.club_service.get_player_owner(

            player_id

        )

        if owner is None:

            return {

                "success": False,

                "message": "❌ Impossibile determinare il proprietario."

            }

        # ==========================================
        # CLUB GESTITO DAL BOT
        # ==========================================

        if owner["manager"] is None:

            negotiation = self.bot_negotiation_service.evaluate_offer(

                player,

                amount

            )

            if not negotiation["accepted"]:

                return {

                    "success": False,

                    "message": negotiation["message"]

                }

            return self.transfer_service.execute_transfer(

                buyer_manager_id,

                None,

                player_id,

                amount

            )

        # ==========================================
        # CLUB GESTITO DA UN MANAGER
        # ==========================================

        request = self.transfer_request_service.create_request(

            buyer_manager_id,

            owner["manager"]["id"],

            player_id,

            amount

        )

        return {

            "success": True,

            "message": (

                "📨 Offerta inviata al manager proprietario.\n"

                f"Richiesta #{request['id']} creata."

            )

        }
    
    # ==========================================================
    # PRESTITO
    # ==========================================================

    def submit_loan(
        self,
        buyer_manager_id,
        player_id
    ):

        return {

            "success": True,

            "message": "🚧 Logica prestiti in sviluppo."

        }

    # ==========================================================
    # VENDITA AL BOT
    # ==========================================================

    def sell_to_bot(
        self,
        manager_id,
        player_id
    ):

        return {

            "success": True,

            "message": "🚧 Vendita al bot in sviluppo."

        }

    # ==========================================================
    # MESSA IN VENDITA
    # ==========================================================

    def list_for_transfer(
        self,
        manager_id,
        player_id
    ):

        return {

            "success": True,

            "message": "🚧 Messa sul mercato in sviluppo."

        }