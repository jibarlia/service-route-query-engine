"""Response models for the /routes endpoint.

The response is a render-ready graph structure: the reduced ``nodes`` and
``edges`` (the subgraph) plus the explicit ``routes`` that matched the query.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.route import Route
from app.domain.subgraph import Subgraph


class NodeOut(BaseModel):
    name: str
    kind: str
    public: bool = Field(description="Whether the service is publicly exposed")
    vulnerable: bool = Field(description="Whether the node has any vulnerability finding")


class EdgeOut(BaseModel):
    from_: str = Field(alias="from")
    to: str

    model_config = {"populate_by_name": True}


class RoutesResponse(BaseModel):
    nodes: list[NodeOut]
    edges: list[EdgeOut]
    routes: list[list[str]] = Field(description="Matching routes as ordered lists of node names")

    @classmethod
    def from_result(cls, subgraph: Subgraph, routes: list[Route]) -> RoutesResponse:
        return cls(
            nodes=[
                NodeOut(
                    name=node.name,
                    kind=node.kind,
                    public=node.public_exposed,
                    vulnerable=node.is_vulnerable,
                )
                for node in subgraph.nodes
            ],
            edges=[EdgeOut(from_=edge.source, to=edge.target) for edge in subgraph.edges],
            routes=[[node.name for node in route.nodes] for route in routes],
        )
