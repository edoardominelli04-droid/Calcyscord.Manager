import re
from datetime import datetime

from services.database_manager import DatabaseManager
from services.game.initial_squad_service import InitialSquadService


class ManagerStatementService:
    """Gestisce la prima dichiarazione del manager dopo la rosa iniziale."""

    MAX_LENGTH = 300

    LINK_PATTERN = re.compile(
        r"(?:https?://|www\.|discord(?:app)?\.com/invite|discord\.gg/)",
        re.IGNORECASE
    )

    MENTION_PATTERN = re.compile(
        r"(?:<@!?\d+>|<@&\d+>|<#\d+>|@everyone|@here)",
        re.IGNORECASE
    )

    def __init__(self):
        self.db = DatabaseManager()
        self.initial_squad_service = InitialSquadService()

    def validate_text(self, text):
        clean_text = " ".join((text or "").split())

        if not clean_text:
            return False, "La dichiarazione non può essere vuota.", None

        if len(clean_text) > self.MAX_LENGTH:
            return (
                False,
                f"La dichiarazione non può superare {self.MAX_LENGTH} caratteri.",
                None
            )

        if self.LINK_PATTERN.search(clean_text):
            return False, "La dichiarazione non può contenere link.", None

        if self.MENTION_PATTERN.search(clean_text):
            return False, "La dichiarazione non può contenere menzioni.", None

        return True, None, clean_text

    def get_current_status(self, manager_id):
        draft = self.initial_squad_service.get_draft(manager_id)

        if draft is None or not draft.get("confirmed"):
            return None

        return draft.get("statement_status", "pending")

    def is_preparation_complete(self, manager_id):
        formation = next(
            (
                item
                for item in self.db.get_formations()
                if item["manager_id"] == manager_id
            ),
            None
        )

        if formation is None:
            return False

        starting = formation.get("starting", {})

        if len(starting) != 11:
            return False

        return any(
            data.get("captain")
            for data in starting.values()
        )

    def can_complete(self, manager_id):
        status = self.get_current_status(manager_id)

        if status is None:
            return False, "La rosa iniziale non è stata ancora confermata."

        if status == "published":
            return False, "La dichiarazione è già stata pubblicata."

        if status == "skipped":
            return False, "La presentazione del manager è già stata completata."

        return True, None

    def _complete(
        self,
        manager_id,
        status,
        channel_id,
        message_id,
        text=None
    ):
        allowed, error = self.can_complete(manager_id)

        if not allowed:
            return False, error

        draft = self.initial_squad_service.get_draft(manager_id)
        manager = self.db.get_manager_by_id(manager_id)
        club = self.db.get_club_by_id(draft["club_id"])

        if manager is None or club is None:
            return False, "Manager o club non trovato."

        records = self.db.get_manager_statements()

        record = {
            "id": max(
                (item.get("id", 0) for item in records),
                default=0
            ) + 1,
            "manager_id": manager_id,
            "discord_id": str(manager["discord_id"]),
            "manager_name": manager["username"],
            "club_id": club["id"],
            "club_name": club["name"],
            "status": status,
            "text": text,
            "channel_id": str(channel_id),
            "message_id": str(message_id),
            "published_at": datetime.now().isoformat()
        }

        records.append(record)
        self.db.save_manager_statements(records)

        draft["statement_status"] = status
        draft["statement_completed_at"] = record["published_at"]
        draft["statement_record_id"] = record["id"]
        self.initial_squad_service.save(draft)

        return True, record

    def publish(
        self,
        manager_id,
        text,
        channel_id,
        message_id
    ):
        valid, error, clean_text = self.validate_text(text)

        if not valid:
            return False, error

        return self._complete(
            manager_id=manager_id,
            status="published",
            channel_id=channel_id,
            message_id=message_id,
            text=clean_text
        )

    def skip(
        self,
        manager_id,
        channel_id,
        message_id
    ):
        return self._complete(
            manager_id=manager_id,
            status="skipped",
            channel_id=channel_id,
            message_id=message_id
        )
