"""The graph query engine.

Two independent responsibilities, deliberately kept separate:
- ``find_routes``: enumerate source->sink paths and narrow them with filters.
- ``build_subgraph``: reduce a set of routes to the minimal renderable slice.

Traversal knows nothing about filters, and filters know nothing about traversal.
"""

from collections.abc import Iterable

from app.domain.edge import Edge
from app.domain.graph import Graph
from app.domain.node import Node
from app.domain.route import Route
from app.domain.subgraph import Subgraph
from app.filters.base import RouteFilter


class QueryEngine:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._routes_cache: list[Route] | None = None

    def find_routes(self, filters: Iterable[RouteFilter] = ()) -> list[Route]:
        """Return every source->sink route that satisfies all filters (AND)."""
        active = list(filters)
        return [route for route in self._all_routes() if self._passes(route, active)]

    def build_subgraph(self, routes: list[Route]) -> Subgraph:
        """Union of the nodes and edges touched by ``routes`` (order-preserving)."""
        nodes: dict[str, Node] = {}
        edges: dict[tuple[str, str], Edge] = {}
        for route in routes:
            for node in route.nodes:
                nodes.setdefault(node.name, node)
            for source, target in zip(route.nodes, route.nodes[1:], strict=False):
                key = (source.name, target.name)
                edges.setdefault(key, Edge(source=source.name, target=target.name))
        return Subgraph(nodes=list(nodes.values()), edges=list(edges.values()))

    @staticmethod
    def _passes(route: Route, filters: list[RouteFilter]) -> bool:
        return all(f.matches(route) for f in filters)

    def _all_routes(self) -> list[Route]:
        """Enumerate all simple (cycle-free) source->sink paths, memoized.

        Enumeration is exhaustive (worst-case exponential) and independent of
        any filters, which are applied downstream. The graph is immutable, so
        the result is a pure function of it — compute once and reuse across
        calls. The cached list is never handed out directly (``find_routes``
        always returns a fresh filtered list), so callers cannot mutate it.
        """
        if self._routes_cache is None:
            sinks = set(self._graph.sinks())
            routes: list[Route] = []
            for source in self._graph.sources():
                self._dfs(source, sinks, [], set(), routes)
            self._routes_cache = routes
        return self._routes_cache

    def _dfs(
        self,
        current: str,
        sinks: set[str],
        path: list[str],
        visited: set[str],
        routes: list[Route],
    ) -> None:
        path.append(current)
        visited.add(current)

        if current in sinks:
            # A sink has no outgoing edges, so the path terminates here. Ignore
            # trivial single-node paths (isolated nodes): a route needs an edge.
            if len(path) >= 2:
                routes.append(Route(nodes=tuple(self._graph.get_node(n) for n in path)))
        else:
            for neighbor in self._graph.neighbors(current):
                if neighbor not in visited:  # keep paths simple: no cycles
                    self._dfs(neighbor, sinks, path, visited, routes)

        path.pop()
        visited.remove(current)
