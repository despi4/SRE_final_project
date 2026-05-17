from pydantic import BaseModel, ConfigDict, Field


class OrderSampleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str = "order"
    sample_order_id: int = Field(gt=0)
    state: str = Field(min_length=1)
