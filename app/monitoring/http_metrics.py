import re
from time import perf_counter
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Gauge, Histogram

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests.",
    labelnames=("method", "path", "status_code"),
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds.",
    labelnames=("method", "path", "status_code"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently in progress.",
    labelnames=("method",),
)

_EXCLUDED_PATH_PREFIXES = ("/metrics", "/health", "/docs", "/redoc", "/openapi.json")
_UUID_PATH_SEGMENT_RE = re.compile(
    r"/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"
)
_INT_PATH_SEGMENT_RE = re.compile(r"/\d+")


def _normalize_path(path: str) -> str:
    normalized = path.rstrip("/") or "/"
    normalized = _UUID_PATH_SEGMENT_RE.sub("/:uuid", normalized)
    normalized = _INT_PATH_SEGMENT_RE.sub("/:id", normalized)
    return normalized


def setup_metrics_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def collect_http_metrics(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        raw_path = request.url.path
        if any(raw_path.startswith(prefix) for prefix in _EXCLUDED_PATH_PREFIXES):
            return await call_next(request)

        method = request.method
        path = _normalize_path(raw_path)
        start_time = perf_counter()
        status_code = 500

        HTTP_REQUESTS_IN_PROGRESS.labels(method=method).inc()
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = perf_counter() - start_time
            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                path=path,
                status_code=str(status_code),
            ).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method,
                path=path,
                status_code=str(status_code),
            ).observe(duration)
            HTTP_REQUESTS_IN_PROGRESS.labels(method=method).dec()
