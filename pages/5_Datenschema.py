import streamlit as st

st.title("ER-Datenschema")

st.write("""
Das Datenmodell besteht aus fünf Tabellen.  
Die Tabelle `personenstamm` ist die zentrale Tabelle.  
Alle versichertenbezogenen Tabellen sind über `PK` verbunden.
""")

er_diagramm = """
digraph {
    graph [rankdir=LR]

    personenstamm [
        label="personenstamm|PK (Primary Key)|Nachname|Vorname|Geburtstag|Geschlecht|Zivilstand"
        shape=record
    ]

    arbeitsverhaeltnis [
        label="arbeitsverhaeltnis|PK (Foreign Key)|Beruf|Branche|Beschaeftigungsgrad|Lohn|AG_ID|Eintrittsdatum"
        shape=record
    ]

    gesundheitsdaten [
        label="gesundheitsdaten|PK (Foreign Key)|Raucher|Groesse_cm|Gewicht_kg|BMI|Psychische_Vorerkrankung|Krankentage_12M|IV_Fall"
        shape=record
    ]

    vorsorgedaten [
        label="vorsorgedaten|PK (Foreign Key)|Versicherter_Lohn|Todesfallkapital|Invalidenrente|PK_Einkauf|Risiko_Klasse|WEF_Vorbezug"
        shape=record
    ]

    arbeitgeber [
        label="arbeitgeber|AG_ID (Primary Key)|Name|Branche|Stadt"
        shape=record
    ]

    personenstamm -> arbeitsverhaeltnis [label="PK"]
    personenstamm -> gesundheitsdaten [label="PK"]
    personenstamm -> vorsorgedaten [label="PK"]

    arbeitgeber -> arbeitsverhaeltnis [label="AG_ID"]
}
"""

st.graphviz_chart(er_diagramm)

st.caption("""
Das Schema zeigt die Beziehungen zwischen Personen, Arbeitsverhältnis,
Gesundheitsdaten, Vorsorgedaten und Arbeitgebern.
""")