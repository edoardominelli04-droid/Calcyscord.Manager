from services.importers.roster_importer import (
    RosterImporter
)


def main():

    importer = RosterImporter()

    rosters = importer.import_rosters()

    print()

    print("=" * 40)

    print(f"Rose ricostruite: {len(rosters)}")

    print("=" * 40)


if __name__ == "__main__":
    main()