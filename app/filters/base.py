"""The RouteFilter strategy interface and the filter registry.

A filter decides whether a single discovered route should be kept. Filters are
independent of traversal and of each other, so new filters can be added without
touching the engine or existing filters.

Each filter also owns the logic that turns a request into an instance of itself
(``from_query``) and registers itself with ``@register_filter``. The API layer
iterates ``registered_filters()`` instead of a hand-maintained builder list, so
adding a filter never requires editing the endpoint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from app.domain.route import Route

if TYPE_CHECKING:
    from app.schemas.requests import RouteQuery


@runtime_checkable
class RouteFilter(Protocol):
    def matches(self, route: Route) -> bool:
        """Return True if the route satisfies this filter."""
        ...


class QueryFilter(Protocol):
    """A registrable filter: it can build itself from a request and match routes."""

    @classmethod
    def from_query(cls, query: RouteQuery) -> RouteFilter | None:
        """Build the filter from the request, or return None to skip it."""
        ...

    def matches(self, route: Route) -> bool: ...


_REGISTRY: list[type[QueryFilter]] = []


def register_filter(cls: type[QueryFilter]) -> type[QueryFilter]:
    """Class decorator that adds a filter to the registry."""
    _REGISTRY.append(cls)
    return cls


def registered_filters() -> tuple[type[QueryFilter], ...]:
    return tuple(_REGISTRY)
