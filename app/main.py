"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Service Route Query Engine",
        description="Query microservice dependency routes and return a render-ready subgraph.",
        version="0.1.0",
    )
    app.include_router(router)
    return app


app = create_app()
