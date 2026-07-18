from services.identity.club_identity_service import ClubIdentityService


class ClubMapper:
    @staticmethod
    def from_providers(row, team, internal_id):
        return {"id":internal_id,"external_id":int(row["club_id"]),"transfermarkt_id":int(row["club_id"]),"football_data_id":int(team["id"]),"code":row["club_code"],"name":ClubIdentityService.public_name(team),"official_name":row["name"],"aliases":ClubIdentityService.aliases(row,team),"football_data_name":team.get("name"),"football_data_tla":team.get("tla"),"competition_external_id":row["domestic_competition_id"],"market_value":row["total_market_value"],"squad_size":row["squad_size"],"average_age":row["average_age"],"foreigners":row["foreigners_number"],"foreigners_percentage":row["foreigners_percentage"],"national_team_players":row["national_team_players"],"stadium_name":row["stadium_name"],"stadium_seats":row["stadium_seats"],"coach_name":row["coach_name"],"last_season":int(row["last_season"]),"logo":team.get("crest") or "","active":True,"playable":True}
