"""Subgraph entity — the minimal slice of the graph needed to render a result.

Given the routes that matched a query, the subgraph is the union of every node
and edge those routes touch. Nodes/edges not involved in any matching route are
dropped, so a client can render exactly the query result without filtering the
full 40+ service graph itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.edge import Edge
from app.domain.node import Node


@dataclass(frozen=True)
class Subgraph:
    nodes: list[Node]
    edges: list[Edge]
