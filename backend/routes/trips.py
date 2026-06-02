from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Trip
from backend.auth.security import get_current_user

from backend.services.smart_classifier import SmartTripClassifier


router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


# -----------------------------------
# CREATE TRIP (AI CLASSIFIED)
# -----------------------------------

@router.post("/create")
def create_trip(
    start_location: str,
    end_location: str,
    kilometers: float,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # -----------------------------------
    # LOAD USER HISTORY
    # -----------------------------------

    past_trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .all()
    )

    # -----------------------------------
    # INITIALISE AI CLASSIFIER
    # -----------------------------------

    classifier = SmartTripClassifier(past_trips)

    trip_type = classifier.classify(
        start_location=start_location,
        end_location=end_location
    )

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not start_location or not end_location:
        raise HTTPException(
            status_code=400,
            detail="Start and end location are required"
        )

    if kilometers <= 0:
        raise HTTPException(
            status_code=400,
            detail="Kilometers must be greater than 0"
        )

    # -----------------------------------
    # CREATE TRIP
    # -----------------------------------

    new_trip = Trip(
        user_id=current_user.id,
        start_location=start_location,
        end_location=end_location,
        kilometers=kilometers,
        trip_type=trip_type
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    return {
        "message": "Trip created successfully",
        "trip": {
            "id": new_trip.id,
            "start_location": new_trip.start_location,
            "end_location": new_trip.end_location,
            "kilometers": new_trip.kilometers,
            "trip_type": new_trip.trip_type
        },
        "ai_classification_used": True
    }