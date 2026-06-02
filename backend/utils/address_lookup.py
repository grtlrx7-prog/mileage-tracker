import time
from functools import lru_cache
from geopy.geocoders import Nominatim

from backend.utils.db import conn


geolocator = Nominatim(user_agent="mileage_tracker")

COMMON_LOCATIONS = {
    "-26.1094,27.8958": "Home",
}


# ============================================
# EXTRACT COORDS
# ============================================

def extract_coords(latlng):

    try:
        if not latlng:
            return None, None

        latlng = str(latlng)

        if "°" not in latlng:
            return None, None

        latlng_clean = latlng.replace("°", "").split(",")

        lat = round(float(latlng_clean[0].strip()), 4)
        lon = round(float(latlng_clean[1].strip()), 4)

        return lat, lon

    except:
        return None, None


# ============================================
# MEMORY CACHE (FAST LAYER)
# ============================================

@lru_cache(maxsize=100000)
def fast_cache(key):
    return None


# ============================================
# GET ADDRESS
# ============================================

def get_address(latlng):

    lat, lon = extract_coords(latlng)

    if lat is None:
        return "Unknown"

    key = f"{lat},{lon}"

    # --------------------------------------------
    # 1. hardcoded locations
    # --------------------------------------------
    if key in COMMON_LOCATIONS:
        return COMMON_LOCATIONS[key]

    # --------------------------------------------
    # 2. SQLite cache
    # --------------------------------------------
    cur = conn.cursor()

    cur.execute(
        "SELECT address FROM address_cache WHERE key=?",
        (key,)
    )

    row = cur.fetchone()

    if row:
        result = row[0]
        fast_cache(key)
        return result

    # --------------------------------------------
    # 3. LIVE GEOCODING (slow path)
    # --------------------------------------------

    location = None

    for attempt in range(3):
        try:
            location = geolocator.reverse(
                (lat, lon),
                exactly_one=True,
                timeout=10
            )

            if location:
                break

        except Exception:
            time.sleep(2)

    if not location:
        return key

    addr = location.raw.get("address", {})

    road = addr.get("road", "")
    suburb = addr.get("suburb", "")

    city = (
        addr.get("city") or
        addr.get("town") or
        addr.get("village") or
        ""
    )

    short = ", ".join(x for x in [road, suburb, city] if x)

    if not short:
        short = key

    # save to DB
    cur.execute(
        "INSERT OR REPLACE INTO address_cache VALUES (?, ?)",
        (key, short)
    )

    conn.commit()

    time.sleep(1.1)

    return short