from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
async def get_stats():
    return {"total_scanned": 0, "genuine": 0, "counterfeit": 0, "yield_rate": 0}
