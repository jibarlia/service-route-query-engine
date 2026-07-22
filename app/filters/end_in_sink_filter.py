"""Keep routes that end in a sink (e.g. an RDS/SQL datastore).

Parametrized by the accepted sink kinds because the graph has more than one sink
kind (``rds`` and ``sqs``); a caller can also target a single kind (``rds``).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from app.domain.route import Route
from app.filters.base import register_filter

if TYPE_CHECKING:
    from app.schemas.requests import RouteQuery


@register_filter
class EndInSinkFilter:
    def __init__(self, sink_kinds: Iterable[str]) -> None:
        self._sink_kinds = set(sink_kinds)

    @classmethod
    def from_query(cls, query: RouteQuery) -> EndInSinkFilter | None:
        return cls(sink_kinds=[query.end_kind]) if query.end_kind is not None else None

    def matches(self, route: Route) -> bool:
        return route.end.kind in self._sink_kinds
