"""Unit tests for the JSON graph repository: parsing, normalization, robustness."""

import json
from pathlib import Path

from app.repositories.json_graph_repository import load_graph


def _write_graph(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "graph.json"
    path.write_text(json.dumps(payload))
    load_graph.cache_clear()  # the loader is process-cached; isolate each test
    return path


def test_polymorphic_to_field_should_be_normalized_to_individual_edges(tmp_path):
    payload = {
        "nodes": [
            {"name": "a", "kind": "service"},
            {"name": "b", "kind": "service"},
            {"name": "c", "kind": "service"},
            {"name": "d", "kind": "service"},
        ],
        "edges": [
            {"from": "a", "to": ["b", "c"]},  # list form
            {"from": "c", "to": "d"},  # string form
        ],
    }
    graph = load_graph(_write_graph(tmp_path, payload))

    assert sorted(graph.neighbors("a")) == ["b", "c"]
    assert graph.neighbors("c") == ["d"]
    assert len(graph.edges) == 3


def test_undeclared_edge_target_should_get_a_stub_node(tmp_path):
    payload = {
        "nodes": [{"name": "a", "kind": "service"}],
        "edges": [{"from": "a", "to": ["ghost-service"]}],
    }
    graph = load_graph(_write_graph(tmp_path, payload))

    assert "ghost-service" in graph.nodes
    assert graph.get_node("ghost-service").kind == "unknown"
    assert graph.get_node("ghost-service").is_stub is True


def test_node_metadata_and_vulnerabilities_should_be_preserved(tmp_path):
    payload = {
        "nodes": [
            {
                "name": "auth",
                "kind": "service",
                "language": "java",
                "publicExposed": True,
                "vulnerabilities": [{"severity": "medium"}],
            }
        ],
        "edges": [],
    }
    graph = load_graph(_write_graph(tmp_path, payload))
    node = graph.get_node("auth")

    assert node.public_exposed is True
    assert node.is_vulnerable is True
    assert node.metadata["language"] == "java"
