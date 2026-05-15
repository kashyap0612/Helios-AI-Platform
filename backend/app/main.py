from fastapi import FastAPI
from app.api.routes import router
from app.config.settings import settings
from app.core.logging import configure_logging
from app.middleware.request_context import RequestContextMiddleware

configure_logging(settings.log_level)
app = FastAPI(title=settings.app_name)
app.add_middleware(RequestContextMiddleware)
app.include_router(router)
