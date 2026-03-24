from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/", summary="Health check")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Business Insights",
    }


@router.get("/ready", summary="Readiness probe")
async def readiness():
    return {"ready": True}
