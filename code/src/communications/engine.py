"""The communications engine: the shared fleet-and-cost loop, and the cellular family.

THE SHARED LOOP. :func:`run_fleet_loop` runs a fleet over the horizon under a
family's deployment rule and returns the shared fleet-and-cost record,
:class:`FleetTrajectory`: per model year (:class:`FleetYear`) the cadence, the
satellites deployed, the living fleet under the cohort cliff, the coverage fraction,
the build, launch, total and replacement cost lines, and the annualized cost with one
line per living cohort (:class:`FleetCohortCost`, its per-satellite cost locked at its
launch year's price); then the trajectory's cost totals. The loop holds no family
branch: a :class:`DeploymentRule` decides how many satellites a year adds and how many
of them replace retired ones, reading only its :class:`DeploymentStep` and keeping no
state, and the loop refuses an impossible answer (:class:`DeploymentRuleError`). Every
family's fleet runs on it; each family's own lines live in its own record beside the
shared one. The shared cost functions live here too: the per-satellite annualization
(:func:`per_satellite_annual_cost_musd`) and the one margin formula
(:func:`margin_pct`, None where revenue is not positive).

THE CELLULAR FAMILY (the High-Bandwidth Cellular Pure Play model, a fixed
subscriber-density dial). Its entry, :func:`run_comms_model`, refuses a config with an
``iridium`` block (:class:`NotACellularConfigError`); otherwise it sizes the fleet
target from the dials (:func:`compute_fleet_target`), runs the loop under
:func:`cellular_rule` (build to the target, then hold it) and builds its record
(:func:`build_cellular_record`, a :class:`CellularTrajectory`), returning the two
records as a :class:`CellularRun`.

THE IRIDIUM FAMILY. Its entry is ``communications.iridium.run_iridium_model(config,
curve)``, which checks its saturation curve against the config before it runs. Until
the Iridium family is built there, that entry sizes the fleet by the density path in
this module (the L-band derivations below: the spectral efficiency, the per-satellite
capacity, the derived density, the aperture-coupled satellites per launch, and the v5
physics block, :func:`build_iridium_result`) and runs it through the cellular rule and
record, so its run is a :class:`CellularRun` whose record carries the v5 block. This
module imports neither the Iridium family module nor the curve's contract: a family
hands the loop its rule.

It mirrors the data-center model's fleet engine (the per-year loop in
``data_center/engine.py`` plus the living-cohort rollup in ``data_center/fleet.py``)
with three deliberate differences, all driven by the comms design:

1. Satellites per launch. The DC deploys one node per launch; comms deploys
   ``satellites_per_launch`` satellites per launch, so
   ``satellites_deployed_this_year = comms_launches_flown_this_year * satellites_per_launch``.
2. The deployment rule. The DC fleet grows with cadence without bound. A comms fleet
   deploys what its family's rule decides. The cellular rule (the treadmill) builds
   toward the FLEET TARGET (the CAPACITY-sized fleet, :func:`compute_fleet_target`:
   the subscriber target divided by the per-satellite density, floored by the
   coverage floor and capped by the saturation cap) and then HOLDS: once the target
   is reached it deploys only enough whole launches to replace the cohorts ageing off
   the service-life cliff, so the living count stays at (or as close as launch
   granularity allows to) the fleet target.
3. Two cadence roles. The shared whole-fleet logistic ramp
   (``common.cadence.compute_launches_per_year``, the 90/year FY2036 ramp) sets
   the WHOLE-fleet launch count. The comms slice flies a SHARE of it
   (``share_of_fleet``). The launch COST is priced at the WHOLE-fleet cadence
   (the cadence-indexed cost-down is a Neutron-production-scale effect shared
   across the whole program, not the comms slice's own rate); the comms share
   sets only how many launches comms flies. This is the load-bearing
   distinction: cost is priced at fleet cadence, the count flown is the comms
   share. (If the investor later wants the comms slice priced at its own lower
   cadence, that is a documented alternative; the default is fleet-cadence
   pricing.)

The cohort cliff is the shared ``common.cohort.LivedCohort`` /
``living_cohorts`` machinery, reused unchanged: a cohort is alive in the
half-open interval ``[launch_year, launch_year + satellite_lifetime_years)``.
The shared ``LivedCohort`` carries only ``launch_year`` + ``units_deployed``,
which is exactly what the cliff needs (no per-satellite economics ride on the
cohort, unlike the DC ``Cohort``), so comms uses it directly with no subclass; the
loop keeps each cohort's locked cost beside it.

The two shared ``common.cadence`` functions return a ``ProvenanceCell``; this
engine unwraps each ``.value`` to a plain ``float``/``int`` ONCE (via the shared
strict :func:`common.provenance.as_float` / :func:`common.provenance.as_int`,
the unwrap the DC engine uses too) at the single seam where the model touches a
cell. Everything downstream is plain numerics; the comms output stays light (no
provenance envelope).

This module imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. It also carries the cellular family's subscriber mapping
(:func:`subscribers_served_at`): subscribers are PEOPLE, NOT households, and never
IoT devices. The fleet is CAPACITY-SIZED to serve the subscriber TARGET (the input
base), and the served count RAMPS with the buildout
(``min(base, people_capacity) x min(1.0, living_fleet / fleet_target)``, where the
base is the target or the served override and ``people_capacity`` is
``fleet_target x subscribers_per_satellite``), so the served count never exceeds what
the fleet can carry: it reaches the target at full deployment unless the saturation
cap binds (or an override asks for more than the fleet carries), in which case it
reaches the fleet's people capacity. This is a sized-base mapping, NOT the old
spectrum -> capacity -> demand chain (cut). The cellular record reports the
served-people count at the FINAL year's buildout
(``CellularTrajectory.subscribers_served``), the final-year cash cost per served
person (``final_year_cash_cost_per_subscriber_usd``), and, interim for the Iridium v5
artifact, the built fleet's annualized cost (``built_fleet_annual_cost_musd``, its
published ARPU margin's cost basis).

THE REPLACEMENT LINE. The loop costs as replacement what the rule counts: the
replaced satellites' build cost plus their whole launches at the year's price. Only
the replacement of retiring cohorts counts as replacement, never a build tranche. The
cellular rule counts, before and in the year the fleet target is first reached, the
part of a year's deployment that replaces the cohorts retiring that year
(``min(satellites_added, retiring)``, both whole launches; the rest is build), and
after that year (the HOLD phase) the whole deployment, which restores retired
satellites. The shared record's headline ``final_year_replacement_cost_musd`` is the
final model year's replacement line, or ``None`` when the final year replaced no
retiring cohort (no cash replacement basis exists that year, so none is published as
if it were one).

THE OVERSHOOT RULE (the cellular rule's; frozen here and in the engine tests).
Launches are granular (a whole launch deploys ``satellites_per_launch`` satellites at
once), so the last build-out launch may push the living count slightly OVER the
target. The rule, applied uniformly in BOTH the build-out and HOLD phases: the
satellites to add this year are the deficit to the target (``target -
living_before``) rounded UP to a whole number of launches (``_ceil_to_launch``),
capped by the comms cadence share for the year. This lets the final build cohort
overshoot the target by strictly less than one launch's worth and never deploys
beyond what is needed to hold. During HOLD the deficit equals that year's cliff
losses less any overshoot carried from the final build cohort, so the same formula
replaces only the ageing cohorts.

THE REVENUE AND MARGIN OVERLAY (the cellular record's; mirrors the data-center
revenue and margin pattern, adapted to the comms model's lighter single-value style;
no R-band, no provenance envelope). On the shared record's annualized cost the
cellular record layers, per cohort and per year, TWO REVENUE CASES. The cost basis is
each living cohort's line: its satellites at the per-satellite LIFETIME cost (the flat
build cost plus the satellite's share of its deployment-year launch cost) spread over
the satellite life, locked at launch, summed over the living cohorts (matching the DC
``cost_annual = node_total / service_life`` convention). It is a different convention
from the cash replacement line (which the final-year cash per-subscriber figure
reads); the two converge only in clean rotational steady state, and in any single
year either can be the larger (the cash line is cohort-timed: the promoted Iridium
scenario's FY2036 cash replacement is 250.0 $M against a 145.0 $M annualized cost,
while a year that replaces no cohort carries no cash replacement at all). Case 1
(COST-PLUS): revenue = annual cost x ``revenue_multiple`` (cost-coupled, the DC
central R = 1.5 mirror). Case 2 (PRICES-TODAY / ARPU): revenue = served subscribers x
``arpu_usd_per_month`` x 12. The margin in both is ``(revenue - cost) / revenue``, a
percent (0.0 where there is no revenue, the cellular record's published convention).
Each living cohort's revenue line is a :class:`CellularCohortRevenue` beside its cost
line, and the year's lines and the steady-state (final-year) headlines sit on
:class:`CellularYear` / :class:`CellularTrajectory`. The revenue is a cost-coupled
multiple or a price-times-served-base figure, NEVER a demand or market-size estimate.

Units: money in $M; counts are integers; margins in percent; time in fiscal years
(FY2026..FY2036, year 0 = ``base_year``).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final, Protocol

from common.cadence import (
    ROUND_TO_NEAREST_OFFSET,
    compute_launch_cost_musd,
    compute_launches_per_year,
    round_half_up,
)
from common.cohort import LivedCohort, cohort_is_alive_at, living_cohorts
from common.provenance import as_float, as_int
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
    MOUNTED_TERMINAL_CLASS_SE_CENTRAL,
    MOUNTED_TERMINAL_CLASS_SE_HIGH,
    MOUNTED_TERMINAL_CLASS_SE_LOW,
    PHONE_CLASS_SE_CENTRAL,
    PHONE_CLASS_SE_HIGH,
    PHONE_CLASS_SE_LOW,
    REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE,
    SMALL_TERMINAL_CLASS_SE_CENTRAL,
    SMALL_TERMINAL_CLASS_SE_HIGH,
    SMALL_TERMINAL_CLASS_SE_LOW,
    BindingRegime,
    DeviceClass,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fixed model constants (named, never bare literals; see CLAUDE.md).
# ---------------------------------------------------------------------------

FULL_COVERAGE_FRACTION: Final[float] = 1.0
"""The coverage fraction at the coverage FLOOR: the living fleet is clamped to this
so the coverage metric (``living_fleet / coverage_floor``) never reports above 1.0
once the fleet meets or exceeds the floor (with a large base the fleet runs well
above the floor, so coverage saturates at 1.0 while the build continues toward the
capacity-sized fleet target)."""

FULL_BUILDOUT_FRACTION: Final[float] = 1.0
"""The buildout fraction at full deployment: the living fleet is clamped to this so
the served-subscribers mapping (``buildout_fraction x subscriber_target``) never
scales beyond the target when the build overshoots the fleet target by less than one
launch's worth."""

