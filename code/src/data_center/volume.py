"""Volume model: stowed solar+radiator volume vs Neutron fairing.

Volume is computed and surfaced but does NOT gate N (D6 mass-only
binding). The binding_constraint enum surfaces which envelope is
active per year.

See `research/SOURCE_INDEX.md` for claim IDs and
`research/node_design/solar_radiator_trajectory.md` for the solar/radiator
dial narrative.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Final

from data_center.config import BindingConstraint
from data_center.constants import NODE_VOLUME_FIXED_M3, SOLAR_CONSTANT_W_M2
from data_center.provenance import FieldPath, ProvenanceCell, cell

logger = logging.getLogger(__name__)

# An envelope (mass or volume) is treated as binding once utilization reaches
# this percent — i.e. within 1% of the envelope ceiling.
ENVELOPE_BINDING_UTILIZATION_PCT: Final[float] = 99.0


@dataclass(frozen=True)
class VolumeBreakdown:
    """Volume calculation breakdown per node.

    Attributes:
        solar_area_per_pkg_m2: Solar collector area per package, m2.
        volume_per_pkg_m3: Stowed volume per package, m3.
        volume_per_node_m3: Total node stowed volume, m3.
        volume_utilization_pct: Volume used as percent of Neutron fairing.
        binding_constraint: Which envelope (mass/volume/both/neither) binds.
    """

    solar_area_per_pkg_m2: ProvenanceCell
    volume_per_pkg_m3: ProvenanceCell
    volume_per_node_m3: ProvenanceCell
    volume_utilization_pct: ProvenanceCell
    binding_constraint: ProvenanceCell


def compute_solar_area_per_pkg(
    kw_per_pkg: float,
    si_bol_efficiency: float,
    *,
    kw_per_pkg_path: FieldPath,
    efficiency_path: FieldPath,
) -> ProvenanceCell:
    """Solar collector area per package required to power it.

    Args:
        kw_per_pkg: The generation's per-package electrical power, kW.
        si_bol_efficiency: Si beginning-of-life AM0 conversion efficiency.
        kw_per_pkg_path: JSON path of the upstream per-package kW figure.
        efficiency_path: JSON path of the Si BOL efficiency dial.

    Returns:
        A :class:`ProvenanceCell` carrying the per-package solar area, m2.
    """
    value = (kw_per_pkg * 1000) / (SOLAR_CONSTANT_W_M2 * si_bol_efficiency)
    return cell(
        value=value,
        unit="m2",
        formula_name="solar_area_per_pkg_from_kw_and_eff",
        uses=[kw_per_pkg_path, efficiency_path],
        sources=[
            "research/SOURCE_INDEX.md#THR-002",
            "research/SOURCE_INDEX.md#THR-007",
        ],
        description="Si solar area per package required to supply pkg kW.",
    )


def compute_volume_per_pkg(
    solar_area_m2: float,
    fold_ratio: float,
    stowed_pitch_mm: float,
    *,
    solar_area_path: FieldPath,
    fold_ratio_path: FieldPath,
    pitch_path: FieldPath,
) -> ProvenanceCell:
    """Stowed volume per package (folded solar + co-mounted radiator).

    Args:
        solar_area_m2: Deployed solar area per package, m2.
        fold_ratio: Deployed-to-stowed solar-array area ratio.
        stowed_pitch_mm: Per-panel stowed thickness, mm.
        solar_area_path: JSON path of the upstream solar-area cell.
        fold_ratio_path: JSON path of the fold-ratio dial.
        pitch_path: JSON path of the stowed-pitch dial.

    Returns:
        A :class:`ProvenanceCell` carrying the per-package stowed volume, m3.
    """
    stowed_footprint_m2 = solar_area_m2 / fold_ratio
    volume_m3 = stowed_footprint_m2 * (stowed_pitch_mm / 1000.0)
    return cell(
        value=volume_m3,
        unit="m3",
        formula_name="volume_per_pkg_stowed",
        uses=[solar_area_path, fold_ratio_path, pitch_path],
        sources=[
            "research/SOURCE_INDEX.md#THR-006",
            "research/node_design/solar_radiator_trajectory.md",
        ],
        description="Per-package stowed volume after folding + co-mounted radiator.",
    )


def compute_volume_per_node(
    n_packages: int,
    volume_per_pkg_m3: float,
    mounting_overhead_pct: float,
    *,
    n_path: FieldPath,
    vol_per_pkg_path: FieldPath,
    mounting_path: FieldPath,
    node_volume_fixed_path: FieldPath = "inputs.config.physical.node_volume_fixed_m3",
) -> ProvenanceCell:
    """Total node stowed volume including bus and mounting overhead.

    Args:
        n_packages: Packages per node.
        volume_per_pkg_m3: Stowed volume per package, m3.
        mounting_overhead_pct: Volume overhead from hinges, yokes, motors.
        n_path: JSON path of the upstream package-count cell.
        vol_per_pkg_path: JSON path of the upstream per-package-volume cell.
        mounting_path: JSON path of the mounting-overhead dial.
        node_volume_fixed_path: JSON path of the fixed node volume dial.

    Returns:
        A :class:`ProvenanceCell` carrying the total node stowed volume, m3.
    """
    array_volume = n_packages * volume_per_pkg_m3
    total = array_volume * (1.0 + mounting_overhead_pct) + NODE_VOLUME_FIXED_M3
    return cell(
        value=total,
        unit="m3",
        formula_name="volume_per_node_from_n_and_vol_per_pkg",
        uses=[n_path, vol_per_pkg_path, mounting_path, node_volume_fixed_path],
        sources=[
            "research/SOURCE_INDEX.md#THR-006",
            "research/node_design/node_mass_model.md",
        ],
        description="Total node stowed volume (array x (1+overhead) + bus).",
    )


def compute_volume_utilization(
    volume_per_node_m3: float,
    neutron_fairing_usable_volume_m3: float,
    *,
    node_volume_path: FieldPath,
    fairing_volume_path: FieldPath,
) -> ProvenanceCell:
    """Fraction of Neutron fairing volume used by stowed node.

    Args:
        volume_per_node_m3: Total node stowed volume, m3.
        neutron_fairing_usable_volume_m3: Neutron fairing usable volume, m3.
        node_volume_path: JSON path of the upstream node-volume cell.
        fairing_volume_path: JSON path of the fairing-volume dial.

    Returns:
        A :class:`ProvenanceCell` carrying volume utilization as a percent.
    """
    util = volume_per_node_m3 / neutron_fairing_usable_volume_m3 * 100.0
    return cell(
        value=util,
        unit="percent",
        formula_name="volume_utilization",
        uses=[node_volume_path, fairing_volume_path],
        sources=[
            "research/node_design/node_mass_model.md",
            "research/rocket_lab/neutron/neutron_specs.md",
        ],
        description="Volume utilization as percent of Neutron fairing usable volume.",
    )


def compute_binding_constraint(
    mass_util_pct: float,
    volume_util_pct: float,
    *,
    mass_util_path: FieldPath,
    volume_util_path: FieldPath,
) -> ProvenanceCell:
    """Which envelope (mass / volume / both / neither) binds at this year.

    Args:
        mass_util_pct: Mass utilization as a percent of the mass envelope.
        volume_util_pct: Volume utilization as a percent of the fairing.
        mass_util_path: JSON path of the upstream mass-utilization cell.
        volume_util_path: JSON path of the upstream volume-utilization cell.

    Returns:
        A :class:`ProvenanceCell` whose value is a :class:`BindingConstraint`
        enum string.
    """
    mass_bound = mass_util_pct >= ENVELOPE_BINDING_UTILIZATION_PCT
    volume_bound = volume_util_pct >= ENVELOPE_BINDING_UTILIZATION_PCT
    if mass_bound and volume_bound:
        val = BindingConstraint.BOTH.value
    elif mass_bound:
        val = BindingConstraint.MASS.value
    elif volume_bound:
        val = BindingConstraint.VOLUME.value
    else:
        val = BindingConstraint.NEITHER.value
    return cell(
        value=val,
        unit="enum",
        formula_name="binding_constraint_from_utilizations",
        uses=[mass_util_path, volume_util_path],
        sources=["research/SOURCE_INDEX.md#NTR-007", "mass-only binding scenario"],
        description="Which envelope is binding (mass / volume / both / neither).",
    )


__all__ = [
    "VolumeBreakdown",
    "compute_binding_constraint",
    "compute_solar_area_per_pkg",
    "compute_volume_per_node",
    "compute_volume_per_pkg",
    "compute_volume_utilization",
]
