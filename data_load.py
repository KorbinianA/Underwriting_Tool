import os
from pathlib import Path

import pandas as pd
import mysql.connector

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def insert_dataframe(cursor, table_name, columns, dataframe):

    placeholders = ", ".join(["%s"] * len(columns))
    column_string = ", ".join(columns)

    sql = f"""
    INSERT INTO {table_name} ({column_string})
    VALUES ({placeholders})
    """

    for _, row in dataframe.iterrows():

        values = []

        for col in columns:
            value = row[col]

            if pd.isna(value):
                value = None

            values.append(value)

        cursor.execute(sql, tuple(values))


def load_personenstamm(cursor):
    df = pd.read_csv("data/01_personenstamm.csv")

    columns = [
        "PK",
        "Nachname",
        "Vorname",
        "Geburtstag",
        "Geschlecht",
        "Zivilstand"
    ]

    insert_dataframe(cursor, "personenstamm", columns, df)


def load_arbeitgeber(cursor):
    df = pd.read_csv("data/05_arbeitgeber.csv")

    columns = [
        "AG_ID",
        "Name",
        "Branche",
        "Stadt"
    ]

    insert_dataframe(cursor, "arbeitgeber", columns, df)


def load_arbeitsverhaeltnis(cursor):
    df = pd.read_csv("data/02_arbeitsverhaeltnis.csv")

    columns = [
        "PK",
        "Beruf",
        "Branche",
        "Beschaeftigungsgrad",
        "Lohn",
        "AG_ID",
        "Eintrittsdatum"
    ]

    insert_dataframe(cursor, "arbeitsverhaeltnis", columns, df)


def load_gesundheitsdaten(cursor):
    df = pd.read_csv("data/03_gesundheitsdaten.csv")

    columns = [
        "PK",
        "Raucher",
        "Groesse_cm",
        "Gewicht_kg",
        "BMI",
        "Psychische_Vorerkrankung",
        "Krankentage_12M",
        "IV_Fall"
    ]

    insert_dataframe(cursor, "gesundheitsdaten", columns, df)


def load_vorsorgedaten(cursor):
    df = pd.read_csv("data/04_vorsorgedaten.csv")

    columns = [
        "PK",
        "Versicherter_Lohn",
        "Todesfallkapital",
        "Invalidenrente",
        "PK_Einkauf",
        "Risiko_Klasse",
        "WEF_Vorbezug"
    ]

    insert_dataframe(cursor, "vorsorgedaten", columns, df)


def main():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        print("Lade arbeitgeber...")
        load_arbeitgeber(cursor)

        print("Lade personenstamm...")
        load_personenstamm(cursor)

        print("Lade arbeitsverhaeltnis...")
        load_arbeitsverhaeltnis(cursor)

        print("Lade gesundheitsdaten...")
        load_gesundheitsdaten(cursor)

        print("Lade vorsorgedaten...")
        load_vorsorgedaten(cursor)

        connection.commit()

        print("Alle Daten erfolgreich geladen.")

    except Exception as error:

        connection.rollback()

        print("Fehler beim Laden der Daten:")
        print(error)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()