from collections import defaultdict


class MileageML:

    def __init__(self):

        self.route_frequency = defaultdict(int)

        self.location_frequency = defaultdict(int)

    # =================================================
    # TRAIN MODEL
    # =================================================

    def train(self, df):

        try:

            for _, row in df.iterrows():

                route = (
                    row["From"],
                    row["To"]
                )

                self.route_frequency[route] += 1

                self.location_frequency[
                    row["From"]
                ] += 1

                self.location_frequency[
                    row["To"]
                ] += 1

        except Exception as e:

            print("ML TRAIN ERROR:", e)

    # =================================================
    # CONFIDENCE SCORE
    # =================================================

    def confidence_score(
        self,
        from_addr,
        to_addr,
        km
    ):

        try:

            score = 0

            route = (from_addr, to_addr)

            # =========================================
            # FREQUENT ROUTE
            # =========================================

            freq = self.route_frequency.get(
                route,
                0
            )

            if freq > 20:
                score += 40

            elif freq > 10:
                score += 25

            elif freq > 5:
                score += 15

            # =========================================
            # LONG DISTANCE
            # =========================================

            if km > 20:
                score += 25

            elif km > 10:
                score += 15

            # =========================================
            # BUSINESS KEYWORDS
            # =========================================

            text = (
                str(from_addr).lower()
                + " "
                + str(to_addr).lower()
            )

            business_words = [

                "office",
                "company",
                "business",
                "park",
                "industrial",
                "client",
                "corporate",
                "pty",
                "ltd"

            ]

            for w in business_words:

                if w in text:
                    score += 10

            return min(score, 100)

        except:

            return 50

    # =================================================
    # RISK ENGINE
    # =================================================

    def risk_level(self, confidence):

        if confidence >= 80:
            return "LOW"

        elif confidence >= 50:
            return "MEDIUM"

        return "HIGH"

    # =================================================
    # ANOMALY DETECTION
    # =================================================

    def detect_anomaly(self, km):

        try:

            if km > 300:
                return True

            return False

        except:
            return False