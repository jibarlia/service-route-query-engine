"""Keep routes that start in a publicly exposed service."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.route import Route
from app.filters.base import register_filter

if TYPE_CHECKING:
    from app.schemas.requests import RouteQuery


@register_filter
class StartPublicFilter:
    @classmethod
    def from_query(cls, query: RouteQuery) -> StartPublicFilter | None:
        return cls() if query.start_public else None

    def matches(self, route: Route) -> bool:
        return route.start.public_exposed
