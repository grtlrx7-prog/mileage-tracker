from backend.parsers.trip_builder import (
    load_positions,
    build_trips,
    reverse_geocode
)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "timeline.json"
)

df = load_positions(FILE)

trips = build_trips(df)

for trip in trips[:5]:

    from_address = reverse_geocode(
        trip["From_lat"],
        trip["From_lon"]
    )

    to_address = reverse_geocode(
        trip["To_lat"],
        trip["To_lon"]
    )

    print("\nTRIP")
    print("FROM:", from_address)
    print("TO:", to_address)
    print("DISTANCE (m):", trip["Distance_m"])