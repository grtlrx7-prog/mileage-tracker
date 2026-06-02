from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def analytics():

    return {
        "status": "ok",
        "message": "Analytics module ready"
    }