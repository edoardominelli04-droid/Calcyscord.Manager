class StadiumMapper:
    """Converte uno stadio Transfermarkt nel formato Calcyscord.Manager."""

    @staticmethod
    def from_transfermarkt(club, internal_id):
        return {
            "id": internal_id,
            "external_id": None,
            "name": club["stadium_name"],
            "club_external_id": club["club_id"],
            "capacity": club["stadium_seats"],
            "photo": "",
            "active": True
        }