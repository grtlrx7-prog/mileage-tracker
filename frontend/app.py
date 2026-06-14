import streamlit as st
import requests
import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
API_URL = os.getenv(
    "API_URL",
    "https://mileage-tracker-api.onrender.com"

st.set_page_config(
    page_title="SARS Mileage Logbook",
    layout="wide"
)

st.title("🚗 SARS Mileage Logbook System")

st.write("Connected to production FastAPI backend")


# -----------------------------
# GENERATE REPORT
# -----------------------------
if st.button("🚀 Generate SARS Report"):

    with st.spinner("Generating report via backend..."):

        try:
            response = requests.post(
                f"{API_URL}/sars/generate-report",
                timeout=60
            )

            if response.status_code == 200:
                st.success("Report generated successfully!")
            else:
                st.error(f"Backend error: {response.text}")

        except Exception as e:
            st.error(f"Connection failed: {str(e)}")


# -----------------------------
# LOAD DATA FROM API (FIXED APPROACH)
# -----------------------------
st.subheader("📊 Trip Overview")


try:
    # 👉 PRODUCTION FIX: frontend should NOT read files directly
    response = requests.get(
        f"{API_URL}/trips",
        timeout=30
    )

    if response.status_code == 200:

        data = response.json()

        if len(data) == 0:
            st.info("No trips available yet.")
        else:
            df = pd.DataFrame(data)

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Summary Stats")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Trips", len(df))

            col2.metric(
                "Total KM",
                round(df["km"].sum(), 2) if "km" in df else 0
            )

            col3.metric(
                "Estimated Claim",
                f"R{round(df['claim'].sum(), 2)}" if "claim" in df else "R0"
            )

    else:
        st.error("Failed to load trip data from backend")

except Exception as e:
    st.warning("Backend not available or API error")
    st.caption(str(e))