NO_BUILDOUT_FRACTION: Final[float] = 0.0
"""The lower clamp on the buildout fraction fed to the served-subscribers mapping: a
negative buildout fraction is meaningless (the engine never produces one), so it
floors at zero before scaling the subscriber target."""

MUSD_TO_USD: Final[float] = 1_000_000.0
"""Conversion from the model's internal money unit ($M) to whole USD. The per-person
cost figures are reported in USD per person per year (the unit the ground interface
is on), so a $M cost line is multiplied by this before dividing by the served-people
base, and a USD revenue line is divided by it to report $M."""

LAUNCH_SHARE_ROUNDING_TOLERANCE: Final[float] = 1e-9
"""Absolute tolerance added before the half-up rounding of the comms launch share
(``fleet_launches x share_of_fleet``), so an exact half rounds up as intended. The
product of an integer cadence and a decimal share carries binary representation
error (0.35 x 90 evaluates to 31.499999999999996, not 31.5), which would otherwise
round an exact half DOWN. The error is of order 1e-14 at any modeled cadence, far
below this tolerance, while 1e-9 of a launch is far below any meaningful fraction a
share dial can express, so the tolerance only ever repairs representation error. A
fixed numerical constant, not a tunable."""

MIN_SUBSCRIBERS_PER_SATELLITE: Final[int] = 1
"""The smallest derived subscriber density the fleet sizing accepts: one person per
satellite. A density that rounds below this describes a satellite that cannot carry
a single subscriber at the configured load, so the fleet sizing would divide by zero;
the derivation raises a clear error instead. A structural bound, not a tunable."""

MIN_SATELLITES_PER_LAUNCH: Final[int] = 1
"""The fewest satellites a launch carries in the shared fleet-and-cost loop: one. The loop
deploys and costs whole launches (a cohort is a multiple of the satellites per launch, and the
launches flown are its quotient), so a count below one has no launch to divide into; the loop
refuses it with a clear error instead. A structural bound, not a tunable."""

MARGIN_PERCENT_SCALE: Final[float] = 100.0
"""The percent scale for a gross margin: ``(revenue - cost) / revenue`` times this
yields a percentage (e.g. 0.333 -> 33.3), mirroring the data-center fleet-margin
convention so the two models report margin in the same unit."""

ZERO_MARGIN_PCT: Final[float] = 0.0
"""The margin percent the cellular family publishes where revenue is not positive (an
empty fleet, or a build-out year before any satellite is on orbit): the margin is
undefined there, so :func:`margin_pct` returns None and the cellular record (with the
Iridium artifact's ARPU margin) reports 0.0 in its place, its published values unchanged,
mirroring the data-center fleet-margin guard."""

NO_ANNUAL_COST_MUSD: Final[float] = 0.0
"""The annualized cost ($M/yr) of nothing: the per-satellite annual cost returned for a
non-positive satellite life (guarded, though the lifetime dial is ``ge=1``: with no life to
spread it over, the annualized cost basis is 0.0), and the start of the shared loop's sum of a
year's cohort cost lines, so a year with no living cohort carries 0.0, a float, as the record's
types say."""


# ---------------------------------------------------------------------------
# Integer launch-count helpers (reuse the shared half-up offset; do not redefine).
# ---------------------------------------------------------------------------


def _comms_launch_count(fleet_launches: int, share_of_fleet: float) -> int:
    """Turn the comms slice of the whole-fleet cadence into a whole launch count.

    ``floor(fleet_launches x share_of_fleet + 0.5 + LAUNCH_SHARE_ROUNDING_TOLERANCE)``:
    half up, like :func:`common.cadence.round_half_up`, plus the named
    :data:`LAUNCH_SHARE_ROUNDING_TOLERANCE` so an exact half is not lost to binary
    representation error (a 0.35 share of 90 launches is 31.5, which rounds to 32,
    although the float product is 31.499999999999996).

    Args:
        fleet_launches: The whole-fleet integer launch count this year.
        share_of_fleet: The comms fraction of the fleet cadence (the config dial).

    Returns:
        The comms slice's whole launch count, rounded half up.
    """
    return math.floor(
        fleet_launches * share_of_fleet + ROUND_TO_NEAREST_OFFSET + LAUNCH_SHARE_ROUNDING_TOLERANCE
    )


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
# BindingRegime (the investor's coverage-vs-capacity question).
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
# the Iridium entry (communications.iridium.run_iridium_model) wires them in before
# it runs the shared loop under the cellular rule. THE THREE LANES
# stay separate: the Iridium model is the MSS lane (purpose-built or in-chipset
# devices on owned L-band), NOT cellular direct-to-cell to an unmodified phone
# (the High-Bandwidth Cellular Pure Play model) and NOT broadband.
# ---------------------------------------------------------------------------


def resolve_device_spectral_efficiency(dials: IridiumDials) -> float:
    """Resolve the Iridium-model spectral efficiency (bps/Hz) from the dials (0.7 step 1).

    Returns the explicit ``spectral_efficiency_bps_per_hz`` override when set,
    otherwise the central spectral-efficiency tier for the ``device_class`` (the
    investor's three device categories, a three-row mapping): ``PHONE_CLASS`` to
    :data:`PHONE_CLASS_SE_CENTRAL` (0.65), ``SMALL_TERMINAL_CLASS`` to
    :data:`SMALL_TERMINAL_CLASS_SE_CENTRAL` (2.0), ``MOUNTED_TERMINAL_CLASS`` to
    :data:`MOUNTED_TERMINAL_CLASS_SE_CENTRAL` (2.5).

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
        DeviceClass.MOUNTED_TERMINAL_CLASS: MOUNTED_TERMINAL_CLASS_SE_CENTRAL,
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
    Mass context for the inverse-linear coupling: ~800 kg at the 25 m^2 reference
    (COMM-256) scales roughly linearly with area, ~1,920 kg at 60 m^2. The published
    coupling is the inverse-AREA convention (5 per launch at 60 m^2); the separate
    estimate-bound mass quotient reads 6 (floor of ~13,000 kg over ~1,920 kg). Close
    but distinct conventions: this function implements the area convention.

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

    Uses the shared :func:`common.cadence.round_half_up` (NOT ``floor`` or ``int()``): it matches
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
        The derived subscribers-per-satellite density (people, a whole count, at least
        :data:`MIN_SUBSCRIBERS_PER_SATELLITE`).

    Raises:
        ValueError: If the density rounds below one person per satellite (for example
            a 0.01 m^2 aperture at full peak concurrency): such dials describe a
            satellite that cannot carry a single subscriber, and the fleet sizing
            would divide by zero.
    """
    offered_load_per_subscriber_mbps = active_user_rate_mbps * concurrency_peak
    per_satellite_capacity_mbps = per_satellite_capacity_gbps * GBPS_TO_MBPS
    density = round_half_up(per_satellite_capacity_mbps / offered_load_per_subscriber_mbps)
    if density < MIN_SUBSCRIBERS_PER_SATELLITE:
        raise ValueError(
            "the Iridium dials derive fewer than one subscriber per satellite: "
            f"per-satellite capacity {per_satellite_capacity_mbps:g} Mbps over a "
            f"per-subscriber peak load of {offered_load_per_subscriber_mbps:g} Mbps "
            f"(active rate {active_user_rate_mbps:g} Mbps x peak concurrency "
            f"{concurrency_peak:g}) rounds to {density}. Raise the aperture, the "
            "spectrum, or the spectral efficiency, or lower the active rate or the "
            "peak concurrency."
        )
    return density


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
# The buildout-to-subscribers mapping (the capacity-sized logic).
#
# Subscribers are PEOPLE, NOT households (a household is the broadband unit) and
# never IoT devices. The served count RAMPS with the buildout: the base is the
# subscriber TARGET (or the served override), capped at the people capacity of the
# fleet target (fleet_target x subscribers_per_satellite), and the fraction served
# is the fraction of the capacity-sized FLEET TARGET on orbit. At full deployment it
# equals the capped base. This is a sized-base map, NOT the old spectrum -> capacity
# -> demand chain (cut): the capacity enters only as the ceiling on the base.
# ---------------------------------------------------------------------------


