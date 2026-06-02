from collections import defaultdict


class TaxRiskEngine:

    def __init__(self):

        self.location_history = defaultdict(int)

    # =================================================
    # LEARN PATTERNS
    # =================================================

    def learn(self, df):

        for _, row in df.iterrows():

            self.location_history[row["From"]] += 1
            self.location_history[row["To"]] += 1

    # =================================================
    # CONFIDENCE SCORE
    # =================================================

    def confidence(self, trip_type, frm, to, km):

        score = 50  # base confidence

        freq_from = self.location_history[frm]
        freq_to = self.location_history[to]

        # frequent location = higher confidence
        if freq_to > 10:
            score += 20

        # known commute pattern
        if freq_from > 10 and freq_to > 10:
            score += 15

        # long trip more likely business
        if km > 10:
            score += 10

        # short random trip = lower confidence
        if km < 1:
            score -= 20

        return max(0, min(100, score))

    # =================================================
    # RISK LEVEL
    # =================================================

    def risk(self, confidence):

        if confidence >= 80:
            return "LOW"

        if confidence >= 50:
            return "MEDIUM"

        return "HIGH"

    # =================================================
    # EXPLANATION
    # =================================================

    def explain(self, frm, to, km, trip_type, confidence):

        reasons = []

        if km > 10:
            reasons.append("Long distance travel")

        if self.location_history[to] > 10:
            reasons.append("Frequent destination")

        if confidence > 75:
            reasons.append("Strong behavioral pattern match")

        if not reasons:
            reasons.append("Low historical pattern data")

        return ", ".join(reasons)