from database.schema import create_tables
from database.database import fetch_one


def main():
    print("===================================")
    print(" Calcyscord.Manager v0.1")
    print(" Avvio del progetto...")
    print("===================================")

    create_tables()

    test = fetch_one("SELECT name FROM sqlite_master WHERE type='table' AND name='manager_teams'")

    if test:
        print("Database inizializzato correttamente.")
        print("Test connessione database: OK")
    else:
        print("Errore: tabella manager_teams non trovata.")


if __name__ == "__main__":
    main()