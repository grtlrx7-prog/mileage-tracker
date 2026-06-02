import streamlit as st
import pandas as pd

from backend.parsers.sars_export import parse_timeline


# =================================================
# PAGE CONFIG
# =================================================

st.set_page_config(
    page_title="SARS Mileage Logbook",
    layout="wide"
)


# =================================================
# TITLE
# =================================================

st.title("🚗 SARS Mileage Logbook System")

st.write("One-click generation of SARS-ready travel reports.")


# =================================================
# RUN BUTTON
# =================================================

if st.button("🚀 Generate SARS Report"):

    with st.spinner("Processing trips..."):

        parse_timeline()

    st.success("Export completed!")


# =================================================
# LOAD OUTPUT FILE
# =================================================

try:

    df = pd.read_excel(
        "backend/exports/mileage_logbook.xlsx",
        sheet_name="Trips"
    )

    st.subheader("📊 Trip Overview")

    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Summary Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Trips", len(df))
    col2.metric("Total KM", round(df["KM"].sum(), 2))
    col3.metric(
        "Estimated Claim",
        f"R{round(df['Claim (ZAR)'].sum(), 2)}"
    )

except Exception:

    st.info("Run export to view data.")