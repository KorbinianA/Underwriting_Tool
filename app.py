import streamlit as st

from scoring import load_data, underwriting_scoring

st.set_page_config(
    page_title="Underwriting Tool",
    page_icon="📊",
    layout="wide"
)

seite = st.sidebar.radio(
    "Navigation",
    ["Hauptseite", "Underwriting Scoring"]
)

if seite == "Hauptseite":
    st.title("Underwriting Tool für Pensionskassen")

    st.write("""
    Willkommen im Underwriting-Demo-Tool.

    Diese App zeigt, wie Versicherte anhand von Stammdaten,
    Arbeitsverhältnis, Gesundheitsdaten und Vorsorgedaten
    risikobasiert bewertet werden können.
    """)

    st.subheader("Verfügbare Funktionen")

    st.markdown("""
    - Underwriting Scoring
    - Risikoklassifikation
    - Übersicht der Versicherten
    - Kennzahlen zum Portfolio
    """)

    st.info("Wähle links in der Navigation **Underwriting Scoring**, um die Scoring-Funktion zu öffnen.")


elif seite == "Underwriting Scoring":
    st.title("Underwriting Scoring")

    df = load_data()
    scored_df = underwriting_scoring(df)

    st.subheader("Kennzahlen")

    col1, col2, col3 = st.columns(3)

    col1.metric("Versicherte", len(scored_df))
    col2.metric("Ø Score", round(scored_df["Underwriting_Score"].mean(), 2))
    col3.metric(
        "High Risk",
        (scored_df["Underwriting_Entscheid"] == "High Risk / Rückversicherung prüfen").sum()
    )

    st.subheader("Verteilung Underwriting-Entscheide")
    st.bar_chart(scored_df["Underwriting_Entscheid"].value_counts())

    st.subheader("Versicherte")
    st.dataframe(scored_df)