from app.schemas.order import OrderSampleResponse


class OrderService:
    def get_sample(self) -> OrderSampleResponse:
        return OrderSampleResponse(
            sample_order_id=1001,
            state="processing",
        )
