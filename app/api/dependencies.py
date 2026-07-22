"""FastAPI dependency providers for the API layer."""

from fastapi import Request

from app.services.query_engine import QueryEngine


def get_engine(request: Request) -> QueryEngine:
    # The engine is an app-lifetime singleton built in the lifespan handler, so
    # its memoized route enumeration is reused across every request.
    return request.app.state.engine
