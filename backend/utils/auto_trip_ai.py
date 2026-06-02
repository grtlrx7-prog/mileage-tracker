from collections import defaultdict


class AutoTripAI:

    def __init__(self):

        self.location_frequency = defaultdict(int)

    # =================================================
    # LEARN PATTERNS
    # =================================================

    def learn(self, df):

        try:

            for _, row in df.iterrows():

                self.location_frequency[
                    row["From"]
                ] += 1

                self.location_frequency[
                    row["To"]
                ] += 1

        except Exception as e:

            print("AI LEARN ERROR:", e)

    # =================================================
    # KEYWORD DETECTION
    # =================================================

    def contains(self, text, words):

        try:

            text = str(text).lower()

            for w in words:

                if w in text:
                    return True

            return False

        except:
            return False

    # =================================================
    # CLASSIFICATION ENGINE
    # =================================================

    def classify(self, from_addr, to_addr, km):

        try:

            f = str(from_addr).lower()
            t = str(to_addr).lower()

            # =========================================
            # HOME KEYWORDS
            # =========================================

            home_words = [
                "home",
                "residential",
                "estate",
                "complex",
                "apartment"
            ]

            # =========================================
            # WORK KEYWORDS
            # =========================================

            work_words = [
                "office",
                "business",
                "company",
                "pty",
                "ltd",
                "park",
                "industrial",
                "work"
            ]

            # =========================================
            # PERSONAL KEYWORDS
            # =========================================

            personal_words = [
                "mall",
                "shop",
                "restaurant",
                "school",
                "gym",
                "hospital",
                "church"
            ]

            # =========================================
            # HOME ↔ WORK
            # =========================================

            if (
                (
                    self.contains(f, home_words)
                    and
                    self.contains(t, work_words)
                )
                or
                (
                    self.contains(f, work_words)
                    and
                    self.contains(t, home_words)
                )
            ):

                return (
                    "Commute",
                    "Home ↔ Work"
                )

            # =========================================
            # PERSONAL
            # =========================================

            if (
                self.contains(f, personal_words)
                or
                self.contains(t, personal_words)
            ):

                return (
                    "Personal",
                    "Personal Travel"
                )

            # =========================================
            # LONG DISTANCE = BUSINESS
            # =========================================

            if km >= 10:

                return (
                    "Business",
                    "Client Visit"
                )

            # =========================================
            # REPEATED DESTINATION
            # =========================================

            if (
                self.location_frequency[t] > 5
                and
                km >= 3
            ):

                return (
                    "Business",
                    "Recurring Business Location"
                )

            # =========================================
            # DEFAULT
            # =========================================

            return (
                "Business",
                "General Business Travel"
            )

        except Exception as e:

            print("AI CLASSIFY ERROR:", e)

            return (
                "Business",
                "General Business Travel"
            )