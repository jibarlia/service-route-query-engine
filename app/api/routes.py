"""REST layer: the single ``GET /routes`` endpoint.

Translates query params into the generic filter list, delegates traversal and
subgraph reduction to the engine, and serializes the result.
"""

from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.filters.base import RouteFilter
from app.filters.end_in_sink_filter import EndInSinkFilter
from app.filters.exclude_stub_filter import ExcludeStubFilter
from app.filters.start_public_filter import StartPublicFilter
from app.filters.vulnerability_filter import VulnerabilityFilter
from app.repositories.json_graph_repository import load_graph
from app.schemas.requests import RouteQuery
from app.schemas.responses import RoutesResponse
from app.services.query_engine import QueryEngine

router = APIRouter()

# One builder per filter: it inspects the request and returns a filter to apply,
# or None to skip. Adding a filter = one entry here
_FILTER_BUILDERS: tuple[Callable[[RouteQuery], RouteFilter | None], ...] = (
    lambda q: StartPublicFilter() if q.start_public else None,
    lambda q: EndInSinkFilter(sink_kinds=[q.end_kind]) if q.end_kind is not None else None,
    lambda q: VulnerabilityFilter() if q.has_vulnerability else None,
)


def _build_filters(query: RouteQuery) -> list[RouteFilter]:
    conditional = [f for build in _FILTER_BUILDERS if (f := build(query)) is not None]
    # Stub exclusion is an always-on default, not a query param: routes touching a
    # dangling-reference placeholder must never surface in a response.
    return [ExcludeStubFilter(), *conditional]


def get_engine() -> QueryEngine:
    # The graph is loaded once and cached; the engine is a thin stateless wrapper.
    return QueryEngine(load_graph())


@router.get("/routes", response_model=RoutesResponse)
def get_routes(
    query: Annotated[RouteQuery, Query()],
    engine: Annotated[QueryEngine, Depends(get_engine)],
) -> RoutesResponse:
    filters = _build_filters(query)
    routes = engine.find_routes(filters)
    subgraph = engine.build_subgraph(routes)
    return RoutesResponse.from_result(subgraph, routes)
