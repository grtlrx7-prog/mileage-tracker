import json
import os

RULES_FILE = "backend/data/manual_trip_rules.json"


# =================================================
# LOAD RULES
# =================================================

def load_rules():

    try:

        if not os.path.exists(RULES_FILE):
            return []

        with open(RULES_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except:

        return []


# =================================================
# SAVE RULE
# =================================================

def save_rule(rule):

    rules = load_rules()

    rules.append(rule)

    with open(RULES_FILE, "w", encoding="utf-8") as f:

        json.dump(
            rules,
            f,
            indent=2,
            ensure_ascii=False
        )


# =================================================
# FIND MATCH
# =================================================

def find_matching_rule(from_addr, to_addr):

    rules = load_rules()

    f = (from_addr or "").lower()
    t = (to_addr or "").lower()

    for r in rules:

        rf = r.get("from", "").lower()
        rt = r.get("to", "").lower()

        if rf in f and rt in t:

            return (
                r.get("trip_type"),
                r.get("purpose")
            )

    return None