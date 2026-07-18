"""Audit completo e non distruttivo di tutti i campionati configurati."""
import sys
from pathlib import Path

# Consente l'esecuzione diretta: python3 tools/audit_live_provider_alignment.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.database_manager import DatabaseManager
from services.identity.club_identity_service import ClubIdentityError, ClubIdentityService
from services.providers.football_data_provider import FootballDataProvider
from services.providers.transfermarkt_provider import TransfermarktProvider


def main():
    db = DatabaseManager()
    tm, fd, identity = TransfermarktProvider(), FootballDataProvider(), ClubIdentityService()
    links = [x for x in db.get_config_file("provider_competitions.json") if x.get("playable") and x.get("football_data_code")]
    overrides = db.get_config_file("club_provider_overrides.json") or {}
    frame = tm.get_clubs()
    season = int(frame["last_season"].max())
    total_tm = total_fd = total_matches = 0
    failures = []
    print(f"AUDIT MULTI-PROVIDER — stagione {season}\n")
    for link in links:
        tm_code, fd_code = link["transfermarkt_id"], link["football_data_code"]
        rows = frame[(frame["domestic_competition_id"] == tm_code) & (frame["last_season"] == season)]
        clubs = [row for _, row in rows.iterrows()]
        try:
            teams = fd.get_teams_by_competition(fd_code, season).get("teams", [])
        except Exception as error:
            failures.append(f"{tm_code}/{fd_code}: errore API {error!r}")
            print(f"❌ {tm_code}/{fd_code}: errore API")
            continue
        total_tm += len(clubs); total_fd += len(teams)
        try:
            matches = identity.match(clubs, teams, overrides.get(tm_code, {}))
            total_matches += len(matches)
            minimum = min((score for _, _, score in matches), default=0)
            print(f"✅ {tm_code}/{fd_code}: TM {len(clubs)}, FD {len(teams)}, collegati {len(matches)}, score minimo {minimum:.2f}")
        except ClubIdentityError as error:
            failures.append(f"{tm_code}/{fd_code}:\n{error}")
            print(f"❌ {tm_code}/{fd_code}: TM {len(clubs)}, FD {len(teams)}")
            print("   " + str(error).replace("\n", "\n   "))
    print(f"\nTOTALI: Transfermarkt {total_tm}, football-data {total_fd}, collegati {total_matches}")
    if failures:
        print(f"ESITO: ❌ {len(failures)} competizioni da revisionare")
        raise SystemExit(1)
    print("ESITO: ✅ tutte le competizioni sono allineate; nessun dato è stato modificato")


if __name__ == "__main__":
    main()
