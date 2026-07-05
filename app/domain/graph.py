"""Graph entity — the full dependency graph loaded from JSON.

Holds the immutable node registry and edge list, and precomputes an adjacency
list so traversal is O(1) per neighbor lookup instead of scanning all edges.
"""

from __future__ import annotations

from app.domain.edge import Edge
from app.domain.node import Node


class Graph:
    def __init__(self, nodes: dict[str, Node], edges: list[Edge]) -> None:
        self._nodes = nodes
        self._edges = edges
        self._adjacency: dict[str, list[str]] = {name: [] for name in nodes}
        self._indegree: dict[str, int] = {name: 0 for name in nodes}
        for edge in edges:
            self._adjacency[edge.source].append(edge.target)
            self._indegree[edge.target] += 1

    @property
    def nodes(self) -> dict[str, Node]:
        return self._nodes

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    def get_node(self, name: str) -> Node:
        return self._nodes[name]

    def neighbors(self, name: str) -> list[str]:
        return self._adjacency[name]

    def sources(self) -> list[str]:
        """Entry points: nodes with no incoming edges."""
        return [name for name, degree in self._indegree.items() if degree == 0]

    def sinks(self) -> list[str]:
        """Terminals: nodes with no outgoing edges."""
        return [name for name, targets in self._adjacency.items() if not targets]
