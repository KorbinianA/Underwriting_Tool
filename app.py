import streamlit as st

from scoring import load_data, underwriting_scoring

st.title("Pensionskasse Underwriting Scoring")

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