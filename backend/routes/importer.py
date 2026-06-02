from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import json

from backend.database.connection import get_db
from backend.database.models import Trip
from backend.auth.security import get_current_user

from backend.services.classifier import classify_trip
from backend.services.google_takeout_parser import extract_trips

router = APIRouter(
    prefix="/import",
    tags=["Import"]
)


# -----------------------------------
# GOOGLE TIMELINE IMPORT
# -----------------------------------

@router.post("/google-timeline")
def import_google_timeline(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:
        content = file.file.read()

        data = json.loads(content)

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid JSON file"
        )

    parsed_trips = extract_trips(data)

    trips_added = 0

    for trip_data in parsed_trips:

        trip_type = classify_trip(
            trip_data["start_location"],
            trip_data["end_location"]
        )

        trip = Trip(
            user_id=current_user.id,
            start_location=trip_data["start_location"],
            end_location=trip_data["end_location"],
            kilometers=trip_data["kilometers"],
            trip_type=trip_type
        )

        db.add(trip)

        trips_added += 1

    db.commit()

    return {
        "message": "Import complete",
        "trips_added": trips_added
    }