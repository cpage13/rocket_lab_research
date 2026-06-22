"""The spectrum requirement, the empirical capacity anchor, and the customer chain.

This is the one genuinely new piece of physics in the comms model (the
data-center has no spectrum). It implements the ``SPECTRUM_spec.md`` Appendix
chain EXACTLY:

* The spectrum REQUIREMENT is the per-beam channel width, reused across every
  beam by angular separation: ``spectrum_to_acquire_mhz = leased_bandwidth_mhz``,
  independent of beam count and satellite count. It is a reported requirement
  and a binary partner GATE (has a carrier agreed to an SCS lease), NOT a cost
  line: under the lease its cost is near zero, so it nets out of the cost
  comparison by construction.
* Per-beam CAPACITY comes from the EMPIRICAL AST anchor (about 120 Mbps measured
  on about 40 MHz), scaled linearly with leased bandwidth, NEVER from a naive
  bandwidth-times-spectral-efficiency division. The naive figure is emitted only
  as a labeled cross-check (the naive-division disaster gate, plan Section 0.9).
* The customer chain (customers per beam, per satellite, total served) emits as
  a low/mid/high planning BAND, never a scalar (the point-estimate disaster
  gate). The band is formed by an INVERTED pairing on the per-user rate: a higher
  per-user rate provisions a fatter pipe and therefore serves FEWER subscribers,
  so ``rate_band.high`` feeds the customer-LOW member.

``num_satellites`` is NOT computed here; the spectrum module is the
capacity-to-customers bridge and consumes the living-fleet satellite count from
upstream (the constellation / engine). It does not set a constellation size.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from common.provenance import FieldPath, ProvenanceCell, cell
from communications.config import BandTriple, SpectrumDials
from communications.constants import (
    PER_BEAM_CAPACITY_ANCHOR_MBPS,
    PER_BEAM_CAPACITY_ANCHOR_MHZ,
)

logger = logging.getLogger(__name__)

_DESIGN_SPECTRUM = "research/comms_model_design/SPECTRUM_spec.md"


# ===========================================================================
# 1. The band-leaf shape (three sibling cells, not one cell of a triple)
# ===========================================================================


@dataclass(frozen=True)
class CustomerBand:
    """A low/mid/high planning band of a customer-chain quantity, each a cell.

    The band-leaf shape this phase commits to: ONE dataclass holding THREE
    ProvenanceCells (low, mid, high), NOT a single cell whose value is a triple.
    (This resolves concern C4/Q4's Phase-2 share: a band leaf is three sibling
    cells, so each member carries its own formula, uses, and sources, and a cold
    reader queries ``...low``, ``...mid``, ``...high`` by path. Phase 3 applies
    this shape consistently to the customer outputs in the business block.)

    Attributes:
        low: The band-low member (FEWEST subscribers: the fattest pipe with the
            most conservative packing).
        mid: The band-mid member.
        high: The band-high member (MOST subscribers: the thinnest pipe with the
            most aggressive packing).
    """

    low: ProvenanceCell
    mid: ProvenanceCell
    high: ProvenanceCell


# ===========================================================================
# 2. The spectrum requirement and the per-beam capacity
# ===========================================================================


def compute_spectrum_to_acquire(
    dials: SpectrumDials,
    *,
    dials_path: FieldPath,
) -> ProvenanceCell:
    """The spectrum the constellation must acquire: one per-beam block, MHz.

    ``spectrum_to_acquire_mhz = leased_bandwidth_mhz`` (SPECTRUM_spec.md
    Section 1.2): one block reused across every beam and every satellite by
    angular separation, NOT that width times the beam count, and independent of
    the satellite count. This is a reported REQUIREMENT and a partner GATE, NOT a
    cost line (it nets out of the cost comparison by construction; the
    spectrum-as-cost disaster gate, plan Section 0.9).

    Args:
        dials: The spectrum dials.
        dials_path: JSON path of the spectrum dials block.

    Returns:
        A :class:`ProvenanceCell` carrying the spectrum to acquire, MHz.
    """
    return cell(
        value=dials.leased_bandwidth_mhz,
        unit="MHz",
        formula_name="comms_spectrum_to_acquire_from_leased",
        uses=[f"{dials_path}.leased_bandwidth_mhz"],
        sources=[f"{_DESIGN_SPECTRUM}#section-1.2"],
        description=(
            "Spectrum the constellation must acquire: one per-beam block, reused "
            "across every beam (a requirement and a partner gate, not a cost line), MHz."
        ),
    )


def compute_per_beam_capacity(
    dials: SpectrumDials,
    *,
    dials_path: FieldPath,
) -> ProvenanceCell:
    """Per-beam capacity from the EMPIRICAL AST anchor, Mbps.

    ``per_beam_capacity_mbps = PER_BEAM_CAPACITY_ANCHOR_MBPS x
    (leased_bandwidth_mhz / PER_BEAM_CAPACITY_ANCHOR_MHZ)`` (SPECTRUM_spec.md
    Section 2.1): the measured AST 40-MHz-to-120-Mbps relationship, scaled
    linearly with leased bandwidth. This is the capacity GENERATOR; the naive
    bandwidth-times-efficiency division is NEVER used to generate capacity (the
    naive-division disaster gate, plan Section 0.9).

    Args:
        dials: The spectrum dials.
        dials_path: JSON path of the spectrum dials block.

    Returns:
        A :class:`ProvenanceCell` carrying the per-beam capacity, Mbps.
    """
    capacity = PER_BEAM_CAPACITY_ANCHOR_MBPS * (
        dials.leased_bandwidth_mhz / PER_BEAM_CAPACITY_ANCHOR_MHZ
    )
    return cell(
        value=capacity,
        unit="Mbps",
        formula_name="comms_per_beam_capacity_from_empirical_anchor",
        uses=[f"{dials_path}.leased_bandwidth_mhz"],
        sources=[f"{_DESIGN_SPECTRUM}#section-2.1"],
        description=(
            "Per-beam capacity from the empirical AST 40-MHz-to-120-Mbps anchor, "
            "scaled by leased MHz, Mbps."
        ),
    )


def compute_naive_capacity_cross_check(
    dials: SpectrumDials,
    *,
    dials_path: FieldPath,
) -> ProvenanceCell:
    """The naive bandwidth-times-spectral-efficiency capacity, Mbps (CROSS-CHECK ONLY).

    ``naive_capacity_mbps = leased_bandwidth_mhz x spectral_efficiency_bps_per_hz``
    (SPECTRUM_spec.md Section 4). This is reported ALONGSIDE the empirical
    capacity as a transparency check, flagged that the empirical figure is higher
    because aperture and beam gain lift the engineered cell above the
    median-SINR floor. It is NEVER substituted for the empirical anchor.

    Args:
        dials: The spectrum dials.
        dials_path: JSON path of the spectrum dials block.

    Returns:
        A :class:`ProvenanceCell` carrying the naive cross-check capacity, Mbps.
    """
    naive = dials.leased_bandwidth_mhz * dials.spectral_efficiency_bps_per_hz
    return cell(
        value=naive,
        unit="Mbps",
        formula_name="comms_naive_capacity_cross_check",
        uses=[
            f"{dials_path}.leased_bandwidth_mhz",
            f"{dials_path}.spectral_efficiency_bps_per_hz",
        ],
        sources=[f"{_DESIGN_SPECTRUM}#section-4"],
        description=(
            "Naive bandwidth-times-spectral-efficiency capacity, Mbps: cross-check "
            "only, not the capacity generator (the empirical anchor is higher)."
        ),
    )


# ===========================================================================
# 3. The customer chain (a low/mid/high planning band)
# ===========================================================================


def compute_customers_per_beam_band(
    per_beam_capacity_mbps: float,
    rate_band: BandTriple,
    oversubscription_band: BandTriple,
    *,
    capacity_path: FieldPath,
    rate_band_path: FieldPath,
    oversubscription_band_path: FieldPath,
) -> CustomerBand:
    """Registered customers per beam, as a low/mid/high planning band.

    The chain line is ``customers_per_beam = (per_beam_capacity /
    target_per_user_rate) x oversubscription`` (SPECTRUM_spec.md Section 2.2),
    but the BAND is formed by an INVERTED pairing on the rate, because a higher
    per-user rate provisions a fatter pipe and therefore serves FEWER
    subscribers (plan Section 0.8, the binding band-convention):

      - ``low  = (per_beam_capacity / rate_band.high) x oversubscription_band.low``
      - ``mid  = (per_beam_capacity / rate_band.mid)  x oversubscription_band.mid``
      - ``high = (per_beam_capacity / rate_band.low)  x oversubscription_band.high``

    So the rate triple is consumed in REVERSE (``rate_band.high`` feeds the
    customer LOW member) while the oversubscription triple is consumed forward.
    This is the ONE place the low/mid/high label flips meaning between the input
    triple (raw magnitude) and the customer output (subscriber count).

    Args:
        per_beam_capacity_mbps: The empirical per-beam capacity, Mbps.
        rate_band: The per-user-rate band (stored ascending by magnitude).
        oversubscription_band: The oversubscription band (stored ascending).
        capacity_path: JSON path of the per-beam-capacity cell.
        rate_band_path: JSON path of the rate-band dials.
        oversubscription_band_path: JSON path of the oversubscription-band dials.

    Returns:
        A :class:`CustomerBand` of three cells (low/mid/high), each registered
        customers per beam.
    """
    low_value = (per_beam_capacity_mbps / rate_band.high) * oversubscription_band.low
    mid_value = (per_beam_capacity_mbps / rate_band.mid) * oversubscription_band.mid
    high_value = (per_beam_capacity_mbps / rate_band.low) * oversubscription_band.high
    uses = [
        capacity_path,
        f"{rate_band_path}.low",
        f"{rate_band_path}.mid",
        f"{rate_band_path}.high",
        f"{oversubscription_band_path}.low",
        f"{oversubscription_band_path}.mid",
        f"{oversubscription_band_path}.high",
    ]
    sources = [f"{_DESIGN_SPECTRUM}#section-2.2"]
    low = cell(
        value=low_value,
        unit="subs",
        formula_name="comms_customers_per_beam_from_capacity_rate_oversub",
        uses=uses,
        sources=sources,
        description=(
            "Registered customers per beam, band-low (fewest subscribers: the "
            "highest per-user rate with the lowest oversubscription)."
        ),
    )
    mid = cell(
        value=mid_value,
        unit="subs",
        formula_name="comms_customers_per_beam_from_capacity_rate_oversub",
        uses=uses,
        sources=sources,
        description="Registered customers per beam, band-mid.",
    )
    high = cell(
        value=high_value,
        unit="subs",
        formula_name="comms_customers_per_beam_from_capacity_rate_oversub",
        uses=uses,
        sources=sources,
        description=(
            "Registered customers per beam, band-high (most subscribers: the "
            "lowest per-user rate with the highest oversubscription)."
        ),
    )
    return CustomerBand(low=low, mid=mid, high=high)


def compute_customers_per_sat_band(
    customers_per_beam: CustomerBand,
    beams_per_sat: int,
    *,
    customers_per_beam_path: FieldPath,
    beams_per_sat_path: FieldPath,
) -> CustomerBand:
    """Registered customers per satellite, as a band: beams_per_sat x per-beam band.

    Each member is ``beams_per_sat x customers_per_beam.<member>``
    (SPECTRUM_spec.md Section 2.3). The band ordering is preserved (low stays
    low) because ``beams_per_sat`` is a positive scalar.

    Args:
        customers_per_beam: The per-beam customer band.
        beams_per_sat: Beams per satellite (a positive scalar).
        customers_per_beam_path: JSON path of the per-beam band sub-object.
        beams_per_sat_path: JSON path of the beams-per-sat dial.

    Returns:
        A :class:`CustomerBand` of three cells, registered customers per
        satellite.
    """
    return _scale_band(
        customers_per_beam,
        beams_per_sat,
        formula_name="comms_customers_per_sat_from_beams_and_per_beam",
        scalar_path=beams_per_sat_path,
        band_path=customers_per_beam_path,
        sources=[f"{_DESIGN_SPECTRUM}#section-2.3"],
        description_stub="Registered customers per satellite",
    )


def compute_total_served_band(
    customers_per_sat: CustomerBand,
    num_satellites: int,
    *,
    customers_per_sat_path: FieldPath,
    num_satellites_path: FieldPath,
) -> CustomerBand:
    """Total registered customers served, as a band: customers_per_sat x num_satellites.

    Each member is ``customers_per_sat.<member> x num_satellites``
    (SPECTRUM_spec.md Section 2.3). ``num_satellites`` is the living-fleet
    satellite count the engine (Phase 3) computes from the cohort treadmill and
    passes in; this module CONSUMES it, it does not set it.

    Args:
        customers_per_sat: The per-satellite customer band.
        num_satellites: The constellation satellite count (positive integer).
        customers_per_sat_path: JSON path of the per-satellite band sub-object.
        num_satellites_path: JSON path of the satellite-count cell.

    Returns:
        A :class:`CustomerBand` of three cells, total registered customers
        served.
    """
    return _scale_band(
        customers_per_sat,
        num_satellites,
        formula_name="comms_total_served_from_per_sat_and_count",
        scalar_path=num_satellites_path,
        band_path=customers_per_sat_path,
        sources=[f"{_DESIGN_SPECTRUM}#section-2.3"],
        description_stub="Total registered customers served",
    )


# ===========================================================================
# 4. Private helpers
# ===========================================================================


def _scale_band(
    band: CustomerBand,
    scalar: float,
    *,
    formula_name: str,
    scalar_path: FieldPath,
    band_path: FieldPath,
    sources: list[str],
    description_stub: str,
) -> CustomerBand:
    """Scale every member of a customer band by a positive scalar, preserving order.

    Args:
        band: The input customer band.
        scalar: The positive scalar to multiply each member by.
        formula_name: The FORMULAS key for the scaled cells.
        scalar_path: JSON path of the scalar cell/dial.
        band_path: JSON path of the input band sub-object.
        sources: Provenance citations for the scaled cells.
        description_stub: The leading phrase for each member's description.

    Returns:
        A :class:`CustomerBand` of three scaled cells (low/mid/high).
    """
    uses = [
        f"{band_path}.low",
        f"{band_path}.mid",
        f"{band_path}.high",
        scalar_path,
    ]
    return CustomerBand(
        low=cell(
            value=_cell_float(band.low) * scalar,
            unit="subs",
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-low (a planning-band member).",
        ),
        mid=cell(
            value=_cell_float(band.mid) * scalar,
            unit="subs",
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-mid (a planning-band member).",
        ),
        high=cell(
            value=_cell_float(band.high) * scalar,
            unit="subs",
            formula_name=formula_name,
            uses=uses,
            sources=sources,
            description=f"{description_stub}, band-high (a planning-band member).",
        ),
    )


def _cell_float(c: ProvenanceCell) -> float:
    """Read a numeric cell value as a plain float for downstream math.

    Args:
        c: A provenance cell whose value is a number.

    Returns:
        The cell value coerced to ``float``.

    Raises:
        TypeError: If the cell value is not a real number.
    """
    value = c.value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"cell value is not numeric: {value!r} (cell: {c.formula_name})")
    return float(value)


__all__ = [
    "CustomerBand",
    "compute_customers_per_beam_band",
    "compute_customers_per_sat_band",
    "compute_naive_capacity_cross_check",
    "compute_per_beam_capacity",
    "compute_spectrum_to_acquire",
    "compute_total_served_band",
]
