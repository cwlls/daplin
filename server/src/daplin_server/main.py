"""FastAPI application factory.

This module is intentionally minimal at this stage — it will be fleshed out
in Task 8 (FastAPI App + Health Check).  It exists here so that the package
is importable and ``mypy`` / ``ruff`` can validate the module graph.
"""

from __future__ import annotations

from fastapi import FastAPI

from daplin_server.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    _settings = settings or Settings()

    app = FastAPI(
        title="Daplin Instance",
        version="0.1.0",
        description="Daplin federated identity instance server",
    )

    # Attach settings to app state so routers can access them.
    app.state.settings = _settings

    return app


# Module-level app instance for uvicorn / gunicorn entry-point.
app = create_app()
