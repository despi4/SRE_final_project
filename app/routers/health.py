from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Service health check")
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", timestamp=datetime.now(timezone.utc))
