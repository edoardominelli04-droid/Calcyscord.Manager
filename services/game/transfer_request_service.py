from datetime import datetime

from services.database_manager import DatabaseManager
from services.game.transfer_service import TransferService
from services.game.club_service import ClubService
from constants.transfer_request_status import (
    PENDING,
    ACCEPTED,
    REJECTED,
    CANCELLED,
    EXPIRED
)

class TransferRequestService:
    """Gestisce le richieste di trasferimento tra manager."""

    def __init__(self):

        self.db = DatabaseManager()

        self.transfer_service = TransferService()

        self.club_service = ClubService()

    # ==========================================================
    # DATABASE
    # ==========================================================

    def get_all(self):

        return self.db.get_transfer_requests()

    def save_all(
        self,
        requests
    ):

        self.db.save_transfer_requests(
            requests
        )

    # ==========================================================
    # CREAZIONE
    # ==========================================================

    def create_request(
        self,
        buyer_manager_id,
        seller_manager_id,
        player_id,
        amount
    ):

        requests = self.get_all()

        request = {

            "id": len(requests) + 1,

            "buyer_manager_id": buyer_manager_id,

            "seller_manager_id": seller_manager_id,

            "player_id": player_id,

            "amount": amount,

            "created_at": datetime.utcnow().isoformat(),

            "status": PENDING

        }

        requests.append(
            request
        )

        self.save_all(
            requests
        )

        return request

    # ==========================================================
    # RICERCA
    # ==========================================================

    def get_request(
        self,
        request_id
    ):

        for request in self.get_all():

            if request["id"] == request_id:

                return request

        return None

    def get_manager_requests(
        self,
        manager_id
    ):

        return [

            request

            for request in self.get_all()

            if (

                request["seller_manager_id"]

                == manager_id

                and

                request["status"] == "pending"

            )

        ]
    
    def get_manager_requests_details(
        self,
        manager_id
    ):

        requests = self.get_manager_requests(

            manager_id

        )

        details = []

        for request in requests:

            buyer = self.db.get_manager_by_id(

                request["buyer_manager_id"]

            )

            seller = self.db.get_manager_by_id(

                request["seller_manager_id"]

            )

            player = self.db.get_player_by_id(
   
                request["player_id"]

            )

            details.append(

                {

                    "request": request,

                    "buyer": buyer,

                    "seller": seller,

                    "player": player

                }

            )

        return sorted(

            details,

            key=lambda item: item["request"]["amount"],

            reverse=True

        )
    
    def get_player_requests(
        self,
        player_id,
        only_pending=True
    ):

        requests = [

            request

            for request in self.get_all()

            if request["player_id"] == player_id

        ]

        if only_pending:

            requests = [

                request

                for request in requests

                if request["status"] == PENDING

            ]

        return sorted(

            requests,

            key=lambda request: request["amount"],

            reverse=True

        )

    # ==========================================================
    # STATO
    # ==========================================================

    def save(
        self,
        request
    ):

        requests = self.get_all()

        for i, current in enumerate(requests):

            if current["id"] == request["id"]:

                requests[i] = request

                break

        self.save_all(
            requests
        )

    def accept_request(
        self,
        request_id
    ):

        request = self.get_request(
            request_id
        )

        if request is None:

            return {

                "success": False,

                "message": "Richiesta non trovata."

            }

        if request["status"] != PENDING:

            return {

                "success": False,

                "message": "La richiesta non è più valida."

            }
        
        owner = self.club_service.get_player_owner(

            request["player_id"]

        )

        if owner is None:

            return {

                "success": False,

                "message": "Impossibile verificare il proprietario."

            }

        if (

            owner["manager"] is None

            or

            owner["manager"]["id"] != request["seller_manager_id"]

        ):

            request["status"] = CANCELLED

            self.save(

                request

            )

            return {

                "success": False,

                "message": (

                    "La richiesta è stata annullata "

                    "perché il giocatore ha cambiato squadra."

                )

            }

        result = self.transfer_service.execute_transfer(

            request["buyer_manager_id"],

            request["seller_manager_id"],

            request["player_id"],

            request["amount"]

        )

        if not result["success"]:

            return result

        request["status"] = ACCEPTED

        self.save(
            request
        )

        self.cancel_other_requests(

            request["player_id"],

            request["id"]

        )

        return {

            "success": True,

            "message": "Trasferimento completato.",

            "request": request

        }

    def reject_request(
        self,
        request_id
    ):

        request = self.get_request(
            request_id
        )

        if request is None:

            return {

                "success": False,

                "message": "Richiesta non trovata."

            }

        if request["status"] != PENDING:

            return {

                "success": False,

                "message": "La richiesta non è più valida."

            }

        request["status"] = REJECTED

        self.save(
            request
        )

        return {

            "success": True,

            "message": "Richiesta rifiutata.",

            "request": request

        }
    
    # ==========================================================
    # ANNULLA ALTRE OFFERTE
    # ==========================================================

    def cancel_other_requests(
        self,
        player_id,
        accepted_request_id
    ):

        requests = self.get_all()

        changed = False

        for request in requests:

            if request["id"] == accepted_request_id:
                continue

            if request["player_id"] != player_id:
                continue

            if request["status"] != PENDING:
                continue

            request["status"] = CANCELLED

            changed = True

        if changed:

            self.save_all(

                requests

            )