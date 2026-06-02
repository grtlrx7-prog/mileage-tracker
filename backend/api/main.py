from fastapi import FastAPI
from backend.db.database import Base, engine

from backend.auth.routes import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Mileage Tracker API Running"}