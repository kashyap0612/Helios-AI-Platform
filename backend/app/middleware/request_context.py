import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
from app.observability.metrics import ACTIVE_REQUESTS, REQUEST_COUNT, REQUEST_LATENCY


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)
        ACTIVE_REQUESTS.inc()
        try:
            response = await call_next(request)
            REQUEST_COUNT.labels(endpoint=request.url.path, status=response.status_code).inc()
            return response
        finally:
            REQUEST_LATENCY.labels(endpoint=request.url.path).observe(time.perf_counter() - start)
            ACTIVE_REQUESTS.dec()
            structlog.contextvars.clear_contextvars()
