from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal
from backend.db.models import Trip

router = APIRouter(prefix="/trips", tags=["Trips"])


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
# GET ALL TRIPS
# =================================================

@router.get("/")
def get_trips(db: Session = Depends(get_db)):

    trips = db.query(Trip).order_by(Trip.start_time.desc()).all()

    return {
        "count": len(trips),
        "data": trips
    }


# =================================================
# GET SINGLE TRIP
# =================================================

@router.get("/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip


# =================================================
# DELETE TRIP
# =================================================

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    db.delete(trip)
    db.commit()

    return {
        "status": "deleted",
        "trip_id": trip_id
    }


# =================================================
# UPDATE TRIP (EDIT)
# =================================================

@router.put("/{trip_id}")
def update_trip(trip_id: int, payload: dict, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for key, value in payload.items():
        if hasattr(trip, key):
            setattr(trip, key, value)

    db.commit()
    db.refresh(trip)

    return {
        "status": "updated",
        "trip": trip
    }