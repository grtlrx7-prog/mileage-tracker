import re


class SelfHealingEngine:

    def __init__(self):

        self.failed_coords = 0

        self.fixed_coords = 0

    # =================================================
    # FIX COORDINATES
    # =================================================

    def fix_latlng(self, latlng):

        try:

            if not latlng:
                self.failed_coords += 1
                return None

            # =========================================
            # DICT FORMAT
            # =========================================

            if isinstance(latlng, dict):

                lat = None
                lng = None

                if "latitude" in latlng and "longitude" in latlng:

                    lat = latlng["latitude"]
                    lng = latlng["longitude"]

                elif "latitudeE7" in latlng and "longitudeE7" in latlng:

                    lat = latlng["latitudeE7"] / 1e7
                    lng = latlng["longitudeE7"] / 1e7

                if lat is not None and lng is not None:

                    self.fixed_coords += 1

                    return {
                        "latitude": float(lat),
                        "longitude": float(lng)
                    }

            # =========================================
            # STRING FORMAT
            # =========================================

            if isinstance(latlng, str):

                nums = re.findall(r"-?\d+\.\d+", latlng)

                if len(nums) >= 2:

                    self.fixed_coords += 1

                    return {
                        "latitude": float(nums[0]),
                        "longitude": float(nums[1])
                    }

            self.failed_coords += 1
            return None

        except:

            self.failed_coords += 1
            return None

    # =================================================
    # FIX ADDRESS
    # =================================================

    def fix_address(self, address):

        try:

            if not address:
                return "Unknown"

            address = str(address).strip()

            # remove garbage numbers
            address = re.sub(r"\b\d{4,}\b", "", address)

            # clean double spaces
            address = re.sub(r"\s+", " ", address)

            return address.strip()

        except:

            return "Unknown"

    # =================================================
    # HEALTH REPORT
    # =================================================

    def report(self):

        return {
            "fixed_coords": self.fixed_coords,
            "failed_coords": self.failed_coords
        }