from fastapi import APIRouter, Depends

from backend.db.database import SessionLocal
from backend.db.models import Trip

from backend.auth.dependencies import get_current_user

router = APIRouter()


# =========================
# GET USER TRIPS
# =========================

@router.get("/")
def get_trips(current_user = Depends(get_current_user)):

    db = SessionLocal()

    trips = db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).all()

    return [
        {
            "id": t.id,
            "date": t.date,
            "from_location": t.from_location,
            "to_location": t.to_location,
            "km": t.km,
            "trip_type": t.trip_type,
            "purpose": t.purpose
        }
        for t in trips
    ]