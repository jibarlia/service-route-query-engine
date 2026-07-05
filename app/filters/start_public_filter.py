"""Keep routes that start in a publicly exposed service."""

from __future__ import annotations

from app.domain.route import Route


class StartPublicFilter:
    def matches(self, route: Route) -> bool:
        return route.start.public_exposed
