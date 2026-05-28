"""Tests for volume module.

The volume model (cycle-2 Phase 3) computes the stowed solar+radiator
volume per node and the Neutron-fairing utilization. Volume is surfaced
for transparency but does NOT gate package count (mass-only binding, D6).

Unit strings are ASCII (``m2`` / ``m3``) for consistency with the rest of
the calculator (the plan's snippet used ``m2`` / ``m3`` — codebase-wide
ASCII convention; deviation logged in execution doc).
"""

from __future__ import annotations

import pytest

from data_center.config import BindingConstraint
from data_center.constants import SOLAR_CONSTANT_W_M2
from data_center.volume import (
    compute_binding_constraint,
    compute_solar_area_per_pkg,
    compute_volume_per_node,
    compute_volume_per_pkg,
    compute_volume_utilization,
)


def test_solar_area_per_pkg_for_1kw_si_20pct() -> None:
    """1 kW at 20% Si efficiency -> ~3.65 m2."""
    c = compute_solar_area_per_pkg(1.0, 0.20, kw_per_pkg_path="x", efficiency_path="y")
    assert c.value == pytest.approx(1000 / (SOLAR_CONSTANT_W_M2 * 0.20), rel=1e-3)
    assert c.unit == "m2"


def test_volume_per_pkg_folded_at_80x() -> None:
    """3.65 m2 folded at 80x with 6mm pitch -> 2.74e-4 m3."""
    c = compute_volume_per_pkg(
        3.65, 80.0, 6.0, solar_area_path="x", fold_ratio_path="y", pitch_path="z"
    )
    assert c.value == pytest.approx(3.65 / 80.0 * 0.006, rel=1e-3)


def test_volume_per_node_includes_mounting_and_bus() -> None:
    """Node volume = array x (1+overhead) + fixed bus volume (5 m3)."""
    c = compute_volume_per_node(
        34, 0.001, 0.30, n_path="x", vol_per_pkg_path="y", mounting_path="z"
    )
    # 34 * 0.001 = 0.034 m3 array, * 1.3 = 0.0442 m3, + 5 m3 bus = ~5.04 m3
    assert c.value == pytest.approx(34 * 0.001 * 1.3 + 5.0, rel=1e-3)


def test_volume_utilization_under_neutron_fairing() -> None:
    """Volume utilization is node volume / fairing volume, as a percent."""
    c = compute_volume_utilization(5.0, 80.0, node_volume_path="x", fairing_volume_path="y")
    assert c.value == pytest.approx(5.0 / 80.0 * 100, rel=1e-3)


def test_binding_constraint_mass_only() -> None:
    """Mass within 1% of envelope, volume slack -> MASS."""
    c = compute_binding_constraint(99.5, 50.0, mass_util_path="x", volume_util_path="y")
    assert c.value == BindingConstraint.MASS.value


def test_binding_constraint_neither() -> None:
    """Both envelopes slack -> NEITHER."""
    c = compute_binding_constraint(50.0, 50.0, mass_util_path="x", volume_util_path="y")
    assert c.value == BindingConstraint.NEITHER.value


def test_binding_constraint_volume_only() -> None:
    """Volume within 1% of fairing, mass slack -> VOLUME."""
    c = compute_binding_constraint(50.0, 99.5, mass_util_path="x", volume_util_path="y")
    assert c.value == BindingConstraint.VOLUME.value


def test_binding_constraint_both() -> None:
    """Both envelopes within 1% -> BOTH."""
    c = compute_binding_constraint(99.5, 99.5, mass_util_path="x", volume_util_path="y")
    assert c.value == BindingConstraint.BOTH.value


def test_volume_sanity_600kw_node_stows_well_under_fairing() -> None:
    """Volume sanity: a 600 kW node stows with large fairing slack (D6).

    The plan's Task-37 snippet asserted ~25 m3, but the plan's own
    Task-36 formulas (fold_ratio 80x + 6 mm pitch on a 21.9 m2 panel +
    a 5.0 m3 fixed bus) produce ~5.2 m3 — the folded array is tiny and
    the fixed bus volume dominates. The 25 m3 band was an internally
    inconsistent test expectation; corrected here to bracket what the
    plan's formulas actually yield. The sanity intent is preserved: a
    high-kW node stows far inside the 80 m3 Neutron fairing, which is
    exactly the D6 "mass-only binding, volume has huge slack" picture.
    """
    # 600 kW node ~= 100 packages x 6 kW/pkg (Feynman+)
    solar_area = compute_solar_area_per_pkg(6.0, 0.20, kw_per_pkg_path="x", efficiency_path="y")
    vol_pkg = compute_volume_per_pkg(
        solar_area.value,  # type: ignore[arg-type]
        80.0,
        6.0,
        solar_area_path="x",
        fold_ratio_path="y",
        pitch_path="z",
    )
    vol_node = compute_volume_per_node(
        100,
        vol_pkg.value,  # type: ignore[arg-type]
        0.30,
        n_path="x",
        vol_per_pkg_path="y",
        mounting_path="z",
    )
    # ~5.2 m3 (folded array ~0.2 m3 + 5.0 m3 bus). Far under the 80 m3
    # Neutron fairing: large volume slack, mass binds first (D6).
    assert 4.0 < vol_node.value < 8.0  # type: ignore[operator]
    util = compute_volume_utilization(
        vol_node.value,  # type: ignore[arg-type]
        80.0,
        node_volume_path="x",
        fairing_volume_path="y",
    )
    # Volume utilization well under 100% — volume never binds.
    assert util.value < 15.0  # type: ignore[operator]
