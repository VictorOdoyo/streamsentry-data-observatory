from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from streamsentry.config import get_settings

from .errors import install_error_handlers
from .routes import checks, datasets, health, incidents, lineage, reliability, workspaces
from .state import ApplicationState, build_state


def create_app(state: ApplicationState | None = None) -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="StreamSentry Data Observatory",
        version="1.0.0",
        description="Operational API for data reliability, incidents, lineage, and cost signals.",
    )
    app.state.container = state or build_state()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["Content-Type", "X-Request-ID"],
    )
    install_error_handlers(app)
    for router in (
        health.router,
        workspaces.router,
        datasets.router,
        checks.router,
        incidents.router,
        lineage.router,
        reliability.router,
    ):
        app.include_router(router)
    return app


app = create_app()
