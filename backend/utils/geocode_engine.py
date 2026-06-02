from backend.utils.geocode_db import init_db, reverse_geocode


# ============================================
# INIT
# ============================================

def init_geocoder():
    init_db()


# ============================================
# EXTRACT UNIQUE COORDS
# ============================================

def extract_unique_coords(df):
    coords = set()

    for c in df["From Coordinates"]:
        if c and "," in c:
            coords.add(c)

    for c in df["To Coordinates"]:
        if c and "," in c:
            coords.add(c)

    return coords


# ============================================
# RESOLVE ALL COORDINATES
# ============================================

def resolve_coordinates(coords, progress=True):
    """
    Takes a set of 'lat,lon' strings
    returns dictionary mapping -> address
    """

    coord_map = {}

    total = len(coords)

    for i, coord in enumerate(coords):

        if progress and i % 50 == 0:
            print(f"Geocoding {i}/{total}")

        try:
            lat, lon = coord.split(",")

            address = reverse_geocode(lat, lon)

            coord_map[coord] = address

        except:
            coord_map[coord] = "Unknown"

    return coord_map


# ============================================
# FULL PIPELINE WRAPPER
# ============================================

def geocode_dataframe(df):

    coords = extract_unique_coords(df)

    print(f"Unique coordinates: {len(coords)}")

    return resolve_coordinates(coords)