"""The communications CELLULAR cost engine: the per-year cohort treadmill.

``run_comms_model(config)`` drives the slim cost-to-serve model across the
horizon and returns a :class:`CommsTrajectory` of plain-numeric per-year rollups.
It mirrors the data-center model's fleet engine (the per-year loop in
``data_center/engine.py`` plus the living-cohort rollup in ``data_center/fleet.py``)
with three deliberate differences, all driven by the comms design:

1. Satellites per launch. The DC deploys one node per launch; comms deploys
   ``satellites_per_launch`` satellites per launch, so
   ``satellites_deployed_this_year = comms_launches_flown_this_year * satellites_per_launch``.
2. The build-and-hold cap (the treadmill). The DC fleet grows with cadence
   without bound. Comms builds toward the FLEET TARGET (the CAPACITY-sized fleet,
   :func:`compute_fleet_target`: the subscriber target divided by the per-satellite
   density, floored by the coverage floor and capped by the saturation cap) and
   then HOLDS: once the target is reached it deploys only enough whole launches to
   replace the cohorts ageing off the 5-year cliff, so the living count stays at (or
   as close as launch granularity allows to) the fleet target.
3. Two cadence roles. The shared whole-fleet logistic ramp
   (``common.cadence.compute_launches_per_year``, the 90/year FY2036 ramp) sets
   the WHOLE-fleet launch count. The comms slice flies a SHARE of it
   (``share_of_fleet``). The launch COST is priced at the WHOLE-fleet cadence
   (the cadence-indexed cost-down is a Neutron-production-scale effect shared
   across the whole program, not the comms slice's own rate); the comms share
   sets only how many launches comms flies. This is the load-bearing
   distinction: cost is priced at fleet cadence, the count flown is the comms
   share. (If the founder later wants the comms slice priced at its own lower
   cadence, that is a documented alternative; the default is fleet-cadence
   pricing.)

The cohort cliff is the shared ``common.cohort.LivedCohort`` /
``living_cohorts`` machinery, reused unchanged: a cohort is alive in the
half-open interval ``[launch_year, launch_year + satellite_lifetime_years)``.
The shared ``LivedCohort`` carries only ``launch_year`` + ``units_deployed``,
which is exactly what comms needs (no per-satellite economics ride on the
cohort, unlike the DC ``Cohort``), so comms uses it directly with no subclass.

The two shared ``common.cadence`` functions return a ``ProvenanceCell``; this
engine unwraps each ``.value`` to a plain ``float``/``int`` ONCE (via the
private ``_cell_float`` / ``_cell_int`` helpers, mirroring the DC engine) at the
single seam where the model touches a cell. Everything downstream is plain
numerics; the comms output stays light (no provenance envelope).

This module imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. It also carries the subscriber mapping
(:func:`subscribers_served_at`): subscribers are PEOPLE (phone subscribers, the
CELLULAR direct-to-cell unit, NOT households). The fleet is CAPACITY-SIZED to serve
the subscriber TARGET (the input base), and the served count RAMPS with the buildout
(``subscriber_target x min(1.0, living_fleet / fleet_target)``), reaching the target
at full deployment. This is a sized-base mapping, NOT the old spectrum -> capacity ->
demand chain (cut) and NOT the coverage-fraction-times-base mapping it replaced (the
served base is now the input, and the fleet is what is built toward). The engine
reports the served-people count at the FINAL year's buildout
(``CommsTrajectory.subscribers_served``) plus the annual cost per subscriber against
the target (``cost_per_subscriber_annual_usd``); the output layer (Phase 5) and the
ground ratio (Phase 4) consume the per-subscriber figure.

THE OVERSHOOT RULE (frozen here and in the parity test). Launches are granular
(a whole launch deploys ``satellites_per_launch`` satellites at once), so the
last build-out launch may push the living count slightly OVER the target. The
rule, applied uniformly in BOTH the build-out and HOLD phases: the satellites to
add this year are the deficit to the target (``target - living_before``) rounded
UP to a whole number of launches (``_ceil_to_launch``), capped by the comms
cadence share for the year (``would_be_deployed``). This lets the final build
cohort overshoot the target by strictly less than one launch's worth and never
deploys beyond what is needed to hold. During HOLD the deficit equals exactly
that year's cliff losses, so the same formula replaces only the ageing cohorts.

THE REVENUE + GROSS-MARGIN OVERLAY (mirrors the data-center revenue/margin pattern,
adapted to the comms model's lighter single-value style; no R-band, no provenance
envelope). On top of the cost treadmill the engine layers, per cohort and per year,
TWO REVENUE CASES against one ANNUALIZED cost basis. The cost basis is the
per-satellite LIFETIME cost (the flat build cost plus the satellite's share of its
deployment-year launch cost) spread over the satellite life, summed over the living
cohorts (matching the DC ``cost_annual = node_total / service_life`` convention). It
is a different convention from the cash replacement line (which the cost-per-
subscriber headline reads); the two converge only in clean rotational steady state.
Case 1 (COST-PLUS): revenue = annual cost x ``revenue_multiple`` (cost-coupled, the
DC central R = 1.5 mirror). Case 2 (PRICES-TODAY / ARPU): revenue = served
subscribers x
``arpu_usd_per_month`` x 12. Gross margin in both is ``(revenue - cost) / revenue``,
a percent. The overlay rides a parallel ``_CohortBuild`` list (the per-satellite
annual cost the bare ``LivedCohort`` does not carry), reusing the shared cohort
cliff; each living cohort's per-year line is a :class:`CommsCohortYear`, and the
fleet roll-up plus the steady-state (final-year) headlines sit on
:class:`CommsYear` / :class:`CommsTrajectory`. The revenue is a cost-coupled multiple
or a price-times-served-base figure, NEVER a demand or market-size estimate.

Units: money in $M; counts are integers; margins in percent; time in fiscal years
(FY2026..FY2036, year 0 = ``base_year``).
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from common.cadence import (
    ROUND_TO_NEAREST_OFFSET,
    compute_launch_cost_musd,
    compute_launches_per_year,
)
from common.cohort import LivedCohort, cohort_is_alive_at, living_cohorts
from common.provenance import ProvenanceCell
from communications.config import CommsConfig, IridiumArpuDials, IridiumDials
from communications.constants import (
    APERTURE_FOLD_CAVEAT_NOTE,
    APERTURE_NO_FOLD_LIMIT_M2,
    APERTURE_REFERENCE_M2,
    ARPU_MIX_TOTAL_PCT,
    ECOSYSTEM_ASSUMPTION_NOTE,
    GBPS_TO_MBPS,
    IRIDIUM_OPERATIONS_COST_MUSD,
    MONTHS_PER_YEAR,
    PHONE_CLASS_SE_CENTRAL,
    PHONE_CLASS_SE_HIGH,
    PHONE_CLASS_SE_LOW,
    REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE,
    SMALL_TERMINAL_CLASS_SE_CENTRAL,
    SMALL_TERMINAL_CLASS_SE_HIGH,
    SMALL_TERMINAL_CLASS_SE_LOW,
    TERMINAL_CLASS_SE_CENTRAL,
    TERMINAL_CLASS_SE_HIGH,
    TERMINAL_CLASS_SE_LOW,
    BindingRegime,
    DeviceClass,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fixed model constants (named, never bare literals; see CLAUDE.md).
# ---------------------------------------------------------------------------

FULL_COVERAGE_FRACTION: float = 1.0
"""The coverage fraction at the coverage FLOOR: the living fleet is clamped to this
so the coverage metric (``living_fleet / coverage_floor``) never reports above 1.0
once the fleet meets or exceeds the floor (with a large base the fleet runs well
above the floor, so coverage saturates at 1.0 while the build continues toward the
capacity-sized fleet target)."""

NO_COVERAGE_FRACTION: float = 0.0
"""The lower clamp on the coverage fraction: a negative coverage fraction is
meaningless (the engine never produces one), so it floors at zero."""

FULL_BUILDOUT_FRACTION: float = 1.0
"""The buildout fraction at full deployment: the living fleet is clamped to this so
the served-subscribers mapping (``buildout_fraction x subscriber_target``) never
scales beyond the target when the build overshoots the fleet target by less than one
launch's worth."""

NO_BUILDOUT_FRACTION: float = 0.0
"""The lower clamp on the buildout fraction fed to the served-subscribers mapping: a
negative buildout fraction is meaningless (the engine never produces one), so it
floors at zero before scaling the subscriber target."""

NO_REPLACEMENT_COST_MUSD: float = 0.0
"""The HOLD-phase replacement-cost line value during the BUILD-OUT phase: there is
no steady-state replacement line until the target is first reached, so build-out
years carry 0.0 on the replacement line (their cost is the build-out cost, not a
replacement cost)."""

MUSD_TO_USD: float = 1_000_000.0
"""Conversion from the model's internal money unit ($M) to whole USD. The
cost-per-subscriber figure is reported in USD per subscriber per year (the unit the
ground interface, Phase 4, is on), so the steady-state annual replacement cost (in
$M) is multiplied by this before dividing by the subscriber target."""

ZERO_SUBSCRIBER_TARGET_COST_USD: float = 0.0
"""The cost-per-subscriber value when the subscriber target is zero (it cannot be,
the dial is ``ge=1``, but the division is guarded for total safety) or the build-out
never reached steady state within the horizon (steady-state annual cost is 0.0, so
the per-subscriber figure is 0.0, a truthful below-steady-state output)."""

MARGIN_PERCENT_SCALE: float = 100.0
"""The percent scale for a gross margin: ``(revenue - cost) / revenue`` times this
yields a percentage (e.g. 0.333 -> 33.3), mirroring the data-center fleet-margin
convention so the two models report margin in the same unit."""

ZERO_MARGIN_PCT: float = 0.0
"""The gross-margin percent when revenue is zero (an empty fleet, or a build-out
year before any satellite is on orbit): the margin is undefined, so it reports 0.0
rather than dividing by zero, mirroring the data-center fleet-margin guard."""

NO_REVENUE_MUSD: float = 0.0
"""The revenue line ($M) for a year with no living fleet (no satellites on orbit yet,
so no cost basis and no served subscribers): both revenue cases report 0.0."""

NO_ANNUAL_COST_MUSD: float = 0.0
"""The annualized fleet-cost basis ($M) for a year with no living fleet: the margin
cost basis (the per-satellite lifetime cost spread over the life, summed over the
living fleet) is 0.0 when nothing is on orbit."""


# ---------------------------------------------------------------------------
# ProvenanceCell unwrap seam (mirrors the DC engine's _cell_float / _cell_int).
# This is the ONLY place the comms model touches a ProvenanceCell; everything
# downstream is plain floats/ints.
# ---------------------------------------------------------------------------


def _cell_float(c: ProvenanceCell) -> float:
    """Unwrap a numeric :class:`ProvenanceCell` to a plain ``float``.

    Args:
        c: A ProvenanceCell whose ``value`` is numeric.

    Returns:
        The cell's value as a ``float``.

    Raises:
        TypeError: If the cell's value is a bool or not a real number.
    """
    if isinstance(c.value, bool) or not isinstance(c.value, (int, float)):
        raise TypeError(f"ProvenanceCell {c.formula_name!r} is not numeric: {c.value!r}")
    return float(c.value)


