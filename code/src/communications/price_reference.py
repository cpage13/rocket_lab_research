"""The space-side price / collectability reference lines and the scope split.

RENAMED from the design's ``demand`` module by plan Section 0.0 Amendment A1.
Demand is ASSUMED, not modeled: if the delivered price undercuts what ground
charges and that price is collectable, the customers follow ("if the price is
right, they will come"). This module therefore carries ONLY price/collectability
references and a geographic scope split, NOT a demand, top-down-market, growth,
or capture-share lever. The top-down addressable-market projection machinery the
pre-A1 design described (a horizon-grown total-addressable figure and its growth
dial) is DELETED by A1 and is not built here: a top-down projection with a growth
dial IS demand modeling, it does not enter the bottom-up cost, and so it changes
no verdict.

The lines this module produces, which the Phase-4 revenue-ceiling reconciliation
consumes:

* The PRICED per-customer revenue: the bottom-up per-customer cost marked up by
  the fixed 1.5x revenue multiple (a 33.3% regular margin). This is the figure
  the retail-undercut check compares against the founder-set retail reference.
* The ARPU-COLLECTABLE revenue: ``arpu x 12 x operator_revenue_share``, the
  ceiling the priced cost must not exceed to be a collectable win.
* The SCOPE-weighted customers: a geographic ALLOCATION of the computed served
  band across US / Europe / Asia-ex-China, NOT a captured market share.

This module computes the SPACE-side lines only; it does NOT compute the
cost-to-cost ratio, the retail-undercut verdict, or the reconciliation itself
(those compare the space side to the ground side, which is Phase 4). The
customers-served number is the spectrum-capacity physics (Phase-2 spectrum
module), never a demand estimate or a fraction of a market.
"""

from __future__ import annotations

import logging

from common.provenance import FieldPath, ProvenanceCell, cell
from communications.config import PriceReferenceDials, ScopeWeights
from communications.constants import MONTHS_PER_YEAR, REVENUE_MULTIPLE
from communications.output import CustomerBandBlock

logger = logging.getLogger(__name__)

_DESIGN = "research/comms_model_design/DESIGN.md"

# The three geographic scope regions (a fixed, enum-like set; an unknown region
# is a programming error, raised explicitly rather than silently ignored).
_SCOPE_REGIONS = ("us", "europe", "asia_ex_china")


def compute_priced_cost_per_customer(
    cost_annual_per_customer_usd: float,
    *,
    cost_path: FieldPath,
) -> ProvenanceCell:
    """Priced per-customer revenue: the per-customer cost marked up by the multiple.

    ``priced = cost_annual_per_customer x REVENUE_MULTIPLE`` where
    ``REVENUE_MULTIPLE = 1.5`` (a 33.3% regular margin held equal on both sides;
    ``DESIGN.md`` Section 7). This is the priced cost the retail-undercut check
    (Phase 4) compares against the founder-set retail reference, and the figure
    the revenue-ceiling reconciliation (Phase 4) checks against the
    ARPU-collectable revenue. It is NOT a captured-share revenue and NOT a
    market estimate.

    Args:
        cost_annual_per_customer_usd: The annual per-customer cost, USD/yr.
        cost_path: JSON path of the per-customer-cost cell.

    Returns:
        A :class:`ProvenanceCell` carrying the priced per-customer revenue,
        USD/yr.
    """
    return cell(
        value=cost_annual_per_customer_usd * REVENUE_MULTIPLE,
        unit="USD",
        formula_name="comms_priced_cost_from_cost_and_multiple",
        uses=[cost_path],
        sources=[f"{_DESIGN}#section-7"],
        description=(
            "Priced per-customer revenue (USD/yr): the per-customer cost marked "
            "up by the 1.5x regular-margin multiple."
        ),
    )


