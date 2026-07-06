class CountryMapper:
    """Converte una nazione Transfermarkt nel formato Calcyscord.Manager."""

    @staticmethod
    def from_transfermarkt(row, internal_id):
        return {
            "id": internal_id,
            "external_id": row["country_id"],
            "name": row["country_name"],
            "code": row["country_code"],
            "continent": row["confederation"],
            "total_clubs": row["total_clubs"],
            "total_players": row["total_players"],
            "average_age": row["average_age"],
            "active": True
        }