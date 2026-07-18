import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from services.database_manager import DatabaseManager


def main():
    clubs = DatabaseManager().get_clubs(); playable = [c for c in clubs if c.get("active") and c.get("playable",True)]
    errors=[]
    for club in playable:
        for field in ("transfermarkt_id","football_data_id","name","official_name"):
            if club.get(field) in (None,""): errors.append(f"Club {club.get('id')}: manca {field}")
    for label, field, values in (("Transfermarkt","transfermarkt_id",clubs),("football-data","football_data_id",playable)):
        duplicates=[k for k,v in Counter(c.get(field) for c in values).items() if k is not None and v>1]
        if duplicates: errors.append(f"{label} ID duplicati: {duplicates}")
    print("Club giocabili per competizione:")
    for code,count in sorted(Counter(c.get("football_data_competition_code") for c in playable).items()): print(f"  {code}: {count}")
    print(f"Totale giocabili: {len(playable)}; archiviati: {len(clubs)-len(playable)}")
    if errors:
        print("\nERRORI:\n"+"\n".join(f"- {e}" for e in errors)); raise SystemExit(1)
    print("OK: identità multi-provider coerenti.")
if __name__=="__main__": main()
