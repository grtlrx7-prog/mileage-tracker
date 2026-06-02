from pydantic import BaseModel

class TripCreate(BaseModel):
    start_location: str
    end_location: str
    kilometers: float
    trip_type: str = "business"