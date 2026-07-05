"""Sanity integration test for the /routes endpoint against the real graph."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_routes_endpoint_should_return_a_renderable_subgraph():
    response = client.get("/routes", params={"has_vulnerability": "true"})

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"nodes", "edges", "routes"}
    assert body["routes"], "expected at least one vulnerable route in the sample graph"

    # The response is a self-contained subgraph: every node referenced by an edge
    # or a route is present in `nodes`, so a client can render it as-is.
    node_names = {node["name"] for node in body["nodes"]}
    for route in body["routes"]:
        assert set(route).issubset(node_names)
    for edge in body["edges"]:
        assert edge["from"] in node_names and edge["to"] in node_names
