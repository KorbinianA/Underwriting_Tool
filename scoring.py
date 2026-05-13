import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def load_data(engine):
    personen = pd.read_sql("SELECT * FROM personenstamm", engine)
    arbeit = pd.read_sql("SELECT * FROM arbeitsverhaeltnis", engine)
    gesundheit = pd.read_sql("SELECT * FROM gesundheitsdaten", engine)
    vorsorge = pd.read_sql("SELECT * FROM vorsorgedaten", engine)
    arbeitgeber = pd.read_sql("SELECT * FROM arbeitgeber", engine)

    df = (
        personen
        .merge(arbeit, on="PK", how="inner")
        .merge(gesundheit, on="PK", how="inner")
        .merge(vorsorge, on="PK", how="inner")
        .merge(arbeitgeber, on="AG_ID", how="left", suffixes=("", "_AG"))
    )

    return df


def calculate_age(birthdate):
    today = pd.Timestamp.today()
    birthdate = pd.to_datetime(birthdate)
    return today.year - birthdate.dt.year - (
        (today.month < birthdate.dt.month) |
        ((today.month == birthdate.dt.month) & (today.day < birthdate.dt.day))
    )


def underwriting_scoring(df):
    df = df.copy()

    df["Alter"] = calculate_age(df["Geburtstag"])

    df["Score_Raucher"] = np.where(df["Raucher"] == "ja", 2, 0)
    df["Score_BMI"] = np.where(df["BMI"] >= 30, 2, 0)
    df["Score_Psychisch"] = np.where(df["Psychische_Vorerkrankung"] == "ja", 4, 0)
    df["Score_Krankentage"] = np.where(df["Krankentage_12M"] > 10, 3, 0)
    df["Score_Alter"] = np.where(df["Alter"] > 55, 2, 0)
    df["Score_Lohn"] = np.where(df["Lohn"] > 180000, 1, 0)
    df["Score_IV"] = np.where(df["IV_Fall"] == "ja", 5, 0)
    df["Score_Branche"] = np.where(df["Branche"].isin(["Bau", "Gesundheitswesen"]), 1, 0)

    score_cols = [
        "Score_Raucher",
        "Score_BMI",
        "Score_Psychisch",
        "Score_Krankentage",
        "Score_Alter",
        "Score_Lohn",
        "Score_IV",
        "Score_Branche"
    ]

    df["Underwriting_Score"] = df[score_cols].sum(axis=1)

    conditions = [
        df["Underwriting_Score"] <= 3,
        df["Underwriting_Score"] <= 6,
        df["Underwriting_Score"] <= 9,
        df["Underwriting_Score"] > 9
    ]

    choices = [
        "Auto Accept",
        "Manual Review",
        "Special Underwriting",
        "High Risk / Rückversicherung prüfen"
    ]

    df["Underwriting_Entscheid"] = np.select(
        conditions,
        choices,
        default="Unbekannt"
    )

    return df