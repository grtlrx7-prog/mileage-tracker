import streamlit as st
import requests
import pandas as pd
import os

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)

st.set_page_config(
    page_title="SARS Mileage Logbook",
    layout="wide"
)

st.title("🚗 SARS Mileage Logbook System")

st.write("Production-grade system connected to FastAPI backend")


# -----------------------------
# GENERATE REPORT BUTTON
# -----------------------------
if st.button("🚀 Generate SARS Report"):

    with st.spinner("Calling backend API..."):

        response = requests.post(
            f"{API_URL}/generate-report"
        )

    if response.status_code == 200:
        st.success("Report generated successfully!")
    else:
        st.error("Backend error occurred")


# -----------------------------
# LOAD OUTPUT FILE
# -----------------------------
try:

    df = pd.read_excel(
        "backend/exports/mileage_logbook.xlsx",
        sheet_name="Trips"
    )

    st.subheader("📊 Trip Overview")

    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Trips", len(df))
    col2.metric("KM", round(df["KM"].sum(), 2))
    col3.metric(
        "Claim (ZAR)",
        f"R{round(df['Claim (ZAR)'].sum(), 2)}"
    )

except Exception:
    st.info("No report yet — click Generate Report")