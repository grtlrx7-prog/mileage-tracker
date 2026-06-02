from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.db.database import SessionLocal
from backend.db.models import Trip
from backend.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def dashboard_summary(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    trips = db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).all()

    total_km = sum(t.kilometers for t in trips)

    # SARS rate (you can update this yearly)
    SARS_RATE = 4.84
    estimated_claim = total_km * SARS_RATE

    return {
        "total_trips": len(trips),
        "total_kilometers": round(total_km, 2),
        "estimated_sars_claim": round(estimated_claim, 2)
    }


@router.get("/monthly")
def monthly_breakdown(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    trips = db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).all()

    monthly = {}

    for trip in trips:
        month = trip.created_at.strftime("%Y-%m")

        if month not in monthly:
            monthly[month] = {
                "trips": 0,
                "kilometers": 0.0
            }

        monthly[month]["trips"] += 1
        monthly[month]["kilometers"] += trip.kilometers

    return monthly