def _cell_int(c: ProvenanceCell) -> int:
    """Unwrap an integer :class:`ProvenanceCell` to a plain ``int``.

    Args:
        c: A ProvenanceCell whose ``value`` is an integer.

    Returns:
        The cell's value as an ``int``.

    Raises:
        TypeError: If the cell's value is a bool or not an int.
    """
    if isinstance(c.value, bool) or not isinstance(c.value, int):
        raise TypeError(f"ProvenanceCell {c.formula_name!r} is not an int: {c.value!r}")
    return c.value


# ---------------------------------------------------------------------------
# Integer launch-count helpers (reuse the shared half-up offset; do not redefine).
# ---------------------------------------------------------------------------


def _round_half_up(x: float) -> int:
    """Round a non-negative rate to an integer launch count, half up.

    Mirrors ``common.cadence._integer_launch_count`` using the shared
    ``ROUND_TO_NEAREST_OFFSET`` authority (imported from ``common.cadence``, not
    redefined): ``floor(x + 0.5)``. Used to turn the comms slice's fractional
    ``fleet_launches * share_of_fleet`` into a whole launch count, and reused
    for the subscriber-density and ARPU bucket counts.

    Args:
        x: A non-negative rate (the comms slice of the fleet launch count).

    Returns:
        The nearest whole-number launch count, rounded half up.
    """
    return math.floor(x + ROUND_TO_NEAREST_OFFSET)


def _ceil_to_launch(satellites_needed: int, satellites_per_launch: int) -> int:
    """Round a satellite deficit UP to a whole number of launches' worth.

    The build is granular: satellites are added a whole launch at a time. This
    rounds the satellite deficit to the target up to the next multiple of
    ``satellites_per_launch`` (the overshoot rule), so the final build launch may
    push the living count over the target by strictly less than one launch's
    worth.

    Args:
        satellites_needed: Satellites still needed to reach the target this year
            (already floored at 0 by the caller).
        satellites_per_launch: Satellites deployed per launch (a positive count).

    Returns:
        ``satellites_needed`` rounded up to the next multiple of
        ``satellites_per_launch`` (``0`` when nothing is needed).
    """
    if satellites_needed <= 0:
        return 0
    launches = math.ceil(satellites_needed / satellites_per_launch)
    return launches * satellites_per_launch


# ---------------------------------------------------------------------------
# The capacity-sizing of the fleet (the NEW capacity dimension).
#
# The fleet is sized to SERVE the subscriber base, not merely to cover it. The
# capacity NEED is the subscriber target divided by the per-satellite attached
# density (rounded UP, since a partial satellite's worth of need still requires a
# whole satellite of capacity). The fleet target floors that at the coverage floor
# (everyone must see a satellite) and caps it at the saturation cap (past which the
# spread servable base is exhausted). Which term binds is reported as the
# BindingRegime (the founder's coverage-vs-capacity question).
# ---------------------------------------------------------------------------


def compute_fleet_target(
    *,
    subscriber_target: int,
    subscribers_per_satellite: int,
    coverage_floor: int,
    max_fleet_satellites: int,
) -> tuple[int, BindingRegime]:
    """Size the fleet to serve the subscriber base, and report which constraint binds.

    The capacity need is ``ceil(subscriber_target / subscribers_per_satellite)``: the
    satellites required to carry the attached base at the per-satellite density. The
    fleet target floors that at ``coverage_floor`` and caps it at
    ``max_fleet_satellites``::

        fleet_target = min(max_fleet_satellites,
                           max(coverage_floor, capacity_need))

    Worked at the defaults (75,000 attached/sat, 340 floor, 2,000 cap):
    10M -> ceil(134) -> max(340, 134) = 340 (the coverage floor binds);
    50M -> 667 -> 667 (capacity binds); 100M -> 1,334 -> 1,334 (capacity binds,
    under the 2,000 cap).

    Args:
        subscriber_target: The subscriber base to serve (the input), people.
        subscribers_per_satellite: The attached subscribers one satellite carries.
        coverage_floor: The minimum fleet for everyone to see a satellite (the lower
            bound on the target).
        max_fleet_satellites: The saturation cap (the upper bound on the target).

    Returns:
        A 2-tuple ``(fleet_target, binding_regime)``: the capacity-sized fleet the
        build-out fills toward, and which constraint set it (the coverage floor, the
        capacity need, or the saturation cap).
    """
    capacity_need = math.ceil(subscriber_target / subscribers_per_satellite)
    floored = max(coverage_floor, capacity_need)
    fleet_target = min(max_fleet_satellites, floored)
    if capacity_need >= max_fleet_satellites:
        binding_regime = BindingRegime.SATURATED
    elif capacity_need <= coverage_floor:
        binding_regime = BindingRegime.COVERAGE
    else:
        binding_regime = BindingRegime.CAPACITY
    return fleet_target, binding_regime


# ---------------------------------------------------------------------------
# The Iridium model (formerly Model B; L-band max-outcome): the pure L-band
# derivation spine.
#
# The Iridium model DERIVES the per-satellite subscriber density from L-band
# physics (held spectrum, device spectral efficiency, satellite aperture area,
# per-user active rate, busy-hour concurrency) instead of reading the fixed
# subscribers_per_satellite dial of the High-Bandwidth Cellular Pure Play model
# (formerly Model A), then feeds the SAME compute_fleet_target above. These are
# pure derivations (primitives or the dials in, primitives out, no side effects);
# run_comms_model wires them in behind the config.iridium branch. THE THREE LANES
# stay separate: the Iridium model is the MSS lane (purpose-built or in-chipset
# devices on owned L-band), NOT cellular direct-to-cell to an unmodified phone
# (the High-Bandwidth Cellular Pure Play model) and NOT broadband.
# ---------------------------------------------------------------------------


def resolve_device_spectral_efficiency(dials: IridiumDials) -> float:
    """Resolve the Iridium-model spectral efficiency (bps/Hz) from the dials (0.7 step 1).

    Returns the explicit ``spectral_efficiency_bps_per_hz`` override when set,
    otherwise the central spectral-efficiency tier for the ``device_class`` (the
    founder's three device categories, a three-row mapping): ``PHONE_CLASS`` to
    :data:`PHONE_CLASS_SE_CENTRAL` (0.65), ``SMALL_TERMINAL_CLASS`` to
    :data:`SMALL_TERMINAL_CLASS_SE_CENTRAL` (2.0), ``TERMINAL_CLASS`` to
    :data:`TERMINAL_CLASS_SE_CENTRAL` (2.5).

    Args:
        dials: The Iridium-model :class:`~communications.config.IridiumDials` block
            (the device class plus the optional override).

    Returns:
        The spectral efficiency in bps/Hz to use in the capacity derivation.
    """
    if dials.spectral_efficiency_bps_per_hz is not None:
        return dials.spectral_efficiency_bps_per_hz
    class_central: dict[DeviceClass, float] = {
        DeviceClass.PHONE_CLASS: PHONE_CLASS_SE_CENTRAL,
        DeviceClass.SMALL_TERMINAL_CLASS: SMALL_TERMINAL_CLASS_SE_CENTRAL,
        DeviceClass.TERMINAL_CLASS: TERMINAL_CLASS_SE_CENTRAL,
    }
    return class_central[dials.device_class]


def derive_per_satellite_capacity_gbps(
    spectrum_mhz: float, spectral_efficiency_bps_per_hz: float, aperture_m2: float
) -> float:
    """Derive the per-satellite capacity in Gbps (0.7 step 2).

    ::

        per_sat_capacity_gbps = spectrum_mhz x spectral_efficiency_bps_per_hz
                                x REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE
                                x (aperture_m2 / APERTURE_REFERENCE_M2)

    The reuse calibration (:data:`REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE`) folds the
    effective ~150x beam-count-times-frequency-reuse multiplier of a modern
    digital-beamforming satellite together with the Mbps-to-Gbps scaling, calibrated
    AT the :data:`APERTURE_REFERENCE_M2` (25 m^2) reference aperture, so the aperture
    factor is 1.0 at the default and every baseline number is unchanged. The aperture
    factor is linear in area (a bigger array forms proportionally more simultaneous
    beams, the reuse term) and is CONSERVATIVE: it ignores the additional per-link
    SNR lift a larger aperture also gives. Worked at the phone-class default aperture:
    8 x 0.65 x 0.15 x (25 / 25) = 0.78 Gbps.

    Args:
        spectrum_mhz: The held L-band width, MHz.
        spectral_efficiency_bps_per_hz: The device spectral efficiency, bps/Hz.
        aperture_m2: The satellite flat-array area, m^2 (the aperture factor divides
            by :data:`APERTURE_REFERENCE_M2`).

    Returns:
        The per-satellite capacity, Gbps.
    """
    aperture_factor = aperture_m2 / APERTURE_REFERENCE_M2
    return (
        spectrum_mhz
        * spectral_efficiency_bps_per_hz
        * REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE
        * aperture_factor
    )


def derive_iridium_satellites_per_launch(
    *, configured_satellites_per_launch: int, aperture_m2: float
) -> int:
    """Derive the aperture-coupled effective satellites-per-launch (0.7 step 10).

    ::

        effective = max(1, floor(configured x APERTURE_REFERENCE_M2 / aperture_m2))

    Multiply BEFORE dividing (keeps the ratio exact at clean apertures: 12 x 25 / 60
    = 5.0 exactly in floats). The ``floor`` is deliberate, the opposite convention
    from the density's round-half-up: a partial satellite cannot fly, so per-launch
    capacity is never overstated. The ``max(1, ...)`` floor means an arbitrarily
    large aperture still flies one satellite per launch (the AST pattern: a 223 m^2
    array flies 1 per launch). Equals the configured value EXACTLY at the 25 m^2
    default aperture (the launch-coupling identity, so the High-Bandwidth Cellular
    Pure Play model's behavior is unchanged).
    Mass rationale for the inverse-linear coupling: ~800 kg at the 25 m^2 reference
    (COMM-256) scales roughly linearly with area, ~1,900 kg at 60 m^2, so ~5 per
    launch by mass, agreeing with the stow-derived count.

    Args:
        configured_satellites_per_launch: The High-Bandwidth Cellular Pure Play
            model's satellites-per-launch dial (the count at the reference aperture).
        aperture_m2: The satellite flat-array area, m^2.

    Returns:
        The effective whole satellites per launch (at least 1).
    """
    return max(
        1,
        math.floor(configured_satellites_per_launch * APERTURE_REFERENCE_M2 / aperture_m2),
    )


def derive_iridium_subscribers_per_satellite(
    *,
    per_satellite_capacity_gbps: float,
    active_user_rate_mbps: float,
    concurrency_peak: float,
) -> int:
    """Derive the per-satellite subscriber density (people) fed to the fleet sizing (0.7 step 3).

    ::

        offered_load_per_subscriber_mbps = active_user_rate_mbps x concurrency_peak
        subscribers_per_satellite = round_half_up(
            per_satellite_capacity_gbps x GBPS_TO_MBPS / offered_load_per_subscriber_mbps)

    Uses the engine's :func:`_round_half_up` (NOT ``floor`` or ``int()``): it matches
    the engine's rounding idiom AND is robust to floating-point representation error
    at the exact-integer boundary (e.g. 31200.0000001 rounds to 31200). This is the
    OPPOSITE rounding convention from the launch coupling's ``floor``, and both are
    deliberate. Worked at the phone-class baseline: 0.78 x 1000 / (1.0 x 0.025) =
    780 / 0.025 = 31,200.

    Args:
        per_satellite_capacity_gbps: The derived per-satellite capacity, Gbps.
        active_user_rate_mbps: The per-subscriber active data rate, Mbps.
        concurrency_peak: The busy-hour peak concurrency fraction.

    Returns:
        The derived subscribers-per-satellite density (people, a whole count).
    """
    offered_load_per_subscriber_mbps = active_user_rate_mbps * concurrency_peak
    return _round_half_up(
        per_satellite_capacity_gbps * GBPS_TO_MBPS / offered_load_per_subscriber_mbps
    )


