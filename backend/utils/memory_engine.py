import json
import os
from collections import defaultdict


MEMORY_FILE = "backend/memory/trip_memory.json"


# =================================================
# LOAD MEMORY
# =================================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {
            "home_candidates": {},
            "work_candidates": {},
            "frequent_locations": {}
        }

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


# =================================================
# SAVE MEMORY
# =================================================

def save_memory(data):

    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# =================================================
# UPDATE MEMORY FROM TRIPS
# =================================================

def update_memory(df):

    memory = load_memory()

    home_counter = defaultdict(int)
    work_counter = defaultdict(int)
    location_counter = defaultdict(int)

    for _, row in df.iterrows():

        from_loc = row["From"]
        to_loc = row["To"]
        trip_type = row.get("Trip Type", "")

        # GENERAL FREQUENCY
        location_counter[from_loc] += 1
        location_counter[to_loc] += 1

        # HOME CANDIDATES (evenings usually)
        if "home" in from_loc.lower():
            home_counter[from_loc] += 1

        # WORK CANDIDATES
        if trip_type == "Commute":
            work_counter[to_loc] += 1

    # =================================================
    # UPDATE MEMORY SCORES
    # =================================================

    for k, v in location_counter.items():
        memory["frequent_locations"][k] = (
            memory["frequent_locations"].get(k, 0) + v
        )

    for k, v in home_counter.items():
        memory["home_candidates"][k] = (
            memory["home_candidates"].get(k, 0) + v
        )

    for k, v in work_counter.items():
        memory["work_candidates"][k] = (
            memory["work_candidates"].get(k, 0) + v
        )

    save_memory(memory)

    return memory


# =================================================
# GET BEST GUESS HOME
# =================================================

def get_best_home(memory):

    if not memory["home_candidates"]:
        return "Unknown"

    return max(
        memory["home_candidates"],
        key=memory["home_candidates"].get
    )


# =================================================
# GET BEST GUESS WORK
# =================================================

def get_best_work(memory):

    if not memory["work_candidates"]:
        return "Unknown"

    return max(
        memory["work_candidates"],
        key=memory["work_candidates"].get
    )