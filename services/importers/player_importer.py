from services.database_manager import DatabaseManager
from services.mappers.player_mapper import PlayerMapper
from services.normalizers.country_normalizer import CountryNormalizer
from services.providers.transfermarkt_provider import TransfermarktProvider


class PlayerImporter:
    """Importa giocatori mantenendo stabili gli ID interni."""
    def __init__(self): self.db, self.provider = DatabaseManager(), TransfermarktProvider()
    def import_players(self):
        clubs = [c for c in self.db.get_clubs() if c.get("playable", c.get("active"))]
        club_by_tm = {int(c.get("transfermarkt_id", c["external_id"])):c for c in clubs}
        countries = {c["name"].strip().lower():c["id"] for c in self.db.get_countries() if c.get("name")}
        existing = self.db.get_players()
        old_by_tm = {int(p.get("transfermarkt_id", p["external_id"])):p for p in existing}
        next_id = max((int(p["id"]) for p in existing), default=0) + 1
        players = []
        for _, row in self.provider.get_players().iterrows():
            club = club_by_tm.get(int(row["current_club_id"]))
            if club is None: continue
            tm_id = int(row["player_id"]); old = old_by_tm.get(tm_id)
            internal_id = int(old["id"]) if old else next_id
            if old is None: next_id += 1
            player = PlayerMapper.from_transfermarkt(row, internal_id)
            player["transfermarkt_id"] = tm_id
            if old and old.get("provider_ids"): player["provider_ids"] = old["provider_ids"]
            player["club_id"], player["competition_id"] = club["id"], club["competition_id"]
            player["last_season"] = club.get("last_season")
            country = CountryNormalizer.normalize(player.get("country"))
            player["nationality_id"] = countries.get(str(country).strip().lower())
            players.append(player)
        # Mantiene i record storici per non spezzare rose, contratti e
        # statistiche quando un calciatore esce dai campionati supportati.
        imported_tm_ids = {p["transfermarkt_id"] for p in players}
        for old in existing:
            tm_id = int(old.get("transfermarkt_id", old["external_id"]))
            if tm_id in imported_tm_ids:
                continue
            archived = dict(old)
            archived["transfermarkt_id"] = tm_id
            archived["active"] = False
            if archived.get("status") == "available":
                archived["status"] = "archived"
            players.append(archived)
        players.sort(key=lambda player: int(player["id"]))
        self.db.save_players(players); return players
