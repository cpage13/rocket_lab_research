"""Tests for the executable comms disaster-prevention and targeted-sanity rules.

The disaster-gate and integrity rules read cells off the enriched output (the
``check_data_dictionary_populated`` rule reads the enriched meta), so the suite
runs against the ``default_enriched_output`` fixture; a few cases contrast the
lean engine output explicitly.
"""

from __future__ import annotations

from common.meta import Severity
from communications import validation
from communications.output import CommsModelOutput
from communications.validation import (
    check_cost_band_inverse_of_served,
    check_customer_outputs_are_bands,
    check_data_dictionary_populated,
    check_empirical_anchor_drives_capacity,
    check_launch_cadence_monotonic,
    check_living_fleet_distinct_from_cohort,
    check_no_baked_in_conclusion_fields,
    check_no_forbidden_vehicle_fields,
    check_no_market_capture_fields,
    check_provenance_formula_keys,
    check_release_status_no_placeholder_or_stale,
    check_satellites_per_launch_fork,
    check_spectrum_is_requirement_not_cost,
    check_steady_state_customer_band_order,
    compute_comms_validation,
)

REL_TOL = 1e-9

_DISASTER_GATE_RULES = (
    check_no_baked_in_conclusion_fields,
    check_no_market_capture_fields,
    check_no_forbidden_vehicle_fields,
    check_customer_outputs_are_bands,
    check_spectrum_is_requirement_not_cost,
    check_empirical_anchor_drives_capacity,
    check_provenance_formula_keys,
    check_satellites_per_launch_fork,
)


def test_compute_comms_validation_returns_all_rules(
    default_enriched_output: CommsModelOutput,
) -> None:
    """The driver returns one well-formed ValidationCheck per rule (fourteen)."""
    result = compute_comms_validation(default_enriched_output)
    assert len(result) == len(validation._RULES) == 14
    for check in result:
        assert check.name
        assert check.what_it_tests
        assert check.expected
        assert check.computed
        assert isinstance(check.pass_check, bool)
        assert isinstance(check.severity, Severity)


def test_disaster_gate_rules_pass_on_default(
    default_enriched_output: CommsModelOutput,
) -> None:
    """All eight disaster-gate rules pass on the default enriched output."""
    for rule in _DISASTER_GATE_RULES:
        check = rule(default_enriched_output)
        assert check.pass_check is True, f"{check.name} failed: {check.computed}"


def test_no_baked_in_conclusion_field_walk(
    default_enriched_output: CommsModelOutput,
) -> None:
    """The rule walks model field names and finds no verdict / conclusion field."""
    check = check_no_baked_in_conclusion_fields(default_enriched_output)
    assert check.pass_check is True
    assert check.severity == Severity.CRITICAL


def test_customer_outputs_are_bands(default_enriched_output: CommsModelOutput) -> None:
    """The customer / cost / priced bands have all three members populated."""
    check = check_customer_outputs_are_bands(default_enriched_output)
    assert check.pass_check is True
    assert check.severity == Severity.CRITICAL


def test_spectrum_is_requirement_not_cost(
    default_enriched_output: CommsModelOutput,
) -> None:
    """The spectrum cell is MHz and no cost line is spectrum-derived."""
    check = check_spectrum_is_requirement_not_cost(default_enriched_output)
    assert check.pass_check is True


def test_empirical_anchor_drives_capacity(
    default_enriched_output: CommsModelOutput,
) -> None:
    """Capacity uses the empirical anchor; the naive figure is a labeled cross-check."""
    check = check_empirical_anchor_drives_capacity(default_enriched_output)
    assert check.pass_check is True


def test_provenance_formula_keys_all_registered(
    default_enriched_output: CommsModelOutput,
) -> None:
    """Every cell's formula_name is registered in FORMULAS."""
    check = check_provenance_formula_keys(default_enriched_output)
    assert check.pass_check is True


def test_satellites_per_launch_fork(default_enriched_output: CommsModelOutput) -> None:
    """The fork is the two distinct constraints with broadband packing more per launch."""
    check = check_satellites_per_launch_fork(default_enriched_output)
    assert check.pass_check is True
    assert check.severity == Severity.MAJOR


def test_release_status_check(default_enriched_output: CommsModelOutput) -> None:
    """The release-status rule reports the placeholder/stale counts truthfully.

    The default config carries the NEEDS-RESEARCH antenna bill-of-materials as
    placeholder inputs, so the check FAILs truthfully (the founder-visible flag).
    The test asserts the rule REPORTS the count, not that it must be zero.
    """
    check = check_release_status_no_placeholder_or_stale(default_enriched_output)
    assert check.severity == Severity.MAJOR
    summary = default_enriched_output.meta.source_status_summary
    expected_pass = summary.placeholder == 0 and summary.stale == 0
    assert check.pass_check is expected_pass
    assert "placeholder=" in check.computed


def test_data_dictionary_populated(
    default_enriched_output: CommsModelOutput,
    default_comms_output: CommsModelOutput,
) -> None:
    """The rule passes on the enriched output and fails on the lean engine output."""
    enriched_check = check_data_dictionary_populated(default_enriched_output)
    assert enriched_check.pass_check is True
    assert enriched_check.severity == Severity.MAJOR
    lean_check = check_data_dictionary_populated(default_comms_output)
    assert lean_check.pass_check is False


def test_targeted_sanity_rules_severity(
    default_enriched_output: CommsModelOutput,
) -> None:
    """The targeted-sanity rules carry MINOR severity and pass on the default scenario."""
    minor_rules = (
        check_steady_state_customer_band_order,
        check_cost_band_inverse_of_served,
        check_launch_cadence_monotonic,
        check_living_fleet_distinct_from_cohort,
    )
    for rule in minor_rules:
        check = rule(default_enriched_output)
        assert check.severity == Severity.MINOR
        assert check.pass_check is True, f"{check.name} failed: {check.computed}"
