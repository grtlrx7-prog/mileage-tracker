import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

st.title("SARS Mileage Dashboard")


FILE = "backend/exports/mileage_logbook.csv"

df = pd.read_csv(FILE)


# ============================================
# KPIs
# ============================================

st.metric(
    "Total KM",
    f"{df['KM'].sum():,.2f}"
)

st.metric(
    "Trips",
    len(df)
)

st.metric(
    "Estimated Claim",
    f"R{df['Claim (ZAR)'].sum():,.2f}"
)


# ============================================
# MONTHLY CHART
# ============================================

monthly = df.groupby("Month")["KM"].sum().reset_index()

fig = px.bar(
    monthly,
    x="Month",
    y="KM",
    title="Monthly Distance"
)

st.plotly_chart(fig, use_container_width=True)


# ============================================
# BUSINESS VS PERSONAL
# ============================================

trip_types = df.groupby("Trip Type")["KM"].sum().reset_index()

fig2 = px.pie(
    trip_types,
    names="Trip Type",
    values="KM",
    title="Business vs Personal"
)

st.plotly_chart(fig2, use_container_width=True)


# ============================================
# TABLE
# ============================================

st.dataframe(df)