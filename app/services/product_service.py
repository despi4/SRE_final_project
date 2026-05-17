from app.schemas.product import ProductSampleResponse


class ProductService:
    def get_sample(self) -> ProductSampleResponse:
        return ProductSampleResponse(
            featured_product="Wireless Keyboard",
            in_stock=True,
        )
