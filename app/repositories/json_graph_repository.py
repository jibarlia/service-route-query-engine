"""Loads the dependency graph from the Train Ticket JSON file.

Responsibilities are strictly data access + parsing:
- read and parse the JSON,
- normalize the polymorphic ``to`` field (string or list) into flat edges,
- create stub nodes for dangling edge targets (e.g. ``assurance-service`` is
  referenced but never declared),
- build the in-memory ``Graph`` (adjacency list included).

The parsed graph is cached with ``functools.lru_cache`` so the file is read and
parsed only once for the lifetime of the process.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.domain.edge import Edge
from app.domain.graph import Graph
from app.domain.node import Node

logger = logging.getLogger(__name__)

_STUB_KIND = "unknown"
# Keys promoted to first-class Node fields; everything else lands in metadata.
_RESERVED_KEYS = {"name", "kind", "publicExposed", "vulnerabilities"}


def _parse_node(raw: dict[str, Any]) -> Node:
    metadata = {k: v for k, v in raw.items() if k not in _RESERVED_KEYS}
    return Node(
        name=raw["name"],
        kind=raw["kind"],
        public_exposed=raw.get("publicExposed", False),
        vulnerabilities=raw.get("vulnerabilities", []),
        metadata=metadata,
    )


def _normalize_targets(to: str | list[str]) -> list[str]:
    """The JSON expresses ``to`` as either a single string or a list of strings."""
    return [to] if isinstance(to, str) else list(to)


def _build_graph(payload: dict[str, Any]) -> Graph:
    nodes: dict[str, Node] = {}
    for raw in payload["nodes"]:
        node = _parse_node(raw)
        nodes[node.name] = node

    edges: list[Edge] = []
    for raw_edge in payload["edges"]:
        source = raw_edge["from"]
        for target in _normalize_targets(raw_edge["to"]):
            # An edge may reference a node that was never declared. Materialize a
            # stub so traversal stays consistent instead of crashing on lookup.
            for name in (source, target):
                if name not in nodes:
                    logger.warning(
                        "Edge references undeclared node; creating stub",
                        extra={"node": name},
                    )
                    nodes[name] = Node(name=name, kind=_STUB_KIND, is_stub=True)
            edges.append(Edge(source=source, target=target))

    return Graph(nodes=nodes, edges=edges)


@lru_cache(maxsize=1)
def load_graph(path: Path | None = None) -> Graph:
    """Load and cache the graph. Subsequent calls return the cached instance."""
    graph_path = path or settings.graph_path
    payload = json.loads(Path(graph_path).read_text())
    graph = _build_graph(payload)
    logger.info(
        "Graph loaded",
        extra={"nodes": len(graph.nodes), "edges": len(graph.edges)},
    )
    return graph
