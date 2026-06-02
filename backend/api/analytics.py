from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from backend.db.database import SessionLocal
from backend.db.models import Trip

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# =================================================
# DB SESSION
# =================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =================================================
# SUMMARY DASHBOARD
# =================================================

@router.get("/summary")
def summary(db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    total_km = sum(t.km for t in trips)
    total_trips = len(trips)

    business_km = sum(t.km for t in trips if t.trip_type == "Business")
    personal_km = sum(t.km for t in trips if t.trip_type == "Personal")

    return {
        "total_trips": total_trips,
        "total_km": round(total_km, 2),
        "business_km": round(business_km, 2),
        "personal_km": round(personal_km, 2),
    }


# =================================================
# MONTHLY BREAKDOWN
# =================================================

@router.get("/monthly")
def monthly(db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    monthly_map = defaultdict(lambda: {"km": 0, "trips": 0})

    for t in trips:

        month = t.start_time.strftime("%B")

        monthly_map[month]["km"] += t.km
        monthly_map[month]["trips"] += 1

    return monthly_map


# =================================================
# BUSINESS VS PERSONAL RATIO
# =================================================

@router.get("/split")
def split(db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    business = sum(t.km for t in trips if t.trip_type == "Business")
    personal = sum(t.km for t in trips if t.trip_type == "Personal")

    total = business + personal

    if total == 0:
        return {"business_pct": 0, "personal_pct": 0}

    return {
        "business_pct": round((business / total) * 100, 2),
        "personal_pct": round((personal / total) * 100, 2),
    }


# =================================================
# RISK ANALYSIS (AI READY)
# =================================================

@router.get("/risk")
def risk(db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    low = 0
    medium = 0
    high = 0

    for t in trips:

        level = (t.risk_level or "").upper()

        if level == "LOW":
            low += 1
        elif level == "MEDIUM":
            medium += 1
        else:
            high += 1

    return {
        "low_risk": low,
        "medium_risk": medium,
        "high_risk": high,
    }


# =================================================
# TOP LOCATIONS
# =================================================

@router.get("/top-locations")
def top_locations(db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    freq = defaultdict(int)

    for t in trips:
        freq[t.from_location] += 1
        freq[t.to_location] += 1

    sorted_locations = sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "top_locations": sorted_locations[:10]
    }