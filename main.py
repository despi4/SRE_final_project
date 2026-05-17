from fastapi import FastAPI

from app.monitoring.http_metrics import setup_metrics_middleware
from app.routers.analytics import router as analytics_router
from app.routers.health import router as health_router
from app.routers.metrics import router as metrics_router
from app.routers.notifications import router as notifications_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.routers.users import router as users_router

app = FastAPI(
    title="Lightweight FastAPI Microservice",
    description="Modular microservice scaffold with 5 service domains.",
    version="1.0.0",
)

setup_metrics_middleware(app)

# Explicit top-level health endpoint
app.include_router(health_router)
app.include_router(metrics_router)

# Versioned API endpoints
API_PREFIX = "/api/v1"
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(products_router, prefix=API_PREFIX)
app.include_router(orders_router, prefix=API_PREFIX)
app.include_router(notifications_router, prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
