class CompetitionMapper:
    """Converte una competizione Transfermarkt nel formato Calcyscord.Manager."""

    @staticmethod
    def from_transfermarkt(row, internal_id):
        return {
            "id": internal_id,
            "external_id": row["competition_id"],
            "code": row["competition_code"],
            "name": row["name"],
            "country_name": row["country_name"],
            "country_id": row["country_id"],
            "continent": row["confederation"],
            "type": row["type"],
            "sub_type": row["sub_type"],
            "total_clubs": row["total_clubs"],
            "logo": "",
            "active": True
        }