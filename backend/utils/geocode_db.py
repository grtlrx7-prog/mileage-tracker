import sqlite3
from geopy.geocoders import Nominatim
from time import sleep

DB_PATH = "backend/data/geocache.db"

geolocator = Nominatim(user_agent="mileage_tracker")


# ============================================
# INIT DATABASE
# ============================================

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS geocache (
        lat TEXT,
        lon TEXT,
        address TEXT,
        PRIMARY KEY (lat, lon)
    )
    """)

    conn.commit()
    conn.close()


# ============================================
# GET CACHED ADDRESS
# ============================================

def get_cached(lat, lon):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        "SELECT address FROM geocache WHERE lat=? AND lon=?",
        (lat, lon)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


# ============================================
# SAVE ADDRESS
# ============================================

def save_address(lat, lon, address):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO geocache (
        lat,
        lon,
        address
    )
    VALUES (?, ?, ?)
    """, (lat, lon, address))

    conn.commit()
    conn.close()


# ============================================
# REVERSE GEOCODE
# ============================================

def reverse_geocode(lat, lon):

    cached = get_cached(lat, lon)

    if cached:
        return cached

    try:

        location = geolocator.reverse(
            (lat, lon),
            exactly_one=True,
            addressdetails=True,
            timeout=10
        )

        if not location:
            return "Unknown"

        addr = location.raw.get("address", {})

        city = (
            addr.get("city")
            or addr.get("town")
            or addr.get("village")
            or ""
        )

        full = ", ".join(
            part for part in [
                addr.get("road", ""),
                addr.get("suburb", ""),
                city,
                addr.get("postcode", "")
            ] if part
        )

        if not full:
            full = "Unknown"

        save_address(lat, lon, full)

        sleep(1)

        return full

    except:
        return "Unknown"