def subscribers_served_at(
    buildout_fraction: float,
    *,
    subscriber_target: int,
    override: int | None,
    people_capacity: int,
) -> int:
    """Map a fleet-buildout fraction to the served-PERSON count, capped at capacity.

    The mapping is linear in the buildout fraction: at full deployment
    (``buildout_fraction == 1.0``) the fully-built constellation serves the whole base;
    at partial deployment it serves proportionally fewer people. The base is the
    optional direct override when supplied, otherwise the ``subscriber_target`` dial,
    and it is capped at ``people_capacity`` (the most people the fleet target can
    carry at its per-satellite density), so the model never reports serving more
    people than the fleet carries. The cap binds only in the saturated regime (the
    target needs more satellites than the saturation cap allows) or when an override
    asks for more than the fleet carries; in the coverage and capacity regimes the
    fleet target's capacity is at or above the target by construction.

    Subscribers are PEOPLE, not households and never IoT devices. The figure is a
    sized served-base count (the capped base scaled by how much of the capacity-sized
    fleet is on orbit), NOT a demand or market estimate.

    Args:
        buildout_fraction: The fraction of the capacity-sized fleet target currently
            on orbit (``living_fleet / fleet_target``, the cellular record's per-year
            ``CellularYear.buildout_fraction``). Clamped to ``[0.0, 1.0]`` before
            scaling, so an out-of-range value (the engine never produces one) cannot
            push the served count below zero or above the capped base.
        subscriber_target: The served-PERSON count at full deployment (the configured
            subscriber target). Used when ``override`` is ``None``.
        override: The OPTIONAL direct served-base scalar. When not ``None`` it
            replaces ``subscriber_target`` as the full-deployment base (still capped
            at ``people_capacity``; below full deployment the count still scales by
            the buildout fraction).
        people_capacity: The fleet target's people capacity
            (``fleet_target x subscribers_per_satellite``), the ceiling on the base.

    Returns:
        The served-PERSON count at the given buildout fraction, rounded half up to a
        whole person (``round_half_up(clamped_buildout_fraction x min(base,
        people_capacity))``).
    """
    base = override if override is not None else subscriber_target
    capped_base = min(base, people_capacity)
    clamped = min(FULL_BUILDOUT_FRACTION, max(NO_BUILDOUT_FRACTION, buildout_fraction))
    return round_half_up(clamped * capped_base)


def usd_per_person(cost_musd: float | None, people_served: int) -> float | None:
    """Divide a $M cost by the served-people base into USD per person.

    The one per-person conversion: the cost (converted from $M to whole USD via
    :data:`MUSD_TO_USD`) over the served people. It prices both published
    per-person figures on the same base: the final-year cash cost (the final
    year's replacement line) and the annualized cost (the final year's annualized
    fleet cost), so an override or a capacity-capped base flows through both.
    ``None`` when there is no cost basis (the final year replaced no retiring
    cohort) or nobody is served (the division is undefined): an undefined figure
    is never published as 0.0.

    Args:
        cost_musd: The cost, $M, or ``None`` when no basis exists.
        people_served: The served-PERSON count.

    Returns:
        The cost per served person, USD, or ``None``.
    """
    if cost_musd is None or people_served <= 0:
        return None
    return cost_musd * MUSD_TO_USD / people_served


# ---------------------------------------------------------------------------
# The shared cost functions: the per-satellite annualization and the one margin.
#
# The COST BASIS for margin is the ANNUALIZED per-satellite cost (the satellite's
# lifetime cost: its flat build cost plus its share of its deployment-year launch
# cost, spread over the satellite life), matching the DC annualized convention
# (cost_annual = node_total / service_life). Each living satellite carries this
# annual cost every year of its life, so the per-year annualized fleet cost is the
# sum over living cohorts. NOTE this is a different convention from the cash
# replacement line (``replacement_cost_this_year_musd``, which the final-year cash
# per-subscriber figure reads): the two CONVERGE only in clean rotational steady state
# (equal-sized cohorts, a full lifecycle elapsed), where replacing ~1/life of the
# fleet per year costs ~lifetime_cost/life per satellite. Off that steady state they
# differ in either direction (a ramped build leaves unequal cohorts, so one year's
# cliff replacement is not 1/life of the fleet: it can be a large cohort or none). The
# annualized basis is the stable economic cost the margins read. The cellular
# record's two revenue cases ride this basis:
#
#   COST-PLUS: revenue = annual cost x revenue_multiple (cost-coupled).
#   ARPU:      revenue = served subscribers x monthly ARPU x 12 (price x served base).
#
# The margin in BOTH cases is (revenue - cost) / revenue, reported as a percent.
# ---------------------------------------------------------------------------


