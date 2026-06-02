from collections import defaultdict
from datetime import datetime


# ------------------------------
# TOTAL KM
# ------------------------------
def total_km(trips):
    return round(sum(t.kilometers for t in trips), 2)


# ------------------------------
# BUSINESS VS PERSONAL
# ------------------------------
def split_km(trips):
    business = sum(t.kilometers for t in trips if t.trip_type == "business")
    personal = sum(t.kilometers for t in trips if t.trip_type != "business")

    return {
        "business_km": round(business, 2),
        "personal_km": round(personal, 2)
    }


# ------------------------------
# MONTHLY ANALYTICS
# ------------------------------
def monthly_breakdown(trips):
    monthly = defaultdict(float)

    for t in trips:
        month = t.created_at.strftime("%Y-%m")
        monthly[month] += t.kilometers

    return dict(sorted(monthly.items()))


# ------------------------------
# SARS ESTIMATE (SIMPLE MODEL)
# ------------------------------
def sars_estimate(trips):
    business_km = sum(t.kilometers for t in trips if t.trip_type == "business")

    # Simplified SARS rate (you can adjust later)
    rate_per_km = 4.18

    return round(business_km * rate_per_km, 2)


# ------------------------------
# FREQUENT LOCATIONS
# ------------------------------
def frequent_locations(trips):
    locations = defaultdict(int)

    for t in trips:
        locations[t.start_location] += 1
        locations[t.end_location] += 1

    sorted_locations = sorted(
        locations.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"location": loc, "count": count}
        for loc, count in sorted_locations[:10]
    ]