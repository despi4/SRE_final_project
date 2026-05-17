from pydantic import BaseModel, ConfigDict, Field


class NotificationSampleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str = "notification"
    channel: str = Field(min_length=1)
    queued: bool
