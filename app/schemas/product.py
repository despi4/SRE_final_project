from pydantic import BaseModel, ConfigDict, Field


class ProductSampleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str = "product"
    featured_product: str = Field(min_length=1)
    in_stock: bool