def derive_iridium_per_user_rates(
    *,
    spectrum_mhz: float,
    spectral_efficiency_bps_per_hz: float,
    active_user_rate_mbps: float,
    concurrency_peak: float,
    concurrency_offpeak: float,
) -> tuple[float, float]:
    """Derive the Iridium-model (peak, off-peak) per-user rates in Mbps (0.7 step 5).

    The peak per-user rate is the active rate by construction (the service tier). The
    off-peak rate is the smaller of the single-beam Shannon pool and the rate a
    subscriber gets when the concurrency drops from peak to off-peak::

        beam_pool_mbps = spectrum_mhz x spectral_efficiency_bps_per_hz   (MHz x bps/Hz = Mbps)
        per_user_rate_offpeak_mbps = min(
            beam_pool_mbps,
            active_user_rate_mbps x concurrency_peak / concurrency_offpeak)

    Worked at the phone-class baseline: peak = 1.0 Mbps; beam_pool = 8 x 0.65 = 5.2
    Mbps; off-peak = min(5.2, 1.0 x 0.025 / 0.005) = min(5.2, 5.0) = 5.0 Mbps.

    Args:
        spectrum_mhz: The held L-band width, MHz.
        spectral_efficiency_bps_per_hz: The device spectral efficiency, bps/Hz.
        active_user_rate_mbps: The per-subscriber active rate, Mbps (the peak rate).
        concurrency_peak: The busy-hour peak concurrency fraction.
        concurrency_offpeak: The off-peak concurrency fraction.

    Returns:
        A 2-tuple ``(per_user_rate_peak_mbps, per_user_rate_offpeak_mbps)``, Mbps.
    """
    beam_pool_mbps = spectrum_mhz * spectral_efficiency_bps_per_hz
    per_user_rate_peak_mbps = active_user_rate_mbps
    per_user_rate_offpeak_mbps = min(
        beam_pool_mbps, active_user_rate_mbps * concurrency_peak / concurrency_offpeak
    )
    return per_user_rate_peak_mbps, per_user_rate_offpeak_mbps


# ---------------------------------------------------------------------------
# The buildout-to-subscribers mapping (the NEW capacity-sized logic).
#
# Subscribers are PEOPLE (phone subscribers, the CELLULAR direct-to-cell unit),
# NOT households (a household is the broadband unit). The served count RAMPS with
# the buildout: the subscriber TARGET is the base, and the fraction served is the
# fraction of the capacity-sized FLEET TARGET on orbit. At full deployment it
# equals the target. This is a sized-base map (target x living/fleet_target), NOT
# the old spectrum -> capacity -> demand chain (cut) and NOT the prior
# coverage-fraction-times-base map (the served base is now the input, and the fleet
# is what is built toward). There is no beam, spectral-efficiency, or capacity term.
# ---------------------------------------------------------------------------


def subscribers_served_at(
    buildout_fraction: float,
    *,
    subscriber_target: int,
    override: int | None,
) -> int:
    """Map a fleet-buildout fraction to the served-PERSON count (the cellular subscribers).

    The mapping is linear in the buildout fraction: at full deployment
    (``buildout_fraction == 1.0``) the fully-built constellation serves the whole
    subscriber target; at partial deployment it serves proportionally fewer people.
    The base is the optional direct override when supplied, otherwise the subscriber
    ``subscriber_target`` dial.

    Subscribers are PEOPLE (phone subscribers), not households, because the product
    is CELLULAR direct-to-cell. The figure is a sized served-base count (the target
    scaled by how much of the capacity-sized fleet is on orbit), NOT a demand or
    market estimate, and it carries no capacity/spectrum/beam term.

    Args:
        buildout_fraction: The fraction of the capacity-sized fleet target currently
            on orbit (``living_fleet / fleet_target``, the engine's per-year
            ``CommsYear.buildout_fraction``). Clamped to ``[0.0, 1.0]`` before
            scaling, so an out-of-range value (the engine never produces one) cannot
            push the served count below zero or above the base.
        subscriber_target: The served-PERSON count at full deployment (the configured
            subscriber target). Used when ``override`` is ``None``.
        override: The OPTIONAL direct served-base scalar. When not ``None`` it
            replaces ``subscriber_target`` as the full-deployment base (the model
            serves this absolute count at full deployment; below it the count still
            scales by the buildout fraction).

    Returns:
        The served-PERSON count at the given buildout fraction, rounded half up to a
        whole person (``round_half_up(clamped_buildout_fraction * base)``).
    """
    base = override if override is not None else subscriber_target
    clamped = min(FULL_BUILDOUT_FRACTION, max(NO_BUILDOUT_FRACTION, buildout_fraction))
    return _round_half_up(clamped * base)


def _cost_per_subscriber_annual_usd(
    steady_state_annual_cost_musd: float, subscriber_target: int
) -> float:
    """Divide the steady-state annual cost ($M) by the subscriber target into USD/sub/yr.

    The cost per subscriber is the steady-state annual replacement cost (converted
    from $M to whole USD via :data:`MUSD_TO_USD`) over the subscriber TARGET (the
    full-deployment base, per the spec, not the partial served count). A zero target
    (impossible under the ``ge=1`` dial bound, but guarded) or a zero steady-state
    cost (the build never reached steady state within the horizon) yields
    :data:`ZERO_SUBSCRIBER_TARGET_COST_USD`.

    Args:
        steady_state_annual_cost_musd: The representative HOLD-phase annual cost, $M.
        subscriber_target: The subscriber target (the full-deployment served base).

    Returns:
        The annual cost per subscriber, USD per subscriber per year.
    """
    if subscriber_target <= 0:
        return ZERO_SUBSCRIBER_TARGET_COST_USD
    return steady_state_annual_cost_musd * MUSD_TO_USD / subscriber_target


# ---------------------------------------------------------------------------
# The revenue + gross-margin overlay (the two revenue cases; mirrors the DC
# revenue/margin pattern, adapted to the comms model's lighter single-value style).
#
# The COST BASIS for margin is the ANNUALIZED per-satellite cost (the satellite's
# lifetime cost: its flat build cost plus its share of its deployment-year launch
# cost, spread over the satellite life), matching the DC annualized convention
# (cost_annual = node_total / service_life). Each living satellite carries this
# annual cost every year of its life, so the per-year annualized fleet cost is the
# sum over living cohorts. NOTE this is a different convention from the cash
# replacement line (``replacement_cost_this_year_musd``, which the cost-per-subscriber
# headline reads): the two CONVERGE only in clean rotational steady state (equal-sized
# cohorts, a full lifecycle elapsed), where replacing ~1/life of the fleet per year
# costs ~lifetime_cost/life per satellite. In the build-just-completed final horizon
# year they differ (the build ramped, so the cohorts are unequal and one year's cliff
# replacement is not 1/life of the fleet). The annualized basis is the stable
# economic cost the margins read. Two revenue cases ride this basis:
#
#   COST-PLUS: revenue = annual cost x revenue_multiple (cost-coupled).
#   ARPU:      revenue = served subscribers x monthly ARPU x 12 (price x served base).
#
# Gross margin in BOTH cases is (revenue - cost) / revenue, reported as a percent.
# ---------------------------------------------------------------------------


def _per_satellite_annual_cost_musd(
    *,
    satellite_build_cost_musd: float,
    launch_cost_per_launch_musd: float,
    satellites_per_launch: int,
    satellite_lifetime_years: int,
) -> float:
    """Annualize one satellite's lifetime cost (build + its launch share) over its life.

    A satellite's lifetime cost is its flat hardware build cost plus its share of the
    launch that carried it (the per-launch cost divided by the satellites per launch).
    Spreading that over the satellite life gives the per-satellite ANNUAL cost, the
    margin cost basis, matching the DC annualized convention
    (``cost_annual = node_total / service_life``). The launch cost is the
    deployment-year per-launch cost (priced at the whole-fleet cadence), so a cohort
    launched in a cheaper-cadence year carries a lower annual cost for its whole life
    (the cost-down is locked in at launch, mirroring the DC per-cohort cost).

    Args:
        satellite_build_cost_musd: The flat per-satellite hardware build cost, $M.
        launch_cost_per_launch_musd: The deployment-year per-launch cost, $M.
        satellites_per_launch: Satellites carried per launch (a positive count).
        satellite_lifetime_years: The satellite life over which to annualize (the
            cohort cliff, a positive count).

    Returns:
        The per-satellite annual cost, $M/yr (``0.0`` if the life is not positive,
        guarded though the dial is ``ge=1``).
    """
    if satellite_lifetime_years <= 0:
        return NO_ANNUAL_COST_MUSD
    launch_cost_per_satellite_musd = launch_cost_per_launch_musd / satellites_per_launch
    lifetime_cost_per_satellite_musd = satellite_build_cost_musd + launch_cost_per_satellite_musd
    return lifetime_cost_per_satellite_musd / satellite_lifetime_years


def _gross_margin_pct(revenue_musd: float, cost_musd: float) -> float:
    """Gross margin as a percent: ``(revenue - cost) / revenue x 100``.

    Mirrors the DC fleet-margin formula, including its zero-revenue guard (a year
    with no living fleet, hence no revenue, reports :data:`ZERO_MARGIN_PCT` rather
    than dividing by zero).

    Args:
        revenue_musd: The annual revenue, $M.
        cost_musd: The annual cost (the annualized cost basis), $M.

    Returns:
        The gross margin in percent, or :data:`ZERO_MARGIN_PCT` when revenue is not
        positive.
    """
    if revenue_musd <= 0.0:
        return ZERO_MARGIN_PCT
    return (revenue_musd - cost_musd) / revenue_musd * MARGIN_PERCENT_SCALE


# ---------------------------------------------------------------------------
# Per-year and whole-trajectory data structures (frozen, plain numerics).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _CohortBuild:
    """One deployed cohort's facts for the economics overlay (engine-internal).

    Tracks, per cohort (one per launch year), the satellites deployed and the
    per-satellite ANNUAL cost locked in at launch (built from the deployment-year
    launch cost, so the cadence cost-down is fixed for the cohort's life, mirroring
    the DC per-cohort cost). The cohort-cliff survival reuses the shared
    ``common.cohort.cohort_is_alive_at`` (no separate cliff machinery). This rides
    alongside the shared ``LivedCohort`` list (which drives the build/cost treadmill,
    unchanged); the parallel record adds only the per-satellite annual cost the
    treadmill does not carry.

    Attributes:
        launch_year: The fiscal year this cohort deployed (a unique key: at most one
            cohort per model year, and only deploying years are recorded).
        satellites: The satellites in this cohort (always strictly positive: empty
            years are not recorded).
        per_satellite_annual_cost_musd: The per-satellite annual cost ($M/yr) locked
            in at launch (:func:`_per_satellite_annual_cost_musd`).
    """

    launch_year: int
    satellites: int
    per_satellite_annual_cost_musd: float


