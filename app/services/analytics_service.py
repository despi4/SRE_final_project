from app.schemas.analytics import AnalyticsSampleResponse


class AnalyticsService:
    def get_sample(self) -> AnalyticsSampleResponse:
        return AnalyticsSampleResponse(
            active_users_24h=128,
            conversion_rate=0.08,
        )
