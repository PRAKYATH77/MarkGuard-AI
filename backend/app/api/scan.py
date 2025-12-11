from fastapi import APIRouter

router = APIRouter()

@router.post("/scan-ic")
async def scan_ic(file: bytes, part_number: str):
    return {"status": "success", "message": "Scan processing"}
