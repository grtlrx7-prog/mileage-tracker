from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
# DB INIT
# ---------------------------
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
# API ROOT
# ---------------------------
@app.get("/api")
def root():
    return {"status": "online"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# ---------------------------
# STATIC FRONTEND (SAFE)
# ---------------------------
if os.path.exists("backend/static"):
    app.mount(
        "/",
        StaticFiles(directory="backend/static", html=True),
        name="static"
    )


# ---------------------------
# LOCAL RUN ONLY
# ---------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )