import streamlit as st

from scoring import load_data, underwriting_scoring

st.title("Rohdaten Versicherte")

df = load_data()
df = underwriting_scoring(df)

st.subheader("Filter")

suche = st.text_input(
    "Suche nach PK, Name, Arbeitgeber, Branche oder Stadt"
)

anzeige_df = df.copy()

if suche:
    suche = suche.lower()

    anzeige_df = anzeige_df[
        anzeige_df.astype(str)
        .apply(
            lambda row: row.str.lower().str.contains(suche).any(),
            axis=1
        )
    ]

st.write(f"Anzahl Datensätze: {len(anzeige_df)}")

st.dataframe(
    anzeige_df,
    use_container_width=True
)