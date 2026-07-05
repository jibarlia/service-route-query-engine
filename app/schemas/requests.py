"""Request model for the /routes endpoint query parameters."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.sink_kind import SinkKind


class RouteQuery(BaseModel):
    """Optional filters. Omitted params mean "don't filter on this dimension".

    Filters combine with AND: a route is returned only if it satisfies every
    provided filter.
    """

    start_public: bool | None = Field(
        default=None,
        description="Keep only routes that start in a publicly exposed service.",
    )
    end_kind: SinkKind | None = Field(
        default=None,
        description="Keep only routes that end in a sink of this kind.",
    )
    has_vulnerability: bool | None = Field(
        default=None,
        description="Keep only routes where at least one node has a vulnerability.",
    )
