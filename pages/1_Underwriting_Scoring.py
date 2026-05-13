import pandas as pd
import streamlit as st

from scoring import load_data, underwriting_scoring

st.title("Underwriting Scoring")

df = load_data()
scored_df = underwriting_scoring(df)

# Button / Fenster Score Definition
if st.button("Score Definition"):
    st.info("""
    **Punkteverteilung im Underwriting Scoring**

    | Kriterium | Punkte |
    |---|---:|
    | Raucher = ja | +2 |
    | BMI ≥ 30 | +2 |
    | Psychische Vorerkrankung = ja | +4 |
    | Krankentage letzte 12 Monate > 10 | +3 |
    | Alter > 55 | +2 |
    | Lohn > 180'000 CHF | +1 |
    | IV-Fall = ja | +5 |
    | Branche Bau oder Gesundheitswesen | +1 |

    **Entscheidungslogik**

    | Score | Entscheid |
    |---:|---|
    | 0–3 | Auto Accept |
    | 4–6 | Manual Review |
    | 7–9 | Special Underwriting |
    | >9 | High Risk / Rückversicherung prüfen |
    """)

st.subheader("Kennzahlen")

col1, col2, col3 = st.columns(3)

col1.metric("Versicherte", len(scored_df))
col2.metric("Ø Score", round(scored_df["Underwriting_Score"].mean(), 2))
col3.metric(
    "High Risk",
    (scored_df["Underwriting_Entscheid"] == "High Risk / Rückversicherung prüfen").sum()
)

# Prozentuale Verteilung
st.subheader("Verteilung Underwriting-Entscheide in Prozent")

verteilung_prozent = (
    scored_df["Underwriting_Entscheid"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

st.bar_chart(verteilung_prozent)

# Suchfunktion
st.subheader("Versicherte suchen")

suchbegriff = st.text_input(
    "Suche nach PK, Nachname, Vorname, Beruf, Branche oder Entscheid"
)

anzeige_df = scored_df.copy()

if suchbegriff:
    suchbegriff = suchbegriff.lower()

    anzeige_df = anzeige_df[
        anzeige_df.astype(str)
        .apply(lambda row: row.str.lower().str.contains(suchbegriff).any(), axis=1)
    ]

st.write(f"Gefundene Versicherte: {len(anzeige_df)}")

st.dataframe(anzeige_df)