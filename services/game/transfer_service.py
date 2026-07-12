from services.database_manager import DatabaseManager
from services.game.finance_service import FinanceService
from services.game.contract_service import ContractService
from services.game.formation_service import FormationService


class TransferService:
    """
    Gestisce l'esecuzione dei trasferimenti.

    Si occupa esclusivamente di aggiornare i dati del gioco
    dopo che una trattativa è stata accettata.
    """

    def __init__(
        self
    ):

        self.db = DatabaseManager()

        self.finance_service = FinanceService()

        self.contract_service = ContractService()

        self.formation_service = FormationService()

    # ==========================================================
    # TRASFERIMENTO DEFINITIVO
    # ==========================================================

    def execute_transfer(
        self,
        buyer_manager_id,
        seller_manager_id,
        player_id,
        amount
    ):

        # ==========================================
        # AGGIORNA LE FINANZE
        # ==========================================

        self.finance_service.transfer_money(

            buyer_manager_id,

            seller_manager_id,

            amount

        )

        squads = self.db.get_squads()

        # ==========================================
        # RIMUOVE IL GIOCATORE DALLA VECCHIA ROSA
        # ==========================================

        if seller_manager_id is not None:

            squads = [

                member

                for member in squads

                if not (

                    member["manager_id"] == seller_manager_id

                    and

                    member["player_id"] == player_id

                )

            ]

        # ==========================================
        # RECUPERA IL NUOVO MANAGER
        # ==========================================

        buyer = self.db.get_manager_by_id(

            buyer_manager_id

        )

        if buyer is None:

            return {

                "success": False,

                "message": "❌ Manager acquirente non trovato."

            }

        # ==========================================
        # CREA IL NUOVO CONTRATTO
        # ==========================================

        player = self.db.get_player_by_id(

            player_id

        )

        contract = self.contract_service.create_transfer_contract(

            player,

            buyer_manager_id,

            amount

        )

        # ==========================================
        # AGGIUNGE IL GIOCATORE ALLA NUOVA ROSA
        # ==========================================

        squads.append(

            {

                "manager_id": buyer_manager_id,

                "club_id": buyer["club_id"],

                "player_id": player_id,

                "contract_id": contract["id"],

                "status": "active"

            }

        )

        # ==========================================
        # SALVA LA ROSA
        # ==========================================

        self.db.save_squads(

            squads

        )

        self.formation_service.refresh_formation(
            buyer_manager_id
        )

        if seller_manager_id is not None:

            self.formation_service.refresh_formation(
                seller_manager_id
            )

        # ==========================================
        # RISULTATO
        # ==========================================

        return {

            "success": True,

            "message": "✅ Trasferimento completato con successo."

        }