from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.db.database import SessionLocal
from backend.db.models import User
from backend.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


# =========================
# REQUEST MODELS
# =========================

class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }