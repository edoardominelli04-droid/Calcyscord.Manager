from services.providers.transfermarkt_provider import TransfermarktProvider

provider = TransfermarktProvider()

datasets = {
    "clubs": provider.get_clubs(),
    "players": provider.get_players(),
    "competitions": provider.get_competitions(),
    "countries": provider.get_countries()
}

for name, df in datasets.items():
    print(f"\n===== {name.upper()} =====")
    print(df.columns.tolist())