@dataclass(frozen=True)
class CommsCohortYear:
    """One living cohort's per-year economics line (both revenue cases).

    The cohort-level mirror of the DC per-cohort economics: each living cohort, in
    each year of its life, carries its annualized cost, its two-case revenue, and its
    two-case gross margin. The cost-plus case is cost-coupled (revenue = cohort annual
    cost x the multiple), so the cost-plus margin is the same flat figure for every
    cohort. The ARPU case allocates the year's served subscribers to the cohort by its
    share of the living fleet (a cohort with more living satellites serves
    proportionally more of the base), so the ARPU revenue and margin vary with the
    cohort's living-satellite share and the year's served base.

    Attributes:
        launch_year: The cohort's deployment year (its identity across the years).
        living_satellites: This cohort's satellites alive this year (under the cliff).
        annual_cost_musd: This cohort's annualized cost this year
            (``living_satellites x per_satellite_annual_cost_musd``), $M/yr.
        cost_plus_revenue_musd: The cost-plus revenue (``annual_cost x multiple``),
            $M/yr.
        cost_plus_gross_margin_pct: The cost-plus gross margin, percent (flat across
            cohorts: ``(multiple - 1) / multiple x 100``).
        arpu_subscribers_served: The served subscribers allocated to this cohort this
            year (the year's served base x this cohort's share of the living fleet).
        arpu_revenue_musd: The ARPU revenue (``arpu_subscribers_served x monthly ARPU
            x 12``), $M/yr.
        arpu_gross_margin_pct: The ARPU gross margin, percent.
    """

    launch_year: int
    living_satellites: int
    annual_cost_musd: float
    cost_plus_revenue_musd: float
    cost_plus_gross_margin_pct: float
    arpu_subscribers_served: int
    arpu_revenue_musd: float
    arpu_gross_margin_pct: float


@dataclass(frozen=True)
class CommsYear:
    """One fiscal year's cost-and-counts rollup (plain numerics, no cells).

    Attributes:
        year: The fiscal year (e.g. 2036).
        fleet_launches_this_year: The whole-fleet integer cadence this year (the
            shared logistic ramp output). The launch cost is priced at this.
        comms_launches_flown_this_year: The comms launches actually flown this
            year, after the cadence share and the build-and-hold cap.
        satellites_deployed_this_year: Satellites added this year
            (= ``comms_launches_flown_this_year * satellites_per_launch``).
        living_fleet: Living satellites at this year under the 5-year cliff,
            counted AFTER this year's cohort is added.
        coverage_fraction: ``living_fleet / coverage_floor``, clamped to 1.0. The
            coverage metric (can everyone see a satellite). With a large subscriber
            base the fleet target exceeds the coverage floor, so this saturates at
            1.0 while the build continues toward the capacity-sized fleet target.
        buildout_fraction: ``living_fleet / fleet_target``, clamped to 1.0. The
            fraction of the capacity-sized fleet on orbit; it drives the served
            subscriber count (the subscriber target scaled by this).
        launch_cost_per_launch_musd: Per-launch cost at the whole-fleet cadence
            this year, $M.
        build_cost_this_year_musd: Satellite hardware build cost this year, $M
            (= ``satellites_deployed_this_year * satellite_build_cost_musd``).
        launch_cost_this_year_musd: Launch cost this year, $M
            (= ``comms_launches_flown_this_year * launch_cost_per_launch_musd``).
        total_cost_this_year_musd: ``build_cost_this_year_musd +
            launch_cost_this_year_musd``.
        is_hold_phase: ``True`` once the build-out target was first reached (this
            year and every year thereafter).
        replacement_cost_this_year_musd: The HOLD-phase ongoing replacement line,
            $M; ``0.0`` during build-out, the year's total cost once in HOLD.
        subscribers_served_this_year: The served-PERSON count at THIS year's buildout
            fraction (the subscriber target scaled by ``buildout_fraction``, or the
            override). Drives the ARPU revenue case per year (the final year's value
            is the trajectory headline ``subscribers_served``).
        annual_cost_this_year_musd: The ANNUALIZED fleet cost this year (the margin
            cost basis), $M/yr: the sum over living cohorts of each cohort's
            per-satellite annual cost (lifetime cost spread over the life). This is
            NOT the deployment cash cost (``total_cost_this_year_musd``) and NOT the
            cash replacement line; it is the steady annual cost each living satellite
            carries, matching the DC annualized convention. It converges with the
            replacement line only in clean rotational steady state (equal cohorts, a
            full lifecycle elapsed); in the build-just-completed final year it runs
            higher (the ramped cohorts are unequal, so one year's cliff replacement is
            below 1/life of the fleet).
        cost_plus_revenue_this_year_musd: The COST-PLUS revenue this year, $M
            (``annual_cost_this_year_musd x revenue_multiple``).
        cost_plus_gross_margin_pct: The COST-PLUS gross margin this year, percent
            (``(revenue - cost) / revenue x 100``; flat at the multiple's implied
            margin once any fleet is on orbit).
        arpu_revenue_this_year_musd: The PRICES-TODAY ARPU revenue this year, $M
            (``subscribers_served_this_year x arpu_usd_per_month x 12 / 1e6``).
        arpu_gross_margin_pct: The ARPU gross margin this year, percent
            (``(revenue - cost) / revenue x 100`` against the annualized cost basis).
        cohort_lines: The per-living-cohort economics breakdown this year (one
            :class:`CommsCohortYear` per cohort alive under the cliff), the
            cohort-level mirror of the DC per-cohort revenue/margin. Empty in a year
            with no living fleet.
    """

    year: int
    fleet_launches_this_year: int
    comms_launches_flown_this_year: int
    satellites_deployed_this_year: int
    living_fleet: int
    coverage_fraction: float
    buildout_fraction: float
    launch_cost_per_launch_musd: float
    build_cost_this_year_musd: float
    launch_cost_this_year_musd: float
    total_cost_this_year_musd: float
    is_hold_phase: bool
    replacement_cost_this_year_musd: float
    subscribers_served_this_year: int
    annual_cost_this_year_musd: float
    cost_plus_revenue_this_year_musd: float
    cost_plus_gross_margin_pct: float
    arpu_revenue_this_year_musd: float
    arpu_gross_margin_pct: float
    cohort_lines: tuple[CommsCohortYear, ...]


@dataclass(frozen=True)
class CommsTrajectory:
    """The whole build-and-hold run: the per-year rollups plus the headlines.

    Attributes:
        years: The per-year rollups, one per model year (FY2026..FY2036).
        total_build_and_hold_cost_musd: The cumulative cost over the trajectory
            (the sum of every year's ``total_cost_this_year_musd``), $M.
        fleet_target: The capacity-sized fleet the build-out fills toward
            (:func:`compute_fleet_target`: the subscriber target divided by the
            per-satellite density, floored by the coverage floor, capped by the
            saturation cap). The treadmill builds and holds to THIS, not the floor.
        subscribers_per_satellite: The attached-subscribers-per-satellite density
            used to size the fleet (echoed from the config for transparency).
        binding_regime: Which constraint set the fleet target (the coverage floor,
            the capacity need, or the saturation cap), the founder's
            coverage-vs-capacity answer for this scenario.
        full_coverage_reached_year: The first fiscal year the living fleet hit the
            FLEET TARGET (full deployment), or ``None`` if it is never reached within
            the horizon (a truthful below-target output, not an error).
        steady_state_annual_replacement_cost_musd: The representative HOLD-phase
            annual replacement cost, $M. Defined as the final model year's
            ``replacement_cost_this_year_musd`` (the steady state once the build
            completes); ``0.0`` if the build never completes within the horizon.
        subscribers_served: The served-PERSON count (cellular phone subscribers) at
            the FINAL year's buildout fraction (FY2036), the buildout mapping
            (:func:`subscribers_served_at`) applied to the subscriber target (or the
            direct override). When the build-out completed, the final buildout
            fraction is ``1.0`` and this equals the target; when it did not, it is
            the proportional partial-deployment count.
        cost_per_subscriber_annual_usd: The steady-state annual cost per subscriber,
            USD/sub/yr: ``steady_state_annual_replacement_cost_musd`` (converted to
            USD) divided by the subscriber TARGET (the full-deployment base, per the
            spec, not the partial served count). ``0.0`` when the build never reached
            steady state within the horizon (the steady-state cost is ``0.0``). This
            is the space side of the ground comparison (Phase 4) and the headline
            cost-to-serve figure.
        steady_state_annual_cost_musd: The representative HOLD-phase ANNUALIZED fleet
            cost, $M/yr (the final model year's ``annual_cost_this_year_musd``), the
            cost basis the steady-state margins read. ``0.0`` if the build never
            completes within the horizon. This is the annualized basis (the DC
            convention); it is the like-for-like cost behind the two steady-state
            revenue headlines. It is generally HIGHER than
            ``steady_state_annual_replacement_cost_musd`` in the final horizon year
            (the cash replacement line is a single lumpy year of the ramped build);
            the two converge only in clean rotational steady state.
        steady_state_revenue_cost_plus_musd: The steady-state COST-PLUS annual
            revenue, $M/yr (the final year's ``cost_plus_revenue_this_year_musd``).
        steady_state_gross_margin_cost_plus_pct: The steady-state COST-PLUS gross
            margin, percent (the multiple's implied flat margin once built out).
        steady_state_revenue_arpu_musd: The steady-state PRICES-TODAY ARPU annual
            revenue, $M/yr (the final year's ``arpu_revenue_this_year_musd``).
        steady_state_gross_margin_arpu_pct: The steady-state ARPU gross margin,
            percent. Unlike the cost-plus margin, this depends on whether the ARPU
            revenue clears the annualized cost basis at the served base.
        iridium: The Iridium model's (L-band max-outcome) physics result block when
            the Iridium model ran (``config.iridium`` was non-None), else ``None``
            (the High-Bandwidth Cellular Pure Play path). It carries the derived
            per-satellite capacity, the fleet aggregate, the per-user peak/off-peak
            rates, the IoT passthrough, and the stated ecosystem assumption; it never
            perturbs the shared fields above.
    """

    years: tuple[CommsYear, ...]
    total_build_and_hold_cost_musd: float
    fleet_target: int
    subscribers_per_satellite: int
    binding_regime: BindingRegime
    full_coverage_reached_year: int | None
    steady_state_annual_replacement_cost_musd: float
    subscribers_served: int
    cost_per_subscriber_annual_usd: float
    steady_state_annual_cost_musd: float
    steady_state_revenue_cost_plus_musd: float
    steady_state_gross_margin_cost_plus_pct: float
    steady_state_revenue_arpu_musd: float
    steady_state_gross_margin_arpu_pct: float
    iridium: IridiumResult | None = None


