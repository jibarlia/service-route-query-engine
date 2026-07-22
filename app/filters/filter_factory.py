"""Assembles the active filter list for a request from the filter registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.filters.base import RouteFilter, registered_filters

if TYPE_CHECKING:
    from app.schemas.requests import RouteQuery


class FilterFactory:
    @classmethod
    def build(cls, query: RouteQuery) -> list[RouteFilter]:
        # Each registered filter decides whether it applies to this request and how
        # to build itself. Adding a filter = drop a module in app/filters/ (no edit here).
        return [
            f
            for filter_cls in registered_filters()
            if (f := filter_cls.from_query(query)) is not None
        ]
