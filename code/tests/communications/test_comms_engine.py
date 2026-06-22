"""Tests for the comms engine (the orchestrator, the rollup, the customer band).

These pin the five-key artifact shape, the per-year keys, the cohort-vs-fleet
reconciliation (the checkpoint's heart), the steady-state living fleet as the
sum of the last `lifetime` cohorts, the cohort-vintaged fleet cost, the
inverse-paired per-customer cost band, the priced-cost band, the populated
required cells (ARPU-collectable, capability), the cohort customer-field
treatment, the direct-to-cell customer chain, the 50k/150k/300k target, the
learning-curve threading, the active-Neutron-envelope choice, the divide guard,
the source-status summary, and the fully assembled metadata block.
"""

from __future__ import annotations

import math
from datetime import datetime

import pytest
from pydantic import BaseModel

from common.input_manifest import SourceStatus
from common.meta import SourceStatusSummary
from common.provenance import FORMULAS, ProvenanceCell
from communications.config import CommsConfig, ConstellationDials
from communications.constants import MONTHS_PER_YEAR, REVENUE_MULTIPLE, USD_PER_MUSD
from communications.engine import (
    _comms_year_to_cohorts,
    _per_customer_cost_value,
    compute_comms_year,
    run_comms_model,
)
from communications.output import CommsModelOutput

REL_TOL = 1e-9


def _default_run() -> CommsModelOutput:
    """Run the default model."""
    return run_comms_model(CommsConfig())


def test_run_comms_model_returns_five_key_artifact() -> None:
    """The run returns a five-key output with 11 per-year records keyed 2026..2036."""
    out = _default_run()
    assert isinstance(out, CommsModelOutput)
    assert out.metadata.schema_version == "comms-v1"
    assert out.metadata.steady_state_year == 2036
    assert len(out.physical.years) == 11
    assert len(out.business.years) == 11
    expected_keys = {str(fy) for fy in range(2026, 2037)}
    assert set(out.physical.years.keys()) == expected_keys
    assert set(out.business.years.keys()) == expected_keys


def test_per_year_count_and_keys() -> None:
    """business.years keys are the calendar years as JSON strings; each .year matches its key."""
    out = _default_run()
    config = CommsConfig()
    for fy in range(
        config.metadata.base_year, config.metadata.base_year + config.metadata.horizon_years + 1
    ):
        record = out.business.years[str(fy)]
        assert record.year == fy


def test_cohort_fleet_reconciliation() -> None:
    """For a mid-horizon year, living fleet == sum of deployed over the last `lifetime` cohorts."""
    out = _default_run()
    lifetime = CommsConfig().constellation.satellite_lifetime_years
    year = 2034
    window = range(year - (lifetime - 1), year + 1)
    for class_name, deployed_field, living_field in (
        (
            "direct_to_cell",
            "direct_to_cell_satellites_deployed_this_year",
            "direct_to_cell_living_fleet",
        ),
        ("broadband", "broadband_satellites_deployed_this_year", "broadband_living_fleet"),
    ):
        expected = sum(getattr(out.business.years[str(fy)], deployed_field).value for fy in window)
        living = getattr(out.business.years[str(year)], living_field).value
        assert living == expected, class_name


def test_steady_state_living_fleet_is_sum_of_last_lifetime_cohorts() -> None:
    """Steady-state living fleet equals the last `lifetime` cohorts' deployed sum."""
    out = _default_run()
    lifetime = CommsConfig().constellation.satellite_lifetime_years
    year = 2036
    window = range(year - (lifetime - 1), year + 1)
    d2c_expected = sum(
        out.business.years[str(fy)].direct_to_cell_satellites_deployed_this_year.value
        for fy in window
    )
    bb_expected = sum(
        out.business.years[str(fy)].broadband_satellites_deployed_this_year.value for fy in window
    )
    assert out.business.years["2036"].direct_to_cell_living_fleet.value == d2c_expected
    assert out.business.years["2036"].broadband_living_fleet.value == bb_expected


def test_fleet_cost_is_cohort_vintaged_sum() -> None:
    """The direct-to-cell fleet cost equals the cohort-vintaged sum (deployed x per-sat cost)."""
    out = _default_run()
    lifetime = CommsConfig().constellation.satellite_lifetime_years
    year = 2036
    window = range(year - (lifetime - 1), year + 1)
    expected = sum(
        out.business.years[str(fy)].direct_to_cell_satellites_deployed_this_year.value
        * out.physical.years[str(fy)].direct_to_cell.cost_annual_per_satellite_musd.value
        for fy in window
    )
    emitted = out.business.years["2036"].direct_to_cell_cost_annual_fleet_musd.value
    assert math.isclose(emitted, expected, rel_tol=REL_TOL)


