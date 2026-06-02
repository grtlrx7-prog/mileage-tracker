from collections import Counter


WORK_HOURS_START = 7
WORK_HOURS_END = 18


BUSINESS_KEYWORDS = [
    "office",
    "industrial",
    "business",
    "park",
    "estate",
    "mall",
]


PERSONAL_KEYWORDS = [
    "home",
    "school",
    "gym",
]


# ============================================
# HOME DETECTION
# ============================================

def detect_home(df):

    home_candidates = []

    for _, r in df.iterrows():

        hour = r["Start Time"].hour

        if hour >= 19 or hour <= 6:
            home_candidates.append(r["From"])

    home = Counter(home_candidates).most_common(1)

    return home[0][0] if home else "Unknown"


# ============================================
# WORK DETECTION
# ============================================

def detect_work_locations(df):

    candidates = []

    for _, r in df.iterrows():

        hour = r["Start Time"].hour

        if 7 <= hour <= 10:
            candidates.append(r["To"])

    common = Counter(candidates).most_common(5)

    return [x[0] for x in common]


# ============================================
# CLASSIFY TRIP
# ============================================

def classify_trip(row, home, work_locations):

    start = str(row["From"]).lower()
    end = str(row["To"]).lower()

    hour = row["Start Time"].hour
    km = row["KM"]

    if start == home and end == home:
        return "Personal"

    if end in work_locations:
        return "Business"

    if WORK_HOURS_START <= hour <= WORK_HOURS_END and km > 5:
        return "Business"

    for k in BUSINESS_KEYWORDS:

        if k in start or k in end:
            return "Business"

    for k in PERSONAL_KEYWORDS:

        if k in start or k in end:
            return "Personal"

    return "Business"