"""Tests for the comms input manifest (the source-linked dial tree + flat index).

These pin that the manifest round-trips the config dials, that the flat
``assumption_index`` is populated and in lockstep with the trees, that every
cell carries the full InputCell field list, that the ground dials are surfaced
even though the engine ignores them, and that no forbidden token (capture-share,
Starship, verdict) leaks into a cell path or label.
"""

from __future__ import annotations

from common.input_manifest import AssumptionRole, InputCell, SourceStatus
from communications.config import CommsConfig
from communications.input_manifest import (
    InputManifest,
    _collect_cells,
    build_comms_input_manifest,
)

_SCENARIO_PATH = "scenarios/comms_default.yaml"


def _manifest() -> InputManifest:
    """Build the manifest from the default config."""
    return build_comms_input_manifest(config=CommsConfig(), source_scenario_path=_SCENARIO_PATH)


def test_manifest_round_trips_config_values() -> None:
    """Each InputCell.value equals the config dial it came from (spot-check every block)."""
    config = CommsConfig()
    manifest = build_comms_input_manifest(config=config, source_scenario_path=_SCENARIO_PATH)
    idx = manifest.assumption_index

    # metadata
    assert idx["inputs.config.metadata.base_year"].value == config.metadata.base_year
    assert idx["inputs.config.metadata.horizon_years"].value == config.metadata.horizon_years
    assert (
        idx["inputs.config.metadata.steady_state_year"].value == config.metadata.steady_state_year
    )

    # per-class four-area costs
    for class_name in ("broadband", "direct_to_cell"):
        dials = getattr(config.constellation, class_name)
        base = f"inputs.config.constellation.{class_name}"
        assert idx[f"{base}.antenna_cost_musd"].value == dials.antenna_cost_musd
        assert idx[f"{base}.satellite_mass_t"].value == dials.satellite_mass_t
        assert idx[f"{base}.stowed_volume_m3"].value == dials.stowed_volume_m3

    # lifetime / cadence / envelopes
    assert (
        idx["inputs.config.constellation.satellite_lifetime_years"].value
        == config.constellation.satellite_lifetime_years
    )
    assert (
        idx["inputs.config.launch.launches_at_year_10"].value == config.launch.launches_at_year_10
    )
    assert (
        idx["inputs.config.launch.neutron_mass_envelope_t"].value
        == config.launch.neutron_mass_envelope_t
    )

    # cost-down pair
    assert (
        idx["inputs.config.cost_down.learning_rate_per_doubling"].value
        == config.cost_down.learning_rate_per_doubling
    )
    assert (
        idx["inputs.config.cost_down.cost_down_reference_units"].value
        == config.cost_down.cost_down_reference_units
    )

    # spectrum dials including the band triples surfaced as low/mid/high cells
    assert (
        idx["inputs.config.spectrum.leased_bandwidth_mhz"].value
        == config.spectrum.leased_bandwidth_mhz
    )
    assert idx["inputs.config.spectrum.beams_per_sat"].value == config.spectrum.beams_per_sat
    assert (
        idx["inputs.config.spectrum.target_per_user_rate_mbps.low"].value
        == config.spectrum.target_per_user_rate_mbps.low
    )
    assert (
        idx["inputs.config.spectrum.target_per_user_rate_mbps.high"].value
        == config.spectrum.target_per_user_rate_mbps.high
    )
    assert (
        idx["inputs.config.spectrum.oversubscription_factor.mid"].value
        == config.spectrum.oversubscription_factor.mid
    )

    # price_reference dials and scope weights (the A1-renamed block)
    assert (
        idx["inputs.config.price_reference.retail_reference_usd_per_month"].value
        == config.price_reference.retail_reference_usd_per_month
    )
    assert (
        idx["inputs.config.price_reference.arpu_usd_per_month"].value
        == config.price_reference.arpu_usd_per_month
    )
    assert idx["inputs.config.price_reference.scope.us"].value == config.price_reference.scope.us

    # ground dials
    assert (
        idx["inputs.config.ground.tower_cost_musd_per_site"].value
        == config.ground.tower_cost_musd_per_site
    )


def test_assumption_index_is_populated_and_matches_trees() -> None:
    """The flat index is non-empty, keyed by cell.path, and holds the same cells as the trees."""
    manifest = _manifest()
    idx = manifest.assumption_index
    assert isinstance(idx, dict)
    assert len(idx) > 0
    for key, input_cell in idx.items():
        assert isinstance(input_cell, InputCell)
        assert key == input_cell.path

    # The trees walked by _collect_cells carry the SAME cells as the flat index.
    tree_cells = _collect_cells(
        [
            manifest.metadata,
            manifest.constellation,
            manifest.launch,
            manifest.cost_down,
            manifest.spectrum,
            manifest.price_reference,
            manifest.ground,
            manifest.scenario,
        ]
    )
    assert len({c.path for c in tree_cells}) == len(idx)

    # a spot-checked tree cell is present in the index under its path
    assert "inputs.config.constellation.broadband.antenna_cost_musd" in idx


def test_manifest_cells_carry_full_field_list() -> None:
    """A sampled InputCell carries the full field list (concern C3's Phase-3 share)."""
    manifest = _manifest()
    sample = manifest.assumption_index["inputs.config.constellation.broadband.antenna_cost_musd"]
    assert sample.path
    assert sample.label
    assert sample.description
    assert isinstance(sample.assumption_role, AssumptionRole)
    assert isinstance(sample.source_status, SourceStatus)
    assert len(sample.source_refs) > 0
    assert sample.rationale


def test_ground_dials_surfaced_even_though_engine_ignores_them() -> None:
    """The ground tree carries the six ground dials; spectrum_cost is the explicit 0.0 wash."""
    manifest = _manifest()
    ground = manifest.ground
    assert ground.tower_cost_musd_per_site.value is not None
    assert ground.sites_per_million_subs.value is not None
    assert ground.backhaul_cost_musd_per_site_year.value is not None
    assert ground.ground_opex_musd_per_site_year.value is not None
    assert ground.ground_amortization_years.value is not None
    assert ground.spectrum_cost_musd.value == 0.0
    assert "wash" in ground.spectrum_cost_musd.rationale.lower()


def test_no_forbidden_tokens_in_manifest_paths() -> None:
    """No InputCell.path or label contains a forbidden disaster-gate token."""
    manifest = _manifest()
    forbidden = (
        "capture_share",
        "share_pct",
        "market_share",
        "starship",
        "verdict",
        "conclusion_label",
        "market_size",
        "market_growth",
        "adoption",
        "take_rate",
        "uptake",
    )
    for input_cell in manifest.assumption_index.values():
        text = f"{input_cell.path} {input_cell.label}".lower()
        for token in forbidden:
            assert token not in text, f"forbidden token {token!r} in {input_cell.path}"
