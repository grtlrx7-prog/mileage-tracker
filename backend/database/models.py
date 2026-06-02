from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database.connection import Base


# -----------------------------------
# USER MODEL
# -----------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    trips = relationship(
        "Trip",
        back_populates="user"
    )


# -----------------------------------
# TRIP MODEL
# -----------------------------------

class Trip(Base):

    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    start_location = Column(
        String,
        nullable=False
    )

    end_location = Column(
        String,
        nullable=False
    )

    kilometers = Column(
        Float,
        nullable=False
    )

    trip_type = Column(
        String,
        default="business"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="trips"
    )