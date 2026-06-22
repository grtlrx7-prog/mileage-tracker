print("===================================")
print("NEW MAIN.PY DEPLOYED")
print("VERSION 2026-06-21")
print("===================================")

from fastapi import FastAPI
import os

from backend.database.connection import engine, Base

from backend.auth.routes import router as auth_router
from backend.routes.trips import router as trips_router
from backend.routes.importer import router as importer_router
from backend.routes.exporter import router as exporter_router
from backend.routes.analytics import router as analytics_router
from backend.routes.sars import router as sars_router


# ---------------------------
# APP INITIALISATION
# ---------------------------
app = FastAPI(
    title="Mileage Tracker API",
    version="1.0.0"
)


# ---------------------------
# STARTUP EVENT (DB INIT)
# ---------------------------
@app.on_event("startup")
async def startup_event():

    print("\n===================================")
    print("APPLICATION STARTUP")
    print("===================================")

    db_url = os.getenv("DATABASE_URL")

    if db_url:
        print("DATABASE_URL FOUND")
        print(db_url[:60] + "...")
    else:
        print("DATABASE_URL NOT FOUND (using fallback SQLite)")

    print("===================================\n")

    Base.metadata.create_all(bind=engine)


# ---------------------------
# ROUTES
# ---------------------------
app.include_router(auth_router)
app.include_router(trips_router)
app.include_router(importer_router)
app.include_router(exporter_router)
app.include_router(analytics_router)
app.include_router(sars_router)


# ---------------------------
# ROOT ENDPOINT
# ---------------------------
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "mileage-tracker-api"
    }


# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }