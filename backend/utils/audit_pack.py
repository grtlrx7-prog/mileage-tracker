import pandas as pd


# =================================================
# SARS AUDIT SUMMARY BUILDER
# =================================================

def build_audit_summary(df, home, work):

    try:

        total_km = df["KM"].sum()

        business_km = df[
            df["Trip Type"] == "Business"
        ]["KM"].sum()

        personal_km = df[
            df["Trip Type"] == "Personal"
        ]["KM"].sum()

        commute_km = df[
            df["Trip Type"] == "Commute"
        ]["KM"].sum()

        return pd.DataFrame([{

            "Home Location": home,
            "Work Location": work,

            "Total Trips": len(df),

            "Total KM": round(total_km, 2),

            "Business KM": round(business_km, 2),

            "Personal KM": round(personal_km, 2),

            "Commute KM": round(commute_km, 2),

            "Business %": round((business_km / total_km) * 100, 2)
            if total_km else 0,

            "System": "AI Generated Mileage Logbook",
            "Status": "Prepared for SARS Review"

        }])

    except Exception as e:

        print("AUDIT SUMMARY ERROR:", e)

        return pd.DataFrame()