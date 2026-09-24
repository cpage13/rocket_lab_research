"""Tests for volume module.

The volume model (cycle-2 Phase 3) computes the stowed solar+radiator
volume per node and the Neutron-fairing utilization. Volume is surfaced
for transparency but does NOT gate package count (mass-only binding, D6).

Stowed-volume physics: a stowed array is a stack of panels, so its stowed
volume is the deployed area times the stowed panel pitch. The node volume
adds the configured fixed bus volume and the mounting overhead.

Unit strings are ASCII (``m2`` / ``m3``) for consistency with the rest of
the calculator.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from common.provenance import as_float
from data_center.config import (
    BindingConstraint,
    VolumeDials,
    config_from_dict,
)
from data_center.constants import SOLAR_CONSTANT_W_M2
from data_center.engine import run_valuation
from data_center.output import SpaceModelOutput
from data_center.volume import (
    FAIRING_FULL_UTILIZATION_PCT,
    compute_binding_constraint,
    compute_solar_area_per_pkg,
    compute_volume_per_node,
    compute_volume_per_pkg,
    compute_volume_utilization,
)


def test_solar_area_per_pkg_for_1kw_si_20pct() -> None:
    """1 kW at 20% Si efficiency -> ~3.67 m2."""
    c = compute_solar_area_per_pkg(1.0, 0.20, kw_per_pkg_uses=["x"], efficiency_path="y")
    assert c.value == pytest.approx(1000 / (SOLAR_CONSTANT_W_M2 * 0.20), rel=1e-3)
    assert c.unit == "m2"


def test_volume_per_pkg_is_deployed_area_times_pitch() -> None:
    """Objective: stowed volume per package is deployed area x panel pitch.

    Expected: 3.65 m2 at a 6 mm pitch stows 0.0219 m3, and the cell cites
    only the solar-area cell and the pitch dial.
    """
    c = compute_volume_per_pkg(3.65, 6.0, solar_area_path="x", pitch_path="z")
    assert c.value == pytest.approx(3.65 * 0.006, rel=1e-12)
    assert c.uses == ["x", "z"]


def test_volume_per_node_includes_mounting_and_bus() -> None:
    """Node volume = array x (1+overhead) + the configured fixed bus volume."""
    c = compute_volume_per_node(
        34,
        0.001,
        0.30,
        5.0,
        n_path="x",
        vol_per_pkg_path="y",
        mounting_path="z",
        node_volume_fixed_path="w",
    )
    # 34 * 0.001 = 0.034 m3 array, * 1.3 = 0.0442 m3, + 5 m3 bus = ~5.04 m3
    assert c.value == pytest.approx(34 * 0.001 * 1.3 + 5.0, rel=1e-12)
    assert "w" in c.uses


def test_volume_per_node_follows_the_fixed_volume_dial() -> None:
    """Objective: the fixed node volume is the value passed in, not a constant.

    Expected: a 50 m3 fixed volume yields array x 1.3 + 50 m3.
    """
    c = compute_volume_per_node(
        34,
        0.001,
        0.30,
        50.0,
        n_path="x",
        vol_per_pkg_path="y",
        mounting_path="z",
        node_volume_fixed_path="w",
    )
    assert c.value == pytest.approx(34 * 0.001 * 1.3 + 50.0, rel=1e-12)


def test_volume_utilization_under_neutron_fairing() -> None:
    """Volume utilization is node volume / fairing volume, as a percent."""
    c = compute_volume_utilization(5.0, 80.0, node_volume_path="x", fairing_volume_path="y")
    assert c.value == pytest.approx(5.0 / 80.0 * 100, rel=1e-3)


def test_binding_constraint_mass_only() -> None:
    """Mass-bound (leftover below one package), fairing not full -> MASS."""
    c = compute_binding_constraint(True, 50.0, mass_bound_uses=["x"], volume_util_path="y")
    assert c.value == BindingConstraint.MASS.value
    assert c.uses == ["x", "y"]


def test_binding_constraint_neither() -> None:
    """Mass slack of a package or more and a fairing with room -> NEITHER."""
    c = compute_binding_constraint(False, 50.0, mass_bound_uses=["x"], volume_util_path="y")
    assert c.value == BindingConstraint.NEITHER.value


def test_binding_constraint_volume_only() -> None:
    """A full fairing without a mass-bound package count -> VOLUME."""
    c = compute_binding_constraint(
        False, FAIRING_FULL_UTILIZATION_PCT, mass_bound_uses=["x"], volume_util_path="y"
    )
    assert c.value == BindingConstraint.VOLUME.value


def test_binding_constraint_both() -> None:
    """Mass-bound and the fairing full (volume utilization reaches 100%) -> BOTH."""
    c = compute_binding_constraint(
        True, FAIRING_FULL_UTILIZATION_PCT, mass_bound_uses=["x"], volume_util_path="y"
    )
    assert c.value == BindingConstraint.BOTH.value


def test_binding_constraint_volume_threshold_is_a_full_fairing() -> None:
    """Objective: the fairing binds at 100%, not at the old 99% threshold.

    Expected: 99.5% volume utilization on a mass-bound node is MASS, not BOTH.
    """
    assert FAIRING_FULL_UTILIZATION_PCT == 100.0
    c = compute_binding_constraint(True, 99.5, mass_bound_uses=["x"], volume_util_path="y")
    assert c.value == BindingConstraint.MASS.value


def test_volume_sanity_600kw_node_stows_about_22_m3() -> None:
    """Objective: a 600 kW node's stowed volume follows the stacked-panel physics.

    100 packages x 6 kW need 22.0 m2 of 20% silicon each; at a 6 mm pitch the
    array stows 13.2 m3, x 1.3 mounting overhead + 5.0 m3 bus = 22.2 m3.
    Expected: about 22.2 m3, 27.7% of the 80 m3 Neutron fairing: well inside
    it, so mass binds first (D6).
    """
    solar_area = compute_solar_area_per_pkg(6.0, 0.20, kw_per_pkg_uses=["x"], efficiency_path="y")
    vol_pkg = compute_volume_per_pkg(
        as_float(solar_area),
        6.0,
        solar_area_path="x",
        pitch_path="z",
    )
    vol_node = compute_volume_per_node(
        100,
        as_float(vol_pkg),
        0.30,
        5.0,
        n_path="x",
        vol_per_pkg_path="y",
        mounting_path="z",
        node_volume_fixed_path="w",
    )
    assert as_float(vol_node) == pytest.approx(22.19, abs=0.01)
    util = compute_volume_utilization(
        as_float(vol_node),
        80.0,
        node_volume_path="x",
        fairing_volume_path="y",
    )
    assert as_float(util) == pytest.approx(27.74, abs=0.01)


def test_default_fy2036_node_stows_about_26_6_m3(default_output: SpaceModelOutput) -> None:
    """Objective: the default FY2036 node volume follows the stowed-stack physics.

    66 packages x 41.9 m2 x 6 mm = 16.6 m3 of array, x 1.3 mounting overhead
    + 5 m3 bus = 26.6 m3, about 33% of the 80 m3 fairing. Expected: FY2036
    volume per node 26.6 m3, utilization 33.2%, and the node mass-bound.
    """
    py = default_output.physical.years["2036"]
    assert as_float(py.gpus_per_node) == 66
    assert as_float(py.volume_per_node_m3) == pytest.approx(26.57, abs=0.01)
    assert as_float(py.volume_utilization_pct) == pytest.approx(33.21, abs=0.01)
    assert py.binding_constraint.value == "mass"


def test_node_volume_fixed_dial_moves_the_reported_node_volume(
    default_output: SpaceModelOutput,
) -> None:
    """Objective: ``gospel.node_volume_fixed_m3`` is not shadowed by a constant.

    Expected: a scenario that sets it to 50 m3 reports FY2036 node volume
    45 m3 above the default's, and nothing but the volume cells moves.
    """
    default = default_output.physical.years["2036"]
    cfg = config_from_dict({"gospel": {"node_volume_fixed_m3": 50.0}})
    bumped = run_valuation(cfg).physical.years["2036"]
    delta = as_float(bumped.volume_per_node_m3) - as_float(default.volume_per_node_m3)
    assert delta == pytest.approx(45.0, abs=1e-9)
    assert bumped.gpus_per_node.value == default.gpus_per_node.value
    assert "inputs.config.physical.node_volume_fixed_m3" in bumped.volume_per_node_m3.uses


@pytest.mark.parametrize(
    "retired", ["si_areal_density_kg_m2", "radiator_solar_area_ratio", "fold_ratio"]
)
def test_retired_inert_volume_dials_fail_at_load(retired: str) -> None:
    """Objective: the three volume dials no computation reads are gone.

    Expected: naming any of them in a ``volume`` block fails validation
    (``extra="forbid"``), rather than being accepted and ignored.
    """
    with pytest.raises(ValidationError, match=retired):
        VolumeDials.model_validate({retired: 1.0})
