from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal
from backend.db.models import Trip

router = APIRouter(prefix="/trips", tags=["Trips V2"])


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
# PAGINATED + FILTERED TRIPS
# =================================================

@router.get("/")
def get_trips(
    db: Session = Depends(get_db),

    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),

    trip_type: str = None,
    purpose: str = None
):

    query = db.query(Trip)

    # FILTER: trip type
    if trip_type:
        query = query.filter(Trip.trip_type == trip_type)

    # FILTER: purpose
    if purpose:
        query = query.filter(Trip.purpose == purpose)

    total = query.count()

    trips = (
        query
        .order_by(Trip.start_time.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "returned": len(trips),
        "data": trips
    }


# =================================================
# SEARCH TRIPS (FAST FILTER)
# =================================================

@router.get("/search")
def search_trips(
    db: Session = Depends(get_db),
    q: str = Query(...)
):

    trips = db.query(Trip).filter(
        (Trip.from_location.contains(q)) |
        (Trip.to_location.contains(q))
    ).limit(100).all()

    return {
        "query": q,
        "results": len(trips),
        "data": trips
    }


# =================================================
# DATE RANGE FILTER
# =================================================

@router.get("/date-range")
def date_range(
    db: Session = Depends(get_db),
    start: str = Query(...),
    end: str = Query(...)
):

    trips = db.query(Trip).filter(
        Trip.start_time >= start,
        Trip.start_time <= end
    ).order_by(Trip.start_time.desc()).all()

    return {
        "start": start,
        "end": end,
        "count": len(trips),
        "data": trips
    }


# =================================================
# MAP DATA ENDPOINT (FOR FRONTEND MAPS)
# =================================================

@router.get("/map")
def map_data(db: Session = Depends(get_db)):

    trips = db.query(Trip).limit(2000).all()

    points = []

    for t in trips:

        points.append({
            "from": t.from_location,
            "to": t.to_location,
            "km": t.km,
            "type": t.trip_type
        })

    return {
        "count": len(points),
        "data": points
    }