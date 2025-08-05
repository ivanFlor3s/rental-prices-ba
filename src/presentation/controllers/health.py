from fastapi import APIRouter, status
from datetime import datetime,timezone

router = APIRouter(prefix="/health", tags=["Health"])
@router.get("", tags=["Health"],status_code= status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    utc_timestamp = datetime.now(timezone.utc)
    return {"status": "healthy", "timestamp": utc_timestamp}