def test_per_customer_cost_is_band_inverse_of_served() -> None:
    """cost-band LOW uses served-HIGH and HIGH uses served-LOW; each = fleet_usd / served_member."""
    out = _default_run()
    b = out.business.years["2036"]
    fleet_cost_usd = b.direct_to_cell_cost_annual_fleet_musd.value * USD_PER_MUSD
    served_low = b.total_served.low.value
    served_high = b.total_served.high.value
    # band-low uses served-HIGH (cheapest per customer)
    assert math.isclose(
        b.cost_annual_per_customer_usd.low.value, fleet_cost_usd / served_high, rel_tol=REL_TOL
    )
    # band-high uses served-LOW (priciest per customer)
    assert math.isclose(
        b.cost_annual_per_customer_usd.high.value, fleet_cost_usd / served_low, rel_tol=REL_TOL
    )
    # the inverse: cost-low < cost-high
    assert b.cost_annual_per_customer_usd.low.value < b.cost_annual_per_customer_usd.high.value


def test_priced_cost_is_per_customer_cost_times_multiple() -> None:
    """Each priced-cost band member equals the cost member times REVENUE_MULTIPLE."""
    out = _default_run()
    b = out.business.years["2036"]
    for member in ("low", "mid", "high"):
        cost = getattr(b.cost_annual_per_customer_usd, member).value
        priced = getattr(b.priced_cost_per_customer_usd, member).value
        assert math.isclose(priced, cost * REVENUE_MULTIPLE, rel_tol=REL_TOL)


def test_arpu_collectable_revenue_populated_and_equals_formula() -> None:
    """Every BusinessYear has a populated scalar ARPU-collectable cell = ARPU x 12 x share."""
    out = _default_run()
    config = CommsConfig()
    expected = (
        config.price_reference.arpu_usd_per_month
        * MONTHS_PER_YEAR
        * config.price_reference.operator_revenue_share
    )
    assert math.isclose(expected, 300.0, rel_tol=REL_TOL)
    values = []
    for record in out.business.years.values():
        cell_value = record.arpu_collectable_revenue_usd.value
        assert cell_value is not None
        assert math.isclose(cell_value, expected, rel_tol=REL_TOL)
        # a scalar cell, not a band block
        assert not hasattr(record.arpu_collectable_revenue_usd, "low")
        values.append(cell_value)
    # year-invariant under the default config
    assert all(math.isclose(v, values[0], rel_tol=REL_TOL) for v in values)


def test_capability_cell_populated_for_both_classes() -> None:
    """Both classes' capability cells are populated = per_beam_capacity x beams x v4_multiplier."""
    out = _default_run()
    config = CommsConfig()
    # default spectrum: per_beam_capacity = 120, beams = 2500 -> base 300000
    expected = 120.0 * config.spectrum.beams_per_sat * config.constellation.v4_capability_multiplier
    assert math.isclose(expected, 300000.0, rel_tol=REL_TOL)
    p = out.physical.years["2036"]
    for class_name in ("broadband", "direct_to_cell"):
        cap = getattr(p, class_name).capability
        assert cap.value is not None
        assert cap.unit == "Mbps"
        assert math.isclose(cap.value, expected, rel_tol=REL_TOL)


def test_cohort_customer_fields_populated_but_not_the_served_source() -> None:
    """D2C cohort carries the per-sat band; broadband zeros; the fleet count is authoritative."""
    config = CommsConfig()
    # build a computed year and its cohorts
    year = compute_comms_year(
        10, config, cumulative_broadband_before=1, cumulative_direct_to_cell_before=1
    )
    broadband_cohort, direct_to_cell_cohort = _comms_year_to_cohorts(year, config)
    # (a) direct-to-cell cohort carries the positive per-sat band
    assert direct_to_cell_cohort.customers_per_sat_low > 0
    assert direct_to_cell_cohort.customers_per_sat_mid > 0
    assert direct_to_cell_cohort.customers_per_sat_high > 0
    assert math.isclose(direct_to_cell_cohort.customers_per_sat_low, 50000.0, rel_tol=REL_TOL)
    assert math.isclose(direct_to_cell_cohort.customers_per_sat_high, 300000.0, rel_tol=REL_TOL)
    # (b) broadband cohort carries exactly 0.0 (intended zero-fill, not a bug)
    assert broadband_cohort.customers_per_sat_low == 0.0
    assert broadband_cohort.customers_per_sat_mid == 0.0
    assert broadband_cohort.customers_per_sat_high == 0.0
    # (c) the fleet served band is the authoritative living-fleet-count path
    out = run_comms_model(config)
    b = out.business.years["2036"]
    d2c_living = b.direct_to_cell_living_fleet.value
    assert math.isclose(b.total_served.low.value, 50000.0 * d2c_living, rel_tol=REL_TOL)
    assert math.isclose(b.total_served.high.value, 300000.0 * d2c_living, rel_tol=REL_TOL)


def test_customer_band_is_direct_to_cell_chain() -> None:
    """The served band comes from the direct-to-cell living-fleet count, not broadband."""
    out = _default_run()
    b = out.business.years["2036"]
    d2c_living = b.direct_to_cell_living_fleet.value
    bb_living = b.broadband_living_fleet.value
    assert d2c_living != bb_living
    # served-mid = 150000 per sat x d2c living (NOT bb living)
    assert math.isclose(b.total_served.mid.value, 150000.0 * d2c_living, rel_tol=REL_TOL)
    assert not math.isclose(b.total_served.mid.value, 150000.0 * bb_living, rel_tol=REL_TOL)


