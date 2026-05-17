from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_analytics_service
from app.schemas.analytics import AnalyticsSampleResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

AnalyticsServiceDep = Annotated[AnalyticsService, Depends(get_analytics_service)]


@router.get("/sample", response_model=AnalyticsSampleResponse, summary="Analytics sample")
def get_analytics_sample(service: AnalyticsServiceDep) -> AnalyticsSampleResponse:
    return service.get_sample()
