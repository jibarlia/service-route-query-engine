"""FastAPI dependency providers for the API layer."""

from app.repositories.json_graph_repository import load_graph
from app.services.query_engine import QueryEngine


def get_engine() -> QueryEngine:
    # The graph is loaded once and cached; the engine is a thin stateless wrapper.
    return QueryEngine(load_graph())
