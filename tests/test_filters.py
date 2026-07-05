"""Unit tests for the individual route filters."""

from __future__ import annotations

from app.domain.node import Node
from app.domain.route import Route
from app.filters.end_in_sink_filter import EndInSinkFilter
from app.filters.start_public_filter import StartPublicFilter
from app.filters.vulnerability_filter import VulnerabilityFilter

_PUBLIC = Node(name="frontend", kind="service", public_exposed=True)
_INTERNAL = Node(name="worker", kind="service")
_VULN = Node(name="order", kind="service", vulnerabilities=[{"severity": "high"}])
_SINK = Node(name="db", kind="rds")


def _route(*nodes: Node) -> Route:
    return Route(nodes=tuple(nodes))


def test_start_public_filter_should_match_when_first_node_is_public():
    assert StartPublicFilter().matches(_route(_PUBLIC, _INTERNAL)) is True


def test_start_public_filter_should_reject_when_first_node_is_internal():
    assert StartPublicFilter().matches(_route(_INTERNAL, _PUBLIC)) is False


def test_end_in_sink_filter_should_match_when_last_node_kind_is_a_sink():
    assert EndInSinkFilter(sink_kinds=["rds"]).matches(_route(_INTERNAL, _SINK)) is True


def test_end_in_sink_filter_should_reject_when_last_node_is_not_a_sink():
    assert EndInSinkFilter(sink_kinds=["rds"]).matches(_route(_SINK, _INTERNAL)) is False


def test_vulnerability_filter_should_match_when_any_node_is_vulnerable():
    assert VulnerabilityFilter().matches(_route(_PUBLIC, _VULN, _SINK)) is True


def test_vulnerability_filter_should_reject_when_no_node_is_vulnerable():
    assert VulnerabilityFilter().matches(_route(_PUBLIC, _INTERNAL, _SINK)) is False
