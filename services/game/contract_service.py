import math
from datetime import datetime
from services.database_manager import DatabaseManager


class ContractService:
    """Gestisce i contratti dei giocatori."""

    DEFAULT_DURATION = 3

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.get_contracts()

    def save_all(self, contracts):
        self.db.save_contracts(contracts)

    def get_by_player(self, player_id):

        for contract in self.get_all():

            if contract["player_id"] == player_id:
                return contract

        return None

    def create_contract(self, player, manager_id):

        contracts = self.get_all()

        if self.get_by_player(player["id"]):
            return None

        market_value = player.get("market_value", 0)

        if market_value is None:

            market_value = 0

        elif isinstance(market_value, float) and math.isnan(market_value):

            market_value = 0

        salary = max(

            50000,

            int(market_value * 0.08)

        )

        current_year = datetime.now().year
        current_datetime = datetime.now().isoformat()

        contract = {
            "id": max(
                (
                    contract["id"]
                    for contract in contracts
                ),
                default=0
            ) + 1,

            "player_id": player["id"],
            "manager_id": manager_id,

            # ==========================
            # Tipo contratto
            # ==========================

            "type": "professional",
            "is_loan": False,

            # ==========================
            # Date
            # ==========================

            "signed_at": current_datetime,
            "expires_at": None,

            "start_season": current_year,
            "end_season": current_year + self.DEFAULT_DURATION,

            # ==========================
            # Economico
            # ==========================

            "salary": salary,
            "transfer_fee": 0,
            "release_clause": None,


            # ==========================
            # Provenienza
            # ==========================

            "origin_club_id": player["club_id"],
            "contract_version": 1,
            "contract_notes": None,

            # ==========================
            # Stato
            # ==========================

            "renewable": True,
            "status": "active"
        }

        contracts.append(contract)

        self.save_all(contracts)

        return contract
    
    def create_transfer_contract(
        self,
        player,
        manager_id,
        transfer_fee
    ):

        contracts = self.get_all()

        current = self.get_by_player(

            player["id"]

        )

        if current is not None:

            current["status"] = "expired"

        market_value = player.get("market_value", 0)

        if market_value is None:

            market_value = 0

        elif isinstance(market_value, float) and math.isnan(market_value):

            market_value = 0

        salary = max(

            50000,

            int(market_value * 0.08)

        )

        current_year = datetime.now().year

        current_datetime = datetime.now().isoformat()

        contract = {

            "id": max(
                (
                    contract["id"]
                    for contract in contracts
                ),
                default=0
            ) + 1,

            "player_id": player["id"],

            "manager_id": manager_id,

            "type": "professional",

            "is_loan": False,

            "signed_at": current_datetime,

            "expires_at": None,

            "start_season": current_year,

            "end_season": current_year + self.DEFAULT_DURATION,

            "salary": salary,

            "transfer_fee": transfer_fee,

            "release_clause": None,

            "origin_club_id": player["club_id"],

            "contract_version": (

                current["contract_version"] + 1

                if current else 1

            ),

            "contract_notes": None,

            "renewable": True,

            "status": "active"

        }

        contracts.append(

            contract

        )

        self.save_all(

            contracts

        )

        return contract