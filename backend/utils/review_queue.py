import pandas as pd


# =================================================
# BUILD REVIEW QUEUE
# =================================================

def build_review_queue(df):

    try:

        review_rows = []

        for _, row in df.iterrows():

            reasons = []

            # =========================================
            # UNKNOWN ADDRESS CHECK
            # =========================================

            if row["From"] == "Unknown":
                reasons.append("Unknown Start Address")

            if row["To"] == "Unknown":
                reasons.append("Unknown End Address")

            # =========================================
            # VERY SHORT TRIPS
            # =========================================

            if row["KM"] <= 1:
                reasons.append("Very Short Trip")

            # =========================================
            # COMMUTE DETECTION UNCERTAINTY
            # =========================================

            if row["Trip Type"] not in [
                "Business",
                "Commute",
                "Personal"
            ]:
                reasons.append("Unclassified Trip Type")

            # =========================================
            # ONLY ADD IF FLAGGED
            # =========================================

            if reasons:

                review_rows.append({

                    "Date": row["Date"],
                    "From": row["From"],
                    "To": row["To"],
                    "KM": row["KM"],
                    "Trip Type": row["Trip Type"],
                    "Purpose": row["Purpose"],
                    "Issues": "; ".join(reasons),
                    "Status": "Pending Review"
                })

        return pd.DataFrame(review_rows)

    except Exception as e:

        print("REVIEW QUEUE ERROR:", e)

        return pd.DataFrame()