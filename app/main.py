from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.core.docs import swagger_ui_offline_html
from app.core.logging import configure_logging

BASE_DIR = Path(__file__).resolve().parent


def create_app() -> FastAPI:
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.app_debug,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )
    app.openapi_version = "3.0.2"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    app.include_router(router, prefix=settings.api_prefix)

    @app.get("/", include_in_schema=False)
    def root():
        return {"service": settings.app_name, "docs": "/docs", "health": settings.api_prefix + "/health"}

    @app.get("/docs", include_in_schema=False)
    def docs():
        return swagger_ui_offline_html(app.openapi_url, "%s docs" % settings.app_name)

    return app


app = create_app()