@dataclass(frozen=True)
class IridiumArpuBucket:
    """One billable-connection ARPU revenue bucket (a mix slice of the pool).

    Attributes:
        mix_pct: The bucket's share of the billable-connection pool, percent (the
            founder-set dial; for the standard bucket the reported count is the
            people-identity residual, so the count is not exactly ``mix_pct`` of the
            pool, off only by the premium bucket's rounding).
        price_usd_month: The bucket's monthly price, USD per connection per month (the
            founder-set dial).
        count: The derived connection count in this bucket (people for standard and
            premium, DEVICES for IoT, contracts for government); an integer.
        revenue_musd_yr: The bucket's annual revenue, $M/yr
            (``count x price_usd_month x MONTHS_PER_YEAR / 1e6``).
    """

    mix_pct: float
    price_usd_month: float
    count: int
    revenue_musd_yr: float


@dataclass(frozen=True)
class IridiumArpuResult:
    """The four-bucket ARPU revenue case computed at the built fleet's people capacity.

    Attached to :attr:`IridiumResult.arpu` when the scenario carries a populated
    :class:`~communications.config.IridiumArpuDials` block; ``None`` otherwise. The
    four buckets partition ONE pool anchored to fleet CAPACITY
    (``fleet_target x subscribers_per_satellite``), so every count is linear in the
    satellite count. Subscribers are PEOPLE (standard, premium); IoT are DEVICES;
    government is a contract line: :attr:`total_connections` is a BILLABLE-CONNECTIONS
    accounting total, NOT one summed people population. The people identity
    (``standard.count + premium.count == people_capacity``) is exact by construction
    (standard is the residual). All revenues are estimate-tier.

    Attributes:
        standard: The STANDARD personal (phone-class) people bucket.
        premium: The PREMIUM terminal (gain-antenna) people bucket.
        iot: The IoT DEVICE bucket (the mix residual to 100).
        government: The GOVERNMENT contract bucket.
        total_connections: The billable-connection pool size, round-half-up of the
            float pool ``people_capacity / people_share`` (an accounting total across
            people, devices, and contracts, not a people count).
        arpu_revenue_total_musd_yr: The sum of the four bucket revenues, $M/yr.
    """

    standard: IridiumArpuBucket
    premium: IridiumArpuBucket
    iot: IridiumArpuBucket
    government: IridiumArpuBucket
    total_connections: int
    arpu_revenue_total_musd_yr: float


@dataclass(frozen=True)
class IridiumResult:
    """The Iridium model's (L-band max-outcome) physics result block.

    Attached to :attr:`CommsTrajectory.iridium` when the Iridium model ran
    (``config.iridium`` was non-None); ``None`` on the High-Bandwidth Cellular Pure
    Play path. All fields are estimate-tier derived quantities. Subscribers are
    PEOPLE; ``iot_devices`` is a separate DEVICE passthrough, never folded into the
    people count. This is the MSS lane (owned L-band, purpose-built or in-chipset
    devices), NEVER the cellular unmodified-phone lane (the High-Bandwidth Cellular
    Pure Play model). See :attr:`ecosystem_assumption`.

    Attributes:
        spectrum_mhz: The held L-band width used, MHz (echo of the dial).
        aperture_m2: The satellite flat-array area used, m^2 (echo of the dial).
        device_class: The device class that set the spectral-efficiency tier.
        spectral_efficiency_bps_per_hz: The resolved spectral efficiency used, bps/Hz
            (the override when set, else the ``device_class`` central).
        per_satellite_capacity_gbps: The derived per-satellite capacity, Gbps
            (0.7 step 2).
        fleet_aggregate_capacity_gbps: ``per_satellite_capacity_gbps x fleet_target``,
            the built-out fleet's aggregate capacity, Gbps (0.7 step 6).
        subscribers_per_satellite: The derived per-satellite density (people) that
            sized the fleet (echo of what fed :func:`compute_fleet_target`).
        effective_satellites_per_launch: The aperture-coupled per-launch count the
            deployment used (0.7 step 10; equals the configured value at the default
            aperture).
        active_user_rate_mbps: The per-subscriber active data rate, Mbps.
        concurrency_peak: The busy-hour peak concurrency fraction.
        concurrency_offpeak: The off-peak concurrency fraction.
        beam_pool_mbps: The single-beam Shannon pool, ``spectrum_mhz x SE``, Mbps.
        per_user_rate_peak_mbps: The peak per-user rate, Mbps (the active rate).
        per_user_rate_offpeak_mbps: The off-peak per-user rate, Mbps (0.7 step 5).
        iot_devices: The passthrough IoT DEVICE count (not people; zero sizing effect).
        operations_cost_musd: The Iridium model's operations cost, $M
            (:data:`IRIDIUM_OPERATIONS_COST_MUSD`, 0.0, an explicit stated assumption,
            a fixed line to research and add later).
        ecosystem_assumption: The stated ecosystem assumption behind the phone-class
            tier (:data:`ECOSYSTEM_ASSUMPTION_NOTE`): in-chipset L-band support, 0 dBi,
            a forward assumption; the Iridium model never claims to reach an
            unmodified handset.
        arpu: The four-bucket ARPU revenue case (:class:`IridiumArpuResult`) computed
            at the built fleet's people capacity, or ``None`` when the scenario carries
            no ``arpu`` block. When set, its IoT bucket count is the model's published
            IoT device count (the ``iot_devices`` passthrough above is superseded at the
            output/assumptions layer; one IoT truth per artifact).
    """

    spectrum_mhz: float
    aperture_m2: float
    device_class: DeviceClass
    spectral_efficiency_bps_per_hz: float
    per_satellite_capacity_gbps: float
    fleet_aggregate_capacity_gbps: float
    subscribers_per_satellite: int
    effective_satellites_per_launch: int
    active_user_rate_mbps: float
    concurrency_peak: float
    concurrency_offpeak: float
    beam_pool_mbps: float
    per_user_rate_peak_mbps: float
    per_user_rate_offpeak_mbps: float
    iot_devices: int
    operations_cost_musd: float
    ecosystem_assumption: str
    arpu: IridiumArpuResult | None = None


def _arpu_bucket(mix_pct: float, price_usd_month: float, count: int) -> IridiumArpuBucket:
    """Build one ARPU bucket, computing its annual revenue from the count and price.

    Args:
        mix_pct: The bucket's mix share of the pool, percent (the dial, carried as-is).
        price_usd_month: The bucket's monthly price, USD per connection per month.
        count: The bucket's derived connection count.

    Returns:
        The populated :class:`IridiumArpuBucket` (revenue = count x price x months / 1e6).
    """
    revenue_musd_yr = count * price_usd_month * MONTHS_PER_YEAR / MUSD_TO_USD
    return IridiumArpuBucket(
        mix_pct=mix_pct,
        price_usd_month=price_usd_month,
        count=count,
        revenue_musd_yr=revenue_musd_yr,
    )


def derive_arpu_buckets(people_capacity: int, dials: IridiumArpuDials) -> IridiumArpuResult:
    """Derive the four ARPU revenue buckets from the people capacity and the mix dials.

    Implements the design's pool algebra verbatim. One pool rides fleet CAPACITY (the
    ``people_capacity`` passed in, ``fleet_target x subscribers_per_satellite``), so
    every bucket count is linear in the satellite count. The people share (standard +
    premium, as a fraction of 100) inverts the pool
    (``total_connections = people_capacity / people_share``); the premium, IoT, and
    government counts are round-half-up of their mix slice of that pool; and STANDARD
    is the RESIDUAL (``people_capacity - premium_count``), so the people identity
    (``standard_count + premium_count == people_capacity``) is exact by construction
    (no rounding drift). Subscribers are PEOPLE (standard, premium); IoT are DEVICES;
    government is a contract line: the pool is a billable-connections accounting frame,
    not one summed people population.

    Args:
        people_capacity: The built fleet's people capacity
            (``fleet_target x subscribers_per_satellite``), a positive integer.
        dials: The validated :class:`~communications.config.IridiumArpuDials` (the four
            mixes sum to 100 within the epsilon; both people mixes are strictly
            positive, so ``people_share`` is never zero).

    Returns:
        The populated :class:`IridiumArpuResult`: the four buckets, the
        billable-connection total, and the summed annual revenue.
    """
    people_share = (dials.standard_mix_pct + dials.premium_mix_pct) / ARPU_MIX_TOTAL_PCT
    total_connections_float = people_capacity / people_share
    premium_count = _round_half_up(
        total_connections_float * dials.premium_mix_pct / ARPU_MIX_TOTAL_PCT
    )
    standard_count = people_capacity - premium_count
    iot_count = _round_half_up(total_connections_float * dials.iot_mix_pct / ARPU_MIX_TOTAL_PCT)
    government_count = _round_half_up(
        total_connections_float * dials.government_mix_pct / ARPU_MIX_TOTAL_PCT
    )
    standard = _arpu_bucket(dials.standard_mix_pct, dials.standard_price_usd_month, standard_count)
    premium = _arpu_bucket(dials.premium_mix_pct, dials.premium_price_usd_month, premium_count)
    iot = _arpu_bucket(dials.iot_mix_pct, dials.iot_price_usd_month, iot_count)
    government = _arpu_bucket(
        dials.government_mix_pct, dials.government_price_usd_month, government_count
    )
    total_revenue_musd_yr = (
        standard.revenue_musd_yr
        + premium.revenue_musd_yr
        + iot.revenue_musd_yr
        + government.revenue_musd_yr
    )
    return IridiumArpuResult(
        standard=standard,
        premium=premium,
        iot=iot,
        government=government,
        total_connections=_round_half_up(total_connections_float),
        arpu_revenue_total_musd_yr=total_revenue_musd_yr,
    )


