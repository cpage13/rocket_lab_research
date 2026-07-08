"""The comms two-regime ground comparison: the model's own cellular space cost vs ground.

This is the SLIM, clean-rewrite ground module. It compares THIS model's OWN
COMPUTED cellular annual cost per subscriber (the space side, a plain ``float``
supplied by the caller, computed by Phase 3 as steady-state annual cost divided by
subscribers served) against TWO marked CELLULAR-ground baselines, the dense-served
incumbent-marginal cost and the sparse fresh-build cost, supplied as a
:class:`communications.config.GroundInterfaceDials` interface block. The space side
is NEVER Starlink's disclosed broadband per-subscriber number (that is a
broadband-product figure for a different product and a different cost stack); only
the model's own computed cellular figure feeds this comparison.

It mirrors the data-center ``ground.py`` ratio mechanics exactly (the total/total
ratio, the 0.5x / 2.0x materiality bands, the ``_safe_ratio`` zero-denominator
guard, the plain-language verdict label) AND the OLD comms ``comparison.py``
two-regime SHAPE (a :class:`~communications.constants.DensityRegime` enum, a
per-regime ratio object, and a per-regime "space is cheaper" boolean). It does NOT
carry the old module's bloat: there are NO ProvenanceCells (this works in plain
floats), NO price-undercut check, NO revenue-ceiling reconciliation, NO
Starlink-floor honesty block, and NO ARPU / operator-share / retail-reference
reads. Those belong to the cut price layer; this module is the cost-to-cost ratio
over two ground denominators and nothing more.

The ground baselines stay MARKED INTERFACE INPUTS the caller supplies (the founder
owns the final ground call): with ``ground=None`` the comparison is absent entirely
and the caller reports the space cost alone; with either regime's baseline ``None``
that one regime's face is absent while the other still computes. The HEADLINE
verdict is a single boolean, ``headline_space_below_sparse_fresh_build``: space
landing below the sparse fresh-build ground cost is the niche.

This module imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from communications.config import GroundInterfaceDials
from communications.constants import DensityRegime

logger = logging.getLogger(__name__)


# ===========================================================================
# Named constants: the materiality bands and the safe-ratio guard
# ===========================================================================

GROUND_MATERIALLY_CHEAPER_RATIO: Final[float] = 0.5
"""Ground/space ratio below which ground is materially cheaper than space.

Mirrors the data-center ``GROUND_MATERIALLY_CHEAPER_RATIO``: a ground cost less
than half the space cost (ratio < 0.5) means ground wins materially in that
regime (expected in the dense served market)."""

SPACE_MATERIALLY_CHEAPER_RATIO: Final[float] = 2.0
"""Ground/space ratio above which space is materially cheaper than ground.

Mirrors the data-center ``ORBITAL_MATERIALLY_CHEAPER_RATIO`` (here "orbital"
reads as "space"): a ground cost more than twice the space cost (ratio > 2.0)
means space wins materially in that regime (expected in the sparse fresh-build
fringe, the niche)."""

SPACE_CHEAPER_AT_ALL_RATIO: Final[float] = 1.0
"""Ground/space ratio above which space is cheaper than ground AT ALL.

The per-regime ``space_is_cheaper`` boolean uses this any-amount threshold
(ground_to_space_ratio > 1.0), DELIBERATELY NOT the 2.0 materially-cheaper
threshold the old ``comparison.py`` used for its boolean. The plan calls for the
"space cheaper at all" reading; the 0.5 / 2.0 bands still set the verdict
LABEL."""

ZERO_COST: Final[float] = 0.0
"""Zero-denominator guard value for :func:`_safe_ratio`.

