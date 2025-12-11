from fastapi import APIRouter
from app.database.connection import scan_collection

router = APIRouter()

@router.get("/stats")
async def get_stats():
    # Get all scans
    all_scans = await scan_collection.find()
    
    total_scanned = len(all_scans)
    genuine = sum(1 for scan in all_scans if "PASS" in scan.get('status', ''))
    counterfeit = sum(1 for scan in all_scans if "FAIL" in scan.get('status', ''))
    
    # Calculate yield rate
    yield_rate = (genuine / total_scanned * 100) if total_scanned > 0 else 0
    
    return {
        "total_scanned": total_scanned,
        "genuine": genuine,
        "counterfeit": counterfeit,
        "yield_rate": round(yield_rate, 2)
    }

@router.get("/history")
async def get_history(page: int = 1, limit: int = 10):
    all_scans = await scan_collection.find()
    return {"scans": all_scans, "total": len(all_scans)}
