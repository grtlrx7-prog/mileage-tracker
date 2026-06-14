import streamlit as st
import pandas as pd
import os

from backend.parsers.sars_export import parse_timeline


# =================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
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
# RUN EXPORT BUTTON
# =================================================
if st.button("🚀 Generate SARS Report"):

    try:
        with st.spinner("Processing trips..."):
            parse_timeline()

        st.success("Export completed successfully!")

    except Exception as e:
        st.error(f"Export failed: {str(e)}")


# =================================================
# LOAD OUTPUT FILE SAFELY
# =================================================
FILE_PATH = "backend/exports/mileage_logbook.xlsx"


if os.path.exists(FILE_PATH):

    try:
        df = pd.read_excel(FILE_PATH, sheet_name="Trips")

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

    except Exception as e:
        st.error(f"Failed to load report: {str(e)}")

else:
    st.info("👉 No report found. Click 'Generate SARS Report' first.")