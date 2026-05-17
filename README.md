## FastAPI Microservice Scaffold (5 Service Domains)

### Summary
Build a lightweight, production-ready FastAPI microservice from scratch with clear separation of concerns:
- `main.py` as app entrypoint and router composition
- `services/` with 5 domain services (`User`, `Product`, `Order`, `Notification`, `Analytics`)
- `routers/` with one router per service plus explicit `/health`
- Full implementation depth for `UserService`; other 4 services as clean mock service layers with representative endpoints
- Pydantic v2 schemas, strict type hints, DI via `Depends`, and basic `HTTPException` handling

### Key Implementation Changes
- Create this project layout:
  - `main.py`
  - `requirements.txt`
  - `app/`
  - `app/routers/` (`health.py`, `users.py`, `products.py`, `orders.py`, `notifications.py`, `analytics.py`)
  - `app/services/` (`user_service.py`, `product_service.py`, `order_service.py`, `notification_service.py`, `analytics_service.py`)
  - `app/schemas/` (`common.py`, `user.py`, `product.py`, `order.py`, `notification.py`, `analytics.py`)
  - `app/dependencies.py`
- `main.py` responsibilities:
  - Instantiate `FastAPI` with metadata/version
  - Include all routers under `/api/v1` (except `/health`, which stays top-level and explicit)
- Health endpoint:
  - `GET /health` returns `{"status":"healthy","timestamp":"<ISO8601 UTC>"}` via typed response schema
- Service/Router interaction pattern:
  - Routers call service methods only (no business logic in routers)
  - Services injected with `Depends` through dependency providers in `app/dependencies.py`
- `UserService` (fully implemented sample):
  - In-memory store (dict-based) and incremental id
  - Methods: create user, get user by id, list users
  - Validation and conflict handling (e.g., duplicate email) with `HTTPException`
- Other 4 services (mock but clean):
  - Each has a dedicated service class and one representative method
  - Each has a dedicated router with one demo endpoint returning structured typed response
- Code quality conventions:
  - Pydantic v2 models (`BaseModel`, `ConfigDict`, constrained fields where needed)
  - Return typed response models for every endpoint
  - Use `Annotated[..., Depends(...)]` for DI typing clarity

### Public API / Interface Notes
- Base route prefix: `/api/v1`
- Endpoints:
  - `GET /health`
  - `POST /api/v1/users`
  - `GET /api/v1/users`
  - `GET /api/v1/users/{user_id}`
  - `GET /api/v1/products/sample`
  - `GET /api/v1/orders/sample`
  - `GET /api/v1/notifications/sample`
  - `GET /api/v1/analytics/sample`
- Schemas exposed:
  - `HealthResponse`
  - `UserCreate`, `UserRead`, `UserListResponse`
  - Simple typed response models for product/order/notification/analytics sample endpoints

### Test Plan
- Manual smoke checks (curl or Swagger):
  - `/health` returns `healthy` + valid ISO timestamp
  - Create user succeeds; duplicate email returns 409
  - Fetch unknown user id returns 404
  - List users returns created entries
  - All four mock domain endpoints return 200 and typed payloads
- Basic startup validation:
  - `uvicorn main:app --reload` boots with no import/runtime errors
  - OpenAPI docs render all routes and schemas

### Assumptions & Defaults
- Python 3.10+ runtime
- Minimal dependency management via `requirements.txt` (`fastapi`, `uvicorn[standard]`, `pydantic>=2`)
- No database/auth for v1 scaffold; in-memory store is intentional for lightweight demonstrator
- Mock services are intentionally thin but structurally production-aligned for later expansion
