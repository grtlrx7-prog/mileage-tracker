from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.connection import get_db
from backend.database.models import Trip
from backend.auth.security import get_current_user

from backend.services.location_detector import detect_frequent_locations
from backend.services.location_intelligence import detect_home_and_work


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

CLAIM_RATE = 4.64


# -----------------------------------
# SUMMARY
# -----------------------------------

@router.get("/summary")
def analytics_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    total_trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .count()
    )

    total_km = (
        db.query(func.sum(Trip.kilometers))
        .filter(Trip.user_id == current_user.id)
        .scalar()
        or 0
    )

    business_km = (
        db.query(func.sum(Trip.kilometers))
        .filter(
            Trip.user_id == current_user.id,
            Trip.trip_type == "business"
        )
        .scalar()
        or 0
    )

    personal_km = (
        db.query(func.sum(Trip.kilometers))
        .filter(
            Trip.user_id == current_user.id,
            Trip.trip_type == "personal"
        )
        .scalar()
        or 0
    )

    estimated_claim = business_km * CLAIM_RATE

    return {
        "total_trips": total_trips,
        "total_km": round(total_km, 2),
        "business_km": round(business_km, 2),
        "personal_km": round(personal_km, 2),
        "estimated_claim": round(estimated_claim, 2)
    }


# -----------------------------------
# MONTHLY ANALYTICS
# -----------------------------------

@router.get("/monthly")
def monthly_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .all()
    )

    monthly_data = {}

    for trip in trips:

        month = trip.created_at.strftime("%Y-%m")

        if month not in monthly_data:
            monthly_data[month] = {
                "business_km": 0,
                "personal_km": 0
            }

        if trip.trip_type == "business":
            monthly_data[month]["business_km"] += trip.kilometers
        else:
            monthly_data[month]["personal_km"] += trip.kilometers

    results = []

    for month in sorted(monthly_data.keys()):
        results.append({
            "month": month,
            "business_km": round(monthly_data[month]["business_km"], 2),
            "personal_km": round(monthly_data[month]["personal_km"], 2)
        })

    return results


# -----------------------------------
# FREQUENT LOCATIONS
# -----------------------------------

@router.get("/frequent-locations")
def frequent_locations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .all()
    )

    return detect_frequent_locations(trips)


# -----------------------------------
# HOME & WORK INTELLIGENCE (NEW)
# -----------------------------------

@router.get("/locations/intelligence")
def location_intelligence(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .all()
    )

    return detect_home_and_work(trips)