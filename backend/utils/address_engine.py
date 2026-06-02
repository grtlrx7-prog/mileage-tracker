import requests
import time
import re

from backend.utils.clean_geo_cache import (
    load_clean_cache,
    get_cached_address,
    set_cached_address,
    save_clean_cache
)

from backend.utils.address_database import (
    load_database,
    save_database,
    get_database_address,
    set_database_address
)


# =================================================
# LOAD SYSTEMS
# =================================================

load_clean_cache()

load_database()


# =================================================
# CLEAN ADDRESS
# =================================================

def clean_address(raw):

    try:

        if not raw:
            return "Unknown"

        parts = raw.split(",")

        cleaned = []

        for p in parts:

            p = p.strip()

            # Remove postal codes
            if re.search(r"\d{4,}", p):
                continue

            # Remove tiny junk
            if len(p) < 2:
                continue

            # Remove duplicates
            if p not in cleaned:
                cleaned.append(p)

        return ", ".join(cleaned[:5])

    except Exception:

        return raw


# =================================================
# UNIVERSAL COORDINATE PARSER
# =================================================

def normalize_latlng(latlng):

    try:

        if not latlng:
            return None, None

        # =========================================
        # DICT FORMAT
        # =========================================

        if isinstance(latlng, dict):

            # NORMAL FLOAT FORMAT
            if (
                "latitude" in latlng
                and "longitude" in latlng
            ):

                return (
                    float(latlng["latitude"]),
                    float(latlng["longitude"])
                )

            # GOOGLE E7 FORMAT
            if (
                "latitudeE7" in latlng
                and "longitudeE7" in latlng
            ):

                return (
                    latlng["latitudeE7"] / 1e7,
                    latlng["longitudeE7"] / 1e7
                )

        # =========================================
        # STRING FORMAT
        # =========================================

        if isinstance(latlng, str):

            # Remove degree symbols
            cleaned = (
                latlng
                .replace("°", "")
                .replace(" ", "")
            )

            # Format:
            # -26.123,27.456

            if "," in cleaned:

                parts = cleaned.split(",")

                if len(parts) == 2:

                    return (
                        float(parts[0]),
                        float(parts[1])
                    )

        return None, None

    except Exception:

        return None, None


# =================================================
# OPENSTREETMAP LOOKUP
# =================================================

def osm_reverse(lat, lng):

    try:

        res = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "format": "json",
                "lat": lat,
                "lon": lng,
                "zoom": 18,
                "addressdetails": 1
            },
            headers={
                "User-Agent": "sars-logbook-app"
            },
            timeout=10
        )

        time.sleep(1)

        if res.status_code != 200:

            print(
                "OSM ERROR:",
                res.status_code
            )

            return None

        data = res.json()

        # =========================================
        # DISPLAY NAME
        # =========================================

        if data.get("display_name"):

            return data["display_name"]

        # =========================================
        # STRUCTURED ADDRESS
        # =========================================

        if "address" in data:

            addr = data["address"]

            parts = [

                addr.get("road"),

                addr.get("suburb"),

                addr.get("city"),

                addr.get("town"),

                addr.get("county"),

                addr.get("state"),

                addr.get("country")
            ]

            parts = [
                p for p in parts if p
            ]

            if parts:

                return ", ".join(parts)

        return None

    except Exception as e:

        print("OSM LOOKUP ERROR:", e)

        return None


# =================================================
# MAIN ADDRESS ENGINE
# =================================================

def get_address(latlng):

    try:

        # =========================================
        # NORMALIZE
        # =========================================

        lat, lng = normalize_latlng(latlng)

        if lat is None or lng is None:

            return "Unknown"

        # =========================================
        # CACHE KEY
        # =========================================

        key = f"{round(lat, 5)},{round(lng, 5)}"

        # =========================================
        # FAST CACHE
        # =========================================

        cached = get_cached_address(key)

        if cached:

            return cached

        # =========================================
        # DATABASE CACHE
        # =========================================

        db_address = get_database_address(key)

        if db_address:

            return db_address

        # =========================================
        # LIVE LOOKUP
        # =========================================

        address = osm_reverse(lat, lng)

        # Fallback to coordinates
        if not address:

            address = f"{lat}, {lng}"

        # =========================================
        # CLEAN ADDRESS
        # =========================================

        final = clean_address(address)

        # =========================================
        # SAVE MEMORY CACHE
        # =========================================

        set_cached_address(key, final)

        save_clean_cache()

        # =========================================
        # SAVE DATABASE
        # =========================================

        set_database_address(key, final)

        save_database()

        return final

    except Exception as e:

        print("ADDRESS ENGINE ERROR:", e)

        return "Unknown"