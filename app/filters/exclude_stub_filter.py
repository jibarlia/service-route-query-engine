"""Reject routes that touch a stub node (a placeholder for a dangling reference).

Applied on every query regardless of request params: ``from_query`` always
returns an instance, so a dangling edge target never surfaces as a real service
in the response.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.route import Route
from app.filters.base import register_filter

if TYPE_CHECKING:
    from app.schemas.requests import RouteQuery


@register_filter
class ExcludeStubFilter:
    @classmethod
    def from_query(cls, query: RouteQuery) -> ExcludeStubFilter:
        return cls()

    def matches(self, route: Route) -> bool:
        return not any(node.is_stub for node in route.nodes)
