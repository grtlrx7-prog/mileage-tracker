from collections import Counter
from datetime import datetime


# -----------------------------------
# DETECT HOME & WORK LOCATIONS
# -----------------------------------

def detect_home_and_work(trips):

    location_counter = Counter()

    morning_locations = Counter()
    evening_locations = Counter()

    for trip in trips:

        start = (trip.start_location or "").lower()
        end = (trip.end_location or "").lower()

        location_counter[start] += 1
        location_counter[end] += 1

        # Try to infer patterns based on time of day
        hour = trip.created_at.hour

        # Morning (likely leaving home)
        if 5 <= hour <= 9:
            morning_locations[start] += 1

        # Evening (likely returning home)
        if 17 <= hour <= 23:
            evening_locations[end] += 1

    # Most common morning start = HOME
    home = morning_locations.most_common(1)

    # Most common destination = WORK
    work = location_counter.most_common(1)

    return {
        "home": home[0][0] if home else None,
        "work": work[0][0] if work else None
    }