def build_iridium_result(
    dials: IridiumDials,
    *,
    fleet_target: int,
    subscribers_per_satellite: int,
    effective_satellites_per_launch: int,
) -> IridiumResult:
    """Assemble the :class:`IridiumResult` from the dials and the sized fleet.

    Resolves the spectral efficiency, re-derives the per-satellite capacity and the
    per-user rates from the dials (the pure derivations above), computes the fleet
    aggregate as ``per_satellite_capacity_gbps x fleet_target`` (0.7 step 6), and
    echoes the derived density and the aperture-coupled effective
    satellites-per-launch (both passed in, already computed once in
    :func:`run_comms_model`, so the density that sized the fleet and the density
    reported here cannot drift). The operations cost and the ecosystem assumption are
    the stated Iridium-model constants (:data:`IRIDIUM_OPERATIONS_COST_MUSD`,
    :data:`ECOSYSTEM_ASSUMPTION_NOTE`). When the dials carry an ``arpu`` block, the
    four-bucket revenue case is derived here at the built fleet's people capacity
    (``fleet_target x subscribers_per_satellite``, :func:`derive_arpu_buckets`) and
    attached; it is ``None`` otherwise.

    Args:
        dials: The Iridium-model :class:`~communications.config.IridiumDials` block.
        fleet_target: The capacity-sized fleet target (from
            :func:`compute_fleet_target`).
        subscribers_per_satellite: The derived per-satellite density that sized the
            fleet (echoed onto the result).
        effective_satellites_per_launch: The aperture-coupled per-launch count the
            deployment used (echoed onto the result).

    Returns:
        The populated :class:`IridiumResult` physics block (with the ARPU revenue case
        when the ``arpu`` dials are set).
    """
    spectral_efficiency = resolve_device_spectral_efficiency(dials)
    per_satellite_capacity_gbps = derive_per_satellite_capacity_gbps(
        dials.spectrum_mhz, spectral_efficiency, dials.aperture_m2
    )
    beam_pool_mbps = dials.spectrum_mhz * spectral_efficiency
    per_user_rate_peak_mbps, per_user_rate_offpeak_mbps = derive_iridium_per_user_rates(
        spectrum_mhz=dials.spectrum_mhz,
        spectral_efficiency_bps_per_hz=spectral_efficiency,
        active_user_rate_mbps=dials.active_user_rate_mbps,
        concurrency_peak=dials.concurrency_peak,
        concurrency_offpeak=dials.concurrency_offpeak,
    )
    # The ARPU revenue case rides the built fleet's people CAPACITY (not the served
    # target), so every bucket count scales with the satellite count. None when the
    # scenario carries no arpu block (the bare-dials path, including the tripwire).
    arpu = (
        derive_arpu_buckets(fleet_target * subscribers_per_satellite, dials.arpu)
        if dials.arpu is not None
        else None
    )
    return IridiumResult(
        spectrum_mhz=dials.spectrum_mhz,
        aperture_m2=dials.aperture_m2,
        device_class=dials.device_class,
        spectral_efficiency_bps_per_hz=spectral_efficiency,
        per_satellite_capacity_gbps=per_satellite_capacity_gbps,
        fleet_aggregate_capacity_gbps=per_satellite_capacity_gbps * fleet_target,
        subscribers_per_satellite=subscribers_per_satellite,
        effective_satellites_per_launch=effective_satellites_per_launch,
        active_user_rate_mbps=dials.active_user_rate_mbps,
        concurrency_peak=dials.concurrency_peak,
        concurrency_offpeak=dials.concurrency_offpeak,
        beam_pool_mbps=beam_pool_mbps,
        per_user_rate_peak_mbps=per_user_rate_peak_mbps,
        per_user_rate_offpeak_mbps=per_user_rate_offpeak_mbps,
        iot_devices=dials.iot_devices,
        operations_cost_musd=IRIDIUM_OPERATIONS_COST_MUSD,
        ecosystem_assumption=ECOSYSTEM_ASSUMPTION_NOTE,
        arpu=arpu,
    )


def arpu_stated_assumptions(dials: IridiumArpuDials) -> tuple[str, ...]:
    """Return the ARPU case's stated-assumption lines (one source of truth).

    The four posture statements the published four-bucket case carries: full
    sell-through on capacity, the honest mix posture (people-and-government share,
    the de-anchored government line, IoT the residual, the constant-mix convention),
    the built-fleet convention, and the margin definition (how the published margin
    is measured). Consumed both by :func:`iridium_assumptions` (spliced into the full
    assumptions tuple) and by the promoted artifact's ``revenue_arpu_buckets`` block,
    so the two never drift.

    Args:
        dials: The validated :class:`~communications.config.IridiumArpuDials` (its
            mixes populate the honest posture line).

    Returns:
        The four ARPU-posture strings, in stable order.
    """
    people_and_gov_pct = dials.standard_mix_pct + dials.premium_mix_pct + dials.government_mix_pct
    return (
        (
            "Full sell-through on capacity: the four-bucket case assumes every "
            "serveable billable-connection slot the built fleet can carry is sold, so "
            "revenue rides the built fleet's people capacity (fleet_target x density), "
            "above the served target, with no penetration or utilization haircut. "
            "Clearly optimistic, stated, founder-owned."
        ),
        (
            "Mix posture (stated honestly): the people-and-government share "
            f"({people_and_gov_pct:.4g} percent of the billable-connection pool) is "
            "loosely anchored on the FY2025 book's like-for-like people-plus-government "
            "share (about 21.2 percent, COMM-617/618); government is deliberately "
            "de-anchored from the book's 4.8 percent to "
            f"{dials.government_mix_pct} percent so the baseline government line "
            "reproduces today's one fixed EMSS contract (COMM-619) rather than scaling a "
            "share; IoT is the residual that closes the mix to 100. The mix is held "
            "constant as the fleet grows (v1); a time-varying mix schedule is the "
            "documented v2 extension."
        ),
        (
            "Built-fleet convention: the revenue case is computed once at the built "
            "fleet (fleet_target), so on a scenario that does not complete its build "
            "inside the horizon the case describes the completed fleet, not the final "
            "horizon year's smaller actual fleet."
        ),
        (
            "Margin definition: the published ARPU margin measures revenue against the "
            "fleet's full build, launch, and replacement cost (the steady-state annual "
            "cost). Operations cost is the explicit zero pending research and corporate "
            "overhead is never included, so it is an operating-style margin (the "
            "data-center model's convention), not a gross margin and not a net margin."
        ),
    )


def iridium_assumptions(dials: IridiumDials) -> tuple[str, ...]:
    """Return the Iridium model's stated-assumptions lines (the assumptions output).

    Takes the dials because one line is conditional on them (the aperture fold
    caveat, 0.8a). Always states: the ecosystem assumption
    (:data:`ECOSYSTEM_ASSUMPTION_NOTE`, 0.8); that operations cost is assumed zero
    (:data:`IRIDIUM_OPERATIONS_COST_MUSD`, an explicit founder-instructed assumption,
    a fixed line to research and add later); the estimate tiers (the
    spectral-efficiency bands, the reuse calibration, the aperture reference and its
    linear conservative scaling, the concurrency pair, the active rate) as
    estimate-tier, founder-owned values; and that the Iridium model is the MSS lane
    (owned L-band, purpose-built or in-chipset devices), never the cellular
    unmodified-phone lane. The revenue-case line is conditional on ``dials.arpu``: with
    the four-bucket ARPU case set it states the PUBLISHED case plus the full
    sell-through assumption, the honest mix posture, the built-fleet convention, and
    the IoT-count supersession; with no ``arpu`` block it states the DEFERRED case
    (cost-plus is the load-bearing revenue, the per-tier MSS ARPUs plug in later).
    Conditionally
    appends :data:`APERTURE_FOLD_CAVEAT_NOTE` when ``dials.aperture_m2`` exceeds
    :data:`APERTURE_NO_FOLD_LIMIT_M2` (0.8a: a documented note, never a validation
    error, so the above-limit what-if stays computable).

    Args:
        dials: The Iridium-model :class:`~communications.config.IridiumDials` block
            (its aperture drives the conditional fold caveat, its concurrency and
            active rate populate the estimate-tier lines, and its optional ``arpu``
            block selects the published-case vs deferred-case revenue lines).

    Returns:
        The stated-assumptions lines, in stable order, as a tuple of strings.
    """
    lines: list[str] = [
        ECOSYSTEM_ASSUMPTION_NOTE,
        (
            f"Operations cost is assumed zero ({IRIDIUM_OPERATIONS_COST_MUSD} USD "
            "millions per year): an explicit founder-instructed assumption, a fixed "
            "operations line to research and add later, stated here rather than "
            "silently omitted."
        ),
        (
            "Spectral efficiency is estimate-tier and founder-owned: the phone-class "
            f"band is {PHONE_CLASS_SE_LOW} to {PHONE_CLASS_SE_HIGH}, the "
            f"small-terminal-class band {SMALL_TERMINAL_CLASS_SE_LOW} to "
            f"{SMALL_TERMINAL_CLASS_SE_HIGH}, the large-terminal-class band "
            f"{TERMINAL_CLASS_SE_LOW} to {TERMINAL_CLASS_SE_HIGH} bps/Hz (class "
            f"centrals {PHONE_CLASS_SE_CENTRAL} / {SMALL_TERMINAL_CLASS_SE_CENTRAL} / "
            f"{TERMINAL_CLASS_SE_CENTRAL})."
        ),
        (
            f"The reuse calibration ({REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE} Gbps per "
            "MHz per unit spectral efficiency) is calibrated at the "
            f"{APERTURE_REFERENCE_M2} m^2 reference aperture; per-satellite capacity "
            "scales linearly with aperture area, which is conservative (it ignores "
            "the additional per-link SNR lift a larger aperture also gives)."
        ),
        (
            f"The busy-hour concurrency pair (peak {dials.concurrency_peak}, off-peak "
            f"{dials.concurrency_offpeak}) and the per-subscriber active rate "
            f"({dials.active_user_rate_mbps} Mbps) are estimate-tier, founder-owned "
            "values."
        ),
    ]
    if dials.arpu is not None:
        lines.append(
            "The prices-today ARPU revenue case is PUBLISHED for the Iridium model as "
            "the four-bucket case (standard personal, premium terminal, IoT devices, "
            "government): a founder-set price-and-mix sheet dated 2026-07-09. Cost-plus "
            "(revenue equals annualized cost times the revenue multiple) stays published "
            "beside it as the cost-recovery floor."
        )
        lines.extend(arpu_stated_assumptions(dials.arpu))
        lines.append(
            "IoT count supersession (one IoT truth): with the ARPU case on, the "
            "published IoT device count derives from the revenue mix (the IoT bucket "
            "count), and the former fixed iot_devices passthrough dial is superseded "
            "(reported only on the no-ARPU path)."
        )
    else:
        lines.append(
            "The prices-today ARPU revenue case is DEFERRED for the Iridium model: "
            "cost-plus (revenue equals annualized cost times the revenue multiple) is "
            "the load-bearing Iridium-model revenue, and the per-tier MSS ARPUs plug "
            "in later."
        )
    lines.append(
        "The Iridium model is the MSS lane (owned L-band, purpose-built or "
        "in-chipset devices), never the cellular direct-to-cell unmodified-phone "
        "lane (the High-Bandwidth Cellular Pure Play model)."
    )
    if dials.aperture_m2 > APERTURE_NO_FOLD_LIMIT_M2:
        lines.append(APERTURE_FOLD_CAVEAT_NOTE)
    return tuple(lines)


# ---------------------------------------------------------------------------
# The cadence-share seam: how many launches the comms slice flies this year.
# ---------------------------------------------------------------------------


def _comms_launches_for_year(year_idx: int, config: CommsConfig) -> tuple[int, int, float]:
    """Price one model year's cadence: fleet launches, comms launches, launch cost.

    Calls the two shared ``common.cadence`` functions and unwraps their cells.
    The whole-fleet cadence drives BOTH the comms launch count (via the share)
    and the launch-cost pricing; the comms model never prices launches at its own
    lower slice cadence.

    Args:
        year_idx: Zero-based model year index.
        config: The comms config (provides the cadence, comms-cadence, and
            launch-cost dial blocks).

    Returns:
        A 3-tuple ``(fleet_launches, comms_launches, launch_cost_per_launch_musd)``:
        the whole-fleet integer launch count, the comms slice's integer launch
        count (``round_half_up(fleet_launches * share_of_fleet)``), and the
        per-launch cost in $M priced at the whole-fleet cadence.
    """
    cad = config.cadence
    fleet_launches = _cell_int(
        compute_launches_per_year(
            year_idx,
            cadence_ceiling=cad.cadence_ceiling,
            launches_at_year_5=cad.launches_at_year_5,
            launches_at_year_10=cad.launches_at_year_10,
            first_launch_year=cad.first_launch_year,
        )
    )
    comms_launches = _round_half_up(fleet_launches * config.comms_cadence.share_of_fleet)
    lc = config.launch_cost
    launch_cost_per_launch_musd = _cell_float(
        compute_launch_cost_musd(
            float(fleet_launches),
            low_cadence_cost_musd=lc.low_cadence_cost_musd,
            high_cadence_cost_musd=lc.high_cadence_cost_musd,
            low_cadence_launches=lc.low_cadence_launches,
            high_cadence_launches=lc.high_cadence_launches,
        )
    )
    return fleet_launches, comms_launches, launch_cost_per_launch_musd