def test_customer_band_reproduces_target_at_steady_state() -> None:
    """The steady-state per-satellite band reproduces the 50k/150k/300k planning order."""
    out = _default_run()
    b = out.business.years["2036"]
    d2c_living = b.direct_to_cell_living_fleet.value
    per_sat_low = b.total_served.low.value / d2c_living
    per_sat_mid = b.total_served.mid.value / d2c_living
    per_sat_high = b.total_served.high.value / d2c_living
    assert math.isclose(per_sat_low, 50000.0, rel_tol=REL_TOL)
    assert math.isclose(per_sat_mid, 150000.0, rel_tol=REL_TOL)
    assert math.isclose(per_sat_high, 300000.0, rel_tol=REL_TOL)


def test_learning_curve_threaded_cumulative() -> None:
    """Year-0 multiplier is 1.0; a later year's multiplier is strictly below 1.0."""
    out = _default_run()
    assert math.isclose(
        out.physical.years["2026"].learning_curve_multiplier.value, 1.0, rel_tol=REL_TOL
    )
    assert out.physical.years["2036"].learning_curve_multiplier.value < 1.0


def test_active_neutron_envelope_baseline_vs_upgraded() -> None:
    """The broadband per-launch count uses the baseline vs upgraded envelope when the flag flips."""
    baseline = run_comms_model(
        CommsConfig(constellation=ConstellationDials(upgraded_neutron=False))
    )
    upgraded = run_comms_model(CommsConfig(constellation=ConstellationDials(upgraded_neutron=True)))
    bb_baseline = baseline.physical.years["2036"].broadband.satellites_per_launch.value
    bb_upgraded = upgraded.physical.years["2036"].broadband.satellites_per_launch.value
    # the upgraded envelope is larger, so the per-launch count rises
    assert bb_upgraded > bb_baseline


def test_no_division_by_zero_guard() -> None:
    """The per-customer-cost helper raises ValueError on a negative served count."""
    with pytest.raises(ValueError, match="negative"):
        _per_customer_cost_value(100.0, -1.0)
    # a zero served count is the guarded early-ramp zero, not a raise
    assert _per_customer_cost_value(100.0, 0.0) == 0.0


def test_source_status_summary_counts_input_cells() -> None:
    """The summary's eight counts sum to the manifest's assumption_index size and are consistent."""
    out = _default_run()
    summary = out.meta.source_status_summary
    assert isinstance(summary, SourceStatusSummary)
    counts = summary.model_dump()
    assert all(count >= 0 for count in counts.values())
    assert sum(counts.values()) == len(out.inputs.assumption_index)
    # consistency: count the scenario cells by hand and compare
    scenario_by_hand = sum(
        1 for c in out.inputs.assumption_index.values() if c.source_status == SourceStatus.SCENARIO
    )
    assert scenario_by_hand == summary.scenario


def test_metadata_block_is_fully_assembled() -> None:
    """The metadata carries all nine fields from their named sources; meta notes are set."""
    config = CommsConfig()
    out = run_comms_model(
        config,
        source_scenario_path="scenarios/comms_default.yaml",
        artifact_role="promoted_default",
    )
    meta = out.metadata
    assert meta.schema_version == "comms-v1"
    assert meta.scenario_name == config.scenario_levers.scenario_name
    assert meta.base_year == 2026
    assert meta.horizon_years == 10
    assert meta.steady_state_year == 2036
    assert meta.model_package == "rklb-comms"
    assert meta.artifact_role == "promoted_default"
    assert meta.source_scenario_path == "scenarios/comms_default.yaml"
    # generated_at is a parseable ISO-8601 string
    assert meta.generated_at
    datetime.fromisoformat(meta.generated_at)
    # model_version is either None or a non-empty string
    assert meta.model_version is None or meta.model_version
    # the schema-version notes constant
    assert "comms-v1" in out.meta.schema_version_notes


def test_provenance_formula_names_all_registered() -> None:
    """Every emitted output ProvenanceCell's formula_name is registered in FORMULAS."""

    def _walk(node: object) -> list[ProvenanceCell]:
        cells: list[ProvenanceCell] = []
        if isinstance(node, ProvenanceCell):
            cells.append(node)
        elif isinstance(node, BaseModel):
            for value in node.__dict__.values():
                cells.extend(_walk(value))
        elif isinstance(node, dict):
            for value in node.values():
                cells.extend(_walk(value))
        elif isinstance(node, list):
            for item in node:
                cells.extend(_walk(item))
        return cells

    out = _default_run()
    cells = _walk(out.physical) + _walk(out.business)
    assert cells
    for c in cells:
        assert c.formula_name in FORMULAS, c.formula_name
