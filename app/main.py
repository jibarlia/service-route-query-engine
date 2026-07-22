"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.repositories.json_graph_repository import load_graph
from app.services.query_engine import QueryEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Built once per process: the graph is parsed once and the engine memoizes
    # its route enumeration, so both are computed a single time at startup.
    app.state.engine = QueryEngine(load_graph())
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Service Route Query Engine",
        description="Query microservice dependency routes and return a render-ready subgraph.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


app = create_app()