A space-cost denominator equal to this triggers the ``None`` path (a ratio is not
computable), mirroring the data-center ground ``ZERO_COST`` guard."""


# ===========================================================================
# The verdict label enum (mirrors the DC GroundConclusionLabel)
# ===========================================================================


class GroundConclusionLabel(StrEnum):
    """Plain-language conclusion labels for one regime's cost-to-cost comparison.

    Mirrors the data-center ``GroundConclusionLabel`` strings verbatim for
    cross-model consistency ("orbital" reads as "space" in the comms context): a
    ground/space ratio inside ``[0.5, 2.0]`` is the same order of magnitude;
    below 0.5 ground is materially cheaper; above 2.0 space (the "orbital" side)
    is materially cheaper.
    """

    SAME_ORDER = "same_order_of_magnitude"
    GROUND_CHEAPER = "ground_materially_cheaper"
    SPACE_CHEAPER = "orbital_materially_cheaper"


# ===========================================================================
# Custom exception (the basis assertion)
# ===========================================================================


class GroundBasisMismatchError(Exception):
    """Raised when the ground baselines and the space figure are on different bases."""


# ===========================================================================
# Data structures (frozen dataclasses, plain floats: NO ProvenanceCells)
# ===========================================================================


@dataclass(frozen=True)
class CommsRegimeComparison:
    """One density regime's cost-to-cost result: space cost vs that regime's ground cost.

    The two-regime shape mirrored from the old ``comparison.py``, stripped to plain
    floats. When the regime's ground baseline was not supplied (``None``), every
    derived field is ``None`` and the regime is reported as absent, not a crash.

    Attributes:
        regime: Which density regime this result is for (SPARSE or DENSE).
        ground_cost_per_subscriber_usd: The supplied ground baseline for this
            regime, USD/sub/yr, or ``None`` if the caller did not supply it.
        ground_to_space_ratio: Ground cost divided by space cost (the DC
            ground/orbital convention). ``None`` if the baseline was not supplied
            or the space cost is zero.
        space_to_ground_ratio: The inverse (space cost over ground cost), for
            convenience. ``None`` under the same conditions, or if the ground cost
            is zero.
        absolute_delta_usd: Ground cost minus space cost, USD/sub/yr. ``None`` if
            the baseline was not supplied.
        conclusion_label: The :class:`GroundConclusionLabel` value for this
            regime's ratio (0.5 / 2.0 bands). ``None`` if not computable.
        space_is_cheaper: Whether space costs less than ground in this regime at
            all (ground_to_space_ratio > 1.0); expected ``True`` in sparse,
            ``False`` in dense. ``None`` if not computable.
    """

    regime: DensityRegime
    ground_cost_per_subscriber_usd: float | None
    ground_to_space_ratio: float | None
    space_to_ground_ratio: float | None
    absolute_delta_usd: float | None
    conclusion_label: str | None
    space_is_cheaper: bool | None


@dataclass(frozen=True)
class CommsGroundComparison:
    """The by-density container: the dense and sparse regime results plus the headline.

    Mirrors the old ``ComparisonByDensity`` two-object split, plus the single
    headline boolean the steering names. The space cost is the same on both regimes
    (coverage is flat); only the ground denominator differs.

    Attributes:
        space_cost_per_subscriber_usd: The model's own computed cellular annual
            cost per subscriber, USD/sub/yr (the space side of every ratio).
        dense: The dense-served incumbent-marginal regime result.
        sparse: The sparse fresh-build regime result.
        headline_space_below_sparse_fresh_build: The niche test: ``True`` when the
            space cost lands below the sparse fresh-build ground cost (the sparse
            regime's ``space_is_cheaper``), ``False`` when at or above, ``None``
            when the sparse baseline was not supplied.
        basis: The shared basis label both sides are on (e.g.
            ``"annual_cost_per_subscriber"``); the comparison asserts the space and
            ground bases match before computing any ratio.
    """

    space_cost_per_subscriber_usd: float
    dense: CommsRegimeComparison
    sparse: CommsRegimeComparison
    headline_space_below_sparse_fresh_build: bool | None
    basis: str


# ===========================================================================
# Ratio + label helpers (mirror the DC ground mechanics)
# ===========================================================================


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    """Return ``numerator / denominator`` or ``None`` when the denominator is zero.

    Mirrors the data-center ground ``_safe_ratio``: a zero denominator yields
    ``None`` (with a logged warning) rather than raising, so a missing or zero cost
    produces an absent ratio instead of a crash.
    """
    if denominator == ZERO_COST:
        logger.warning("comms ground comparison ratio requested with zero denominator")
        return None
    return numerator / denominator


def _conclusion_label(ground_to_space_ratio: float | None) -> str | None:
    """Choose the plain-language verdict label for one regime's ground/space ratio.

    Mirrors the data-center ``_conclusion_label`` bands (< 0.5 ground cheaper,
    > 2.0 space cheaper, else same order), but returns ``None`` for a ``None``
    ratio rather than raising. The comms space-cost denominator can legitimately be
    zero (an edge case with zero subscribers served or zero cost), so a
    non-computable ratio is reported as an absent label, not an error.

    Args:
        ground_to_space_ratio: Ground cost divided by space cost, or ``None`` when
            the ratio is not computable.

    Returns:
        The :class:`GroundConclusionLabel` value, or ``None`` if the ratio is
        ``None``.
    """
    if ground_to_space_ratio is None:
        return None
    if ground_to_space_ratio < GROUND_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.GROUND_CHEAPER.value
    if ground_to_space_ratio > SPACE_MATERIALLY_CHEAPER_RATIO:
        return GroundConclusionLabel.SPACE_CHEAPER.value
    return GroundConclusionLabel.SAME_ORDER.value


# ===========================================================================
# Per-regime builder
# ===========================================================================


def _build_regime_comparison(
    regime: DensityRegime,
    ground_cost_per_subscriber_usd: float | None,
    space_cost_per_subscriber_usd: float,
) -> CommsRegimeComparison:
    """Build one density regime's cost-to-cost comparison.

    When this regime's ground baseline is ``None`` (not supplied), the result is an
    absent face: the ground cost and every derived field are ``None``. Otherwise the
    ground/space ratio, its inverse, the verdict label, and the per-regime
    "space is cheaper at all" boolean are computed against the shared space cost.

    Args:
        regime: Which density regime this is (SPARSE or DENSE).
        ground_cost_per_subscriber_usd: The supplied ground baseline, USD/sub/yr,
            or ``None`` if the caller did not supply this regime.
        space_cost_per_subscriber_usd: The model's own computed cellular annual cost
            per subscriber, USD/sub/yr (the same on both regimes).

    Returns:
        A frozen :class:`CommsRegimeComparison`.
    """
    if ground_cost_per_subscriber_usd is None:
        return CommsRegimeComparison(
            regime=regime,
            ground_cost_per_subscriber_usd=None,
            ground_to_space_ratio=None,
            space_to_ground_ratio=None,
            absolute_delta_usd=None,
            conclusion_label=None,
            space_is_cheaper=None,
        )
    ground_to_space_ratio = _safe_ratio(
        ground_cost_per_subscriber_usd, space_cost_per_subscriber_usd
    )
    space_to_ground_ratio = _safe_ratio(
        space_cost_per_subscriber_usd, ground_cost_per_subscriber_usd
    )
    label = _conclusion_label(ground_to_space_ratio)
    space_is_cheaper = (
        None
        if ground_to_space_ratio is None
        else ground_to_space_ratio > SPACE_CHEAPER_AT_ALL_RATIO
    )
    return CommsRegimeComparison(
        regime=regime,
        ground_cost_per_subscriber_usd=ground_cost_per_subscriber_usd,
        ground_to_space_ratio=ground_to_space_ratio,
        space_to_ground_ratio=space_to_ground_ratio,
        absolute_delta_usd=ground_cost_per_subscriber_usd - space_cost_per_subscriber_usd,
        conclusion_label=label,
        space_is_cheaper=space_is_cheaper,
    )


# ===========================================================================
# Public builder
# ===========================================================================


def build_comms_ground_comparison(
    space_cost_per_subscriber_usd: float,
    space_basis: str,
    ground: GroundInterfaceDials | None,
) -> CommsGroundComparison | None:
    """Compare the model's own cellular space cost per subscriber against both ground regimes.

    The space side is THIS model's OWN COMPUTED cellular annual cost per subscriber,
    NOT Starlink's disclosed broadband per-subscriber number. For each ground regime
    whose baseline is supplied, this computes the ground/space ratio, its inverse,
    the 0.5 / 2.0-band verdict label, and the per-regime "space is cheaper" boolean;
    a regime with no baseline is reported as an absent face. The headline boolean is
    the sparse regime's "space is cheaper" (space below the sparse fresh-build cost
    is the niche).

    Args:
        space_cost_per_subscriber_usd: The model's own computed cellular annual cost
            per subscriber, USD/sub/yr (steady-state annual cost / subscribers
            served, from Phase 3).
        space_basis: The basis label the space figure is on (e.g.
            ``"annual_cost_per_subscriber"``); must match ``ground.basis``.
        ground: The two-regime ground interface block, or ``None``. When ``None``,
            no ground numbers were supplied and the caller reports the space cost
            alone.

    Returns:
        A frozen :class:`CommsGroundComparison`, or ``None`` when ``ground`` is
        ``None`` (the cost side does not block on the ground numbers).

    Raises:
        GroundBasisMismatchError: When ``ground.basis`` differs from
            ``space_basis`` (a build-and-hold space cost must never be compared
            against an annual ground cost).
    """
    if ground is None:
        return None
    if ground.basis != space_basis:
        raise GroundBasisMismatchError(
            "comms ground comparison basis mismatch: "
            f"space basis {space_basis!r} != ground basis {ground.basis!r}"
        )
    dense = _build_regime_comparison(
        DensityRegime.DENSE,
        ground.dense_ground_cost_per_subscriber_usd,
        space_cost_per_subscriber_usd,
    )
    sparse = _build_regime_comparison(
        DensityRegime.SPARSE,
        ground.sparse_ground_cost_per_subscriber_usd,
        space_cost_per_subscriber_usd,
    )
    return CommsGroundComparison(
        space_cost_per_subscriber_usd=space_cost_per_subscriber_usd,
        dense=dense,
        sparse=sparse,
        headline_space_below_sparse_fresh_build=sparse.space_is_cheaper,
        basis=ground.basis,
    )


__all__ = [
    "CommsGroundComparison",
    "CommsRegimeComparison",
    "GroundBasisMismatchError",
    "GroundConclusionLabel",
    "build_comms_ground_comparison",
]
