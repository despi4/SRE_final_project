from pydantic import BaseModel, ConfigDict, Field


class AnalyticsSampleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str = "analytics"
    active_users_24h: int = Field(ge=0)
    conversion_rate: float = Field(ge=0.0, le=1.0)
