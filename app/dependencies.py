from app.services.analytics_service import AnalyticsService
from app.services.notification_service import NotificationService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.user_service import UserService

_user_service = UserService()
_product_service = ProductService()
_order_service = OrderService()
_notification_service = NotificationService()
_analytics_service = AnalyticsService()


def get_user_service() -> UserService:
    return _user_service


def get_product_service() -> ProductService:
    return _product_service


def get_order_service() -> OrderService:
    return _order_service


def get_notification_service() -> NotificationService:
    return _notification_service


def get_analytics_service() -> AnalyticsService:
    return _analytics_service
