from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_product_service
from app.schemas.product import ProductSampleResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.get("/sample", response_model=ProductSampleResponse, summary="Product sample")
def get_product_sample(service: ProductServiceDep) -> ProductSampleResponse:
    return service.get_sample()
