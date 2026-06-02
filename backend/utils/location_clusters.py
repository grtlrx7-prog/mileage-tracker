from collections import defaultdict


class LocationClusterer:

    def __init__(self, radius_km=0.8):

        # Not used for now, but reserved for future geo clustering
        self.radius_km = radius_km

        # Stores how often each address appears
        self.location_counts = defaultdict(int)

        # Stores raw history if you want to extend later
        self.history = []

    # =================================================
    # CORE LEARNING FUNCTION (FIX FOR YOUR ERROR)
    # =================================================

    def learn_location(self, address):

        try:

            if not address:
                return

            address = str(address).strip()

            if len(address) < 3:
                return

            self.location_counts[address] += 1

            self.history.append(address)

        except Exception as e:

            print("LocationClusterer learn_location error:", e)

    # =================================================
    # FREQUENCY SCORE
    # =================================================

    def get_location_score(self, address):

        try:

            if not address:
                return 0

            return self.location_counts.get(address, 0)

        except:

            return 0

    # =================================================
    # TOP LOCATIONS
    # =================================================

    def get_top_locations(self, limit=10):

        try:

            sorted_locations = sorted(

                self.location_counts.items(),

                key=lambda x: x[1],

                reverse=True

            )

            return sorted_locations[:limit]

        except Exception as e:

            print("get_top_locations error:", e)

            return []

    # =================================================
    # HOTSPOT DETECTION
    # =================================================

    def is_hotspot(self, address):

        try:

            if not address:
                return False

            return self.get_location_score(address) >= 20

        except:

            return False

    # =================================================
    # CLEAR DATA (OPTIONAL RESET)
    # =================================================

    def reset(self):

        self.location_counts.clear()

        self.history.clear()