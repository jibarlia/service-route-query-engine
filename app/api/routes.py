"""REST layer: the single ``GET /routes`` endpoint.

Translates query params into the generic filter list, delegates traversal and
subgraph reduction to the engine, and serializes the result.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_engine
from app.filters.filter_factory import FilterFactory
from app.schemas.requests import RouteQuery
from app.schemas.responses import RoutesResponse
from app.services.query_engine import QueryEngine

router = APIRouter()


@router.get("/routes", response_model=RoutesResponse)
def get_routes(
    query: Annotated[RouteQuery, Query()],
    engine: Annotated[QueryEngine, Depends(get_engine)],
) -> RoutesResponse:
    filters = FilterFactory.build(query)
    routes = engine.find_routes(filters)
    subgraph = engine.build_subgraph(routes)
    return RoutesResponse.from_result(subgraph, routes)
