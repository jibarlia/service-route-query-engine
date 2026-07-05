"""Route entity — one concrete path through the graph."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.node import Node


@dataclass(frozen=True)
class Route:
    """An ordered path of nodes, from a source to a sink."""

    nodes: tuple[Node, ...]

    @property
    def start(self) -> Node:
        return self.nodes[0]

    @property
    def end(self) -> Node:
        return self.nodes[-1]
