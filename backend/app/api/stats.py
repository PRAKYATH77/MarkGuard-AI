from fastapi import APIRouter

router = APIRouter()

@router.get("/history")
async def get_history(page: int = 1, limit: int = 10):
    return {"scans": [], "total": 0}
