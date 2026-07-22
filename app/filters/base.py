"""The RouteFilter strategy interface.

A filter decides whether a single discovered route should be kept. Filters are
independent of traversal and of each other, so new filters can be added without
touching the engine or existing filters.
"""

from typing import Protocol, runtime_checkable

from app.domain.route import Route


@runtime_checkable
class RouteFilter(Protocol):
    def matches(self, route: Route) -> bool:
        """Return True if the route satisfies this filter."""
        ...
