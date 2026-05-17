from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_notification_service
from app.schemas.notification import NotificationSampleResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

NotificationServiceDep = Annotated[NotificationService, Depends(get_notification_service)]


@router.get(
    "/sample",
    response_model=NotificationSampleResponse,
    summary="Notification sample",
)
def get_notification_sample(service: NotificationServiceDep) -> NotificationSampleResponse:
    return service.get_sample()
