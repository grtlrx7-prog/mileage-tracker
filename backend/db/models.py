from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    start_location = Column(String)
    end_location = Column(String)

    kilometers = Column(Float)

    # NEW FIELD 👇
    trip_type = Column(String, default="business")  
    # values: "business" | "personal"

    created_at = Column(DateTime, default=datetime.utcnow)