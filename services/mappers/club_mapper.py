class ClubMapper:
    """Converte un club Transfermarkt nel formato Calcyscord.Manager."""

    @staticmethod
    def from_transfermarkt(row, internal_id):
        return {
            "id": internal_id,
            "external_id": row["club_id"],
            "code": row["club_code"],
            "name": row["name"],
            "competition_external_id": row["domestic_competition_id"],
            "market_value": row["total_market_value"],
            "squad_size": row["squad_size"],
            "average_age": row["average_age"],
            "foreigners": row["foreigners_number"],
            "foreigners_percentage": row["foreigners_percentage"],
            "national_team_players": row["national_team_players"],
            "stadium_name": row["stadium_name"],
            "stadium_seats": row["stadium_seats"],
            "coach_name": row["coach_name"],
            "last_season": row["last_season"],
            "logo": "",
            "active": True
        }