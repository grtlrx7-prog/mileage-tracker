from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
import os

from backend.db.database import SessionLocal
from backend.db.models import Trip
from backend.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/excel")
def export_excel(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    trips = db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).all()

    if not trips:
        return {"message": "No trips found"}

    data = []

    for t in trips:
        data.append({
            "Date": t.created_at.strftime("%Y-%m-%d"),
            "Start Location": t.start_location,
            "End Location": t.end_location,
            "Kilometers": t.kilometers
        })

    df = pd.DataFrame(data)

    # Create exports folder if not exists
    os.makedirs("backend/exports", exist_ok=True)

    file_path = "backend/exports/sars_logbook.xlsx"

    df.to_excel(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename="SARS_Logbook.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )