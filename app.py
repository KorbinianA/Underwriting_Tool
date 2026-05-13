import os
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from scoring import load_data, underwriting_scoring

load_dotenv()

st.title("Pensionskasse Underwriting Scoring")

url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "my_db"),
)

engine = create_engine(url)

df = load_data(engine)
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

st.bar_chart(
    scored_df["Underwriting_Entscheid"].value_counts()
)

st.subheader("Versicherte")

st.dataframe(scored_df)