from fastapi import APIRouter, status
from datetime import datetime,timezone

from src.application.use_cases.scrapper_health import ScrapperHealthCheckUseCase

router = APIRouter(prefix="/health", tags=["Health"])
@router.get("", tags=["Health"],status_code= status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    utc_timestamp = datetime.now(timezone.utc)
    return {"status": "healthy", "timestamp": utc_timestamp}

@router.get("/scrapper", tags=["Health"], status_code=status.HTTP_200_OK)
async def scrapper_health_check():
    """Endpoint for verifying DOM selectors are working correctly."""
    use_case = ScrapperHealthCheckUseCase()
    health_report = use_case.check_zonaprop_health()
    return health_report