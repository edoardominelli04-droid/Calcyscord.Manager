from database.schema import create_tables

def main():
    print("===================================")
    print(" Calcyscord.Manager v0.1")
    print(" Avvio del progetto...")
    print("===================================")

    create_tables()

    print("Database inizializzato correttamente.")

if __name__ == "__main__":
    main()