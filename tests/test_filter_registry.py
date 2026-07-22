"""Tests for filter auto-discovery and request-driven filter assembly."""

from app.filters.base import registered_filters
from app.filters.end_in_sink_filter import EndInSinkFilter
from app.filters.exclude_stub_filter import ExcludeStubFilter
from app.filters.filter_factory import FilterFactory
from app.filters.start_public_filter import StartPublicFilter
from app.filters.vulnerability_filter import VulnerabilityFilter
from app.schemas.requests import RouteQuery

_ALL_FILTERS = {
    StartPublicFilter,
    EndInSinkFilter,
    VulnerabilityFilter,
    ExcludeStubFilter,
}


def test_every_filter_module_is_auto_registered():
    assert _ALL_FILTERS.issubset(set(registered_filters()))


def test_build_filters_should_only_include_always_on_filters_for_an_empty_query():
    built = FilterFactory.build(RouteQuery())

    assert [type(f) for f in built] == [ExcludeStubFilter]


def test_build_filters_should_include_a_filter_only_when_its_param_is_provided():
    built = FilterFactory.build(RouteQuery(start_public=True))

    assert {type(f) for f in built} == {ExcludeStubFilter, StartPublicFilter}


def test_build_filters_should_assemble_all_requested_filters():
    built = FilterFactory.build(
        RouteQuery(start_public=True, end_kind="rds", has_vulnerability=True)
    )

    assert {type(f) for f in built} == {
        ExcludeStubFilter,
        StartPublicFilter,
        EndInSinkFilter,
        VulnerabilityFilter,
    }
