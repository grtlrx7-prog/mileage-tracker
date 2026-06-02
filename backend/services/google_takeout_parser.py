import json


def extract_trips(data):

    trips = []

    # New Google Timeline format
    if "semanticSegments" in data:

        for item in data["semanticSegments"]:

            activity = item.get("activitySegment")

            if not activity:
                continue

            distance = activity.get(
                "distanceMeters",
                0
            )

            if distance <= 0:
                continue

            start_location = str(
                activity.get(
                    "startLocation",
                    {}
                )
            )

            end_location = str(
                activity.get(
                    "endLocation",
                    {}
                )
            )

            trips.append({
                "start_location": start_location,
                "end_location": end_location,
                "kilometers": distance / 1000
            })

    return trips