# =========================================
# BUSINESS KEYWORDS
# =========================================

BUSINESS_KEYWORDS = [

    "office",
    "client",
    "meeting",
    "warehouse",
    "site",
    "airport",
    "factory",
    "conference",
    "work",
    "branch",
    "business",
    "sars",
    "bank",
    "lawyer",
    "consulting",
]



# =========================================
# PRIVATE KEYWORDS
# =========================================

PRIVATE_KEYWORDS = [

    "mall",
    "restaurant",
    "home",
    "school",
    "gym",
    "shopping",
    "cinema",
    "hospital",
    "vacation",
    "holiday",
    "friend",
    "family",
]



# =========================================
# CLASSIFIER
# =========================================

def classify_trip(from_location, to_location):

    text = f"{from_location} {to_location}".lower()

    # =========================
    # BUSINESS DETECTION
    # =========================

    for keyword in BUSINESS_KEYWORDS:

        if keyword in text:

            return {
                "trip_type": "Business",
                "confidence": "90",
                "risk_level": "Low",
                "reason": f"Matched business keyword: {keyword}"
            }

    # =========================
    # PRIVATE DETECTION
    # =========================

    for keyword in PRIVATE_KEYWORDS:

        if keyword in text:

            return {
                "trip_type": "Private",
                "confidence": "85",
                "risk_level": "Medium",
                "reason": f"Matched private keyword: {keyword}"
            }

    # =========================
    # UNKNOWN
    # =========================

    return {
        "trip_type": "Unclassified",
        "confidence": "40",
        "risk_level": "High",
        "reason": "No keyword match found"
    }