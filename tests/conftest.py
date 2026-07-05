"""Shared fixtures: a small, hand-built graph that exercises every filter.

    auth (public) ──▶ user ──▶ travel
        │
        └──▶ order (vulnerable) ──▶ postgres (rds sink)
"""

from __future__ import annotations

import pytest

from app.domain.edge import Edge
from app.domain.graph import Graph
from app.domain.node import Node


@pytest.fixture
def sample_graph() -> Graph:
    nodes = {
        "auth": Node(name="auth", kind="service", public_exposed=True),
        "user": Node(name="user", kind="service"),
        "travel": Node(name="travel", kind="service"),
        "order": Node(
            name="order",
            kind="service",
            vulnerabilities=[{"severity": "high", "message": "SQLi"}],
        ),
        "postgres": Node(name="postgres", kind="rds"),
    }
    edges = [
        Edge("auth", "user"),
        Edge("auth", "order"),
        Edge("user", "travel"),
        Edge("order", "postgres"),
    ]
    return Graph(nodes=nodes, edges=edges)
