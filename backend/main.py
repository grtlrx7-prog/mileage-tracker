from fastapi import FastAPI
import os

from backend.database.connection import engine
from backend.database.models import Base

from backend.auth.routes import router as auth_router
from backend.routes.trips import router as trips_router
from backend.routes.importer import router as importer_router
from backend.routes.exporter import router as exporter_router
from backend.routes.analytics import router as analytics_router
from backend.routes.sars import router as sars_router


app = FastAPI(
    title="Mileage Tracker API",
    version="1.0.0"
)


# ---------------------------
# DB INIT (SAFE VERSION)
# ---------------------------
# ⚠️ Only runs when app starts, not on import crash-prone reload loops
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# ---------------------------
# ROUTES
# ---------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(trips_router, prefix="/trips", tags=["Trips"])
app.include_router(importer_router, prefix="/import", tags=["Import"])
app.include_router(exporter_router, prefix="/export", tags=["Export"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(sars_router, prefix="/sars", tags=["SARS"])


# ---------------------------
# API ROOT
# ---------------------------
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "mileage-tracker-api"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}