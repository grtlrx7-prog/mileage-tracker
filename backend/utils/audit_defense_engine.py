from collections import defaultdict
import pandas as pd


class AuditDefenseEngine:

    def __init__(self):
        self.location_counts = defaultdict(int)

    # =================================================
    # LEARN PATTERNS
    # =================================================

    def learn(self, df):

        for _, row in df.iterrows():
            self.location_counts[row["From"]] += 1
            self.location_counts[row["To"]] += 1

    # =================================================
    # EXPLAIN SINGLE TRIP
    # =================================================

    def explain_trip(self, row):

        reasons = []

        if row["Trip Type"] == "Business":
            reasons.append("Trip classified as business due to travel pattern analysis")

        if row["KM"] > 10:
            reasons.append("Long-distance travel consistent with client or work-related movement")

        if self.location_counts[row["To"]] > 8:
            reasons.append("Repeated destination indicating operational/business site")

        if not reasons:
            reasons.append("Default classification based on travel behaviour model")

        return ". ".join(reasons)

    # =================================================
    # BUILD MONTHLY NARRATIVE
    # =================================================

    def monthly_narrative(self, df):

        narratives = []

        for month, group in df.groupby("Month"):

            total_km = group["KM"].sum()
            business_km = group[group["Trip Type"] == "Business"]["KM"].sum()

            narratives.append({
                "Month": month,
                "Summary": (
                    f"In {month}, total travel was {total_km:.2f} km "
                    f"with {business_km:.2f} km classified as business travel "
                    f"based on recurring location patterns and travel frequency analysis."
                )
            })

        return pd.DataFrame(narratives)