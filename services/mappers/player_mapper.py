class PlayerMapper:
    """Converte un giocatore Transfermarkt nel formato Calcyscord.Manager."""

    @staticmethod
    def from_transfermarkt(row, internal_id):
        return {
            "id": internal_id,
            "external_id": row["player_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "name": row["name"],
            "player_code": row["player_code"],
            "club_external_id": row["current_club_id"],
            "competition_external_id": row["current_club_domestic_competition_id"],
            "country": row["country_of_citizenship"],
            "country_of_birth": row["country_of_birth"],
            "city_of_birth": row["city_of_birth"],
            "date_of_birth": row["date_of_birth"],
            "position": row["position"],
            "sub_position": row["sub_position"],
            "preferred_foot": row["foot"],
            "height_cm": row["height_in_cm"],
            "contract_until": row["contract_expiration_date"],
            "market_value": row["market_value_in_eur"],
            "highest_market_value": row["highest_market_value_in_eur"],
            "national_team_id": row["current_national_team_id"],
            "image": row["image_url"],
            "status": "available",
            "active": True
        }