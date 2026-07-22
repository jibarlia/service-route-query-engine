"""Unit tests for the individual route filters."""

from app.domain.node import Node
from app.domain.route import Route
from app.filters.end_in_sink_filter import EndInSinkFilter
from app.filters.exclude_stub_filter import ExcludeStubFilter
from app.filters.start_public_filter import StartPublicFilter
from app.filters.vulnerability_filter import VulnerabilityFilter
from app.schemas.requests import RouteQuery

_PUBLIC = Node(name="frontend", kind="service", public_exposed=True)
_INTERNAL = Node(name="worker", kind="service")
_VULN = Node(name="order", kind="service", vulnerabilities=[{"severity": "high"}])
_SINK = Node(name="db", kind="rds")
_STUB = Node(name="ghost", kind="unknown", is_stub=True)


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


def test_exclude_stub_filter_should_reject_route_containing_a_stub():
    assert ExcludeStubFilter().matches(_route(_PUBLIC, _STUB)) is False


def test_exclude_stub_filter_should_match_route_with_no_stub():
    assert ExcludeStubFilter().matches(_route(_PUBLIC, _INTERNAL, _SINK)) is True


class TestFromQuery:
    """Each filter builds itself from the request, or returns None to skip."""

    def test_start_public_should_build_when_param_set(self):
        assert isinstance(
            StartPublicFilter.from_query(RouteQuery(start_public=True)), StartPublicFilter
        )

    def test_start_public_should_skip_when_param_unset(self):
        assert StartPublicFilter.from_query(RouteQuery()) is None

    def test_vulnerability_should_build_when_param_set(self):
        assert isinstance(
            VulnerabilityFilter.from_query(RouteQuery(has_vulnerability=True)),
            VulnerabilityFilter,
        )

    def test_vulnerability_should_skip_when_param_unset(self):
        assert VulnerabilityFilter.from_query(RouteQuery()) is None

    def test_end_in_sink_should_forward_the_requested_kind(self):
        built = EndInSinkFilter.from_query(RouteQuery(end_kind="rds"))

        assert isinstance(built, EndInSinkFilter)
        assert built.matches(_route(_INTERNAL, _SINK)) is True

    def test_end_in_sink_should_skip_when_param_unset(self):
        assert EndInSinkFilter.from_query(RouteQuery()) is None

    def test_exclude_stub_should_always_build_regardless_of_request(self):
        assert isinstance(ExcludeStubFilter.from_query(RouteQuery()), ExcludeStubFilter)
