from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.db.models import User

router = APIRouter(
    prefix="/protected",
    tags=["protected"]
)


# =========================
# PROTECTED TEST ROUTE
# =========================
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "message": "Protected route works!",
        "user_id": current_user.id,
        "email": current_user.email
    }