from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.connection import get_db
from backend.database.models import Trip
from backend.auth.security import get_current_user

router = APIRouter(
    prefix="/sars",
    tags=["SARS"]
)

CLAIM_RATE = 4.64


@router.get("/report")
def sars_report(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

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

    total_km = business_km + personal_km

    estimated_claim = business_km * CLAIM_RATE

    return {
        "total_km": round(total_km, 2),
        "business_km": round(business_km, 2),
        "personal_km": round(personal_km, 2),
        "business_percentage": round(
            (business_km / total_km * 100),
            2
        ) if total_km > 0 else 0,
        "estimated_claim": round(
            estimated_claim,
            2
        )
    }