def compute_priced_cost_band(
    *,
    cost_low: float,
    cost_mid: float,
    cost_high: float,
    band_uses: list[FieldPath],
) -> CustomerBandBlock:
    """Priced per-customer revenue band: each cost-band member marked up by the multiple.

    Every member's priced VALUE is produced by
    :func:`compute_priced_cost_per_customer` so the 1.5x markup has a single
    production source (the canonical helper), rather than an inline multiply.
    The three returned cells are then re-emitted carrying the shared ``band_uses``
    (the full cost-band path set) so the band's provenance trace, ``formula_name``
    (``comms_priced_cost_from_cost_and_multiple``), and emitted values are
    identical to the prior engine output.

    Args:
        cost_low: The band-low per-customer cost, USD/yr.
        cost_mid: The band-mid per-customer cost, USD/yr.
        cost_high: The band-high per-customer cost, USD/yr.
        band_uses: The shared upstream cost-band paths every member derives from.

    Returns:
        A :class:`CustomerBandBlock` of three priced per-customer-revenue cells.
    """

    def _member(cost_value: float, position: str) -> ProvenanceCell:
        """Priced cell for one band member: value via the canonical helper, shared uses."""
        priced_value = compute_priced_cost_per_customer(cost_value, cost_path=band_uses[0]).value
        return cell(
            value=priced_value,
            unit="USD",
            formula_name="comms_priced_cost_from_cost_and_multiple",
            uses=band_uses,
            sources=[f"{_DESIGN}#section-7"],
            description=f"Priced per-customer revenue (cost x 1.5), USD/yr, band-{position}.",
        )

    return CustomerBandBlock(
        low=_member(cost_low, "low"),
        mid=_member(cost_mid, "mid"),
        high=_member(cost_high, "high"),
    )


def compute_arpu_collectable_revenue(
    dials: PriceReferenceDials,
    *,
    dials_path: FieldPath,
) -> ProvenanceCell:
    """Annual per-customer revenue the operator can collect, USD/yr.

    ``arpu_usd_per_month x MONTHS_PER_YEAR x operator_revenue_share`` (the
    revenue-ceiling reconciliation basis; plan Section 0.9 the revenue-ceiling
    rule). This is the CEILING the priced cost must not exceed to be a
    collectable win; Phase 4 reconciles the two. Computing it here keeps the
    ceiling a source-linked cell.

    Args:
        dials: The price-reference dials (ARPU and operator share).
        dials_path: JSON path of the price-reference dials block.

    Returns:
        A :class:`ProvenanceCell` carrying the ARPU-collectable revenue,
        USD/yr.
    """
    collectable = dials.arpu_usd_per_month * MONTHS_PER_YEAR * dials.operator_revenue_share
    return cell(
        value=collectable,
        unit="USD",
        formula_name="comms_arpu_collectable_revenue_from_arpu_and_share",
        uses=[
            f"{dials_path}.arpu_usd_per_month",
            f"{dials_path}.operator_revenue_share",
        ],
        sources=[f"{_DESIGN}#section-7"],
        description=(
            "Annual per-customer revenue the operator can collect (USD/yr): ARPU "
            "times twelve months times the operator revenue share."
        ),
    )


def compute_scope_weighted_customers(
    total_served: float,
    scope: ScopeWeights,
    *,
    region: str,
    total_served_path: FieldPath,
    scope_path: FieldPath,
) -> ProvenanceCell:
    """Customers in one scope region by the scope-weight split.

    ``total_served x scope.<region>`` for ``region`` in
    ``{"us", "europe", "asia_ex_china"}`` (the scope split, US + Europe + Asia
    ex-China; ``DESIGN.md`` Section 8). The weights sum to 1 (validated in the
    config), so the three regional cells sum to ``total_served``. This is a
    geographic ALLOCATION of the computed served band, NOT a captured market
    share.

    Args:
        total_served: A total-served value (a band member; the engine calls this
            once per band member per region).
        scope: The scope weights.
        region: ``"us"`` / ``"europe"`` / ``"asia_ex_china"``.
        total_served_path: JSON path of the total-served cell.
        scope_path: JSON path of the scope-weights block.

    Returns:
        A :class:`ProvenanceCell` carrying the regional customer count, subs.

    Raises:
        ValueError: If ``region`` is not one of the three scope keys.
    """
    if region not in _SCOPE_REGIONS:
        raise ValueError(f"region must be one of {_SCOPE_REGIONS} (got {region!r})")
    weight = getattr(scope, region)
    return cell(
        value=total_served * weight,
        unit="subs",
        formula_name="comms_scope_weighted_customers_from_total_and_weight",
        uses=[total_served_path, f"{scope_path}.{region}"],
        sources=[f"{_DESIGN}#section-8"],
        description=(
            f"Customers allocated to the {region} scope region by the scope-weight "
            f"split (geographic context, not a captured market share), subs."
        ),
    )


__all__ = [
    "compute_arpu_collectable_revenue",
    "compute_priced_cost_band",
    "compute_priced_cost_per_customer",
    "compute_scope_weighted_customers",
]
