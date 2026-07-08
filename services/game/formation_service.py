from services.database_manager import DatabaseManager
from services.game.module_service import ModuleService
from services.game.data.position_rules import POSITION_RULES
from services.utils.slot_utils import SlotUtils
from services.game.constants.errors import *


class FormationService:
    """Gestisce le formazioni dei manager."""

    def __init__(self):
        self.db = DatabaseManager()
        self.module_service = ModuleService()

    # ==========================================================
    # DATABASE
    # ==========================================================

    def get_all(self):
        return self.db.get_formations()

    def save_all(self, formations):
        self.db.save_formations(formations)

    # ==========================================================
    # GET
    # ==========================================================

    def get_manager_formation(self, manager_id):

        for formation in self.get_all():

            if formation["manager_id"] == manager_id:
                return formation

        return None
    
    # ==========================================================
    # BUILD FORMAZIONE
    # ==========================================================

    def _build_formation(
        self,
        manager_id,
        module_name
    ):

        slots = self.module_service.get_slots(
            module_name
        )

        squad = [

            player

            for player in self.db.get_squads()

            if player["manager_id"] == manager_id

        ]

        players = []

        for squad_player in squad:

            player = self.db.get_player_by_id(
                squad_player["player_id"]
            )

            if player is not None:
                players.append(player)

        starting = {}

        used_players = set()

        for slot in slots:

            family = SlotUtils.family(slot)

            wanted_positions = POSITION_RULES[
                family
            ]

            selected = None

            # ==========================================
            # Cerca prima il sottoruolo ideale
            # ==========================================

            for player in players:

                if player["id"] in used_players:
                    continue

                if (
                    player.get("sub_position")
                    in wanted_positions
                ):
                    selected = player
                    break

            # ==========================================
            # Fallback sul ruolo principale
            # ==========================================

            if selected is None:

                category = SlotUtils.department(
                    slot
                )

                for player in players:

                    if player["id"] in used_players:
                        continue

                    if (
                        player.get("position")
                        == category
                    ):
                        selected = player
                        break

            if selected is None:
                continue

            starting[slot] = {

                "player_id": selected["id"],

                "captain": False,

                "vice_captain": False

            }

            used_players.add(
                selected["id"]
            )

        bench = []

        for player in players:

            if player["id"] not in used_players:

                bench.append(
                    player["id"]
                )

        return {

            "manager_id": manager_id,

            "module": module_name,

            "starting": starting,

            "bench": bench

        }

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_starting_slot_by_player(
        self,
        formation,
        player_id
    ):
        """
        Restituisce lo slot occupato dal giocatore.
        Se non è titolare restituisce None.
        """

        for slot, data in formation["starting"].items():

            if data["player_id"] == player_id:
                return slot

        return None

    def _get_bench_player(
        self,
        formation,
        player_id
    ):
        """
        Verifica se il giocatore è in panchina.
        Restituisce il player_id oppure None.
        """

        for bench_player in formation["bench"]:

            if bench_player == player_id:
                return bench_player

        return None

    def _validate_slot(
        self,
        formation,
        slot
    ):
        """
        Verifica che lo slot esista nella formazione.
        """

        if slot not in formation["starting"]:

            return self._error(
                INVALID_SLOT,
                "Lo slot selezionato non esiste."
            )

        return self._success(
            {
                "slot": slot
            }
        )

    def _validate_player(
            self,
            manager_id,
            player_id
        ):
            """
            Verifica che il giocatore esista e
            appartenga alla rosa del manager.
            """

            player = self.db.get_player_by_id(
                player_id
            )

            if player is None:

                return self._error(
                    PLAYER_NOT_FOUND,
                    "Giocatore non trovato."
                )

            squad = self.db.get_squads()

            found = False

            for squad_player in squad:

                if (
                    squad_player["manager_id"] == manager_id
                    and
                    squad_player["player_id"] == player_id
                ):

                    found = True
                    break

            if not found:

                return self._error(
                    PLAYER_NOT_IN_SQUAD,
                    "Il giocatore non appartiene alla tua rosa."
                )

            return self._success(
                {
                    "player": player
                }
            )

    def _is_player_compatible(
        self,
        slot,
        player
    ):
        """
        Verifica se un giocatore può occupare
        lo slot richiesto.
        """

        family = SlotUtils.family(
            slot
        )

        wanted_positions = POSITION_RULES.get(
            family,
            []
        )

        if (
            player.get("sub_position")
            in wanted_positions
        ):

            return self._success(
                {
                    "compatible": True
                }
            )

        category = SlotUtils.department(
            slot
        )

        if (
            player.get("position")
            == category
        ):

            return self._success(
                {
                    "compatible": True
                }
            )

        return self._error(
            INCOMPATIBLE_POSITION,
            "Il ruolo del giocatore non è compatibile con lo slot selezionato."
        )

    def _save_formation(
        self,
        formation
    ):
        """
        Salva la formazione aggiornata.
        """

        formations = self.get_all()

        for i, current in enumerate(formations):

            if (
                current["manager_id"]
                == formation["manager_id"]
            ):

                formations[i] = formation

                self.save_all(
                    formations
                )

                return self._success(
                    {
                        "formation": formation
                    }
                )

        return self._error(
            SAVE_ERROR,
            "Impossibile salvare la formazione."
        )

    def _success(
        self,
        data
    ):

        return {

            "success": True,

            "data": data

        }

    def _error(
        self,
        code,
        message
    ):

        return {

            "success": False,

            "error": {

                "code": code,

                "message": message

            }

        }

    # ==========================================================
    # CREAZIONE FORMAZIONE
    # ==========================================================

    def create_initial_formation(
        self,
        manager_id,
        module_name=None
    ):

        if self.get_manager_formation(manager_id):
            raise ValueError(
                "La formazione esiste già."
            )

        if module_name is None:
            module_name = (
                self.module_service.DEFAULT_MODULE
            )

        formation = self._build_formation(
            manager_id,
            module_name
        )

        formations = self.get_all()

        formations.append(
            formation
        )

        self.save_all(
            formations
        )

        return formation

    # ==========================================================
    # STARTING
    # ==========================================================

    def get_starting_players(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return {}

        return formation["starting"]

    # ==========================================================
    # PANCHINA
    # ==========================================================

    def get_bench_players(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return []

        return formation["bench"]

    # ==========================================================
    # CREAZIONE FORMAZIONE
    # ==========================================================

    def create_initial_formation(
        self,
        manager_id,
        module_name=None
    ):

        if self.get_manager_formation(manager_id):
            raise ValueError(
                "La formazione esiste già."
            )

        if module_name is None:
            module_name = (
                self.module_service.DEFAULT_MODULE
            )

        formation = self._build_formation(
            manager_id,
            module_name
        )

        formations = self.get_all()

        formations.append(
            formation
        )

        self.save_all(
            formations
        )

        return formation

    # ==========================================================
    # CAMBIO MODULO
    # ==========================================================

    def change_module(
        self,
        manager_id,
        module_name
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:

            return self._error(
                FORMATION_NOT_FOUND,
                "Formazione non trovata."
            )

        if formation["module"] == module_name:

            return self._error(
                INVALID_OPERATION,
                "Hai già questo modulo."
            )

        formation["module"] = module_name

        result = self._save_formation(
            formation
        )

        if not result["success"]:
            return result

        return self._success(

            {

                "formation": formation,

                "module": module_name

            }

        )
    
    # ==========================================================
    # CAPITANO
    # ==========================================================

    def set_captain(
        self,
        manager_id,
        player_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:

            return self._error(
                FORMATION_NOT_FOUND,
                "Formazione non trovata."
            )

        result = self._validate_player(
            manager_id,
            player_id
        )

        if not result["success"]:
            return result

        player = result["data"]["player"]

        found = False

        for slot, data in formation["starting"].items():

            data["captain"] = False

            if data["player_id"] == player_id:

                data["captain"] = True

                found = True

        if not found:

            return self._error(
                PLAYER_ALREADY_STARTER,
                "Il giocatore non è titolare."
            )

        result = self._save_formation(
            formation
        )

        if not result["success"]:
            return result

        return self._success(

            {

                "formation": formation,

                "player": player

            }

        )

    # ==========================================================
    # SCHIERA GIOCATORE
    # ==========================================================

    def swap_player(
        self,
        manager_id,
        slot,
        player_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:

            return self._error(
                FORMATION_NOT_FOUND,
                "Formazione non trovata."
            )

        # ==========================================
        # Verifica slot
        # ==========================================

        result = self._validate_slot(
            formation,
            slot
        )

        if not result["success"]:
            return result

        # ==========================================
        # Verifica giocatore
        # ==========================================

        result = self._validate_player(
            manager_id,
            player_id
        )

        if not result["success"]:
            return result

        player = result["data"]["player"]

        # ==========================================
        # Verifica che non sia già titolare
        # ==========================================

        starter_slot = self._get_starting_slot_by_player(
            formation,
            player_id
        )

        if starter_slot is not None:

            return self._error(
                PLAYER_ALREADY_STARTER,
                "Il giocatore è già titolare."
            )

        # ==========================================
        # Compatibilità ruolo
        # ==========================================

        result = self._is_player_compatible(
            slot,
            player
        )

        if not result["success"]:
            return result

        # ==========================================
        # Recupera il vecchio titolare
        # ==========================================

        old_player_id = (
            formation["starting"][slot]["player_id"]
        )

        old_player = self.db.get_player_by_id(
            old_player_id
        )

        # ==========================================
        # Aggiorna la panchina
        # ==========================================

        formation["bench"].remove(
            player_id
        )

        formation["bench"].append(
            old_player_id
        )

        # ==========================================
        # Inserisce il nuovo titolare
        # ==========================================

        formation["starting"][slot][
            "player_id"
        ] = player_id

        # ==========================================
        # Salvataggio
        # ==========================================

        result = self._save_formation(
            formation
        )

        if not result["success"]:
            return result

        # ==========================================
        # Successo
        # ==========================================

        return self._success(

            {

                "slot": slot,

                "old_player": old_player,

                "new_player": player,

                "formation": formation

            }

        )
    
    # ==========================================================
    # GIOCATORI COMPATIBILI
    # ==========================================================

    def get_compatible_bench_players(
        self,
        manager_id,
        slot
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:

            return self._error(
                FORMATION_NOT_FOUND,
                "Formazione non trovata."
            )

        players = []

        for player_id in formation["bench"]:

            player = self.db.get_player_by_id(
                player_id
            )

            if player is None:
                continue

            result = self._is_player_compatible(
                slot,
                player
            )

            if result["success"]:

                players.append(
                    player
                )

        return self._success(

            {

                "players": players

            }

        )

    # ==========================================================
    # SLOT
    # ==========================================================

    def get_slot_player(
        self,
        manager_id,
        slot
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return None

        return formation["starting"].get(slot)

    def set_slot_player(
        self,
        manager_id,
        slot,
        player_id
    ):

        formations = self.get_all()

        for formation in formations:

            if formation["manager_id"] != manager_id:
                continue

            formation["starting"][slot] = {

                "player_id": player_id,

                "captain": False,

                "vice_captain": False

            }

            self.save_all(
                formations
            )

            return formation

        return None
    
    # ==========================================================
    # PLAYER HELPERS
    # ==========================================================

    def get_starting_players_full(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return {}

        players = {}

        for slot, data in formation["starting"].items():

            player = self.db.get_player_by_id(
                data["player_id"]
            )

            if player is None:
                continue

            players[slot] = {
                "player": player,
                "captain": data["captain"],
                "vice_captain": data["vice_captain"]
            }

        return players

    def get_bench_players_full(
        self,
        manager_id
    ):

        formation = self.get_manager_formation(
            manager_id
        )

        if formation is None:
            return []

        bench = []

        for player_id in formation["bench"]:

            player = self.db.get_player_by_id(
                player_id
            )

            if player is not None:
                bench.append(player)

        return bench