from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Trip
from backend.auth.security import get_current_user

import io
from openpyxl import Workbook


router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


CLAIM_RATE = 4.64


# -----------------------------------
# XLSX EXPORT (SARS READY)
# -----------------------------------

@router.get("/xlsx")
def export_xlsx(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    trips = (
        db.query(Trip)
        .filter(Trip.user_id == current_user.id)
        .all()
    )

    wb = Workbook()

    # --------------------------
    # SHEET 1: TRIPS
    # --------------------------
    ws = wb.active
    ws.title = "Trips"

    ws.append([
        "Date",
        "Start Location",
        "End Location",
        "Distance (KM)",
        "Trip Type"
    ])

    total_km = 0
    business_km = 0
    personal_km = 0

    for trip in trips:

        ws.append([
            trip.created_at.strftime("%Y-%m-%d"),
            trip.start_location,
            trip.end_location,
            round(trip.kilometers, 2),
            trip.trip_type
        ])

        total_km += trip.kilometers

        if trip.trip_type == "business":
            business_km += trip.kilometers
        else:
            personal_km += trip.kilometers

    # --------------------------
    # SHEET 2: SUMMARY
    # --------------------------
    summary = wb.create_sheet("Summary")

    summary.append(["Metric", "Value"])
    summary.append(["Total KM", round(total_km, 2)])
    summary.append(["Business KM", round(business_km, 2)])
    summary.append(["Personal KM", round(personal_km, 2)])
    summary.append([
        "Estimated SARS Claim",
        round(business_km * CLAIM_RATE, 2)
    ])

    # --------------------------
    # RETURN FILE
    # --------------------------
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            "attachment; filename=sars_logbook.xlsx"
        }
    )