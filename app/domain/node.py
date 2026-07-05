"""Node entity — one microservice, datastore, or queue in the dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Node:
    """A single vertex in the graph.
    ``name`` is the canonical identity: the source JSON has no separate ``id``
    field, and every edge references nodes by name.
    """

    name: str
    kind: str
    public_exposed: bool = False
    # Raw vulnerability findings attached to the service (empty when none).
    vulnerabilities: list[dict[str, Any]] = field(default_factory=list)
    # Everything else from the JSON we want to keep for the client (language,
    # path, cloud metadata, ...). Kept generic so new fields survive untouched.
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_vulnerable(self) -> bool:
        return len(self.vulnerabilities) > 0
