from app.schemas.notification import NotificationSampleResponse


class NotificationService:
    def get_sample(self) -> NotificationSampleResponse:
        return NotificationSampleResponse(
            channel="email",
            queued=True,
        )
