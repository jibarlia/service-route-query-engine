"""Keep routes that start in a publicly exposed service."""

from app.domain.route import Route


class StartPublicFilter:
    def matches(self, route: Route) -> bool:
        return route.start.public_exposed
