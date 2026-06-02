from collections import Counter


def detect_frequent_locations(trips):

    locations = []

    for trip in trips:

        if trip.start_location:
            locations.append(trip.start_location)

        if trip.end_location:
            locations.append(trip.end_location)

    counts = Counter(locations)

    return counts.most_common(10)