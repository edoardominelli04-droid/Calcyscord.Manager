from services.database_updater import DatabaseUpdater


def main():

    updater = DatabaseUpdater()

    updater.update_all()


if __name__ == "__main__":

    main()