# ---------------------------------------------------------------------------
# The build-and-hold treadmill: one model year.
# ---------------------------------------------------------------------------


def _cohort_economics_for_year(
    *,
    fy: int,
    life: int,
    cohort_builds: list[_CohortBuild],
    living_fleet: int,
    subscribers_served_this_year: int,
    revenue_multiple: float,
    arpu_usd_per_month: float,
) -> tuple[CommsCohortYear, ...]:
    """Build the per-living-cohort economics breakdown for one year (both cases).

    For each cohort alive at ``fy`` under the cliff, computes its annualized cost
    (its living satellites x its locked-in per-satellite annual cost), its cost-plus
    revenue + margin, and its ARPU revenue + margin. The year's served subscribers are
    allocated across cohorts by each cohort's share of the living fleet (a cohort with
    more living satellites serves proportionally more of the base). The last living
    cohort absorbs any rounding remainder so the per-cohort served counts sum exactly
    to the year's served total (no drift versus the fleet-level ARPU figure).

    Args:
        fy: The fiscal year of this rollup.
        life: The satellite life (the cohort cliff).
        cohort_builds: The deployed cohorts so far (the economics overlay).
        living_fleet: The total living satellites this year (the allocation base).
        subscribers_served_this_year: The year's served-PERSON count (the ARPU base).
        revenue_multiple: The cost-plus multiple.
        arpu_usd_per_month: The monthly ARPU.

    Returns:
        The per-living-cohort economics lines, oldest cohort first (empty when no
        cohort is alive).
    """
    living_builds = [b for b in cohort_builds if cohort_is_alive_at(b.launch_year, fy, life)]
    lines: list[CommsCohortYear] = []
    subscribers_allocated = 0
    for idx, build in enumerate(living_builds):
        annual_cost_musd = build.satellites * build.per_satellite_annual_cost_musd
        cost_plus_revenue_musd = annual_cost_musd * revenue_multiple
        # Allocate the year's served subscribers by the cohort's living-satellite
        # share; the last living cohort takes the remainder so the parts sum exactly.
        if idx == len(living_builds) - 1:
            cohort_subscribers = subscribers_served_this_year - subscribers_allocated
        elif living_fleet > 0:
            cohort_subscribers = round(
                subscribers_served_this_year * build.satellites / living_fleet
            )
        else:
            cohort_subscribers = 0
        subscribers_allocated += cohort_subscribers
        arpu_revenue_musd = cohort_subscribers * arpu_usd_per_month * MONTHS_PER_YEAR / MUSD_TO_USD
        cost_plus_margin_pct = _gross_margin_pct(cost_plus_revenue_musd, annual_cost_musd)
        arpu_margin_pct = _gross_margin_pct(arpu_revenue_musd, annual_cost_musd)
        lines.append(
            CommsCohortYear(
                launch_year=build.launch_year,
                living_satellites=build.satellites,
                annual_cost_musd=annual_cost_musd,
                cost_plus_revenue_musd=cost_plus_revenue_musd,
                cost_plus_gross_margin_pct=cost_plus_margin_pct,
                arpu_subscribers_served=cohort_subscribers,
                arpu_revenue_musd=arpu_revenue_musd,
                arpu_gross_margin_pct=arpu_margin_pct,
            )
        )
    return tuple(lines)


def _compute_comms_year(
    year_idx: int,
    fy: int,
    config: CommsConfig,
    cohorts: list[LivedCohort],
    cohort_builds: list[_CohortBuild],
    fleet_target: int,
    satellites_per_launch: int,
    target_already_reached: bool,
) -> tuple[CommsYear, bool]:
    """Roll up one model year: deploy toward the fleet target, hold, cost it, and price revenue.

    Applies the build-and-hold cap in launch-year order:

    1. Price the cadence (fleet launches, comms launches, launch cost).
    2. ``would_be_deployed = comms_launches * satellites_per_launch`` (the
       cadence-share cap on the build rate this year).
    3. ``living_before`` = the living fleet from PRIOR cohorts under the cliff at
       ``fy`` (cohorts that aged off are already excluded).
    4. ``satellites_added = min(would_be_deployed, ceil_to_launch(max(0,
       fleet_target - living_before), satellites_per_launch))`` (the overshoot rule:
       the deficit rounded up to whole launches, capped by the cadence share).
       During HOLD the deficit equals that year's cliff losses, so this replaces
       only the ageing cohorts.
    5. Append ``LivedCohort(fy, satellites_added)`` and re-derive ``living_after``
       under the cliff (so the living count tracks the cohort window).

    Then it layers the REVENUE + GROSS MARGIN overlay (the two cases). It records this
    year's cohort on the parallel ``cohort_builds`` list with its locked-in
    per-satellite annual cost, sums the annualized fleet cost over the living cohorts
    (the margin cost basis, matching the DC annualized convention), scales the served
    subscribers to this year's buildout, and computes both the cost-plus revenue
    (annual cost x the multiple) and the ARPU revenue (served base x monthly ARPU x
    12), each with its gross margin, plus the per-cohort breakdown.

    The fleet target is the CAPACITY-sized fleet (:func:`compute_fleet_target`); the
    treadmill builds and holds to it. The coverage metric is reported separately
    against the coverage floor (it can saturate at 1.0 well before full deployment
    when the fleet target exceeds the floor).

    Args:
        year_idx: Zero-based model year index (for the cadence ramp).
        fy: The fiscal year (``base_year + year_idx``), the cohort launch year.
        config: The comms config.
        cohorts: The cohort list so far (this year's cohort is appended in place).
        cohort_builds: The parallel economics-overlay cohort list (this year's cohort,
            with its locked-in per-satellite annual cost, is appended in place).
        fleet_target: The capacity-sized fleet the build-out fills toward.
        satellites_per_launch: The satellites deployed per launch this run (0.6 seam
            2). The High-Bandwidth Cellular Pure Play model passes the configured
            ``satellite.satellites_per_launch`` dial; the Iridium model passes the
            aperture-coupled EFFECTIVE value (0.7 step 10).
            Consumed by the would-be-deployed count, the overshoot ceil, the
            flown-launches re-derivation, and the per-satellite launch-cost
            annualization.
        target_already_reached: Whether the fleet target was reached in a PRIOR year
            (carries the HOLD-phase flag forward across years).

    Returns:
        A 2-tuple ``(comms_year, target_reached_now_or_before)``: the year's
        rollup and the updated "target reached" flag to thread to the next year.
    """
    life = config.satellite.satellite_lifetime_years
    coverage_floor = config.coverage.satellites_for_full_coverage

    fleet_launches, comms_launches, launch_cost_per_launch_musd = _comms_launches_for_year(
        year_idx, config
    )
    would_be_deployed = comms_launches * satellites_per_launch

    living_before = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))
    deficit = max(0, fleet_target - living_before)
    satellites_added = min(would_be_deployed, _ceil_to_launch(deficit, satellites_per_launch))
    # The launches actually flown for cost is the whole-launch count we deployed
    # (an integer, since satellites_added is a whole-launch multiple). The cadence
    # share may have allowed more launches than the cap used near the end of the
    # build-out; only the flown launches are costed.
    comms_launches_flown = satellites_added // satellites_per_launch

    cohorts.append(LivedCohort(launch_year=fy, units_deployed=satellites_added))
    living_after = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))

    coverage_fraction = min(FULL_COVERAGE_FRACTION, living_after / coverage_floor)
    buildout_fraction = min(FULL_BUILDOUT_FRACTION, living_after / fleet_target)
    target_reached_now = target_already_reached or living_after >= fleet_target

    build_cost_this_year_musd = satellites_added * config.satellite.satellite_build_cost_musd
    launch_cost_this_year_musd = comms_launches_flown * launch_cost_per_launch_musd
    total_cost_this_year_musd = build_cost_this_year_musd + launch_cost_this_year_musd
    # The replacement line is the ongoing HOLD-phase cost: 0.0 during build-out,
    # the year's total cost once the target has been reached (this year's cost in
    # HOLD is exactly the replacement of the cohorts that aged off).
    replacement_cost_this_year_musd = (
        total_cost_this_year_musd if target_reached_now else NO_REPLACEMENT_COST_MUSD
    )

    # --- The revenue + gross-margin overlay (the two cases). ---
    # Record this year's cohort with its locked-in per-satellite annual cost (built
    # from this year's launch cost, so the cadence cost-down is fixed for its life).
    # Only NON-EMPTY cohorts are recorded: a year that deploys zero satellites (e.g.
    # the early build-out years at a small cadence share) launches no cohort and so
    # adds no economics line (it would carry zero satellites, zero cost, zero
    # revenue, an undefined margin); skipping it keeps the cohort lines to the real
    # living satellites.
    if satellites_added > 0:
        per_satellite_annual_cost_musd = _per_satellite_annual_cost_musd(
            satellite_build_cost_musd=config.satellite.satellite_build_cost_musd,
            launch_cost_per_launch_musd=launch_cost_per_launch_musd,
            satellites_per_launch=satellites_per_launch,
            satellite_lifetime_years=life,
        )
        cohort_builds.append(
            _CohortBuild(
                launch_year=fy,
                satellites=satellites_added,
                per_satellite_annual_cost_musd=per_satellite_annual_cost_musd,
            )
        )
    # The annualized fleet cost (the margin cost basis): sum over living cohorts of
    # each cohort's living satellites x its per-satellite annual cost. This is the
    # steady annual cost each satellite carries, NOT the deployment cash cost; it is
    # a different convention from the cash replacement line (they converge only in
    # clean rotational steady state).
    annual_cost_this_year_musd = sum(
        b.satellites * b.per_satellite_annual_cost_musd
        for b in cohort_builds
        if cohort_is_alive_at(b.launch_year, fy, life)
    )
    # The served subscribers at THIS year's buildout (the ARPU base for the year).
    subscribers_served_this_year = subscribers_served_at(
        buildout_fraction,
        subscriber_target=config.subscribers.subscribers_at_full_coverage,
        override=config.subscribers.subscribers_served_override,
    )
    revenue_multiple = config.revenue.revenue_multiple
    arpu_usd_per_month = config.revenue.arpu_usd_per_month
    # Case 1, COST-PLUS: revenue = annual cost x the multiple (cost-coupled).
    cost_plus_revenue_this_year_musd = annual_cost_this_year_musd * revenue_multiple
    cost_plus_gross_margin_pct = _gross_margin_pct(
        cost_plus_revenue_this_year_musd, annual_cost_this_year_musd
    )
    # Case 2, ARPU: revenue = served base x monthly ARPU x 12 (price x served base).
    arpu_revenue_this_year_musd = (
        subscribers_served_this_year * arpu_usd_per_month * MONTHS_PER_YEAR / MUSD_TO_USD
    )
    arpu_gross_margin_pct = _gross_margin_pct(
        arpu_revenue_this_year_musd, annual_cost_this_year_musd
    )
    cohort_lines = _cohort_economics_for_year(
        fy=fy,
        life=life,
        cohort_builds=cohort_builds,
        living_fleet=living_after,
        subscribers_served_this_year=subscribers_served_this_year,
        revenue_multiple=revenue_multiple,
        arpu_usd_per_month=arpu_usd_per_month,
    )

    comms_year = CommsYear(
        year=fy,
        fleet_launches_this_year=fleet_launches,
        comms_launches_flown_this_year=comms_launches_flown,
        satellites_deployed_this_year=satellites_added,
        living_fleet=living_after,
        coverage_fraction=coverage_fraction,
        buildout_fraction=buildout_fraction,
        launch_cost_per_launch_musd=launch_cost_per_launch_musd,
        build_cost_this_year_musd=build_cost_this_year_musd,
        launch_cost_this_year_musd=launch_cost_this_year_musd,
        total_cost_this_year_musd=total_cost_this_year_musd,
        is_hold_phase=target_reached_now,
        replacement_cost_this_year_musd=replacement_cost_this_year_musd,
        subscribers_served_this_year=subscribers_served_this_year,
        annual_cost_this_year_musd=annual_cost_this_year_musd,
        cost_plus_revenue_this_year_musd=cost_plus_revenue_this_year_musd,
        cost_plus_gross_margin_pct=cost_plus_gross_margin_pct,
        arpu_revenue_this_year_musd=arpu_revenue_this_year_musd,
        arpu_gross_margin_pct=arpu_gross_margin_pct,
        cohort_lines=cohort_lines,
    )
    return comms_year, target_reached_now


