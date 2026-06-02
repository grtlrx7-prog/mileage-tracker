from collections import Counter


# -----------------------------------
# SIMPLE SMART CLASSIFIER (RULE BASED AI)
# -----------------------------------

def classify_trip(start_location: str, end_location: str):

    start = (start_location or "").lower()
    end = (end_location or "").lower()

    # -----------------------------------
    # RULE 1: WORK PATTERN DETECTION
    # -----------------------------------

    work_keywords = [
        "office",
        "company",
        "work",
        "hq",
        "business",
        "client"
    ]

    if any(word in start for word in work_keywords) or \
       any(word in end for word in work_keywords):
        return "business"

    # -----------------------------------
    # RULE 2: DEFAULT RULE
    # -----------------------------------

    return "personal"