import streamlit as st
import pandas as pd
import plotly.express as px
from scoring import load_data, underwriting_scoring

st.title("Top Arbeitgeber")

df = load_data()
df = underwriting_scoring(df)

# =========================
# Kennzahlen je Arbeitgeber
# =========================

ag_stats = (
    df
    .groupby(["AG_ID", "Name", "Stadt", "Branche_AG"], dropna=False)
    .agg(
        Anzahl_Versicherte=("PK", "count"),
        Altersschnitt=("Alter", "mean"),
        Durchschnittslohn=("Lohn", "mean"),
        Durchschnitt_Versicherter_Lohn=("Versicherter_Lohn", "mean"),
        Total_Todesfallkapital=("Todesfallkapital", "sum"),
        Total_Invalidenrente=("Invalidenrente", "sum"),
    )
    .reset_index()
)

ag_stats["Altersschnitt"] = ag_stats["Altersschnitt"].round(1)
ag_stats["Durchschnittslohn"] = ag_stats["Durchschnittslohn"].round(0)
ag_stats["Durchschnitt_Versicherter_Lohn"] = (
    ag_stats["Durchschnitt_Versicherter_Lohn"].round(0)
)

# =========================
# Funktion für Layout
# =========================

def show_section(title, dataframe, metric):

    st.subheader(title)

    dataframe = dataframe.sort_values(
        by=metric,
        ascending=False
    )

    fig = px.bar(
        dataframe,
        x=metric,
        y="Name",
        orientation="h",
        text=metric
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "array",
            "categoryarray": dataframe["Name"].tolist()[::-1]
        },
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# =========================
# Anzahl Versicherte
# =========================

top_versicherte = ag_stats.sort_values(
    by="Anzahl_Versicherte",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach Anzahl Versicherte",
    top_versicherte,
    "Anzahl_Versicherte"
)

# =========================
# Altersschnitt
# =========================

top_alter = ag_stats.sort_values(
    by="Altersschnitt",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach Altersschnitt",
    top_alter,
    "Altersschnitt"
)

# =========================
# Durchschnittslohn
# =========================

top_lohn = ag_stats.sort_values(
    by="Durchschnittslohn",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach Durchschnittslohn",
    top_lohn,
    "Durchschnittslohn"
)

# =========================
# Versicherter Lohn
# =========================

top_vers_lohn = ag_stats.sort_values(
    by="Durchschnitt_Versicherter_Lohn",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach versichertem Lohn",
    top_vers_lohn,
    "Durchschnitt_Versicherter_Lohn"
)

# =========================
# Todesfallkapital
# =========================

top_tod = ag_stats.sort_values(
    by="Total_Todesfallkapital",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach Todesfallkapital",
    top_tod,
    "Total_Todesfallkapital"
)

# =========================
# Invalidenrente
# =========================

top_iv = ag_stats.sort_values(
    by="Total_Invalidenrente",
    ascending=False
).head(10)

show_section(
    "Top 10 Arbeitgeber nach Invalidenrente",
    top_iv,
    "Total_Invalidenrente"
)