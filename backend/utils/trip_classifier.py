import pandas as pd


# =================================================
# SMART TRIP CLASSIFIER (BEHAVIOR-BASED)
# =================================================

def classify_trip(row, home="Unknown", work="Unknown"):

    try:

        from_addr = (row.get("From") or "").lower()
        to_addr = (row.get("To") or "").lower()

        date = row.get("Date")
        km = row.get("KM", 0)

        # =========================================
        # DEFAULTS
        # =========================================

        trip_type = "Business"
        purpose = "Business Travel"

        # =========================================
        # UNKNOWN LOCATIONS
        # =========================================

        if "unknown" in from_addr or "unknown" in to_addr:

            return (
                "Business",
                "Needs Review"
            )

        # =========================================
        # HOME ↔ WORK COMMUTE
        # =========================================

        if home != "Unknown" and work != "Unknown":

            if (
                home.lower() in from_addr
                and work.lower() in to_addr
            ) or (
                work.lower() in from_addr
                and home.lower() in to_addr
            ):

                return (
                    "Commute",
                    "Home to Work"
                )

        # =========================================
        # SHORT TRIPS = PERSONAL
        # =========================================

        if km <= 2:

            return (
                "Personal",
                "Short Trip"
            )

        # =========================================
        # WEEKEND RULE
        # =========================================

        if isinstance(date, pd.Timestamp):

            weekday = date.weekday()

            if weekday >= 5:

                return (
                    "Personal",
                    "Weekend Travel"
                )

        # =========================================
        # HOME AREA DETECTION
        # =========================================

        if home != "Unknown":

            if home.lower() in from_addr:

                return (
                    "Business",
                    "Client Visit"
                )

        # =========================================
        # DEFAULT BUSINESS
        # =========================================

        return (
            "Business",
            "Business Travel"
        )

    except Exception as e:

        print("CLASSIFIER ERROR:", e)

        return (
            "Business",
            "Business Travel"
        )