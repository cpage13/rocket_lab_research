"""The shared cadence spine: the launch ramp, the cadence-indexed launch cost, their dials.

The one source both ventures use for the whole-fleet Neutron launch cadence:
the eight cadence and launch-cost defaults, the two validated dial blocks
(:class:`CadenceDials` and :class:`LaunchCostDials`, the ``cadence`` and
``launch_cost`` blocks of the data-center and communications configs), the
two cell functions that turn them into provenance cells
(:func:`compute_launches_per_year` and :func:`compute_launch_cost_musd`), and
:func:`round_half_up`, the one half-up rounding both models use.

The launch ramp is a logistic curve fit through the year-5 and year-10
scenario anchors. Those anchors are source-indexed as model scenarios
(``NTR-010``), not Rocket Lab guidance. Launch cost is the cadence-indexed
internal-cost estimate from ``NTR-009``.

The two cell functions return :class:`ProvenanceCell`; ``_log_interp`` stays
a bare helper. The cells compute exactly the v7 formulas.
"""

from __future__ import annotations

import logging
import math
from typing import Final

from pydantic import BaseModel, ConfigDict, Field, model_validator

from common.provenance import FieldPath, ProvenanceCell, cell

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cadence + launch-cost defaults (the one authority; both configs' dial blocks
# below default to these)
# ---------------------------------------------------------------------------

CADENCE_CEILING_DEFAULT: Final[int] = 150
"""ESTIMATE/SCENARIO (RLDC-CADENCE-CEILING-150, NTR-010; v7 archaeology).
Carrying capacity of the logistic launch ramp: a horizon-scoped
infrastructure parameter for the launch pads and rocket production
plausibly built within the ten-year window, not a cap on the system.
Launches are clamped to it inside the window; a longer-horizon run must
re-set it. Venture-model scenario, not Rocket Lab guidance."""

LAUNCHES_AT_YEAR_5_DEFAULT: Final[int] = 14
"""ESTIMATE/SCENARIO (NTR-010; v7 archaeology). Logistic anchor at
model year 5. Public launch counts are integer missions, not fractional
rates."""

LAUNCHES_AT_YEAR_10_DEFAULT: Final[int] = 90
"""ESTIMATE/SCENARIO (NTR-010; v7 archaeology). Logistic anchor at
model year 10; high-cadence venture scenario. With base year 2026, this
anchors FY2036 at about 90 launches."""

FIRST_LAUNCH_YEAR_DEFAULT: Final[int] = 1
"""ESTIMATE/SCENARIO (NTR-011; v7 archaeology). First venture launch
index (FY2027 if base_year=2026), downstream of Rocket Lab's forward-
looking late-2026 Neutron first-flight target."""

LOW_CADENCE_COST_MUSD_DEFAULT: Final[float] = 25.0
"""ESTIMATE (NTR-009). Launch cost at low cadence (<=5 launches/yr).
Use as a cadence-specific model estimate, not a certified internal
Rocket Lab cost."""

HIGH_CADENCE_COST_MUSD_DEFAULT: Final[float] = 13.5
"""ESTIMATE (NTR-009). Launch cost at high cadence (>=100 launches/yr).
Learning-curve scenario inside the $12-15M very-high-cadence band."""

LOW_CADENCE_LAUNCHES_DEFAULT: Final[float] = 5.0
"""ESTIMATE (NTR-009). Cadence at low-cost anchor."""

HIGH_CADENCE_LAUNCHES_DEFAULT: Final[float] = 100.0
"""ESTIMATE (NTR-009, NTR-010). Cadence at high-cost anchor; model
scenario, not published Rocket Lab guidance."""

YEAR_5_ANCHOR_IDX: Final[float] = 5.0
"""Launch-ramp anchor index for the year-5 cadence dial."""

YEAR_10_ANCHOR_IDX: Final[float] = 10.0
"""Launch-ramp anchor index for the year-10 cadence dial."""

ROUND_TO_NEAREST_OFFSET: Final[float] = 0.5
"""Offset added before flooring to round a non-negative quantity to the nearest
integer, half up: every half-up rounding in the models uses it
(:func:`round_half_up`, and the communications launch-share count, which adds
its own float tolerance on top)."""


# ---------------------------------------------------------------------------
# The two dial blocks (each config's ``cadence`` and ``launch_cost`` block)
# ---------------------------------------------------------------------------


class CadenceDials(BaseModel):
    """Whole-fleet launch-cadence dials feeding the logistic launches-per-year ramp.

    The ``cadence`` block of both the data-center and the communications
    config. The defaults are a source-indexed scenario: ``launches_at_year_5``
    and ``launches_at_year_10`` fit the logistic curve to integer mission
    counts. ``first_launch_year`` only clamps earlier years to zero; it does
    not move the year-5 or year-10 anchors. Consumed by
    :func:`compute_launches_per_year`.

    The logistic fit needs ``0 < launches_at_year_5 < launches_at_year_10 <
    cadence_ceiling`` (the condition :func:`compute_launches_per_year` raises
    on); :meth:`_anchors_inside_logistic_range` rejects any other combination
    at load instead of letting a model fail mid-run.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    cadence_ceiling: int = Field(
        default=CADENCE_CEILING_DEFAULT,
        gt=0,
        description=(
            "Carrying capacity of the logistic launch ramp, launches per year: a "
            "horizon-scoped infrastructure parameter standing for the launch pads "
            "and rocket production plausibly built within the modeled ten-year "
            "window (RLDC-CADENCE-CEILING-150), not a cap on the system. Launches "
            "are clamped to it inside the window; a longer-horizon run re-sets it."
        ),
    )
    launches_at_year_5: int = Field(
        default=LAUNCHES_AT_YEAR_5_DEFAULT,
        ge=0,
        description="Integer logistic anchor: launches per year at model year 5.",
    )
    launches_at_year_10: int = Field(
        default=LAUNCHES_AT_YEAR_10_DEFAULT,
        ge=0,
        description="Integer logistic anchor: launches per year at model year 10.",
    )
    first_launch_year: int = Field(
        default=FIRST_LAUNCH_YEAR_DEFAULT,
        ge=0,
        description="Model-year index before which launch count is clamped to zero.",
    )

    @model_validator(mode="after")
    def _anchors_inside_logistic_range(self) -> CadenceDials:
        """Require ``0 < launches_at_year_5 < launches_at_year_10 < cadence_ceiling``."""
        y5 = self.launches_at_year_5
        y10 = self.launches_at_year_10
        ceiling = self.cadence_ceiling
        if not 0 < y5 < y10 < ceiling:
            raise ValueError(
                "cadence anchors must satisfy 0 < launches_at_year_5 < "
                "launches_at_year_10 < cadence_ceiling (the logistic ramp is fit "
                f"through them); got launches_at_year_5={y5}, "
                f"launches_at_year_10={y10}, cadence_ceiling={ceiling}"
            )
        return self


class LaunchCostDials(BaseModel):
    """Cadence-indexed launch-cost dials feeding the log-linear cost curve.

    The ``launch_cost`` block of both the data-center and the communications
    config; the cost is priced at the whole-fleet cadence. Consumed by
    :func:`compute_launch_cost_musd`. The low-cost anchor must sit at a lower
    cadence than the high-cadence anchor (:meth:`_cadence_anchors_ordered`):
    reversed anchors would flat-clamp every year to the low-cadence cost and
    silently switch the cost-down off.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    low_cadence_cost_musd: float = Field(
        default=LOW_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the low-cadence anchor, $M.",
    )
    high_cadence_cost_musd: float = Field(
        default=HIGH_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the high-cadence anchor, $M.",
    )
    low_cadence_launches: float = Field(
        default=LOW_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the low-cost anchor.",
    )
    high_cadence_launches: float = Field(
        default=HIGH_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the high-cost anchor.",
    )

    @model_validator(mode="after")
    def _cadence_anchors_ordered(self) -> LaunchCostDials:
        """Require ``low_cadence_launches < high_cadence_launches``."""
        if not self.low_cadence_launches < self.high_cadence_launches:
            raise ValueError(
                "launch-cost anchors must satisfy low_cadence_launches < "
                "high_cadence_launches (the log-linear curve runs from the low "
                f"to the high cadence); got low_cadence_launches="
                f"{self.low_cadence_launches}, high_cadence_launches="
                f"{self.high_cadence_launches}"
            )
        return self


def _log_interp(x: float, x_lo: float, x_hi: float, y_lo: float, y_hi: float) -> float:
    """Log-linear interpolation, flat-clamped outside ``[x_lo, x_hi]``.

    Lifted verbatim from v7 ``engine.py:892-906`` at ``8fdc210``.

    Args:
        x: The query point on the x-axis.
        x_lo: Lower x anchor (must be > 0 for the log to be defined).
        x_hi: Upper x anchor (must be > 0 and > ``x_lo``).
        y_lo: y value at ``x_lo``.
        y_hi: y value at ``x_hi``.

    Returns:
        ``y_lo`` for ``x <= x_lo``, ``y_hi`` for ``x >= x_hi``, and the
        log-linear interpolant between the anchors otherwise.
    """
    if x <= x_lo:
        return y_lo
    if x >= x_hi:
        return y_hi
    frac = (math.log(x) - math.log(x_lo)) / (math.log(x_hi) - math.log(x_lo))
    return y_lo + frac * (y_hi - y_lo)


def _logit_launch_anchor(launches: int, cadence_ceiling: int) -> float:
    """Return the logistic logit for a launch-rate anchor.

    Args:
        launches: Launches per year at the anchor.
        cadence_ceiling: The maximum launch cadence.

    Returns:
        The logistic logit for ``launches / cadence_ceiling``.

    Raises:
        ValueError: If the anchor is outside the open interval
            ``(0, cadence_ceiling)``.
    """
    if launches <= 0 or launches >= cadence_ceiling:
        raise ValueError(
            "launch anchor must be greater than 0 and less than cadence_ceiling "
            f"(launches={launches}, cadence_ceiling={cadence_ceiling})"
        )
    return math.log(launches / (cadence_ceiling - launches))


def round_half_up(quantity: float) -> int:
    """Round a non-negative quantity to the nearest integer, half up.

    ``floor(quantity + ROUND_TO_NEAREST_OFFSET)``: the one half-up rounding both
    models use (the launch ramp's mission counts here; the communications
    subscriber density, served base, and ARPU bucket counts), where Python's
    ``round`` would round an exact half to even.

    Args:
        quantity: A non-negative quantity, e.g. the smooth logistic launch rate.

    Returns:
        The nearest whole number, rounded half up.
    """
    return math.floor(quantity + ROUND_TO_NEAREST_OFFSET)


def compute_launches_per_year(
    year_idx: int,
    *,
    dials_path: FieldPath = "inputs.config.cadence",
    cadence_ceiling: int = CADENCE_CEILING_DEFAULT,
    launches_at_year_5: int = LAUNCHES_AT_YEAR_5_DEFAULT,
    launches_at_year_10: int = LAUNCHES_AT_YEAR_10_DEFAULT,
    first_launch_year: int = FIRST_LAUNCH_YEAR_DEFAULT,
) -> ProvenanceCell:
    """Integer launches per year via a logistic ramp.

    Logistic: ``L(t) = ceiling / (1 + exp(-k(t - t0)))`` where ``(k, t0)``
    are fit to pass through ``(5, launches_at_year_5)`` and
    ``(10, launches_at_year_10)``. The smooth value is rounded before it
    leaves this module: launches are missions, not fractional rates.
    ``first_launch_year`` only clamps earlier model years to zero; it does
    not shift the year-5 or year-10 anchors.

    Args:
        year_idx: Zero-based model year index.
        dials_path: JSON path of the upstream cadence-dials block.
        cadence_ceiling: Hard cap on launches per year.
        launches_at_year_5: Logistic anchor at year 5.
        launches_at_year_10: Logistic anchor at year 10.
        first_launch_year: Model-year index before which launch count is zero.

    Returns:
        A :class:`ProvenanceCell` carrying an integer launches-per-year count:
        ``0`` for ``year_idx < first_launch_year``; otherwise the rounded
        logistic value clamped to ``cadence_ceiling``.
    """
    if year_idx < first_launch_year:
        value = 0
    else:
        if launches_at_year_10 <= launches_at_year_5:
            raise ValueError(
                "launches_at_year_10 must be greater than launches_at_year_5 "
                f"({launches_at_year_10} <= {launches_at_year_5})"
            )
        logit_y5 = _logit_launch_anchor(launches_at_year_5, cadence_ceiling)
        logit_y10 = _logit_launch_anchor(launches_at_year_10, cadence_ceiling)
        k = (logit_y10 - logit_y5) / (YEAR_10_ANCHOR_IDX - YEAR_5_ANCHOR_IDX)
        t0 = YEAR_5_ANCHOR_IDX - logit_y5 / k
        raw = cadence_ceiling / (1.0 + math.exp(-k * (year_idx - t0)))
        value = min(round_half_up(raw), cadence_ceiling)
    return cell(
        value=value,
        unit="count",
        formula_name="launches_per_year_from_logistic",
        uses=[
            f"{dials_path}.cadence_ceiling",
            f"{dials_path}.launches_at_year_5",
            f"{dials_path}.launches_at_year_10",
            f"{dials_path}.first_launch_year",
        ],
        sources=[
            "research/SOURCE_INDEX.md#NTR-010",
            "research/rocket_lab/neutron/launch_cost_economics.md",
        ],
        description=f"Integer launches per year at year_idx={year_idx} (rounded logistic ramp).",
    )


def compute_launch_cost_musd(
    launches_per_year: float,
    *,
    dials_path: FieldPath = "inputs.config.launch",
    low_cadence_cost_musd: float = LOW_CADENCE_COST_MUSD_DEFAULT,
    high_cadence_cost_musd: float = HIGH_CADENCE_COST_MUSD_DEFAULT,
    low_cadence_launches: float = LOW_CADENCE_LAUNCHES_DEFAULT,
    high_cadence_launches: float = HIGH_CADENCE_LAUNCHES_DEFAULT,
) -> ProvenanceCell:
    """Cadence-indexed launch cost via log-linear interpolation.

    Formula: log-linear interpolation between ``(low_cadence_launches,
    low_cadence_cost_musd)`` and ``(high_cadence_launches,
    high_cadence_cost_musd)``, flat-clamped outside the anchors.

    Args:
        launches_per_year: The cadence at which to price a launch.
        dials_path: JSON path of the upstream launch-cost-dials block.
        low_cadence_cost_musd: Launch cost at the low-cadence anchor, $M.
        high_cadence_cost_musd: Launch cost at the high-cadence anchor, $M.
        low_cadence_launches: Cadence at the low-cost anchor.
        high_cadence_launches: Cadence at the high-cost anchor.

    Returns:
        A :class:`ProvenanceCell` carrying the interpolated launch cost
        in $M.
    """
    value = _log_interp(
        launches_per_year,
        low_cadence_launches,
        high_cadence_launches,
        low_cadence_cost_musd,
        high_cadence_cost_musd,
    )
    return cell(
        value=value,
        unit="MUSD",
        formula_name="launch_cost_musd_from_cadence_log_linear",
        uses=[
            f"{dials_path}.low_cadence_cost_musd",
            f"{dials_path}.high_cadence_cost_musd",
            f"{dials_path}.low_cadence_launches",
            f"{dials_path}.high_cadence_launches",
        ],
        sources=[
            "research/SOURCE_INDEX.md#NTR-009",
            "research/rocket_lab/neutron/launch_cost_economics.md",
        ],
        description=f"Launch cost at cadence={launches_per_year} launches/yr.",
    )
