from pydantic import BaseModel
from datetime import datetime


class TripCreate(BaseModel):
    start_location: str
    end_location: str
    kilometers: float


class TripResponse(BaseModel):
    id: int
    start_location: str
    end_location: str
    kilometers: float
    created_at: datetime

    class Config:
        from_attributes = True