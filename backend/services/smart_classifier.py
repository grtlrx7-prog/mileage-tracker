from collections import Counter


class SmartTripClassifier:

    def __init__(self, trips):

        self.trips = trips

        self.location_counts = Counter()
        self.route_counts = Counter()

        self.home = None
        self.work = None

        self._analyze()

    # -----------------------------------
    # ANALYZE HISTORY
    # -----------------------------------

    def _analyze(self):

        morning_counts = Counter()
        evening_counts = Counter()

        for trip in self.trips:

            start = (trip.start_location or "").lower()
            end = (trip.end_location or "").lower()

            self.location_counts[start] += 1
            self.location_counts[end] += 1

            self.route_counts[(start, end)] += 1

            hour = trip.created_at.hour

            # HOME detection (morning departures)
            if 5 <= hour <= 9:
                morning_counts[start] += 1

            # HOME return (evening arrivals)
            if 17 <= hour <= 23:
                evening_counts[end] += 1

        # Most likely HOME
        if morning_counts:
            self.home = morning_counts.most_common(1)[0][0]

        # Most frequent location = WORK
        if self.location_counts:
            self.work = self.location_counts.most_common(1)[0][0]

    # -----------------------------------
    # CLASSIFY NEW TRIP
    # -----------------------------------

    def classify(self, start_location, end_location):

        start = (start_location or "").lower()
        end = (end_location or "").lower()

        # RULE 1: HOME → WORK
        if start == self.home and end == self.work:
            return "business"

        # RULE 2: WORK → HOME
        if start == self.work and end == self.home:
            return "business"

        # RULE 3: REPEATED CLIENT ROUTES
        if self.route_counts[(start, end)] > 2:
            return "business"

        # DEFAULT
        return "personal"