"""Reject routes that touch a stub node (a placeholder for a dangling reference).

Applied by default on every query (see api/routes.py::_build_filters) so a
dangling edge target never surfaces as a real service in the response.
"""

from app.domain.route import Route


class ExcludeStubFilter:
    def matches(self, route: Route) -> bool:
        return not any(node.is_stub for node in route.nodes)
