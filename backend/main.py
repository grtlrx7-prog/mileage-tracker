from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.database.connection import engine, Base

from backend.auth.routes import router as auth_router
from backend.routes.trips import router as trips_router
from backend.routes.importer import router as importer_router
from backend.routes.exporter import router as exporter_router
from backend.routes.analytics import router as analytics_router
from backend.routes.sars import router as sars_router


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="Mileage Tracker API",
    description="AI Powered SARS Mileage Tracker",
    version="2.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
async def startup():

    print("\n========================================")
    print("Mileage Tracker API Started")
    print("========================================")

    db_url = os.getenv("DATABASE_URL")

    if db_url:
        print("Database Connected")
    else:
        print("WARNING: DATABASE_URL not found")

    print("========================================\n")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "application": "Mileage Tracker API",
        "status": "online",
        "version": "2.0.0"
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =====================================================
# INCLUDE ROUTERS
# IMPORTANT:
# Every router already has its own prefix.
# DO NOT ADD PREFIXES HERE.
# =====================================================

app.include_router(auth_router)

app.include_router(trips_router)

app.include_router(importer_router)

app.include_router(exporter_router)

app.include_router(analytics_router)

app.include_router(sars_router)