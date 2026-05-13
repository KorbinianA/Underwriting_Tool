def load_data():

    base_path = os.path.join(os.path.dirname(__file__), "data")

    personen = pd.read_csv(os.path.join(base_path, "01_personenstamm.csv"))
    arbeit = pd.read_csv(os.path.join(base_path, "02_arbeitsverhaeltnis.csv"))
    gesundheit = pd.read_csv(os.path.join(base_path, "03_gesundheitsdaten.csv"))
    vorsorge = pd.read_csv(os.path.join(base_path, "04_vorsorgedaten.csv"))
    arbeitgeber = pd.read_csv(os.path.join(base_path, "05_arbeitgeber.csv"))

    df = (
        personen
        .merge(arbeit, on="PK", how="inner")
        .merge(gesundheit, on="PK", how="inner")
        .merge(vorsorge, on="PK", how="inner")
        .merge(arbeitgeber, on="AG_ID", how="left", suffixes=("", "_AG"))
    )

    return df