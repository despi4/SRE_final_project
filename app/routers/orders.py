from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_order_service
from app.schemas.order import OrderSampleResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.get("/sample", response_model=OrderSampleResponse, summary="Order sample")
def get_order_sample(service: OrderServiceDep) -> OrderSampleResponse:
    return service.get_sample()
