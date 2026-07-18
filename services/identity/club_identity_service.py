import re
import unicodedata
from difflib import SequenceMatcher


class ClubIdentityError(RuntimeError):
    pass


class ClubIdentityService:
    """Collega club di provider diversi senza usare il nome come ID persistente."""
    NOISE = {
        "club", "football", "calcio", "fc", "cf", "afc", "sc", "ac",
        "ss", "as", "rcd", "futbol", "fussball", "futebol",
        "association", "societa", "sportiva", "reial", "real", "deportiu",
        "deportivo", "esportiu", "spa", "sad", "de", "del", "da", "do",
        "the", "1900", "1899"
    }
    TOKEN_ALIASES = {
        "rasenballsport": "rb",
    }
    PHRASE_ALIASES = {
        "vitoria sport clube": "vitoria sc",
    }

    @classmethod
    def normalize(cls, value):
        value = unicodedata.normalize("NFKD", str(value or ""))
        value = "".join(c for c in value if not unicodedata.combining(c))
        return " ".join(re.findall(r"[a-z0-9]+", value.lower()))

    @classmethod
    def compact(cls, value):
        # Elimina anche i frammenti di sigle societarie come S.p.A. -> s p a.
        # Altrimenti club diversi condividono artificialmente la stringa "s p a".
        normalized = cls.normalize(value)
        normalized = cls.PHRASE_ALIASES.get(normalized, normalized)
        tokens = []
        for token in normalized.split():
            token = cls.TOKEN_ALIASES.get(token, token)
            if token not in cls.NOISE and len(token) > 1:
                tokens.append(token)
        return " ".join(tokens)

    @classmethod
    def names(cls, team):
        return {v for v in (team.get("name"), team.get("shortName"), team.get("tla")) if v}

    @classmethod
    def score(cls, club, team):
        left = {club.get("name"), club.get("club_code")}
        left.update(club.get("aliases", []))
        scores = []
        for a0 in filter(None, left):
            for b0 in cls.names(team):
                a, b = cls.compact(a0), cls.compact(b0)
                if not a or not b:
                    continue
                scores.append(1.0 if a == b else 0.94 if a in b or b in a else SequenceMatcher(None, a, b).ratio())
        return max(scores, default=0.0)

    def match(self, clubs, teams, overrides=None):
        overrides = {str(k): int(v) for k, v in (overrides or {}).items()}
        by_id = {int(t["id"]): t for t in teams}
        used, result, problems = set(), [], []
        for club in clubs:
            tm_id = str(int(club["club_id"]))
            forced = overrides.get(tm_id)
            if forced is not None:
                team = by_id.get(forced)
                if team is None:
                    problems.append(f"Override TM {tm_id}: team football-data {forced} assente")
                    continue
                result.append((club, team, 1.0)); used.add(forced); continue
            candidates = sorted(((self.score(club, t), t) for t in teams), key=lambda x: x[0], reverse=True)
            best, team = candidates[0] if candidates else (0.0, None)
            second = candidates[1][0] if len(candidates) > 1 else 0.0
            if team is None or best < 0.72 or best - second < 0.06:
                problems.append(f"TM {tm_id} {club.get('name')}: corrispondenza incerta ({team and team.get('name')}, {best:.2f})")
                continue
            fd_id = int(team["id"])
            if fd_id in used:
                problems.append(f"Team football-data {fd_id} collegato più volte"); continue
            result.append((club, team, best)); used.add(fd_id)
        for team in teams:
            if int(team["id"]) not in used:
                problems.append(f"Football-data {team['id']} {team.get('name')}: nessun club Transfermarkt")
        if problems:
            raise ClubIdentityError("\n".join(problems))
        return result

    @classmethod
    def public_name(cls, team):
        return team.get("shortName") or team.get("name")

    @classmethod
    def aliases(cls, club, team):
        public, seen, result = cls.public_name(team), set(), []
        for value in (club.get("name"), team.get("name"), team.get("shortName"), team.get("tla")):
            key = cls.normalize(value)
            if value and key != cls.normalize(public) and key not in seen:
                seen.add(key); result.append(value)
        return result