def per_satellite_annual_cost_musd(
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
    (the cost-down is locked in at launch, mirroring the DC per-cohort cost). The one
    annualization: the shared fleet-and-cost loop locks each cohort's cost with it
    (:func:`run_fleet_loop`), and a family prices a fleet the trajectory does not hold
    with it at a chosen year's launch price.

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


def margin_pct(revenue_musd: float, cost_musd: float) -> float | None:
    """A margin as a percent: ``(revenue - cost) / revenue x 100``, or None without revenue.

    The one margin formula, for every family: the cellular family's per-cohort and
    per-year margins, and the Iridium artifact's published ARPU margin (whose cost is
    the built fleet's annualized cost). Mirrors the DC fleet-margin formula. A margin
    is undefined where revenue is not positive (a year with no living fleet, hence no
    revenue), so it is None there, never a number published as if it were a margin:
    each record decides what it shows in its place (the cellular record keeps its
    published :data:`ZERO_MARGIN_PCT`).

    Args:
        revenue_musd: The annual revenue, $M.
        cost_musd: The annual cost (the annualized cost basis), $M.

    Returns:
        The margin in percent, or None when revenue is not positive.
    """
    if revenue_musd <= 0.0:
        return None
    return (revenue_musd - cost_musd) / revenue_musd * MARGIN_PERCENT_SCALE


def _cellular_margin_pct(revenue_musd: float, cost_musd: float) -> float:
    """The cellular family's published margin: :func:`margin_pct`, with
    :data:`ZERO_MARGIN_PCT` where it is None (revenue not positive), so the cellular
    record's values do not move."""
    margin = margin_pct(revenue_musd, cost_musd)
    return margin if margin is not None else ZERO_MARGIN_PCT


# ---------------------------------------------------------------------------
# The shared fleet-and-cost record (frozen, plain numerics) and the deployment rule.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _CohortBuild:
    """One deployed cohort's locked-in cost (engine-internal): the per-cohort lock-in.

    Tracks, per cohort (one per launch year), the satellites deployed and the
    per-satellite ANNUAL cost locked in at launch (built from the deployment-year
    launch cost, so the cadence cost-down is fixed for the cohort's life, mirroring
    the DC per-cohort cost). The cohort-cliff survival reuses the shared
    ``common.cohort.cohort_is_alive_at`` (no separate cliff machinery). This rides
    alongside the shared ``LivedCohort`` list (which carries the living fleet under
    the cliff); the parallel record adds only the per-satellite annual cost the
    ``LivedCohort`` does not carry, from which each year's cohort cost lines
    (:class:`FleetCohortCost`) are drawn.

    Attributes:
        launch_year: The fiscal year this cohort deployed (a unique key: at most one
            cohort per model year, and only deploying years are recorded).
        satellites: The satellites in this cohort (always strictly positive: empty
            years are not recorded).
        per_satellite_annual_cost_musd: The per-satellite annual cost ($M/yr) locked
            in at launch (:func:`per_satellite_annual_cost_musd`).
    """

    launch_year: int
    satellites: int
    per_satellite_annual_cost_musd: float


@dataclass(frozen=True)
class FleetCohortCost:
    """One living cohort's cost line in one year: its satellites at its locked annual cost.

    A cohort is one year's deployment; the cohort cliff retires it whole, so while it
    lives its living satellites are all it deployed. Its per-satellite annual cost is
    locked at its launch year's launch price (:func:`per_satellite_annual_cost_musd`),
    so a later year's cadence cost-down never reprices it.

    Attributes:
        launch_year: The fiscal year the cohort deployed (its identity across the years).
        living_satellites: The cohort's satellites alive this year.
        annual_cost_musd: ``living_satellites`` times the cohort's locked per-satellite
            annual cost, $M/yr.
    """

    launch_year: int
    living_satellites: int
    annual_cost_musd: float


@dataclass(frozen=True)
class FleetYear:
    """One model year of the shared fleet-and-cost record (plain numerics, no cells).

    What every family's fleet shares: the cadence, the deployment its rule chose, the
    living fleet under the cohort cliff, and the cost lines. A family's own lines (a
    target, its served people, its revenue) live in its own record, beside this one.

    Attributes:
        year: The fiscal year (e.g. 2036).
        fleet_launches_this_year: The whole-fleet integer cadence this year (the shared
            logistic ramp). The launch price is priced at this.
        comms_launches_flown_this_year: The comms launches flown this year: the
            satellites the rule deployed over the satellites per launch, a whole count
            at most the cadence share's launches.
        satellites_deployed_this_year: Satellites added this year
            (= ``comms_launches_flown_this_year * satellites_per_launch``).
        living_fleet: Living satellites this year under the service-life cliff, counted
            AFTER this year's cohort is added.
        coverage_fraction: ``living_fleet / coverage_floor``, at most 1.0
            (:data:`FULL_COVERAGE_FRACTION`): can everyone see a satellite.
        launch_cost_per_launch_musd: The per-launch price at the whole-fleet cadence this
            year, $M.
        build_cost_this_year_musd: Satellite hardware build cost this year, $M
            (= ``satellites_deployed_this_year * satellite_build_cost_musd``).
        launch_cost_this_year_musd: Launch cost this year, $M
            (= ``comms_launches_flown_this_year * launch_cost_per_launch_musd``).
        total_cost_this_year_musd: ``build_cost_this_year_musd +
            launch_cost_this_year_musd``, the year's deployment cash.
        satellites_replaced_this_year: The satellites of this year's deployment the rule
            counts as replacing retired satellites (whole launches, at most the year's
            deployment); ``0`` when nothing is replaced.
        replacement_cost_this_year_musd: The cash cost of the replaced satellites, $M:
            their build cost plus their whole launches at this year's per-launch price.
            ``0.0`` in a year that replaces nothing.
        annual_cost_this_year_musd: The ANNUALIZED fleet cost this year, $M/yr: the sum
            of this year's ``cohort_costs``, each living satellite at its cohort's
            locked per-satellite annual cost (lifetime cost spread over the life). NOT
            the deployment cash (``total_cost_this_year_musd``) and NOT the cash
            replacement line: the two conventions converge only in clean rotational
            steady state (equal cohorts, a full lifecycle elapsed); in any other year
            either can be the larger (the cash line replaces whatever cohort retires
            that year, which may be a large cohort or none).
        cohort_costs: One cost line per living cohort, oldest first (empty in a year with
            no living fleet).
    """

    year: int
    fleet_launches_this_year: int
    comms_launches_flown_this_year: int
    satellites_deployed_this_year: int
    living_fleet: int
    coverage_fraction: float
    launch_cost_per_launch_musd: float
    build_cost_this_year_musd: float
    launch_cost_this_year_musd: float
    total_cost_this_year_musd: float
    satellites_replaced_this_year: int
    replacement_cost_this_year_musd: float
    annual_cost_this_year_musd: float
    cohort_costs: tuple[FleetCohortCost, ...]


@dataclass(frozen=True)
class FleetTrajectory:
    """The shared fleet-and-cost record of one run: every model year and the cost totals.

    Attributes:
        years: One :class:`FleetYear` per model year (FY2026..FY2036 at the defaults).
        total_cost_through_final_year_musd: The cumulative deployment cash over the
            trajectory (the sum of every year's ``total_cost_this_year_musd``), $M.
        final_year_replacement_cost_musd: The FINAL model year's cash replacement line, $M
            (``years[-1].replacement_cost_this_year_musd``): cohort-timed and lumpy, the
            cost of replacing what that year's rule counts as replacement, NOT an
            annualized basis. ``None`` when the final year's rule counted no replacement
            (its ``satellites_replaced_this_year`` is 0: no cash replacement basis exists that
            year, so none is published as if it were one).
        final_year_annual_cost_musd: The FINAL model year's ANNUALIZED fleet cost, $M/yr
            (``years[-1].annual_cost_this_year_musd``; ``0.0`` with nothing on orbit).
    """

    years: tuple[FleetYear, ...]
    total_cost_through_final_year_musd: float
    final_year_replacement_cost_musd: float | None
    final_year_annual_cost_musd: float


@dataclass(frozen=True)
class DeploymentStep:
    """What a deployment rule reads for one model year (and all it may read).

    Attributes:
        year: The fiscal year being deployed.
        launches_allowed: The year's comms launches under the cadence share (the
            whole-fleet cadence times ``share_of_fleet``, rounded half up).
        satellites_per_launch: The satellites one launch carries this run.
        living_before: The satellites of prior cohorts still alive this year, before
            this year's launches.
        retiring_this_year: The satellites that aged off the cohort cliff at the start
            of this year (last year's living fleet less ``living_before``).
        years_so_far: The shared records of the years already computed, oldest first
            (empty in the first model year).
    """

    year: int
    launches_allowed: int
    satellites_per_launch: int
    living_before: int
    retiring_this_year: int
    years_so_far: tuple[FleetYear, ...]


@dataclass(frozen=True)
class Deployment:
    """A deployment rule's answer for one model year.

    Attributes:
        satellites_added: The satellites deployed this year: whole launches, at most
            ``launches_allowed x satellites_per_launch``.
        satellites_replaced: The part of them counted as replacing retired satellites:
            whole launches, at most ``satellites_added``.
    """

    satellites_added: int
    satellites_replaced: int


class DeploymentRule(Protocol):
    """A family's deployment rule: how many satellites a year adds and how many replace.

    A rule reads only its :class:`DeploymentStep` and keeps no state between calls, so
    the loop can run it on any trajectory, and twice with one rule gives one record.
    """

    def __call__(self, step: DeploymentStep) -> Deployment:
        """Decide one model year's deployment.

        Args:
            step: The year's cadence allowance, living fleet, retirements and the years
                already computed.

        Returns:
            The satellites the year adds and how many of them count as replacement.
        """
        ...


class DeploymentRuleError(ValueError):
    """A deployment rule returned an impossible deployment: an addition that is not whole
    launches or exceeds the cadence share's launches, or a replacement that is not whole
    launches or exceeds the addition."""


# ---------------------------------------------------------------------------
# The cellular family's record (beside the shared one; plain numerics).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CellularSizing:
    """How the cellular family sized a run's fleet, the input of its rule and its record.

    Attributes:
        fleet_target: The capacity-sized fleet the build fills toward and holds
            (:func:`compute_fleet_target`).
        binding_regime: Which constraint set the target (the coverage floor, the capacity
            need, or the saturation cap).
        subscribers_per_satellite: The per-satellite density that sized the target (people).
        satellites_per_launch: The satellites per launch the run deploys with.
    """

    fleet_target: int
    binding_regime: BindingRegime
    subscribers_per_satellite: int
    satellites_per_launch: int


@dataclass(frozen=True)
class CellularCohortRevenue:
    """The cellular revenue on one living cohort's cost line in one year (both cases).

    The cohort-level mirror of the DC per-cohort economics, read against the cohort's line
    in the shared record (:class:`FleetCohortCost`, its satellites and annualized cost). The
    cost-plus case is cost-coupled (revenue = the cohort's annual cost x the multiple), so
    its margin is the same flat figure for every cohort. The ARPU case allocates the year's
    served subscribers to the cohort by its share of the living fleet, so its revenue and
    margin vary with the cohort's share and the year's served base.

    Attributes:
        launch_year: The cohort's deployment year (its key in the shared record's lines).
        cost_plus_revenue_musd: The cost-plus revenue (the cohort's annual cost x the
            multiple), $M/yr.
        cost_plus_gross_margin_pct: The cost-plus margin, percent (flat across cohorts:
            ``(multiple - 1) / multiple x 100``).
        arpu_subscribers_served: The served subscribers allocated to this cohort this year
            (the year's served base x this cohort's share of the living fleet).
        arpu_revenue_musd: The ARPU revenue (``arpu_subscribers_served x monthly ARPU x
            12``), $M/yr.
        arpu_gross_margin_pct: The ARPU margin, percent.
    """

    launch_year: int
    cost_plus_revenue_musd: float
    cost_plus_gross_margin_pct: float
    arpu_subscribers_served: int
    arpu_revenue_musd: float
    arpu_gross_margin_pct: float


@dataclass(frozen=True)
class CellularYear:
    """One model year of the cellular family's record, beside its :class:`FleetYear`.

    Attributes:
        year: The fiscal year (the key of the shared record's year).
        buildout_fraction: ``living_fleet / fleet_target``, at most 1.0: the fraction of the
            capacity-sized fleet on orbit, which scales the served subscribers.
        is_hold_phase: ``True`` in every year AFTER the year the fleet target was first
            reached (:attr:`CellularTrajectory.full_coverage_reached_year`); the completion
            year itself is the last build-out year (its deployment carries the final build
            tranche).
        subscribers_served_this_year: The served-PERSON count at this year's buildout
            fraction (the subscriber target, or the override, capped at the fleet target's
            people capacity and scaled by ``buildout_fraction``); it drives the year's ARPU
            revenue (the final year's value is the headline ``subscribers_served``).
        cost_plus_revenue_this_year_musd: The COST-PLUS revenue this year, $M (the shared
            record's annualized cost x ``revenue_multiple``).
        cost_plus_gross_margin_pct: The COST-PLUS margin this year, percent (``(revenue -
            cost) / revenue x 100``; flat at the multiple's implied margin once any fleet is
            on orbit; 0.0 with no revenue).
        arpu_revenue_this_year_musd: The PRICES-TODAY ARPU revenue this year, $M
            (``subscribers_served_this_year x arpu_usd_per_month x 12 / 1e6``).
        arpu_gross_margin_pct: The ARPU margin this year, percent, against the annualized
            cost (0.0 with no revenue).
        cohort_revenue: The revenue on each living cohort's cost line, in the shared record's
            order (oldest first; empty with no living fleet).
    """

    year: int
    buildout_fraction: float
    is_hold_phase: bool
    subscribers_served_this_year: int
    cost_plus_revenue_this_year_musd: float
    cost_plus_gross_margin_pct: float
    arpu_revenue_this_year_musd: float
    arpu_gross_margin_pct: float
    cohort_revenue: tuple[CellularCohortRevenue, ...]


@dataclass(frozen=True)
class CellularTrajectory:
    """The cellular family's record of a run: its target, regime, served people and revenue.

    Read beside the run's shared fleet-and-cost record (:class:`FleetTrajectory`), which
    holds the deployment, the living fleet and every cost line; nothing here repeats it.

    Attributes:
        years: One :class:`CellularYear` per model year, in the shared record's order.
        fleet_target: The capacity-sized fleet the build-out fills toward
            (:func:`compute_fleet_target`: the subscriber target divided by the
            per-satellite density, floored by the coverage floor, capped by the saturation
            cap). The cellular rule builds and holds to THIS, not the floor.
        subscribers_per_satellite: The attached-subscribers-per-satellite density that sized
            the fleet.
        binding_regime: Which constraint set the fleet target (the coverage floor, the
            capacity need, or the saturation cap), the investor's coverage-vs-capacity
            answer for this scenario.
        full_coverage_reached_year: The first fiscal year the living fleet reached the
            FLEET TARGET (full deployment, :func:`first_year_at_target`), or ``None`` if it
            is never reached within the horizon (a truthful below-target output, not an
            error).
        subscribers_served: The served-PERSON count at the FINAL year's buildout fraction
            (the final year's ``subscribers_served_this_year``): the capped base when the
            build-out completed, the proportional partial-deployment count when it did not.
        final_year_cash_cost_per_subscriber_usd: The shared record's final-year cash
            replacement per served person, USD; ``None`` when that replacement is ``None``
            or nobody is served. A lumpy cash figure, NOT an annualized cost to serve.
        steady_state_revenue_cost_plus_musd: The steady-state COST-PLUS annual revenue,
            $M/yr (the final year's ``cost_plus_revenue_this_year_musd``).
        steady_state_gross_margin_cost_plus_pct: The steady-state COST-PLUS margin, percent.
        steady_state_revenue_arpu_musd: The steady-state PRICES-TODAY ARPU annual revenue,
            $M/yr (the final year's ``arpu_revenue_this_year_musd``).
        steady_state_gross_margin_arpu_pct: The steady-state ARPU margin, percent; unlike
            the cost-plus margin, it depends on whether the ARPU revenue clears the
            annualized cost at the served base.
        built_fleet_annual_cost_musd: Interim, read only by the Iridium artifact (v5): the
            BUILT fleet's annualized cost, $M/yr, the published ARPU margin's cost basis.
            When the final-year living fleet is at or above the fleet target it equals the
            final year's annualized cost; otherwise it projects the whole-launch built fleet
            (the target rounded up to whole launches) at the final year's per-satellite
            annual cost.
        iridium: Interim: the Iridium entry's v5 physics block (:class:`IridiumResult`) on
            an Iridium run, ``None`` on a cellular run. It never perturbs the fields above.
    """

    years: tuple[CellularYear, ...]
    fleet_target: int
    subscribers_per_satellite: int
    binding_regime: BindingRegime
    full_coverage_reached_year: int | None
    subscribers_served: int
    final_year_cash_cost_per_subscriber_usd: float | None
    steady_state_revenue_cost_plus_musd: float
    steady_state_gross_margin_cost_plus_pct: float
    steady_state_revenue_arpu_musd: float
    steady_state_gross_margin_arpu_pct: float
    built_fleet_annual_cost_musd: float
    iridium: IridiumResult | None


@dataclass(frozen=True)
class CellularRun:
    """A run of the cellular family's rule: the shared fleet-and-cost record and the
    cellular record beside it.

    Attributes:
        fleet: The shared fleet-and-cost record (the deployment, living fleet, cost lines
            and totals).
        cellular: The cellular record (the target, regime, hold, served people and the two
            revenue cases).
    """

    fleet: FleetTrajectory
    cellular: CellularTrajectory


@dataclass(frozen=True)
class IridiumArpuBucket:
    """One billable-connection ARPU revenue bucket (a mix slice of the pool).

    Attributes:
        mix_pct: The bucket's share of the billable-connection pool, percent (the
            investor-set dial; for the standard bucket the reported count is the
            people-identity residual, so the count is not exactly ``mix_pct`` of the
            pool, off only by the premium bucket's rounding).
        price_usd_month: The bucket's monthly price, USD per connection per month (the
            investor-set dial).
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

    Attached to the cellular record's interim :attr:`CellularTrajectory.iridium` by
    the Iridium entry (``config.iridium`` is non-None); ``None`` on a run of the
    High-Bandwidth Cellular Pure Play model. All fields are estimate-tier derived
    quantities. Subscribers are PEOPLE; ``iot_devices`` is a separate DEVICE
    passthrough, never folded into the people count. This is the MSS lane (owned
    L-band, purpose-built or in-chipset devices), NEVER the cellular
    unmodified-phone lane (the High-Bandwidth Cellular Pure Play model). See
    :attr:`ecosystem_assumption`.

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
    premium_count = round_half_up(
        total_connections_float * dials.premium_mix_pct / ARPU_MIX_TOTAL_PCT
    )
    standard_count = people_capacity - premium_count
    iot_count = round_half_up(total_connections_float * dials.iot_mix_pct / ARPU_MIX_TOTAL_PCT)
    government_count = round_half_up(
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
        total_connections=round_half_up(total_connections_float),
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
    satellites-per-launch (both passed in, already computed once by the Iridium entry,
    ``communications.iridium.run_iridium_model``, so the density that sized the fleet
    and the density reported here cannot drift). The operations cost and the
    ecosystem assumption are the stated Iridium-model constants
    (:data:`IRIDIUM_OPERATIONS_COST_MUSD`, :data:`ECOSYSTEM_ASSUMPTION_NOTE`). When
    the dials carry an ``arpu`` block, the four-bucket revenue case is derived here
    at the built fleet's people capacity (``fleet_target x subscribers_per_satellite``,
    :func:`derive_arpu_buckets`) and attached; it is ``None`` otherwise.

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
    the built-fleet convention (revenue and the margin's cost basis both at the built
    fleet), and the margin definition (how the published margin is measured).
    Consumed both by :func:`iridium_assumptions` (spliced into the full assumptions
    tuple) and by the promoted artifact's ``revenue_arpu_buckets`` block, so the two
    never drift.

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
            "Clearly optimistic, stated, investor-owned."
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
            "Built-fleet convention: the revenue case and its margin's cost basis are "
            "both computed at the built fleet (fleet_target), so on a scenario that "
            "does not complete its build inside the horizon (the trajectory summary's "
            "build_completes_in_horizon is false) the case describes the completed "
            "fleet, not the final horizon year's smaller actual fleet."
        ),
        (
            "Margin definition: the published ARPU margin measures revenue against the "
            "built fleet's full build, launch, and replacement cost, annualized over "
            "the satellite life (built_fleet_annual_cost_musd). Operations cost is the "
            "explicit zero pending research and corporate overhead is never included, "
            "so it is an operating-style margin (the data-center model's convention), "
            "not a gross margin and not a net margin."
        ),
    )


def iridium_assumptions(dials: IridiumDials) -> tuple[str, ...]:
    """Return the Iridium model's stated-assumptions lines (the assumptions output).

    Takes the dials because one line is conditional on them (the aperture fold
    caveat, 0.8a). Always states: the ecosystem assumption
    (:data:`ECOSYSTEM_ASSUMPTION_NOTE`, 0.8); that operations cost is assumed zero
    (:data:`IRIDIUM_OPERATIONS_COST_MUSD`, an explicit investor-instructed assumption,
    a fixed line to research and add later); the estimate tiers (the
    spectral-efficiency bands, the reuse calibration, the aperture reference and its
    linear conservative scaling, the concurrency pair, the active rate) as
    estimate-tier, investor-owned values; and that the Iridium model is the MSS lane
    (owned L-band, purpose-built or in-chipset devices), never the cellular
    unmodified-phone lane. The revenue-case line is conditional on ``dials.arpu``: with
    the four-bucket ARPU case set it states the PUBLISHED case (the Iridium model's
    only published revenue case) plus the full sell-through assumption, the honest mix
    posture, the built-fleet convention, and the IoT-count supersession; with no
    ``arpu`` block it states the DEFERRED case (no revenue case is published on that
    path; the per-tier MSS ARPUs plug in via the ARPU block). The synthetic cost-plus
    line is off every Iridium-facing surface as of iridium-v3 (investor direction
    2026-07-10); it stays the cellular family's shared-engine convention on the
    trajectory. Conditionally
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
            "millions per year): an explicit investor-instructed assumption, a fixed "
            "operations line to research and add later, stated here rather than "
            "silently omitted."
        ),
        (
            "Spectral efficiency is estimate-tier and investor-owned: the phone-class "
            f"band is {PHONE_CLASS_SE_LOW} to {PHONE_CLASS_SE_HIGH}, the "
            f"small-terminal-class band {SMALL_TERMINAL_CLASS_SE_LOW} to "
            f"{SMALL_TERMINAL_CLASS_SE_HIGH}, the large-terminal-class band "
            f"{MOUNTED_TERMINAL_CLASS_SE_LOW} to {MOUNTED_TERMINAL_CLASS_SE_HIGH} bps/Hz (class "
            f"centrals {PHONE_CLASS_SE_CENTRAL} / {SMALL_TERMINAL_CLASS_SE_CENTRAL} / "
            f"{MOUNTED_TERMINAL_CLASS_SE_CENTRAL})."
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
            f"({dials.active_user_rate_mbps} Mbps) are estimate-tier, investor-owned "
            "values."
        ),
    ]
    if dials.arpu is not None:
        lines.append(
            "The prices-today ARPU revenue case is PUBLISHED for the Iridium model as "
            "the four-bucket case (standard personal, premium terminal, IoT devices, "
            "government): an investor-set price-and-mix sheet dated 2026-07-09. It is the "
            "Iridium model's only published revenue case."
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
            "The prices-today ARPU revenue case is DEFERRED for the Iridium model on "
            "this no-ARPU configuration: the four-bucket ARPU case is the Iridium "
            "model's published revenue when its block is set, so on this configuration "
            "the Iridium model publishes no revenue case, and the per-tier MSS ARPUs "
            "plug in via the ARPU block."
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
        count (:func:`_comms_launch_count`: ``fleet_launches * share_of_fleet``
        rounded half up with the representation-error tolerance), and the
        per-launch cost in $M priced at the whole-fleet cadence.
    """
    cad = config.cadence
    fleet_launches = as_int(
        compute_launches_per_year(
            year_idx,
            cadence_ceiling=cad.cadence_ceiling,
            launches_at_year_5=cad.launches_at_year_5,
            launches_at_year_10=cad.launches_at_year_10,
            first_launch_year=cad.first_launch_year,
        )
    )
    comms_launches = _comms_launch_count(fleet_launches, config.comms_cadence.share_of_fleet)
    lc = config.launch_cost
    launch_cost_per_launch_musd = as_float(
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
# The shared fleet-and-cost loop: one loop under a family's deployment rule.
# ---------------------------------------------------------------------------


def _is_whole_launches(count: int, satellites_per_launch: int) -> bool:
    """Whether a satellite count is whole launches: an integer of zero or more, a multiple
    of the satellites per launch (a bool or a float is not a count)."""
    return (
        isinstance(count, int)
        and not isinstance(count, bool)
        and count >= 0
        and count % satellites_per_launch == 0
    )


def _check_deployment(step: DeploymentStep, deployment: Deployment) -> None:
    """Refuse a deployment no year can fly: the loop's check of its rule.

    A year adds whole launches, at most the launches the cadence share allows it, and
    counts whole launches of that addition, at most all of it, as replacement. The
    checks run in that order, so each refusal names the first condition broken.

    Args:
        step: The year's step, as the rule read it.
        deployment: What the rule returned for it.

    Raises:
        DeploymentRuleError: If the deployment breaks a condition, naming the year, the
            count and the bound.
    """
    per_launch = step.satellites_per_launch
    added = deployment.satellites_added
    replaced = deployment.satellites_replaced
    deployment_in_year = f"the deployment rule's deployment in {step.year}"
    whole_launches = (
        f"where a count is an integer of zero or more and a multiple of {per_launch}, the "
        "satellites per launch"
    )
    if not _is_whole_launches(added, per_launch):
        raise DeploymentRuleError(
            f"{deployment_in_year} does not add whole launches: satellites added {added!r}, "
            f"{whole_launches}"
        )
    allowed = step.launches_allowed * per_launch
    if added > allowed:
        raise DeploymentRuleError(
            f"{deployment_in_year} adds more than the cadence share allows: satellites added "
            f"{added}, at most {allowed} (launches allowed {step.launches_allowed}, "
            f"satellites per launch {per_launch})"
        )
    if not _is_whole_launches(replaced, per_launch):
        raise DeploymentRuleError(
            f"{deployment_in_year} does not replace whole launches: satellites replaced "
            f"{replaced!r}, {whole_launches}"
        )
    if replaced > added:
        raise DeploymentRuleError(
            f"{deployment_in_year} replaces more than it adds: satellites replaced "
            f"{replaced}, satellites added {added}"
        )


def run_fleet_loop(
    config: CommsConfig, rule: DeploymentRule, *, satellites_per_launch: int
) -> FleetTrajectory:
    """Run the shared fleet-and-cost loop over the horizon under a deployment rule.

    The loop every family's fleet runs on; it holds no family branch. For each model year
    (``base_year`` to ``base_year + horizon_years``), in order:

    1. Price the cadence (:func:`_comms_launches_for_year`): the whole-fleet launches,
       the comms launches the share allows, and the per-launch price at the whole-fleet
       cadence.
    2. Under the shared cohort cliff, the living fleet of prior cohorts this year
       (``living_before``) and the satellites that aged off at the start of the year
       (last year's living fleet less ``living_before``).
    3. Ask the rule for the year's deployment (a :class:`DeploymentStep` in, a
       :class:`Deployment` out) and check it (:func:`_check_deployment`).
    4. Append the cohort; the living fleet after it and the coverage fraction against
       the coverage floor.
    5. The cost lines: build, launch (the launches flown, the deployment's whole
       launches, at the year's price) and their total; the replacement line (the
       replaced satellites' build cost plus their whole launches at the year's price).
    6. Lock a new cohort's per-satellite annual cost at this year's launch price
       (:func:`per_satellite_annual_cost_musd`; a year that deploys nothing adds no
       cohort line), then one cost line per living cohort and their sum, the
       annualized fleet cost.

    The trajectory's totals follow: the cumulative deployment cash, the final year's
    cash replacement (None when it replaced nothing), and the final year's annualized
    cost.

    Args:
        config: The comms config (the cadence, comms-cadence, launch-cost, satellite,
            coverage and metadata blocks).
        rule: The family's deployment rule; it reads only its step and keeps no state.
        satellites_per_launch: The satellites one launch carries this run (at least
            :data:`MIN_SATELLITES_PER_LAUNCH`).

    Returns:
        The :class:`FleetTrajectory`: one :class:`FleetYear` per model year and the
        trajectory's cost totals.

    Raises:
        ValueError: If ``satellites_per_launch`` is not an integer (a bool or a float is
            not one) or is below :data:`MIN_SATELLITES_PER_LAUNCH`.
        DeploymentRuleError: If the rule returns an impossible deployment for a year.
    """
    if (
        not isinstance(satellites_per_launch, int)
        or isinstance(satellites_per_launch, bool)
        or satellites_per_launch < MIN_SATELLITES_PER_LAUNCH
    ):
        raise ValueError(
            f"the fleet loop deploys whole launches, so satellites_per_launch must be an "
            f"integer of at least {MIN_SATELLITES_PER_LAUNCH}; got {satellites_per_launch!r}"
        )
    life = config.satellite.satellite_lifetime_years
    coverage_floor = config.coverage.satellites_for_full_coverage
    build_cost_musd = config.satellite.satellite_build_cost_musd
    # The shared cliff runs on the LivedCohort list (every year's cohort, empty ones
    # included); the lock-in rides beside it on the deploying cohorts only.
    cohorts: list[LivedCohort] = []
    cohort_builds: list[_CohortBuild] = []
    years: list[FleetYear] = []

    for year_idx in range(config.metadata.horizon_years + 1):
        fy = config.metadata.base_year + year_idx
        fleet_launches, comms_launches, launch_cost_per_launch_musd = _comms_launches_for_year(
            year_idx, config
        )
        # The prior cohorts alive at the end of last year and still alive this year; the
        # difference is the satellites that aged off the cliff at the start of this year.
        living_prior_year = sum(c.units_deployed for c in living_cohorts(cohorts, fy - 1, life))
        living_before = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))
        step = DeploymentStep(
            year=fy,
            launches_allowed=comms_launches,
            satellites_per_launch=satellites_per_launch,
            living_before=living_before,
            retiring_this_year=living_prior_year - living_before,
            years_so_far=tuple(years),
        )
        deployment = rule(step)
        _check_deployment(step, deployment)
        satellites_added = deployment.satellites_added
        satellites_replaced = deployment.satellites_replaced
        # The launches flown is the deployment's whole-launch count; the cadence share
        # may have allowed more than the rule used, and only the flown launches are costed.
        comms_launches_flown = satellites_added // satellites_per_launch

        cohorts.append(LivedCohort(launch_year=fy, units_deployed=satellites_added))
        living_after = sum(c.units_deployed for c in living_cohorts(cohorts, fy, life))
        coverage_fraction = min(FULL_COVERAGE_FRACTION, living_after / coverage_floor)

        build_cost_this_year_musd = satellites_added * build_cost_musd
        launch_cost_this_year_musd = comms_launches_flown * launch_cost_per_launch_musd
        total_cost_this_year_musd = build_cost_this_year_musd + launch_cost_this_year_musd
        # The replaced satellites are whole launches (the check), so their launches divide
        # exactly; their line is their build cost plus those launches at this year's price.
        replacement_launches = satellites_replaced // satellites_per_launch
        replacement_cost_this_year_musd = (
            satellites_replaced * build_cost_musd
            + replacement_launches * launch_cost_per_launch_musd
        )

        # Lock this year's cohort's per-satellite annual cost at this year's launch price,
        # so the cadence cost-down is fixed for its life. Only a cohort that deploys is
        # recorded (an empty one would carry no satellites, no cost and no line).
        if satellites_added > 0:
            cohort_builds.append(
                _CohortBuild(
                    launch_year=fy,
                    satellites=satellites_added,
                    per_satellite_annual_cost_musd=per_satellite_annual_cost_musd(
                        satellite_build_cost_musd=build_cost_musd,
                        launch_cost_per_launch_musd=launch_cost_per_launch_musd,
                        satellites_per_launch=satellites_per_launch,
                        satellite_lifetime_years=life,
                    ),
                )
            )
        # One cost line per living cohort, oldest first; their sum is the annualized
        # fleet cost (the margin's cost basis), not the deployment cash.
        cohort_costs = tuple(
            FleetCohortCost(
                launch_year=build.launch_year,
                living_satellites=build.satellites,
                annual_cost_musd=build.satellites * build.per_satellite_annual_cost_musd,
            )
            for build in cohort_builds
            if cohort_is_alive_at(build.launch_year, fy, life)
        )
        annual_cost_this_year_musd = sum(
            (line.annual_cost_musd for line in cohort_costs), NO_ANNUAL_COST_MUSD
        )

        years.append(
            FleetYear(
                year=fy,
                fleet_launches_this_year=fleet_launches,
                comms_launches_flown_this_year=comms_launches_flown,
                satellites_deployed_this_year=satellites_added,
                living_fleet=living_after,
                coverage_fraction=coverage_fraction,
                launch_cost_per_launch_musd=launch_cost_per_launch_musd,
                build_cost_this_year_musd=build_cost_this_year_musd,
                launch_cost_this_year_musd=launch_cost_this_year_musd,
                total_cost_this_year_musd=total_cost_this_year_musd,
                satellites_replaced_this_year=satellites_replaced,
                replacement_cost_this_year_musd=replacement_cost_this_year_musd,
                annual_cost_this_year_musd=annual_cost_this_year_musd,
                cohort_costs=cohort_costs,
            )
        )

    # The horizon is at least MIN_HORIZON_YEARS (a config bound), so the loop above
    # always yields the base year plus at least one more; the final year exists.
    final_year = years[-1]
    return FleetTrajectory(
        years=tuple(years),
        total_cost_through_final_year_musd=sum(y.total_cost_this_year_musd for y in years),
        final_year_replacement_cost_musd=(
            final_year.replacement_cost_this_year_musd
            if final_year.satellites_replaced_this_year > 0
            else None
        ),
        final_year_annual_cost_musd=final_year.annual_cost_this_year_musd,
    )


# ---------------------------------------------------------------------------
# The cellular family: its deployment rule (target and hold) and its record.
# ---------------------------------------------------------------------------


def first_year_at_target(years: Sequence[FleetYear], fleet_target: int) -> int | None:
    """The first year whose living fleet reached the fleet target: the cellular hold, defined once.

    The cellular rule holds in a year when this is not None over the years before it, and
    the cellular record reads its hold flag and its completion year the same way, so the
    hold has one definition.

    Args:
        years: Shared records of consecutive model years, oldest first.
        fleet_target: The cellular fleet target.

    Returns:
        The fiscal year of the first record whose living fleet is at or above the target,
        or None if none is.
    """
    return next((year.year for year in years if year.living_fleet >= fleet_target), None)


def cellular_rule(fleet_target: int) -> DeploymentRule:
    """The cellular family's deployment rule: build to the fleet target, then hold it.

    THE OVERSHOOT RULE. Launches are granular (a whole launch deploys its satellites at
    once), so the last build-out launch may push the living fleet slightly OVER the target.
    In every year, build-out and hold alike, the rule adds the deficit to the target
    (``fleet_target - living_before``, at least 0) rounded UP to whole launches
    (:func:`_ceil_to_launch`), capped by the cadence share's launches. The final build
    cohort may overshoot by strictly less than one launch's worth, and the rule never
    deploys beyond what holding needs: in hold the deficit is that year's cliff losses less
    any overshoot still on orbit, so it replaces only the ageing cohorts.

    THE REPLACEMENT SPLIT. Only the replacement of retiring cohorts counts as replacement,
    never a build tranche. Up to and including the year the target is first reached, the
    replacement is the part of the addition that matches the year's retirements
    (``min(added, retiring)``, both whole launches); the rest is build. Once the target is
    held (it was reached in an EARLIER year, :func:`first_year_at_target` over the years
    already computed), every addition restores retired satellites and counts as
    replacement.

    The rule reads only its step (the hold from ``step.years_so_far``) and keeps no state
    between calls.

    Args:
        fleet_target: The cellular fleet target (:func:`compute_fleet_target`).

    Returns:
        The :class:`DeploymentRule` for that target.
    """

    def build_and_hold(step: DeploymentStep) -> Deployment:
        """Deploy one year toward the fleet target, and split its replacement by the hold."""
        would_be_deployed = step.launches_allowed * step.satellites_per_launch
        deficit = max(0, fleet_target - step.living_before)
        satellites_added = min(
            would_be_deployed, _ceil_to_launch(deficit, step.satellites_per_launch)
        )
        holding = first_year_at_target(step.years_so_far, fleet_target) is not None
        satellites_replaced = (
            satellites_added if holding else min(satellites_added, step.retiring_this_year)
        )
        return Deployment(
            satellites_added=satellites_added, satellites_replaced=satellites_replaced
        )

    return build_and_hold


def _cellular_cohort_revenue(
    fleet_year: FleetYear,
    *,
    subscribers_served_this_year: int,
    revenue_multiple: float,
    arpu_usd_per_month: float,
) -> tuple[CellularCohortRevenue, ...]:
    """The cellular revenue on each living cohort's cost line for one year (both cases).

    For each of the year's cohort cost lines (oldest first), the cost-plus revenue (the
    line's annualized cost x the multiple) and the ARPU revenue on the served subscribers
    allocated to the cohort by its share of the living fleet (a cohort with more living
    satellites serves proportionally more of the base), each with its margin. The last
    living cohort absorbs any rounding remainder, so the per-cohort served counts sum
    exactly to the year's served total (no drift versus the year's ARPU line).

    Args:
        fleet_year: The year's shared record (its cohort cost lines and living fleet).
        subscribers_served_this_year: The year's served-PERSON count (the ARPU base).
        revenue_multiple: The cost-plus multiple.
        arpu_usd_per_month: The monthly ARPU.

    Returns:
        One :class:`CellularCohortRevenue` per cohort cost line, in its order.
    """
    lines: list[CellularCohortRevenue] = []
    subscribers_allocated = 0
    last_index = len(fleet_year.cohort_costs) - 1
    for idx, cost in enumerate(fleet_year.cohort_costs):
        cost_plus_revenue_musd = cost.annual_cost_musd * revenue_multiple
        # Allocate the year's served subscribers by the cohort's living-satellite share;
        # the last living cohort takes the remainder so the parts sum exactly.
        if idx == last_index:
            cohort_subscribers = subscribers_served_this_year - subscribers_allocated
        else:
            # A cohort line exists only for a living cohort with satellites, so the living
            # fleet that sums the same window is never 0 here.
            cohort_subscribers = round(
                subscribers_served_this_year * cost.living_satellites / fleet_year.living_fleet
            )
        subscribers_allocated += cohort_subscribers
        arpu_revenue_musd = cohort_subscribers * arpu_usd_per_month * MONTHS_PER_YEAR / MUSD_TO_USD
        lines.append(
            CellularCohortRevenue(
                launch_year=cost.launch_year,
                cost_plus_revenue_musd=cost_plus_revenue_musd,
                cost_plus_gross_margin_pct=_cellular_margin_pct(
                    cost_plus_revenue_musd, cost.annual_cost_musd
                ),
                arpu_subscribers_served=cohort_subscribers,
                arpu_revenue_musd=arpu_revenue_musd,
                arpu_gross_margin_pct=_cellular_margin_pct(
                    arpu_revenue_musd, cost.annual_cost_musd
                ),
            )
        )
    return tuple(lines)


def _built_fleet_annual_cost_musd(
    config: CommsConfig,
    *,
    final_year: FleetYear,
    fleet_target: int,
    satellites_per_launch: int,
) -> float:
    """The built fleet's annualized cost: the Iridium artifact's ARPU margin's cost basis, $M/yr.

    Interim: the cellular record carries it only for the Iridium v5 artifact. A revenue
    case computed at the fleet target needs a cost for the same fleet. When the
    final-year living fleet is at or above the fleet target, the built fleet is on
    orbit, so this is that year's annualized fleet cost (each cohort at its own
    locked-in launch price). Otherwise (a build that does not complete inside the
    horizon, or a hold that fell short) it projects the whole-launch built fleet (the
    fleet target rounded up to whole launches, exactly the fleet the overshoot rule
    builds) at the final year's per-satellite annual cost.

    Args:
        config: The comms config (the build cost and the satellite life).
        final_year: The final model year's shared record (its living fleet, annualized
            cost, and per-launch price).
        fleet_target: The capacity-sized fleet target.
        satellites_per_launch: The satellites per launch this run deployed with.

    Returns:
        The built fleet's annualized cost, $M/yr.
    """
    if final_year.living_fleet >= fleet_target:
        return final_year.annual_cost_this_year_musd
    built_fleet_satellites = _ceil_to_launch(fleet_target, satellites_per_launch)
    final_year_cost_per_satellite_musd = per_satellite_annual_cost_musd(
        satellite_build_cost_musd=config.satellite.satellite_build_cost_musd,
        launch_cost_per_launch_musd=final_year.launch_cost_per_launch_musd,
        satellites_per_launch=satellites_per_launch,
        satellite_lifetime_years=config.satellite.satellite_lifetime_years,
    )
    return built_fleet_satellites * final_year_cost_per_satellite_musd


def build_cellular_record(
    config: CommsConfig,
    fleet: FleetTrajectory,
    sizing: CellularSizing,
    *,
    iridium: IridiumResult | None,
) -> CellularTrajectory:
    """Build the cellular family's record of a run on its shared fleet-and-cost record.

    Per year: the hold flag (the target reached in an earlier year,
    :func:`first_year_at_target` over the years before it, the rule's own test), the
    buildout fraction (the living fleet over the target, at most 1.0), the served people at
    it (:func:`subscribers_served_at`, the subscriber target or the override capped at the
    target's people capacity), and the two revenue cases on the year's annualized cost
    (COST-PLUS: the cost x ``revenue_multiple``; ARPU: the served people x
    ``arpu_usd_per_month`` x 12), each with its margin (:data:`ZERO_MARGIN_PCT` where there
    is no revenue), with the revenue on each cohort cost line. Then the headlines: the
    completion year, the final year's served people and its cash cost per person (the
    shared final-year replacement over them, :func:`usd_per_person`), the steady-state
    revenue and margins (the final year's), and the interim built-fleet cost.

    It logs a WARNING when a served override exceeds the target's people capacity (the
    served count is capped there; the fleet is sized from the target, not the override)
    and when the build never reaches the target inside the horizon (a truthful
    below-target output, not an error).

    Args:
        config: The comms config (the subscriber, revenue, satellite and comms-cadence
            blocks).
        fleet: The run's shared fleet-and-cost record, deployed under
            :func:`cellular_rule` for ``sizing.fleet_target``.
        sizing: How the fleet was sized (the target, its regime, the density, the
            satellites per launch).
        iridium: Interim: the Iridium entry's v5 physics block, or None on a cellular run.

    Returns:
        The :class:`CellularTrajectory`.
    """
    subscriber_target = config.subscribers.subscribers_at_full_coverage
    served_override = config.subscribers.subscribers_served_override
    fleet_target = sizing.fleet_target
    # The most people the fleet target can carry: the ceiling on the served base.
    people_capacity = fleet_target * sizing.subscribers_per_satellite
    if served_override is not None and served_override > people_capacity:
        logger.warning(
            "subscribers_served_override (%d) exceeds the fleet target's people capacity "
            "(%d = %d satellites x %d per satellite); the served count is capped at the "
            "capacity (the fleet is sized from the subscriber target, not the override).",
            served_override,
            people_capacity,
            fleet_target,
            sizing.subscribers_per_satellite,
        )
    revenue_multiple = config.revenue.revenue_multiple
    arpu_usd_per_month = config.revenue.arpu_usd_per_month

    years: list[CellularYear] = []
    for index, fleet_year in enumerate(fleet.years):
        annual_cost_musd = fleet_year.annual_cost_this_year_musd
        buildout_fraction = min(FULL_BUILDOUT_FRACTION, fleet_year.living_fleet / fleet_target)
        subscribers_served_this_year = subscribers_served_at(
            buildout_fraction,
            subscriber_target=subscriber_target,
            override=served_override,
            people_capacity=people_capacity,
        )
        # Case 1, COST-PLUS: revenue = annual cost x the multiple (cost-coupled).
        cost_plus_revenue_musd = annual_cost_musd * revenue_multiple
        # Case 2, ARPU: revenue = served base x monthly ARPU x 12 (price x served base).
        arpu_revenue_musd = (
            subscribers_served_this_year * arpu_usd_per_month * MONTHS_PER_YEAR / MUSD_TO_USD
        )
        years.append(
            CellularYear(
                year=fleet_year.year,
                buildout_fraction=buildout_fraction,
                is_hold_phase=first_year_at_target(fleet.years[:index], fleet_target) is not None,
                subscribers_served_this_year=subscribers_served_this_year,
                cost_plus_revenue_this_year_musd=cost_plus_revenue_musd,
                cost_plus_gross_margin_pct=_cellular_margin_pct(
                    cost_plus_revenue_musd, annual_cost_musd
                ),
                arpu_revenue_this_year_musd=arpu_revenue_musd,
                arpu_gross_margin_pct=_cellular_margin_pct(arpu_revenue_musd, annual_cost_musd),
                cohort_revenue=_cellular_cohort_revenue(
                    fleet_year,
                    subscribers_served_this_year=subscribers_served_this_year,
                    revenue_multiple=revenue_multiple,
                    arpu_usd_per_month=arpu_usd_per_month,
                ),
            )
        )

    final_fleet_year = fleet.years[-1]
    final_year = years[-1]
    full_coverage_reached_year = first_year_at_target(fleet.years, fleet_target)
    if full_coverage_reached_year is None:
        logger.warning(
            "Comms build-out did not reach the fleet target (%d satellites, %s regime) within "
            "the %d-year horizon at share_of_fleet=%.3f; living fleet at FY%d is %d. This is a "
            "truthful below-target output, not an error.",
            fleet_target,
            sizing.binding_regime.value,
            config.metadata.horizon_years,
            config.comms_cadence.share_of_fleet,
            final_fleet_year.year,
            final_fleet_year.living_fleet,
        )
    return CellularTrajectory(
        years=tuple(years),
        fleet_target=fleet_target,
        subscribers_per_satellite=sizing.subscribers_per_satellite,
        binding_regime=sizing.binding_regime,
        full_coverage_reached_year=full_coverage_reached_year,
        subscribers_served=final_year.subscribers_served_this_year,
        final_year_cash_cost_per_subscriber_usd=usd_per_person(
            fleet.final_year_replacement_cost_musd, final_year.subscribers_served_this_year
        ),
        steady_state_revenue_cost_plus_musd=final_year.cost_plus_revenue_this_year_musd,
        steady_state_gross_margin_cost_plus_pct=final_year.cost_plus_gross_margin_pct,
        steady_state_revenue_arpu_musd=final_year.arpu_revenue_this_year_musd,
        steady_state_gross_margin_arpu_pct=final_year.arpu_gross_margin_pct,
        built_fleet_annual_cost_musd=_built_fleet_annual_cost_musd(
            config,
            final_year=final_fleet_year,
            fleet_target=fleet_target,
            satellites_per_launch=sizing.satellites_per_launch,
        ),
        iridium=iridium,
    )


# ---------------------------------------------------------------------------
# The cellular entry.
# ---------------------------------------------------------------------------

_NOT_A_CELLULAR_CONFIG: Final[str] = (
    "the config selects the Iridium model (it has an 'iridium:' block), which the cellular "
    "entry does not run: run it through the Iridium entry, "
    "communications.iridium.run_iridium_model(config, curve), on its saturation curve"
)
"""The cellular entry's refusal of an Iridium config, naming the Iridium entry."""


class NotACellularConfigError(ValueError):
    """A config of the Iridium family (one with an ``iridium:`` block) handed to the cellular
    entry, :func:`run_comms_model`."""


def run_comms_model(config: CommsConfig) -> CellularRun:
    """The cellular entry: run a High-Bandwidth Cellular Pure Play config.

    A config with an ``iridium:`` block belongs to the Iridium family, whose entry is
    ``communications.iridium.run_iridium_model(config, curve)`` (it checks its saturation
    curve against the config before it runs); this entry refuses it, so through the two
    entries no Iridium config runs without its curve. Any other config is sized from its
    dials (:func:`compute_fleet_target`: the subscriber target over the fixed per-satellite
    density, floored by the coverage floor, capped by the saturation cap), deployed on the
    shared fleet-and-cost loop (:func:`run_fleet_loop`) under the cellular rule
    (:func:`cellular_rule`: build to the target, then hold it, replacing each retiring
    cohort), at the configured satellites per launch, and recorded by
    :func:`build_cellular_record`. The launch cost is priced at the WHOLE-fleet Neutron
    cadence; the comms share sets only how many launches the fleet flies. A target the
    cadence share cannot reach within the horizon still runs, reported truthfully (no
    completion year, a WARNING).

    Args:
        config: The comms config (the frozen Pydantic tree). The all-defaults config
            reproduces the High-Bandwidth Cellular Pure Play central case.

    Returns:
        The :class:`CellularRun`: the shared fleet-and-cost record and the cellular record.

    Raises:
        NotACellularConfigError: If the config has an ``iridium:`` block, naming the Iridium
            entry.
    """
    if config.iridium is not None:
        raise NotACellularConfigError(_NOT_A_CELLULAR_CONFIG)
    subscribers_per_satellite = config.subscribers.subscribers_per_satellite
    satellites_per_launch = config.satellite.satellites_per_launch
    fleet_target, binding_regime = compute_fleet_target(
        subscriber_target=config.subscribers.subscribers_at_full_coverage,
        subscribers_per_satellite=subscribers_per_satellite,
        coverage_floor=config.coverage.satellites_for_full_coverage,
        max_fleet_satellites=config.coverage.max_fleet_satellites,
    )
    sizing = CellularSizing(
        fleet_target=fleet_target,
        binding_regime=binding_regime,
        subscribers_per_satellite=subscribers_per_satellite,
        satellites_per_launch=satellites_per_launch,
    )
    fleet = run_fleet_loop(
        config, cellular_rule(fleet_target), satellites_per_launch=satellites_per_launch
    )
    return CellularRun(
        fleet=fleet, cellular=build_cellular_record(config, fleet, sizing, iridium=None)
    )


__all__ = [
    "CellularCohortRevenue",
    "CellularRun",
    "CellularSizing",
    "CellularTrajectory",
    "CellularYear",
    "Deployment",
    "DeploymentRule",
    "DeploymentRuleError",
    "DeploymentStep",
    "FleetCohortCost",
    "FleetTrajectory",
    "FleetYear",
    "IridiumArpuBucket",
    "IridiumArpuResult",
    "IridiumResult",
    "NotACellularConfigError",
    "arpu_stated_assumptions",
    "build_cellular_record",
    "build_iridium_result",
    "cellular_rule",
    "compute_fleet_target",
    "derive_arpu_buckets",
    "derive_iridium_per_user_rates",
    "derive_iridium_satellites_per_launch",
    "derive_iridium_subscribers_per_satellite",
    "derive_per_satellite_capacity_gbps",
    "first_year_at_target",
    "iridium_assumptions",
    "margin_pct",
    "per_satellite_annual_cost_musd",
    "resolve_device_spectral_efficiency",
    "run_comms_model",
    "run_fleet_loop",
    "subscribers_served_at",
    "usd_per_person",
]