# ---------------------------------------------------------------------------
# The engine entry point.
# ---------------------------------------------------------------------------


def run_comms_model(config: CommsConfig) -> CommsTrajectory:
    """Run the build-and-hold cost trajectory for one comms cellular scenario.

    Iterates the model years 0..``horizon_years`` inclusive (FY2026..FY2036 at
    the defaults), deploying satellites toward the CAPACITY-sized FLEET TARGET
    (:func:`compute_fleet_target`: the subscriber target divided by the per-satellite
    density, floored by the coverage floor, capped by the saturation cap), holding
    the constellation once reached (replacing the 5-year-cliff losses), and summing
    the satellite build cost plus the cadence-indexed launch cost over the
    trajectory.

    The launch cost is priced at the WHOLE-fleet Neutron cadence (the shared
    90/year FY2036 ramp drives the cost-down); the comms cadence share sets only
    how many launches comms flies. If the fleet target is too high for the chosen
    cadence share to reach within the horizon, the model still runs and reports a
    living fleet below the target at the final year (a truthful output, surfaced via
    ``full_coverage_reached_year is None`` and a WARNING log), not an error.

    Args:
        config: The comms config (the slim, roughly 6-dial frozen Pydantic tree).
            The all-defaults config reproduces the central case.

    Returns:
        A :class:`CommsTrajectory`: the per-year rollups plus the cumulative
        build-and-hold cost, the fleet target and its binding regime, the first
        full-deployment year (or ``None``), the steady-state annual replacement cost,
        the served-subscriber count, the annual cost per subscriber, and the
        steady-state two-case revenue + gross margin (cost-plus and ARPU).
    """
    base_year = config.metadata.base_year
    horizon_years = config.metadata.horizon_years
    subscriber_target = config.subscribers.subscribers_at_full_coverage

    # The per-satellite density and the effective satellites-per-launch: the
    # High-Bandwidth Cellular Pure Play model reads them from the dials; the Iridium
    # model (a non-None iridium block) DERIVES the density from L-band physics and
    # the effective per-launch count from the aperture coupling (0.6 seams 1 and 2;
    # 0.7 steps 2/3/10). Everything downstream (compute_fleet_target, the year loop)
    # consumes the two values unchanged, so the High-Bandwidth Cellular Pure Play
    # path (config.iridium is None) is behavior-identical.
    if config.iridium is not None:
        spectral_efficiency = resolve_device_spectral_efficiency(config.iridium)
        per_sat_capacity_gbps = derive_per_satellite_capacity_gbps(
            config.iridium.spectrum_mhz, spectral_efficiency, config.iridium.aperture_m2
        )
        subscribers_per_satellite = derive_iridium_subscribers_per_satellite(
            per_satellite_capacity_gbps=per_sat_capacity_gbps,
            active_user_rate_mbps=config.iridium.active_user_rate_mbps,
            concurrency_peak=config.iridium.concurrency_peak,
        )
        satellites_per_launch_effective = derive_iridium_satellites_per_launch(
            configured_satellites_per_launch=config.satellite.satellites_per_launch,
            aperture_m2=config.iridium.aperture_m2,
        )
    else:
        subscribers_per_satellite = config.subscribers.subscribers_per_satellite
        satellites_per_launch_effective = config.satellite.satellites_per_launch

    # Size the fleet to SERVE the subscriber base (the capacity dimension): the
    # treadmill below builds and holds to this fleet target, not the coverage floor.
    fleet_target, binding_regime = compute_fleet_target(
        subscriber_target=subscriber_target,
        subscribers_per_satellite=subscribers_per_satellite,
        coverage_floor=config.coverage.satellites_for_full_coverage,
        max_fleet_satellites=config.coverage.max_fleet_satellites,
    )

    # Build the Iridium-model physics result block once the fleet is sized (None on
    # the High-Bandwidth Cellular Pure Play path). It re-derives the physics from
    # the dials and echoes the density
    # and the effective per-launch count that actually sized and deployed the fleet.
    iridium_result: IridiumResult | None = None
    if config.iridium is not None:
        iridium_result = build_iridium_result(
            config.iridium,
            fleet_target=fleet_target,
            subscribers_per_satellite=subscribers_per_satellite,
            effective_satellites_per_launch=satellites_per_launch_effective,
        )

    cohorts: list[LivedCohort] = []
    # The parallel economics-overlay cohort list (carries the per-satellite annual
    # cost the build/cost treadmill does not). Threaded alongside ``cohorts``.
    cohort_builds: list[_CohortBuild] = []
    years: list[CommsYear] = []
    target_reached = False
    full_coverage_reached_year: int | None = None

    for year_idx in range(horizon_years + 1):
        fy = base_year + year_idx
        comms_year, target_reached = _compute_comms_year(
            year_idx,
            fy,
            config,
            cohorts,
            cohort_builds,
            fleet_target,
            satellites_per_launch_effective,
            target_reached,
        )
        years.append(comms_year)
        if full_coverage_reached_year is None and target_reached:
            full_coverage_reached_year = fy

    total_build_and_hold_cost_musd = sum(y.total_cost_this_year_musd for y in years)
    # The steady-state annual replacement cost is the final model year's
    # replacement line (the representative HOLD-phase annual cost once the build
    # completes); 0.0 if the build never completed within the horizon.
    steady_state_annual_replacement_cost_musd = (
        years[-1].replacement_cost_this_year_musd if years else NO_REPLACEMENT_COST_MUSD
    )
    # The reported subscribers served is the buildout mapping applied to the FINAL
    # year's buildout fraction (FY2036). At a completed build-out the final buildout
    # fraction is 1.0 and this equals the subscriber target (or the override); below
    # full deployment it is the proportional partial-deployment count.
    final_buildout_fraction = years[-1].buildout_fraction if years else NO_BUILDOUT_FRACTION
    subscribers_served = subscribers_served_at(
        final_buildout_fraction,
        subscriber_target=subscriber_target,
        override=config.subscribers.subscribers_served_override,
    )
    # Cost per subscriber per year (the headline cost-to-serve, the space side of the
    # ground comparison): the steady-state annual cost in USD over the subscriber
    # TARGET (the full-deployment base, per the spec). 0.0 when steady state was not
    # reached within the horizon (the steady-state cost is 0.0 then).
    cost_per_subscriber_annual_usd = _cost_per_subscriber_annual_usd(
        steady_state_annual_replacement_cost_musd, subscriber_target
    )

    # The steady-state revenue + gross-margin headlines (both cases) read the FINAL
    # model year's lines (the representative HOLD-phase steady state, matching the
    # ``steady_state_annual_replacement_cost`` convention). The margin cost basis is
    # the ANNUALIZED fleet cost (``annual_cost_this_year_musd``), the DC convention;
    # it converges with the cash replacement line only in clean rotational steady
    # state (in the build-just-completed final year it runs higher).
    final_year = years[-1] if years else None
    steady_state_annual_cost_musd = (
        final_year.annual_cost_this_year_musd if final_year else NO_ANNUAL_COST_MUSD
    )
    steady_state_revenue_cost_plus_musd = (
        final_year.cost_plus_revenue_this_year_musd if final_year else NO_REVENUE_MUSD
    )
    steady_state_gross_margin_cost_plus_pct = (
        final_year.cost_plus_gross_margin_pct if final_year else ZERO_MARGIN_PCT
    )
    steady_state_revenue_arpu_musd = (
        final_year.arpu_revenue_this_year_musd if final_year else NO_REVENUE_MUSD
    )
    steady_state_gross_margin_arpu_pct = (
        final_year.arpu_gross_margin_pct if final_year else ZERO_MARGIN_PCT
    )

    if full_coverage_reached_year is None:
        logger.warning(
            "Comms build-out did not reach the fleet target (%d satellites, %s regime) within "
            "the %d-year horizon at share_of_fleet=%.3f; living fleet at FY%d is %d. This is a "
            "truthful below-target output, not an error.",
            fleet_target,
            binding_regime.value,
            horizon_years,
            config.comms_cadence.share_of_fleet,
            years[-1].year if years else base_year,
            years[-1].living_fleet if years else 0,
        )

    return CommsTrajectory(
        years=tuple(years),
        total_build_and_hold_cost_musd=total_build_and_hold_cost_musd,
        fleet_target=fleet_target,
        subscribers_per_satellite=subscribers_per_satellite,
        binding_regime=binding_regime,
        full_coverage_reached_year=full_coverage_reached_year,
        steady_state_annual_replacement_cost_musd=steady_state_annual_replacement_cost_musd,
        subscribers_served=subscribers_served,
        cost_per_subscriber_annual_usd=cost_per_subscriber_annual_usd,
        steady_state_annual_cost_musd=steady_state_annual_cost_musd,
        steady_state_revenue_cost_plus_musd=steady_state_revenue_cost_plus_musd,
        steady_state_gross_margin_cost_plus_pct=steady_state_gross_margin_cost_plus_pct,
        steady_state_revenue_arpu_musd=steady_state_revenue_arpu_musd,
        steady_state_gross_margin_arpu_pct=steady_state_gross_margin_arpu_pct,
        iridium=iridium_result,
    )


__all__ = [
    "CommsCohortYear",
    "CommsTrajectory",
    "CommsYear",
    "IridiumArpuBucket",
    "IridiumArpuResult",
    "IridiumResult",
    "arpu_stated_assumptions",
    "build_iridium_result",
    "compute_fleet_target",
    "derive_arpu_buckets",
    "derive_iridium_per_user_rates",
    "derive_iridium_satellites_per_launch",
    "derive_iridium_subscribers_per_satellite",
    "derive_per_satellite_capacity_gbps",
    "iridium_assumptions",
    "resolve_device_spectral_efficiency",
    "run_comms_model",
    "subscribers_served_at",
]
