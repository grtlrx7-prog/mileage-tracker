import json
import time
from datetime import datetime

import pandas as pd
import geopy.distance

from geopy.geocoders import Nominatim


# ----------------------------
# GEOCODER
# ----------------------------
geolocator = Nominatim(user_agent="mileage_tracker")


# ----------------------------
# LOAD GPS DATA
# ----------------------------
def load_positions(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    positions = []

    for item in data["rawSignals"]:

        if "position" in item:
            pos = item["position"]

            if "LatLng" in pos:

                latlng = (
                    pos["LatLng"]
                    .replace("°", "")
                    .split(",")
                )

                lat = float(latlng[0].strip())
                lon = float(latlng[1].strip())

                positions.append({
                    "time": pos["timestamp"],
                    "lat": lat,
                    "lon": lon
                })

    return pd.DataFrame(positions)


# ----------------------------
# REVERSE GEOCODING
# ----------------------------
def reverse_geocode(lat, lon):

    try:
        location = geolocator.reverse(
            (lat, lon),
            exactly_one=True,
            addressdetails=True,
            timeout=10
        )

        if location:

            address = location.raw.get("address", {})

            road = address.get("road", "")
            house_number = address.get("house_number", "")
            suburb = address.get("suburb", "")
            city = address.get("city", "")
            town = address.get("town", "")
            village = address.get("village", "")

            area = city or town or village

            full_address = ", ".join(
                part for part in [
                    f"{house_number} {road}".strip(),
                    suburb,
                    area
                ]
                if part
            )

            return full_address

    except Exception as e:
        print("Geocoding error:", e)

    return "Unknown"


# ----------------------------
# BUILD TRIPS
# ----------------------------
def build_trips(
    df,
    threshold_meters=500,
    min_time_gap_minutes=5
):

    trips = []

    if len(df) == 0:
        return trips

    start_point = df.iloc[0]

    for i in range(1, len(df)):

        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Distance between GPS points
        dist = geopy.distance.distance(
            (prev["lat"], prev["lon"]),
            (curr["lat"], curr["lon"])
        ).meters

        # Parse timestamps
        prev_time = datetime.fromisoformat(
            prev["time"].replace("Z", "+00:00")
        )

        curr_time = datetime.fromisoformat(
            curr["time"].replace("Z", "+00:00")
        )

        # Time difference in minutes
        time_gap = (
            curr_time - prev_time
        ).total_seconds() / 60

        # Detect real trip movement
        if (
            dist > threshold_meters
            or time_gap > min_time_gap_minutes
        ):

            trips.append({
                "From_time": start_point["time"],
                "To_time": prev["time"],

                "From_lat": float(start_point["lat"]),
                "From_lon": float(start_point["lon"]),

                "To_lat": float(prev["lat"]),
                "To_lon": float(prev["lon"]),

                "Distance_m": round(dist, 2)
            })

            # Start new trip
            start_point = curr

    return trips