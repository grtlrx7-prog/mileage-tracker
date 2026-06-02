from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User
from backend.auth.security import verify_password, create_access_token
from backend.auth.security import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# REGISTER USER (MISSING BEFORE)
# -----------------------------
@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=username,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


# -----------------------------
# LOGIN USER
# -----------------------------
@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }