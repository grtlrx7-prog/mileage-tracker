import requests


# ==========================================
# YOUR OPENROUTESERVICE API KEY
# ==========================================
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjBmZDFiMjUxZWJjYTRkYzViMDc4YWI3NjcwYzczYjdmIiwiaCI6Im11cm11cjY0In0="


# ==========================================
# GET COORDINATES
# ==========================================
def get_coordinates(location: str):

    url = "https://api.openrouteservice.org/geocode/search"

    headers = {
        "Authorization": API_KEY
    }

    params = {
        "text": location,
        "boundary.country": "ZA",
        "size": 1
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        print("GEOCODE STATUS:", response.status_code)
        print("GEOCODE RESPONSE:", response.text)

        if response.status_code != 200:
            return None

        data = response.json()

        features = data.get("features")

        if not features:
            return None

        coords = features[0]["geometry"]["coordinates"]

        return coords

    except Exception as e:

        print("GEOCODE ERROR:", str(e))

        return None


# ==========================================
# GET DISTANCE
# ==========================================
def get_distance_km(
    start_location: str,
    end_location: str
):

    start_coords = get_coordinates(start_location)

    end_coords = get_coordinates(end_location)

    print("START COORDS:", start_coords)
    print("END COORDS:", end_coords)

    if not start_coords or not end_coords:
        return None

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start_coords,
            end_coords
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=20
        )

        print("ROUTE STATUS:", response.status_code)
        print("ROUTE RESPONSE:", response.text)

        if response.status_code != 200:
            return None

        data = response.json()

        routes = data.get("routes")

        if not routes:
            return None

        meters = routes[0]["summary"]["distance"]

        km = round(meters / 1000, 2)

        return km

    except Exception as e:

        print("ROUTING ERROR:", str(e))

        return None