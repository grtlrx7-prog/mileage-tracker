import json
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

CACHE_FILE = "backend/data/address_cache.json"
EXCEL_FILE = "backend/exports/mileage_logbook.xlsx"

geolocator = Nominatim(
    user_agent="mileage_tracker",
    timeout=10
)


# ============================================
# LOAD CACHE
# ============================================

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    cache = json.load(f)


# ============================================
# SMART LOOKUP
# ============================================

def lookup(latlng):

    try:

        if not latlng:
            return "Unknown"

        latlng = str(latlng)

        latlng = latlng.replace("°", "")
        latlng = latlng.replace(" ", "")

        parts = latlng.split(",")

        if len(parts) != 2:
            return "Unknown"

        lat = float(parts[0])
        lon = float(parts[1])

        key = f"{lat:.6f},{lon:.6f}"

        # ====================================
        # CACHE FIRST
        # ====================================

        cached = cache.get(key)

        if cached and cached != "Unknown":
            return cached

        # ====================================
        # MULTI-RETRY ENGINE
        # ====================================

        for attempt in range(3):

            try:

                print(
                    f"Lookup attempt "
                    f"{attempt+1}: {key}"
                )

                location = geolocator.reverse(
                    (lat, lon),
                    exactly_one=True,
                    addressdetails=True,
                    timeout=10
                )

                if not location:
                    sleep(2)
                    continue

                addr = location.raw.get("address", {})

                # ====================================
                # BROADER FIELD EXTRACTION
                # ====================================

                house = addr.get("house_number", "")

                road = (
                    addr.get("road")
                    or addr.get("residential")
                    or addr.get("pedestrian")
                    or ""
                )

                suburb = (
                    addr.get("suburb")
                    or addr.get("neighbourhood")
                    or addr.get("quarter")
                    or ""
                )

                city = (
                    addr.get("city")
                    or addr.get("town")
                    or addr.get("village")
                    or addr.get("municipality")
                    or ""
                )

                county = addr.get("county", "")

                state = addr.get("state", "")

                postcode = addr.get("postcode", "")

                country = addr.get("country", "")

                parts = [
                    house,
                    road,
                    suburb,
                    city,
                    county,
                    state,
                    postcode,
                    country
                ]

                full = ", ".join(
                    p for p in parts if p
                )

                # ====================================
                # FALLBACK MODE
                # ====================================

                if len(full.strip()) < 5:

                    broader = ", ".join(
                        p for p in [
                            suburb,
                            city,
                            state,
                            country
                        ] if p
                    )

                    if broader:
                        full = broader

                if len(full.strip()) < 5:
                    sleep(2)
                    continue

                # ====================================
                # SAVE CACHE
                # ====================================

                cache[key] = full

                sleep(1)

                return full

            except:

                sleep(2)

        return "Unknown"

    except:
        return "Unknown"


# ============================================
# LOAD EXCEL
# ============================================

print("Loading Excel...")

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Trips"
)

print("Rows:", len(df))


# ============================================
# RECOVERY
# ============================================

recovered = 0

for i, row in df.iterrows():

    # ========================================
    # FROM
    # ========================================

    if row["From"] == "Unknown":

        print(f"\nRecovering FROM row {i}")

        new_addr = lookup(
            row["From Coordinates"]
        )

        if new_addr != "Unknown":

            df.at[i, "From"] = new_addr

            recovered += 1

            print("Recovered:", new_addr)

    # ========================================
    # TO
    # ========================================

    if row["To"] == "Unknown":

        print(f"\nRecovering TO row {i}")

        new_addr = lookup(
            row["To Coordinates"]
        )

        if new_addr != "Unknown":

            df.at[i, "To"] = new_addr

            recovered += 1

            print("Recovered:", new_addr)


# ============================================
# SAVE CACHE
# ============================================

with open(CACHE_FILE, "w", encoding="utf-8") as f:

    json.dump(cache, f, indent=2)


# ============================================
# SAVE EXCEL
# ============================================

print("\nSaving repaired Excel...")

with pd.ExcelWriter(
    EXCEL_FILE,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Trips",
        index=False
    )

print("\n===================================")
print("RECOVERY COMPLETE")
print("===================================")

print(f"Recovered addresses: {recovered}")

print("DONE ✔")