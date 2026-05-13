import streamlit as st

st.set_page_config(
    page_title="Underwriting Tool",
    page_icon="📊",
    layout="wide"
)

st.title("Underwriting Tool für Pensionskassen")

st.write("""
Willkommen im Underwriting-Demo-Tool von Korbinian Auer.

Nutze die Navigation links, um zwischen den Funktionen zu wechseln.
""")

st.subheader("Verfügbare Module")

st.markdown("""
- Underwriting Scoring
- PK Einkäufe
- Top Arbeitgeber
- Rohdaten Versicherte
- Datenschema
""")