"""Unit tests for traversal, filtering, and subgraph reduction."""

from app.domain.edge import Edge
from app.domain.graph import Graph
from app.domain.node import Node
from app.filters.end_in_sink_filter import EndInSinkFilter
from app.services.query_engine import QueryEngine


def _route_ids(routes):
    return {tuple(node.name for node in route.nodes) for route in routes}


def test_find_routes_should_enumerate_all_source_to_sink_paths(sample_graph):
    routes = QueryEngine(sample_graph).find_routes()

    assert _route_ids(routes) == {
        ("auth", "user", "travel"),
        ("auth", "order", "postgres"),
    }


def test_find_routes_should_apply_filters_with_and_semantics(sample_graph):
    engine = QueryEngine(sample_graph)

    routes = engine.find_routes([EndInSinkFilter(sink_kinds=["rds"])])

    assert _route_ids(routes) == {("auth", "order", "postgres")}


def test_traversal_should_be_cycle_safe():
    # The a <-> b cycle would loop forever without a per-path visited set.
    nodes = {
        "entry": Node(name="entry", kind="service"),
        "a": Node(name="a", kind="service"),
        "b": Node(name="b", kind="service"),
        "sink": Node(name="sink", kind="rds"),
    }
    edges = [Edge("entry", "a"), Edge("a", "b"), Edge("b", "a"), Edge("b", "sink")]
    graph = Graph(nodes=nodes, edges=edges)

    routes = QueryEngine(graph).find_routes()

    assert _route_ids(routes) == {("entry", "a", "b", "sink")}


def test_build_subgraph_should_drop_nodes_not_involved_in_matching_routes(sample_graph):
    engine = QueryEngine(sample_graph)
    routes = engine.find_routes([EndInSinkFilter(sink_kinds=["rds"])])

    subgraph = engine.build_subgraph(routes)

    node_names = {node.name for node in subgraph.nodes}
    assert node_names == {"auth", "order", "postgres"}
    assert "user" not in node_names  # user is not on any matching route
    assert {(e.source, e.target) for e in subgraph.edges} == {
        ("auth", "order"),
        ("order", "postgres"),
    }
