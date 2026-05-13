import streamlit as st
import pandas as pd
import plotly.express as px

from scoring import load_data, underwriting_scoring

st.title("PK-Einkäufe")

df = load_data()
df = underwriting_scoring(df)

# =========================
# Arbeitgeber Filter
# =========================

arbeitgeber_filter = st.multiselect(
    "Arbeitgeber",
    sorted(df["Name"].unique())
)

filtered_df = df.copy()

if arbeitgeber_filter:
    filtered_df = filtered_df[
        filtered_df["Name"].isin(arbeitgeber_filter)
    ]

# =========================
# Altersgruppen
# =========================

filtered_df["Altersgruppe"] = pd.cut(
    filtered_df["Alter"],
    bins=[0, 34, 44, 54, 65, 100],
    labels=["<35", "35–44", "45–54", "55–65", "65+"]
)

# =========================
# Heatmap Daten
# =========================

heatmap_data = (
    filtered_df
    .groupby(
        ["Altersgruppe", "Risiko_Klasse"],
        observed=False
    )["PK_Einkauf"]
    .sum()
    .reset_index()
)

pivot = heatmap_data.pivot(
    index="Altersgruppe",
    columns="Risiko_Klasse",
    values="PK_Einkauf"
).fillna(0)

# =========================
# Heatmap
# =========================

st.subheader(
    "PK-Einkäufe nach Altersgruppe und Risiko-Klasse"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    labels=dict(
        x="Risiko-Klasse",
        y="Altersgruppe",
        color="PK-Einkauf CHF"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    """
    Die Heatmap zeigt die Summe der PK-Einkäufe
    je Altersgruppe und Risiko-Klasse.
    """
)