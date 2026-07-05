"""Edge entity — a directed dependency from one node to another."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    """A directed edge ``source -> target`` (both referenced by node name).

    The source JSON expresses a fan-out as ``{"from": "a", "to": ["b", "c"]}``;
    those are normalized into individual ``Edge`` instances at load time.
    """

    source: str
    target: str
