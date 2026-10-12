"""The Iridium family: its entry, its full-cadence rule, its record and its economics.

A communications config of the Iridium family carries a top-level ``iridium:`` block; one of
the High-Bandwidth Cellular Pure Play family does not. Each way into the Iridium family (the
two commands and the Iridium entry) starts by narrowing its config with
:func:`iridium_dials_of`, which returns the Iridium dials or refuses a config of the other
family with :class:`NotAnIridiumConfigError`, so one condition and one error guard each of
them: the saturation command (``python -m communications.saturation``) calls it before it
reads the dials the curve depends on, the Iridium promotion command
(``python -m communications.json_output``) before it loads the curve, and the Iridium entry
before anything else. It also re-validates the config whole, so a config built with
``model_copy`` (which pydantic does not validate) cannot carry a setting past the validators
into a run (a ``pydantic.ValidationError`` naming the field). The refusal of the other
family's config gives the Iridium promotion command's message.

The Iridium entry, :func:`run_iridium_model`, takes the config and its saturation curve, both
required, so the curve's presence is a type fact. On every run it narrows the config, checks
that the curve was computed for the config's own inputs (the identity check,
:func:`communications.saturation_curve.check_curve_matches`), and only then runs:

1. **The fleet**: the shared fleet-and-cost loop
   (:func:`communications.engine.run_fleet_loop`) under :func:`full_cadence_rule`, which flies
   every comms launch the cadence share allows at the scenario's satellites per launch and
   counts as replacement only what matches the year's retirements. There is no fleet target,
   no hold and no cap: no saturation number sizes, caps, stops or slows the build.
2. **The years**: in every year whose living fleet is at or above the coverage floor
   (pinned at 340 on the Iridium path), each device class serves every person its living fleet
   carries (the curve's people, read at the downlink share d and the panel factor, rounded half
   up) at its own flat price, and the two IoT lines earn their fixed books; below the floor
   nothing is sold. Each class's own margin is its own revenue against the year's whole-fleet
   annualized cost, null with no revenue; the IoT lines are never inside it. The years are
   read before anything else, so a year's fleet past a class's last computed row raises
   :class:`~communications.saturation_curve.CurveBeyondLastRowError` naming that year.
3. **The readings**: every class at four reported fleets (the coverage floor; 2,000, the
   retired cap, kept for comparison; the horizon-end full-cadence reach; the steady state
   beyond the horizon), each priced by its reading cost, and the IoT check at each.
4. **Each class's block**: its price, usage and physics (the satellite's peak at the
   panel, the downlink pool and the per-user rates), its markers from the curve, the limit
   that binds at the horizon's end, and its marginal intervals on the curve's own rows.
5. **The record**, :class:`IridiumRecord`: everything the ``iridium-v6`` artifact publishes
   beside the shared fleet-and-cost record, with the stated assumptions, so the artifact
   builder reads no dial and holds no Optional check.

Every list of classes runs small terminal, mounted terminal, phone class (the order of
:class:`~communications.constants.DeviceClass`), never phone-first. No quantity that does not
exist is published as a number: a margin with no revenue, U at a fleet of 0, a marker not
reached and an IoT share below the floor are None, and nothing divides by zero. A run whose
records would hold an infinity or a NaN (a setting past what the model can compute) is
refused as the entry's last step, naming the first such field and the settings behind it, so
a run the entry returns holds only finite numbers.

numpy-free, like every communications module but the saturation module (ADR 010).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final, assert_never

from common.cadence import round_half_up
from communications.config import CommsConfig, IridiumArpuDials, IridiumDials
from communications.constants import (
    APERTURE_STACK_CAVEAT_NOTE,
    APERTURE_VALIDATED_STACK_LIMIT_M2,
    BITS_PER_BYTE,
    CLASS_SE_CENTRAL,
    CLASS_USAGE,
    DATA_IOT_BURST_BYTES,
    DATA_IOT_BURSTS_PER_DAY,
    DATA_IOT_DEVICES,
    DATA_IOT_PRICE_USD_MONTH_DEFAULT,
    ECOSYSTEM_ASSUMPTION_NOTE,
    HZ_PER_MHZ,
    IOT_MAC_EFFICIENCY,
    IOT_MESSAGE_AIRTIME_HIGH_S,
    IOT_MESSAGE_AIRTIME_LOW_S,
    IOT_RANDOM_ACCESS_WINDOW_DEVICES_HIGH,
    IOT_RANDOM_ACCESS_WINDOW_DEVICES_LOW,
    IOT_RANDOM_ACCESS_WINDOWS_PER_SECOND,
    IRIDIUM_IOT_BOOK_DEVICES,
    IRIDIUM_OPERATIONS_COST_MUSD,
    MINIMAL_PACKET_IOT_COUNT_FLOOR_SATELLITES,
    MINIMAL_PACKET_IOT_DEVICES,
    MINIMAL_PACKET_IOT_MESSAGE_BYTES,
    MINIMAL_PACKET_IOT_MESSAGES_PER_DAY,
    MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT,
    MONTHS_PER_YEAR,
    MOUNTED_TERMINAL_CLASS_SE_HIGH,
    MOUNTED_TERMINAL_CLASS_SE_LOW,
    NB_IOT_TONE_HZ,
    PANEL_RULE_LIMITS_NOTE,
    PHONE_CLASS_PRICE_FLOOR_USD_MONTH,
    PHONE_CLASS_SE_HIGH,
    PHONE_CLASS_SE_LOW,
    RETIRED_CAP_READING_FLEET,
    REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE,
    SATELLITES_PER_LAUNCH_BLOCK_UPGRADE,
    SATELLITES_PER_LAUNCH_MAX,
    SATELLITES_PER_LAUNCH_MIN,
    SATELLITES_PER_LAUNCH_NO_UPGRADE,
    SECONDS_PER_DAY,
    SMALL_TERMINAL_CLASS_SE_HIGH,
    SMALL_TERMINAL_CLASS_SE_LOW,
    ClassUsage,
    DeviceClass,
)
from communications.engine import (
    MUSD_TO_USD,
    Deployment,
    DeploymentStep,
    FleetTrajectory,
    FleetYear,
    margin_pct,
    per_satellite_annual_cost_musd,
    run_fleet_loop,
)
from communications.saturation_curve import (
    BandName,
    ClassCurve,
    CurveBeyondLastRowError,
    SaturationCurve,
    SaturationCurveError,
    check_curve_matches,
    people_at,
    read_fleet,
    saturation_inputs_for,
)

logger = logging.getLogger(__name__)

_NOT_AN_IRIDIUM_CONFIG: Final[str] = (
    "the scenario does not select the Iridium model: it needs a top-level "
    "'iridium:' block (see scenarios/iridium.yaml)"
)
"""The refusal of a config without an ``iridium:`` block, word for word the Iridium promotion
command's (``communications.json_output``)."""

COVERAGE_FLOOR_LABEL: Final[str] = "the coverage floor"
"""The first reading's label: the coverage floor, the fewest satellites for a quality link over
the populated band, where every sale starts."""

RETIRED_CAP_LABEL: Final[str] = "the retired cap, kept for comparison"
"""The second reading's label: :data:`~communications.constants.RETIRED_CAP_READING_FLEET`,
the 2,000-satellite cap the Iridium model once inherited, which caps nothing (ADR 005)."""

HORIZON_END_LABEL: Final[str] = "the horizon-end full-cadence reach"
"""The third reading's label: the final model year's living fleet."""

STEADY_STATE_LABEL_FORMAT: Final[str] = "the steady state, beyond the {horizon_years}-year horizon"
"""The fourth reading's label, with the model's horizon in years: the final year's comms
launches times satellites per launch times the life, a fleet the horizon does not hold."""

_WHOLE_FRAME: Final[float] = 1.0
"""The band's whole time-division frame: the uplink holds what the downlink share leaves of it
(1 - d, ADR 008)."""

_NO_FLEET: Final[int] = 0
"""A fleet of no satellites: the lower end of a class's first marginal interval."""

_NO_PEOPLE: Final[float] = 0.0
"""The people a fleet of no satellites serves: the lower end of the first interval's chord."""

_NOTHING_SOLD_MUSD: Final[float] = 0.0
"""Revenue in a year or at a reading whose fleet is below the coverage floor, $M a year: nothing
is sold there (the floor rule)."""

_PERCENT: Final[float] = 100.0
"""A fraction's percent scale, for the stated assumptions' text."""

_BYTES_PER_KB: Final[int] = 1_000
"""Bytes in a KB (decimal), for the stated assumptions' text on data IoT's bursts."""

_TONE_KHZ_PER_HZ: Final[float] = 1e-3
"""Hz to kHz, for the stated assumptions' text on the IoT tone."""


class NotAnIridiumConfigError(ValueError):
    """A config of the cellular family where an Iridium path needs the Iridium dials."""


class BindingLimit(StrEnum):
    """What bounds a device class's fleet at the horizon's end, reported beside the launch
    cadence and never a cap on the build (ADR 005)."""

    LAUNCH_CADENCE = "launch_cadence"
    """The launch cadence: the final year's living fleet is below the class's saturation number,
    or the class has none on the curve."""

    SPECTRUM = "spectrum"
    """The owned spectrum: the final year's living fleet is at or past the class's saturation
    number (reported, never a cap: the build continues at the cadence)."""


@dataclass(frozen=True)
class ClassRates:
    """One class's downlink pool and per-user rates (the rule is
    :func:`derive_iridium_per_user_rates`'s).

    Attributes:
        beam_pool_mbps: One beam's downlink pool, W x SE x d, Mbps.
        per_user_rate_peak_mbps: The rate while active, the class's usage, Mbps.
        per_user_rate_offpeak_mbps: The lower of the pool and the rate x the busy-hour share
            over the off-peak share, Mbps.
    """

    beam_pool_mbps: float
    per_user_rate_peak_mbps: float
    per_user_rate_offpeak_mbps: float


@dataclass(frozen=True)
class MarginalIntervalRecord:
    """One interval of a class's curve rows and what one more satellite adds across it.

    Attributes:
        lower_fleet: The interval's lower fleet (0 for the first interval).
        upper_fleet: Its upper fleet, a row of the class's curve.
        people_added_per_satellite: (people at the upper fleet - people at the lower) over the
            fleets' difference, at d and the panel factor, unrounded.
        revenue_per_satellite_year_musd: Those people at the class's price for a year, $M.
        pays: Whether that revenue is at least the cost per satellite-year.
    """

    lower_fleet: int
    upper_fleet: int
    people_added_per_satellite: float
    revenue_per_satellite_year_musd: float
    pays: bool


@dataclass(frozen=True)
class ClassRecord:
    """One device class's block: its price, usage, physics, markers, limit and intervals.

    Attributes:
        device_class: The class.
        price_usd_per_month: Its flat monthly price, dollars.
        active_user_rate_mbps: Its rate while active, Mbps (its usage).
        concurrency_peak: Its busy-hour share of users active at once.
        concurrency_offpeak: Its off-peak share.
        spectral_efficiency_bps_per_hz: Its central spectral efficiency, bps/Hz.
        per_satellite_capacity_gbps: The satellite's peak for the class, every beam lit and
            used and the band full time, times the panel factor, Gbps.
        beam_pool_mbps: One beam's downlink pool, W x SE x d, Mbps.
        per_user_rate_peak_mbps: Its peak per-user rate, Mbps.
        per_user_rate_offpeak_mbps: Its off-peak per-user rate, Mbps.
        maximum_use_beams: The curve's maximum use times the panel factor, beams.
        saturation_number: The curve's saturation number, or None when not reached.
        saturation_not_reached_by: The curve's last row when the number is not reached.
        elasticity_under_0p25_fleet: The curve's 0.25 marker, or None.
        fleet_at_90pct_of_maximum_use: The curve's 90 percent fleet, or None.
        binding_limit_at_horizon_end: Spectrum when the final year's living fleet is at or past
            the saturation number, else the launch cadence.
        marginal_intervals: Its intervals, from 0 to the first row and between consecutive
            rows of its curve.
    """

    device_class: DeviceClass
    price_usd_per_month: float
    active_user_rate_mbps: float
    concurrency_peak: float
    concurrency_offpeak: float
    spectral_efficiency_bps_per_hz: float
    per_satellite_capacity_gbps: float
    beam_pool_mbps: float
    per_user_rate_peak_mbps: float
    per_user_rate_offpeak_mbps: float
    maximum_use_beams: float
    saturation_number: int | None
    saturation_not_reached_by: int | None
    elasticity_under_0p25_fleet: int | None
    fleet_at_90pct_of_maximum_use: int | None
    binding_limit_at_horizon_end: BindingLimit
    marginal_intervals: tuple[MarginalIntervalRecord, ...]


@dataclass(frozen=True)
class ClassYearRecord:
    """One class's line in one model year.

    Attributes:
        device_class: The class.
        people_served: Every person the living fleet carries for the class, rounded half up;
            0 below the coverage floor.
        revenue_musd: Those people at the class's price for the year, $M; 0.0 below the floor.
        own_margin_pct: The class's own revenue against the year's whole-fleet annualized
            cost, percent; None when the revenue is 0.0.
    """

    device_class: DeviceClass
    people_served: int
    revenue_musd: float
    own_margin_pct: float | None


@dataclass(frozen=True)
class YearRecord:
    """One model year's Iridium lines, beside the shared record's year of the same index.

    Attributes:
        year: The fiscal year (the key of the shared record's year).
        minimal_packet_iot_revenue_musd: Minimal-packet IoT's book, $M; 0.0 below the floor.
        data_iot_revenue_musd: Data IoT's book, $M; 0.0 below the floor.
        classes: Each class's line, in class order.
    """

    year: int
    minimal_packet_iot_revenue_musd: float
    data_iot_revenue_musd: float
    classes: tuple[ClassYearRecord, ...]


@dataclass(frozen=True)
class FixedBooksRecord:
    """The two IoT lines (ADR 007): fixed counts at their prices, each its own line.

    Attributes:
        minimal_packet_iot_devices: Minimal-packet IoT's fixed count.
        minimal_packet_iot_price_usd_per_month: Its monthly price, dollars.
        minimal_packet_iot_annual_revenue_musd: Its book, $M a year, from the floor year.
        data_iot_devices: Data IoT's fixed count.
        data_iot_price_usd_per_month: Its monthly price, dollars.
        data_iot_annual_revenue_musd: Its book, $M a year, from the floor year.
        basis: Where the counts come from and how the lines are sold.
    """

    minimal_packet_iot_devices: int
    minimal_packet_iot_price_usd_per_month: float
    minimal_packet_iot_annual_revenue_musd: float
    data_iot_devices: int
    data_iot_price_usd_per_month: float
    data_iot_annual_revenue_musd: float
    basis: str


@dataclass(frozen=True)
class ClassReadingRecord:
    """One class at one reported fleet.

    Attributes:
        device_class: The class.
        useful_beams: L at the fleet times the panel factor, beams.
        share_of_maximum_use: L over the class's maximum use.
        ocean_factor: U, None at a fleet of 0.
        people: The people the fleet carries for the class, rounded half up.
        revenue_musd: Those people at the class's price for a year, $M; 0.0 below the floor.
        own_margin_pct: That revenue against the reading's fleet cost, percent; None when the
            revenue is 0.0.
    """

    device_class: DeviceClass
    useful_beams: float
    share_of_maximum_use: float
    ocean_factor: float | None
    people: int
    revenue_musd: float
    own_margin_pct: float | None


@dataclass(frozen=True)
class ReadingRecord:
    """Every class at one reported fleet.

    Attributes:
        label: What the fleet is (the coverage floor, the retired cap, the horizon-end reach,
            the steady state).
        fleet: The fleet, satellites.
        fleet_annual_cost_musd: The reading's cost, $M a year: the final year's annualized
            cost at the horizon-end reach, else the fleet times the cost per satellite-year.
        classes: Each class's reading, in class order.
    """

    label: str
    fleet: int
    fleet_annual_cost_musd: float
    classes: tuple[ClassReadingRecord, ...]


@dataclass(frozen=True)
class IotCheckRowRecord:
    """One IoT line at one reported fleet; every field but ``fleet`` None below the floor.

    Attributes:
        fleet: The fleet, satellites.
        devices_per_useful_beam: The line's devices over the phone class's useful beams (times
            the panel factor).
        uplink_bits_share: A beam's daily IoT bits over its uplink's daily bits, a fraction;
            None when the uplink holds no time (d = 1).
        uplink_bits_share_with_mac: The same over the MAC efficiency.
        access_attempts_per_second_per_beam: One attempt per message or burst.
        uplink_tone_share_low: Minimal-packet IoT's message channel time over the uplink's
            tone time at the low airtime, a fraction; None with no uplink, and None for data
            IoT, whose bursts are not single-tone messages (the tone time of the single-tone
            messages it sends beside them goes unreported).
        uplink_tone_share_high: The same at the high airtime.
    """

    fleet: int
    devices_per_useful_beam: float | None
    uplink_bits_share: float | None
    uplink_bits_share_with_mac: float | None
    access_attempts_per_second_per_beam: float | None
    uplink_tone_share_low: float | None
    uplink_tone_share_high: float | None


@dataclass(frozen=True)
class IotCheckRecord:
    """The IoT check, one row per reported fleet for each line.

    Attributes:
        minimal_packet_iot: Minimal-packet IoT's rows.
        data_iot: Data IoT's rows (its tone shares None: its bursts are not single-tone
            messages, and the tone time of the single-tone messages it sends beside them goes
            unreported).
    """

    minimal_packet_iot: tuple[IotCheckRowRecord, ...]
    data_iot: tuple[IotCheckRowRecord, ...]


@dataclass(frozen=True)
class SaturationRecord:
    """The curve a run read and what it read from it.

    Attributes:
        curve_path: The scenario's curve path (repository-relative, or absolute as given).
        curve_schema_version: The curve's schema version.
        curve_version_stamp: The curve's version stamp.
        input_hash: The curve's input hash.
        downlink_share: The downlink share d the run read the curve at.
        panel_factor: The scenario's panel over the curve's reference panel.
        readings: The four reported fleets' readings, in order.
        band_saturation_numbers: The phone class's band points' saturation numbers (None when
            not reached), in band order.
        iot_check: The IoT check.
        limits: The curve's stated limits, carried over.
    """

    curve_path: str
    curve_schema_version: str
    curve_version_stamp: str
    input_hash: str
    downlink_share: float
    panel_factor: float
    readings: tuple[ReadingRecord, ...]
    band_saturation_numbers: Mapping[BandName, int | None]
    iot_check: IotCheckRecord
    limits: tuple[str, ...]


@dataclass(frozen=True)
class IridiumRecord:
    """The Iridium family's record of a run, read beside its shared fleet-and-cost record.

    It mirrors the ``iridium-v6`` artifact's Iridium blocks (the class blocks, each year's
    Iridium lines, the fixed books, the saturation block and the assumptions) and carries
    what the artifact reads from the Iridium dials, so the builder needs no config. The
    deployment, the living fleet and every cost line are the shared record's; nothing here
    repeats them.

    Attributes:
        scenario_name: The scenario's label.
        spectrum_mhz: The held width, MHz.
        aperture_m2: The panel, m^2.
        satellites_per_launch: The satellites one launch carries.
        operations_cost_musd: The operations cost, $M (an explicit zero).
        ecosystem_assumption: The ecosystem assumption behind the phone class.
        coverage_floor_reached_year: The first year the living fleet is at or above the
            coverage floor, when every sale starts; None when never.
        cost_per_satellite_year_musd: One satellite's annualized cost at the final year's
            launch price, $M (defined even when no cohort flies).
        classes: Each class's block, in class order.
        years: Each model year's Iridium lines, in the shared record's order.
        fixed_books: The two IoT lines.
        saturation: The curve and its readings.
        assumptions: The stated assumptions, in order.
    """

    scenario_name: str
    spectrum_mhz: float
    aperture_m2: float
    satellites_per_launch: int
    operations_cost_musd: float
    ecosystem_assumption: str
    coverage_floor_reached_year: int | None
    cost_per_satellite_year_musd: float
    classes: tuple[ClassRecord, ...]
    years: tuple[YearRecord, ...]
    fixed_books: FixedBooksRecord
    saturation: SaturationRecord
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class IridiumRun:
    """A run of the Iridium entry: the shared fleet-and-cost record and the Iridium record.

    Attributes:
        fleet: The shared fleet-and-cost record (the deployment, living fleet, cost lines and
            totals), under :func:`full_cadence_rule`.
        iridium: The Iridium record.
    """

    fleet: FleetTrajectory
    iridium: IridiumRecord


@dataclass(frozen=True)
class _IotUsage:
    """What one IoT device sends a day (engine-internal): its usage, apart from any count.

    The IoT check takes a line's device count beside it (:func:`_iot_row`), so the shares a
    usage gives read at whatever count a caller supplies.

    Attributes:
        bytes_per_day: The device's daily volume, bytes.
        attempts_per_day: Its access attempts a day, one per message or burst.
        single_tone_messages_per_day: Its messages a day read on single tones; None for data
            IoT, whose bursts are not single-tone messages, so the tone time of the messages it
            sends beside them goes unreported.
    """

    bytes_per_day: int
    attempts_per_day: int
    single_tone_messages_per_day: int | None


_MINIMAL_PACKET_IOT_USAGE: Final[_IotUsage] = _IotUsage(
    bytes_per_day=MINIMAL_PACKET_IOT_MESSAGES_PER_DAY * MINIMAL_PACKET_IOT_MESSAGE_BYTES,
    attempts_per_day=MINIMAL_PACKET_IOT_MESSAGES_PER_DAY,
    single_tone_messages_per_day=MINIMAL_PACKET_IOT_MESSAGES_PER_DAY,
)
"""A minimal-packet IoT device: 48 messages of 340 bytes a day, each on one tone."""

_DATA_IOT_USAGE: Final[_IotUsage] = _IotUsage(
    bytes_per_day=DATA_IOT_BURSTS_PER_DAY * DATA_IOT_BURST_BYTES
    + MINIMAL_PACKET_IOT_MESSAGES_PER_DAY * MINIMAL_PACKET_IOT_MESSAGE_BYTES,
    attempts_per_day=DATA_IOT_BURSTS_PER_DAY + MINIMAL_PACKET_IOT_MESSAGES_PER_DAY,
    single_tone_messages_per_day=None,
)
"""A data IoT device: 4 bursts of 100 KB a day beside the 48 messages; its bursts are not
single-tone, and its messages' tone time goes unreported (no tone share)."""


def iridium_dials_of(config: CommsConfig) -> IridiumDials:
    """Return a config's Iridium dials, refusing a config that does not select the Iridium model
    and one that does not validate whole.

    Every Iridium path narrows its config here, so here the config is re-validated whole
    (``CommsConfig.model_validate(config.model_dump())``): a config built with ``model_copy``,
    which pydantic does not validate, cannot carry a setting past the validators (a coverage
    floor off its pinned value, a negative price) into a run.

    Args:
        config: A communications config.

    Returns:
        Its ``iridium`` block.

    Raises:
        NotAnIridiumConfigError: If the config has no ``iridium:`` block (it is the cellular
            family's), checked first.
        pydantic.ValidationError: If the config does not validate whole, naming the field.
    """
    if config.iridium is None:
        raise NotAnIridiumConfigError(_NOT_AN_IRIDIUM_CONFIG)
    CommsConfig.model_validate(config.model_dump())
    return config.iridium


def full_cadence_rule(step: DeploymentStep) -> Deployment:
    """The Iridium family's deployment rule: fly every launch the cadence share allows.

    Each year deploys every comms launch the cadence share allows, times the satellites per
    launch, with no target, hold or cap; the part of the deployment that matches the year's
    retirements (the cohort one life earlier) counts as replacement, the rest is growth. Both
    are whole launches: every cohort is, at one count per launch. The rule reads only its step
    and keeps no state.

    Args:
        step: The year's cadence allowance, satellites per launch and retirements.

    Returns:
        The year's deployment: every allowed launch, and ``min(added, retiring)`` replaced.
    """
    satellites_added = step.launches_allowed * step.satellites_per_launch
    return Deployment(
        satellites_added=satellites_added,
        satellites_replaced=min(satellites_added, step.retiring_this_year),
    )


def derive_per_satellite_capacity_gbps(
    spectrum_mhz: float, spectral_efficiency_bps_per_hz: float, panel_factor: float
) -> float:
    """Return a satellite's peak for one class, Gbps: every beam lit and used, the band full time.

    ::

        spectrum_mhz x spectral_efficiency_bps_per_hz
            x REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE x panel_factor

    The calibration folds the effective beam count of a digital-beamforming satellite
    (about 150 beams at the reference panel) with the Mbps-to-Gbps scaling; the panel factor
    is the scenario's panel over the curve's reference panel, so the peak scales linearly
    with the panel (the stated rule). Worked: the small terminal at 8 MHz and SE 2.0 is 2.4
    Gbps at the reference panel and 1.4784 Gbps at 15.4 m^2 (a factor of 0.616).

    Args:
        spectrum_mhz: The held width, MHz.
        spectral_efficiency_bps_per_hz: The class's central spectral efficiency, bps/Hz.
        panel_factor: The scenario's panel over the reference panel.

    Returns:
        The peak, Gbps.
    """
    return (
        spectrum_mhz
        * spectral_efficiency_bps_per_hz
        * REUSE_CALIBRATION_GBPS_PER_MHZ_PER_SE
        * panel_factor
    )


def derive_iridium_per_user_rates(
    *,
    spectrum_mhz: float,
    spectral_efficiency_bps_per_hz: float,
    downlink_share: float,
    usage: ClassUsage,
) -> ClassRates:
    """Return one class's downlink pool and per-user rates at its own usage.

    ::

        beam_pool_mbps = spectrum_mhz x spectral_efficiency_bps_per_hz x downlink_share
        peak = the class's rate while active
        off-peak = min(beam_pool_mbps, rate x concurrency_peak / concurrency_offpeak)

    One beam's data pool caps one person's rate; beam reuse multiplies the people served, not
    that rate. Worked at 8 MHz and d = 0.67: the small terminal (SE 2.0; 2 Mbps, 2.5 and 0.5
    percent) has a 10.72 Mbps pool, 2.0 peak and 10.0 off-peak (the ratio binds); the mounted
    terminal (SE 2.5; 5 Mbps, 10 and 2 percent) 13.4, 5.0 and 13.4 (the pool binds).

    Args:
        spectrum_mhz: The held width, MHz.
        spectral_efficiency_bps_per_hz: The class's central spectral efficiency, bps/Hz.
        downlink_share: The downlink share d.
        usage: The class's usage (its rate while active and its two shares).

    Returns:
        The class's pool and rates.
    """
    beam_pool_mbps = spectrum_mhz * spectral_efficiency_bps_per_hz * downlink_share
    return ClassRates(
        beam_pool_mbps=beam_pool_mbps,
        per_user_rate_peak_mbps=usage.active_rate_mbps,
        per_user_rate_offpeak_mbps=min(
            beam_pool_mbps,
            usage.active_rate_mbps * usage.concurrency_peak / usage.concurrency_offpeak,
        ),
    )


def _panel_factor(dials: IridiumDials, curve: SaturationCurve) -> float:
    """Return the scenario's panel over the curve's reference panel, refusing one that is not a
    positive finite number (a panel so small its ratio underflows to 0).

    Raises:
        ValueError: Naming ``iridium.aperture_m2``, the reference panel and the factor.
    """
    reference_m2 = curve.parameters.shell.reference_aperture_m2
    factor = dials.aperture_m2 / reference_m2
    if not (math.isfinite(factor) and factor > 0):
        raise ValueError(
            f"iridium.aperture_m2 ({dials.aperture_m2!r} m^2) over the saturation curve's "
            f"reference panel ({reference_m2!r} m^2) gives a panel factor of {factor!r}; it "
            "must be a positive finite number"
        )
    return factor


def _class_price(arpu: IridiumArpuDials, device_class: DeviceClass) -> float:
    """Return a class's monthly price from the five prices."""
    match device_class:
        case DeviceClass.SMALL_TERMINAL_CLASS:
            return arpu.small_terminal_class_price_usd_month
        case DeviceClass.MOUNTED_TERMINAL_CLASS:
            return arpu.mounted_terminal_class_price_usd_month
        case DeviceClass.PHONE_CLASS:
            return arpu.phone_class_price_usd_month
        case _:
            assert_never(device_class)


def _annual_revenue_musd(count: float, price_usd_per_month: float) -> float:
    """Return a count (people, devices, or the people one satellite adds) at a monthly price
    for a year, $M."""
    return count * price_usd_per_month * MONTHS_PER_YEAR / MUSD_TO_USD


def _sells(fleet: int, coverage_floor: int) -> bool:
    """Whether a fleet sells: the floor rule's one home. At or above the coverage floor every
    class and both IoT lines are sold in full; below it nothing is sold."""
    return fleet >= coverage_floor


@dataclass(frozen=True)
class _ClassSale:
    """A class's sale at one fleet (engine-internal): its revenue and its own margin.

    Attributes:
        revenue_musd: The people at the class's price for a year, $M; 0.0 below the floor.
        own_margin_pct: That revenue against the fleet's annualized cost, percent; None when
            the revenue is 0.0.
    """

    revenue_musd: float
    own_margin_pct: float | None


def _class_sale(
    people: int,
    *,
    sold: bool,
    price_usd_per_month: float,
    fleet_annual_cost_musd: float,
) -> _ClassSale:
    """A class's floor-gated sale at a fleet, for the years and the readings alike: its people at
    its price when the fleet sells (:func:`_sells`), else nothing, and its own margin against
    the fleet's annualized cost."""
    revenue_musd = _annual_revenue_musd(people, price_usd_per_month) if sold else _NOTHING_SOLD_MUSD
    return _ClassSale(
        revenue_musd=revenue_musd,
        own_margin_pct=margin_pct(revenue_musd, fleet_annual_cost_musd),
    )


def _people_served(
    curve: SaturationCurve,
    device_class: DeviceClass,
    fleet_year: FleetYear,
    *,
    downlink_share: float,
    panel_factor: float,
) -> int:
    """Return every person a year's living fleet carries for a class, rounded half up.

    Raises:
        CurveBeyondLastRowError: If the year's fleet lies past the class's last row, naming the
            year beside the reading's own message (the fleet, the class and the last row).
    """
    try:
        people = people_at(
            curve,
            device_class,
            fleet_year.living_fleet,
            downlink_share=downlink_share,
            panel_factor=panel_factor,
        )
    except CurveBeyondLastRowError as exc:
        raise CurveBeyondLastRowError(f"FY{fleet_year.year}'s living fleet: {exc}") from exc
    return round_half_up(people)


def _years(
    fleet: FleetTrajectory,
    curve: SaturationCurve,
    *,
    coverage_floor: int,
    downlink_share: float,
    panel_factor: float,
    prices: Mapping[DeviceClass, float],
    books: FixedBooksRecord,
) -> tuple[YearRecord, ...]:
    """Each model year's Iridium lines: every seat sold at or above the floor, nothing below it."""
    years: list[YearRecord] = []
    for fleet_year in fleet.years:
        sold = _sells(fleet_year.living_fleet, coverage_floor)
        lines: list[ClassYearRecord] = []
        for device_class in DeviceClass:
            people = (
                _people_served(
                    curve,
                    device_class,
                    fleet_year,
                    downlink_share=downlink_share,
                    panel_factor=panel_factor,
                )
                if sold
                else 0
            )
            sale = _class_sale(
                people,
                sold=sold,
                price_usd_per_month=prices[device_class],
                fleet_annual_cost_musd=fleet_year.annual_cost_this_year_musd,
            )
            lines.append(
                ClassYearRecord(
                    device_class=device_class,
                    people_served=people,
                    revenue_musd=sale.revenue_musd,
                    own_margin_pct=sale.own_margin_pct,
                )
            )
        years.append(
            YearRecord(
                year=fleet_year.year,
                minimal_packet_iot_revenue_musd=(
                    books.minimal_packet_iot_annual_revenue_musd if sold else _NOTHING_SOLD_MUSD
                ),
                data_iot_revenue_musd=(
                    books.data_iot_annual_revenue_musd if sold else _NOTHING_SOLD_MUSD
                ),
                classes=tuple(lines),
            )
        )
    return tuple(years)


@dataclass(frozen=True)
class _ReportedFleet:
    """A fleet the readings are taken at (engine-internal).

    Attributes:
        label: What the fleet is (the reading's published label).
        fleet: The fleet, satellites.
        annual_cost_musd: The reading's cost, $M a year.
        basis: How the fleet is formed and the settings that set it, for a refusal's message.
    """

    label: str
    fleet: int
    annual_cost_musd: float
    basis: str


def _reported_fleets(
    config: CommsConfig,
    fleet: FleetTrajectory,
    *,
    coverage_floor: int,
    cost_per_satellite_year_musd: float,
) -> tuple[_ReportedFleet, ...]:
    """The four reported fleets, each with its reading cost and its basis.

    The horizon-end reach takes the final year's annualized cost, so it and the final year agree
    under any launch-cost path; the coverage floor, the retired cap and the steady state, fleets
    the trajectory does not hold, are priced at the cost per satellite-year.
    """
    final = fleet.years[-1]
    satellites_per_launch = config.satellite.satellites_per_launch
    life = config.satellite.satellite_lifetime_years
    steady_state = final.comms_launches_flown_this_year * satellites_per_launch * life
    return (
        _ReportedFleet(
            COVERAGE_FLOOR_LABEL,
            coverage_floor,
            coverage_floor * cost_per_satellite_year_musd,
            "the floor pinned on the Iridium path (coverage.satellites_for_full_coverage)",
        ),
        _ReportedFleet(
            RETIRED_CAP_LABEL,
            RETIRED_CAP_READING_FLEET,
            RETIRED_CAP_READING_FLEET * cost_per_satellite_year_musd,
            "a reading set by no setting",
        ),
        _ReportedFleet(
            HORIZON_END_LABEL,
            final.living_fleet,
            final.annual_cost_this_year_musd,
            f"FY{final.year}'s living fleet, set by the cadence (cadence.*, "
            "comms_cadence.share_of_fleet), satellite.satellites_per_launch and "
            "satellite.satellite_lifetime_years",
        ),
        _ReportedFleet(
            STEADY_STATE_LABEL_FORMAT.format(horizon_years=config.metadata.horizon_years),
            steady_state,
            steady_state * cost_per_satellite_year_musd,
            f"FY{final.year}'s {final.comms_launches_flown_this_year} comms launches (set by "
            "cadence.* and comms_cadence.share_of_fleet) x "
            f"{satellites_per_launch} satellites per launch "
            f"(satellite.satellites_per_launch) x the {life}-year life "
            "(satellite.satellite_lifetime_years)",
        ),
    )


def _reading(
    curve: SaturationCurve,
    reported: _ReportedFleet,
    *,
    coverage_floor: int,
    downlink_share: float,
    panel_factor: float,
    prices: Mapping[DeviceClass, float],
) -> ReadingRecord:
    """Every class at one reported fleet; below the floor it carries people and sells nothing.

    Raises:
        CurveBeyondLastRowError: If the reported fleet lies past a class's last row, naming the
            reading (its label, its fleet and the settings that set it) beside the reading's
            own message (the fleet, the class and the last row), as a year's refusal names its
            year.
    """
    sold = _sells(reported.fleet, coverage_floor)
    lines: list[ClassReadingRecord] = []
    for device_class in DeviceClass:
        try:
            reading = read_fleet(
                curve,
                device_class,
                reported.fleet,
                downlink_share=downlink_share,
                panel_factor=panel_factor,
            )
        except CurveBeyondLastRowError as exc:
            raise CurveBeyondLastRowError(
                f"{reported.label} ({reported.fleet} satellites, {reported.basis}): {exc}"
            ) from exc
        people = round_half_up(reading.people)
        sale = _class_sale(
            people,
            sold=sold,
            price_usd_per_month=prices[device_class],
            fleet_annual_cost_musd=reported.annual_cost_musd,
        )
        lines.append(
            ClassReadingRecord(
                device_class=device_class,
                useful_beams=reading.useful_beams,
                share_of_maximum_use=reading.share_of_maximum_use,
                ocean_factor=reading.ocean_factor,
                people=people,
                revenue_musd=sale.revenue_musd,
                own_margin_pct=sale.own_margin_pct,
            )
        )
    return ReadingRecord(
        label=reported.label,
        fleet=reported.fleet,
        fleet_annual_cost_musd=reported.annual_cost_musd,
        classes=tuple(lines),
    )


def _iot_row(
    usage: _IotUsage,
    reading: ReadingRecord,
    *,
    devices: int,
    coverage_floor: int,
    uplink_bits_per_beam_day: float,
    uplink_tone_seconds_per_beam_day: float,
) -> IotCheckRowRecord:
    """One IoT line at one reported fleet: ``devices`` of one usage, spread over the phone
    class's useful beams.

    The count is an argument apart from the per-device usage, and every share is the devices
    a beam times that usage over the beam's uplink, so the same usage reads at any count.
    Every field but the fleet is None below the coverage floor (the books are not sold there)
    and wherever its denominator does not exist (no useful beam; an uplink with no time).
    """
    phone_beams = next(
        line_reading.useful_beams
        for line_reading in reading.classes
        if line_reading.device_class is DeviceClass.PHONE_CLASS
    )
    if not _sells(reading.fleet, coverage_floor) or phone_beams <= 0:
        return IotCheckRowRecord(
            fleet=reading.fleet,
            devices_per_useful_beam=None,
            uplink_bits_share=None,
            uplink_bits_share_with_mac=None,
            access_attempts_per_second_per_beam=None,
            uplink_tone_share_low=None,
            uplink_tone_share_high=None,
        )
    per_beam = devices / phone_beams
    bits_share = (
        per_beam * usage.bytes_per_day * BITS_PER_BYTE / uplink_bits_per_beam_day
        if uplink_bits_per_beam_day > 0
        else None
    )
    tone_shares: tuple[float | None, float | None] = (None, None)
    if usage.single_tone_messages_per_day is not None and uplink_tone_seconds_per_beam_day > 0:
        messages = per_beam * usage.single_tone_messages_per_day
        tone_shares = (
            messages * IOT_MESSAGE_AIRTIME_LOW_S / uplink_tone_seconds_per_beam_day,
            messages * IOT_MESSAGE_AIRTIME_HIGH_S / uplink_tone_seconds_per_beam_day,
        )
    return IotCheckRowRecord(
        fleet=reading.fleet,
        devices_per_useful_beam=per_beam,
        uplink_bits_share=bits_share,
        uplink_bits_share_with_mac=None if bits_share is None else bits_share / IOT_MAC_EFFICIENCY,
        access_attempts_per_second_per_beam=per_beam * usage.attempts_per_day / SECONDS_PER_DAY,
        uplink_tone_share_low=tone_shares[0],
        uplink_tone_share_high=tone_shares[1],
    )


def _iot_check(
    readings: tuple[ReadingRecord, ...],
    dials: IridiumDials,
    *,
    coverage_floor: int,
) -> IotCheckRecord:
    """The IoT check at every reported fleet, each line on its own.

    A beam's uplink is the held width at the phone class's spectral efficiency over the share of
    the frame the downlink leaves (1 - d, ADR 008), and its tones are the held width over the
    NB-IoT tone in that share; both are per day.
    """
    uplink_share = _WHOLE_FRAME - dials.saturation.downlink_share
    width_hz = dials.spectrum_mhz * HZ_PER_MHZ
    uplink_bits_per_beam_day = (
        width_hz * CLASS_SE_CENTRAL[DeviceClass.PHONE_CLASS] * uplink_share * SECONDS_PER_DAY
    )
    uplink_tone_seconds_per_beam_day = width_hz / NB_IOT_TONE_HZ * uplink_share * SECONDS_PER_DAY

    def rows(usage: _IotUsage, devices: int) -> tuple[IotCheckRowRecord, ...]:
        """A line's row at each reported fleet: its count of devices of its usage."""
        return tuple(
            _iot_row(
                usage,
                reading,
                devices=devices,
                coverage_floor=coverage_floor,
                uplink_bits_per_beam_day=uplink_bits_per_beam_day,
                uplink_tone_seconds_per_beam_day=uplink_tone_seconds_per_beam_day,
            )
            for reading in readings
        )

    return IotCheckRecord(
        minimal_packet_iot=rows(_MINIMAL_PACKET_IOT_USAGE, MINIMAL_PACKET_IOT_DEVICES),
        data_iot=rows(_DATA_IOT_USAGE, DATA_IOT_DEVICES),
    )


def _marginal_intervals(
    curve: SaturationCurve,
    class_curve: ClassCurve,
    *,
    downlink_share: float,
    panel_factor: float,
    price_usd_per_month: float,
    cost_per_satellite_year_musd: float,
) -> tuple[MarginalIntervalRecord, ...]:
    """A class's marginal intervals on its curve's own rows: from 0 to the first row, then
    between consecutive rows, every one listed, so an interval that pays after a first stop
    shows."""
    intervals: list[MarginalIntervalRecord] = []
    lower_fleet, lower_people = _NO_FLEET, _NO_PEOPLE
    for row in class_curve.rows:
        upper_people = people_at(
            curve,
            class_curve.device_class,
            row.fleet,
            downlink_share=downlink_share,
            panel_factor=panel_factor,
        )
        added = (upper_people - lower_people) / (row.fleet - lower_fleet)
        revenue_musd = _annual_revenue_musd(added, price_usd_per_month)
        intervals.append(
            MarginalIntervalRecord(
                lower_fleet=lower_fleet,
                upper_fleet=row.fleet,
                people_added_per_satellite=added,
                revenue_per_satellite_year_musd=revenue_musd,
                pays=revenue_musd >= cost_per_satellite_year_musd,
            )
        )
        lower_fleet, lower_people = row.fleet, upper_people
    return tuple(intervals)


def _class_curve(curve: SaturationCurve, device_class: DeviceClass) -> ClassCurve:
    """Return a class's central curve.

    Raises:
        SaturationCurveError: If the curve holds no curve for the class.
    """
    for entry in curve.classes:
        if entry.device_class is device_class:
            return entry
    raise SaturationCurveError(f"the saturation curve holds no {device_class.value} curve to read")


def _class_record(
    curve: SaturationCurve,
    device_class: DeviceClass,
    dials: IridiumDials,
    *,
    panel_factor: float,
    price_usd_per_month: float,
    final_living_fleet: int,
    cost_per_satellite_year_musd: float,
) -> ClassRecord:
    """One class's block: its price, usage and physics, its markers, its limit, its intervals."""
    class_curve = _class_curve(curve, device_class)
    usage = CLASS_USAGE[device_class]
    spectral_efficiency = CLASS_SE_CENTRAL[device_class]
    downlink_share = dials.saturation.downlink_share
    rates = derive_iridium_per_user_rates(
        spectrum_mhz=dials.spectrum_mhz,
        spectral_efficiency_bps_per_hz=spectral_efficiency,
        downlink_share=downlink_share,
        usage=usage,
    )
    markers = class_curve.markers
    binding = (
        BindingLimit.SPECTRUM
        if markers.saturation_number is not None and final_living_fleet >= markers.saturation_number
        else BindingLimit.LAUNCH_CADENCE
    )
    return ClassRecord(
        device_class=device_class,
        price_usd_per_month=price_usd_per_month,
        active_user_rate_mbps=usage.active_rate_mbps,
        concurrency_peak=usage.concurrency_peak,
        concurrency_offpeak=usage.concurrency_offpeak,
        spectral_efficiency_bps_per_hz=spectral_efficiency,
        per_satellite_capacity_gbps=derive_per_satellite_capacity_gbps(
            dials.spectrum_mhz, spectral_efficiency, panel_factor
        ),
        beam_pool_mbps=rates.beam_pool_mbps,
        per_user_rate_peak_mbps=rates.per_user_rate_peak_mbps,
        per_user_rate_offpeak_mbps=rates.per_user_rate_offpeak_mbps,
        maximum_use_beams=markers.maximum_use_beams * panel_factor,
        saturation_number=markers.saturation_number,
        saturation_not_reached_by=markers.saturation_not_reached_by,
        elasticity_under_0p25_fleet=markers.elasticity_under_0p25_fleet,
        fleet_at_90pct_of_maximum_use=markers.fleet_at_90pct_of_maximum_use,
        binding_limit_at_horizon_end=binding,
        marginal_intervals=_marginal_intervals(
            curve,
            class_curve,
            downlink_share=downlink_share,
            panel_factor=panel_factor,
            price_usd_per_month=price_usd_per_month,
            cost_per_satellite_year_musd=cost_per_satellite_year_musd,
        ),
    )


def _fixed_books(arpu: IridiumArpuDials) -> FixedBooksRecord:
    """The two IoT lines at their fixed counts and prices (ADR 007).

    The basis states where the counts come from in named constants alone (the iridium-v5
    model's count at the floor it was read at; Iridium's own book; the price relation at the
    default prices), so it reads true at any setting a run takes.
    """
    return FixedBooksRecord(
        minimal_packet_iot_devices=MINIMAL_PACKET_IOT_DEVICES,
        minimal_packet_iot_price_usd_per_month=arpu.minimal_packet_iot_price_usd_month,
        minimal_packet_iot_annual_revenue_musd=_annual_revenue_musd(
            MINIMAL_PACKET_IOT_DEVICES, arpu.minimal_packet_iot_price_usd_month
        ),
        data_iot_devices=DATA_IOT_DEVICES,
        data_iot_price_usd_per_month=arpu.data_iot_price_usd_month,
        data_iot_annual_revenue_musd=_annual_revenue_musd(
            DATA_IOT_DEVICES, arpu.data_iot_price_usd_month
        ),
        basis=(
            "Minimal-packet IoT's count is the capable count: the iridium-v5 model's Sheet A "
            f"IoT count at the {MINIMAL_PACKET_IOT_COUNT_FLOOR_SATELLITES}-satellite coverage "
            "floor, held as a stated assumption (ADR 007), not Iridium's own IoT book "
            f"({IRIDIUM_IOT_BOOK_DEVICES:,} devices, COMM-617). Data IoT's count is half of it, "
            "in proportion, the investor's setting of 2026-10-04: at the default prices "
            f"(${MINIMAL_PACKET_IOT_PRICE_USD_MONTH_DEFAULT:g} and "
            f"${DATA_IOT_PRICE_USD_MONTH_DEFAULT:g} a month) half the count at double the "
            "price. Each line is its own revenue line, never inside a class's margin; neither "
            "moves with the fleet, a class, the downlink share, the panel or satellites per "
            "launch; both are sold in full from the first year the living fleet reaches the "
            "coverage floor, and not before. Government is left out of revenue."
        ),
    )


def _assumptions(
    config: CommsConfig,
    dials: IridiumDials,
    curve: SaturationCurve,
    *,
    panel_factor: float,
) -> tuple[str, ...]:
    """The run's stated assumptions, in order, built from its config and its curve."""
    arpu = dials.arpu
    small = CLASS_USAGE[DeviceClass.SMALL_TERMINAL_CLASS]
    mounted = CLASS_USAGE[DeviceClass.MOUNTED_TERMINAL_CLASS]
    phone = CLASS_USAGE[DeviceClass.PHONE_CLASS]
    floor = config.coverage.satellites_for_full_coverage
    below_phone_floor = (
        "; this run sets the phone class below that floor, at "
        f"${arpu.phone_class_price_usd_month:g} a month (a scenario setting, not a haircut)"
        if arpu.phone_class_price_usd_month < PHONE_CLASS_PRICE_FLOOR_USD_MONTH
        else ""
    )
    lines = [
        ECOSYSTEM_ASSUMPTION_NOTE,
        (
            f"Operations cost is assumed zero ({IRIDIUM_OPERATIONS_COST_MUSD} USD millions per "
            "year): an explicit investor-instructed assumption, a fixed operations line to "
            "research and add later, stated here rather than silently omitted."
        ),
        (
            f"People come from the promoted saturation curve ({curve.schema_version}), "
            "computed once with the band in full-time use at the "
            f"{curve.parameters.shell.reference_aperture_m2:g} m^2 reference panel and the held "
            f"{curve.parameters.spectrum_mhz:g} MHz: each class's people at a fleet are the "
            "curve's capacity there, times the downlink share d, times the panel factor, over "
            "the class's busy-hour load per person (its rate while active times its busy-hour "
            "share). Beams over oceans and empty land carry no one."
        ),
        (
            "The reuse calibration is "
            f"{curve.parameters.shell.reuse_calibration_gbps_per_mhz_per_se:g} Gbps per MHz per "
            "unit of spectral efficiency at the "
            f"{curve.parameters.shell.reference_aperture_m2:g} m^2 reference panel, an estimate "
            "(COMM-410, COMM-411): it sets each class's satellite peak and the curve's beams per "
            "satellite."
        ),
        (
            f"The downlink share d is {dials.saturation.downlink_share:g}, the time-division "
            "duplex band's downlink time share (ADR 008): every people and capacity figure but "
            "the satellite's peak scales with it, and the uplink holds the rest of the frame."
        ),
        (
            f"The panel is {dials.aperture_m2:g} m^2, applied linearly on the curve: a panel "
            f"factor of {panel_factor:.4g} on people, useful beams, capacity and maximum use, "
            "never on the saturation numbers, the ocean factor or satellites per launch. "
            f"{PANEL_RULE_LIMITS_NOTE}"
        ),
        (
            "The fleet is every comms launch the cadence share allows "
            f"({config.comms_cadence.share_of_fleet * _PERCENT:g} percent of the Neutron "
            "cadence) times "
            f"{config.satellite.satellites_per_launch} satellites per launch, each cohort "
            f"living {config.satellite.satellite_lifetime_years} years: there is no fleet "
            "target and no cap, and no saturation number sizes, caps, stops or slows the build."
        ),
        (
            "Satellites per launch is a direct scenario setting (bounds "
            f"{SATELLITES_PER_LAUNCH_MIN} to {SATELLITES_PER_LAUNCH_MAX}); this run flies "
            f"{config.satellite.satellites_per_launch}. The validated counts are "
            f"{SATELLITES_PER_LAUNCH_BLOCK_UPGRADE} with the Neutron block upgrade assumed from "
            "the first launch, for the stack kept in the fairing's cylinder at calculation C's "
            "pitch on a rod-held base (COMM-713), and "
            f"{SATELLITES_PER_LAUNCH_NO_UPGRADE} without the upgrade, the mass-bound count "
            "today (COMM-712)."
        ),
        (
            "Every seat is sold: each year each device class serves every person its living "
            "fleet carries, and each class's column is the whole fleet sold to that class "
            "alone, so revenue rises with the fleet."
        ),
        (
            "Each class's price is held flat: the small terminal "
            f"${arpu.small_terminal_class_price_usd_month:g}, the mounted terminal "
            f"${arpu.mounted_terminal_class_price_usd_month:g} and the phone class "
            f"${arpu.phone_class_price_usd_month:g} a month. The phone class's floor is the "
            f"investor's ${PHONE_CLASS_PRICE_FLOOR_USD_MONTH:g} a month, which no price haircut "
            f"goes below{below_phone_floor}. A lower price or a "
            "smaller market is a division in the conclusions, never in the model: a price "
            "haircut divides revenue only, a market haircut people and revenue, and every "
            "margin is re-derived against the same fleet cost, never divided or averaged."
        ),
        (
            "Each class's own margin is its own revenue against the whole fleet's annualized "
            "build and launch cost (operations zero, above), null in a year with no revenue; "
            "the IoT lines are never inside it."
        ),
        (
            "Each class's usage is the investor's (2026-10-04): the small terminal "
            f"{small.active_rate_mbps:g} Mbps while active, "
            f"{small.concurrency_peak * _PERCENT:g} percent of users at the busy hour and "
            f"{small.concurrency_offpeak * _PERCENT:g} percent off-peak; the mounted terminal "
            f"{mounted.active_rate_mbps:g} Mbps, {mounted.concurrency_peak * _PERCENT:g} and "
            f"{mounted.concurrency_offpeak * _PERCENT:g} percent; the phone class "
            f"{phone.active_rate_mbps:g} Mbps, {phone.concurrency_peak * _PERCENT:g} and "
            f"{phone.concurrency_offpeak * _PERCENT:g} percent."
        ),
        (
            "Spectral efficiency is estimate-tier: the small terminal's band "
            f"{SMALL_TERMINAL_CLASS_SE_LOW:g} to {SMALL_TERMINAL_CLASS_SE_HIGH:g}, the mounted "
            f"terminal's {MOUNTED_TERMINAL_CLASS_SE_LOW:g} to {MOUNTED_TERMINAL_CLASS_SE_HIGH:g} "
            f"and the phone class's {PHONE_CLASS_SE_LOW:g} to {PHONE_CLASS_SE_HIGH:g} bps/Hz, "
            "each class read at its central value "
            f"({CLASS_SE_CENTRAL[DeviceClass.SMALL_TERMINAL_CLASS]:g}, "
            f"{CLASS_SE_CENTRAL[DeviceClass.MOUNTED_TERMINAL_CLASS]:g} and "
            f"{CLASS_SE_CENTRAL[DeviceClass.PHONE_CLASS]:g})."
        ),
        (
            "IoT is two fixed lines, each its own revenue line and never inside a class's "
            f"margin: minimal-packet IoT, {MINIMAL_PACKET_IOT_DEVICES:,} devices at "
            f"${arpu.minimal_packet_iot_price_usd_month:g} a month "
            f"({MINIMAL_PACKET_IOT_MESSAGES_PER_DAY} messages of "
            f"{MINIMAL_PACKET_IOT_MESSAGE_BYTES} bytes a day), and data IoT, "
            f"{DATA_IOT_DEVICES:,} devices at ${arpu.data_iot_price_usd_month:g} a month "
            f"({DATA_IOT_BURSTS_PER_DAY} bursts of {DATA_IOT_BURST_BYTES // _BYTES_PER_KB} KB a "
            "day beside the messages). Their counts are fixed (ADR 007): they never move with "
            "the fleet, a class, d, the panel or satellites per launch."
        ),
        (
            f"The coverage floor ({floor} satellites) gates every sale: nothing is sold, by a "
            "class or an IoT line, in a year whose living fleet is below it, and from the first "
            "year at it every class and both IoT lines are sold in full (a step with no "
            "phase-in)."
        ),
        "Government is left out of revenue: the model carries no government count, price or line.",
        (
            f"The readings: the coverage floor ({floor}); {RETIRED_CAP_READING_FLEET:,} "
            "satellites, the retired cap, kept for comparison; the horizon-end full-cadence "
            "reach (the final year's living fleet, priced at the final year's annualized cost); "
            f"and the steady state beyond the {config.metadata.horizon_years}-year horizon (the "
            "final year's comms launches times satellites per launch times the life). The "
            "coverage floor, the retired cap and the steady state are priced at the final "
            "year's cost per satellite-year; a reading below the coverage floor sells nothing."
        ),
        (
            "The IoT check spreads each line's devices over the phone class's useful beams "
            "(IoT devices are low gain, so their reuse follows the phone rule) and reads its "
            "daily volume against a beam's uplink (the frame's share 1 - d), with and without a "
            f"{IOT_MAC_EFFICIENCY * _PERCENT:g} percent MAC efficiency; its access attempts a "
            "second a beam, one per message or burst, against a random-access window of "
            f"{IOT_RANDOM_ACCESS_WINDOW_DEVICES_LOW} to {IOT_RANDOM_ACCESS_WINDOW_DEVICES_HIGH:,} "
            f"devices (COMM-654) at an assumed {IOT_RANDOM_ACCESS_WINDOWS_PER_SECOND} window a "
            "second (no source gives a window rate); "
            "and, for minimal-packet IoT, its messages' channel time on "
            f"{NB_IOT_TONE_HZ * _TONE_KHZ_PER_HZ:g} kHz tones at {IOT_MESSAGE_AIRTIME_LOW_S:g} "
            f"to {IOT_MESSAGE_AIRTIME_HIGH_S:g} s a message (COMM-714, COMM-719)."
        ),
        (
            "Each class's saturation number is a spectrum bound reported beside the launch "
            "cadence, never a build target or a cap; a fleet past a class's last computed row "
            "is refused, never extrapolated or clamped. The curve's stated limits are carried "
            "in saturation.limits."
        ),
        (
            "The Iridium model is the MSS lane (owned L-band, purpose-built or in-chipset "
            "devices), never the cellular direct-to-cell unmodified-phone lane (the "
            "High-Bandwidth Cellular Pure Play model)."
        ),
    ]
    if dials.aperture_m2 > APERTURE_VALIDATED_STACK_LIMIT_M2:
        lines.append(APERTURE_STACK_CAVEAT_NOTE)
    return tuple(lines)


def _first_non_finite(value: object, path: str) -> tuple[str, float] | None:
    """Return the first float in a record that is an infinity or a NaN, with its path.

    The walk goes depth first in field order: a dataclass by its fields, a mapping by its
    keys, a tuple or a list by index; any other value (an int, a string, an enum, None) holds
    no float. None when every float is finite.
    """
    if isinstance(value, float):
        return None if math.isfinite(value) else (path, value)
    children: list[tuple[str, object]]
    if is_dataclass(value) and not isinstance(value, type):
        children = [(f"{path}.{field.name}", getattr(value, field.name)) for field in fields(value)]
    elif isinstance(value, Mapping):
        children = [(f"{path}[{key}]", child) for key, child in value.items()]
    elif isinstance(value, tuple | list):
        children = [(f"{path}[{index}]", child) for index, child in enumerate(value)]
    else:
        return None
    for child_path, child in children:
        found = _first_non_finite(child, child_path)
        if found is not None:
            return found
    return None


def _refuse_a_number_that_is_not_finite(
    run: IridiumRun, config: CommsConfig, dials: IridiumDials
) -> None:
    """Refuse a run whose records hold an infinity or a NaN (an invariant, checked last).

    The shared fleet-and-cost record is walked first, then the Iridium record. The fleet
    record's numbers are its cost lines, which scale with the cost settings alone; the Iridium
    record's scale with the panel (people, beams, capacity and the IoT check), the prices
    (revenue) and the cost settings (the margins, the readings' costs and the cost per
    satellite-year). No bound moves: a setting this far out is one the model cannot compute.

    Raises:
        ValueError: Naming the first field that is not finite, its value, and the settings its
            record scales with, each with its value.
    """
    cost_settings = (
        f"satellite.satellite_build_cost_musd ({config.satellite.satellite_build_cost_musd!r})",
        *(
            f"launch_cost.{name} ({setting!r})"
            for name, setting in config.launch_cost.model_dump().items()
        ),
    )
    settings: tuple[str, ...] = cost_settings
    record = "the fleet-and-cost record"
    found = _first_non_finite(run.fleet, "fleet")
    if found is None:
        found = _first_non_finite(run.iridium, "iridium")
        if found is None:
            return
        record = "the Iridium record"
        settings = (
            f"iridium.aperture_m2 ({dials.aperture_m2!r})",
            *(
                f"iridium.arpu.{name} ({price!r})"
                for name, price in dials.arpu.model_dump().items()
            ),
            *cost_settings,
        )
    path, value = found
    raise ValueError(
        f"the run's {path} is {value!r}, not a finite number: {record} scales with "
        f"{', '.join(settings)}, and one of them is past what the model can compute"
    )


def run_iridium_model(config: CommsConfig, curve: SaturationCurve) -> IridiumRun:
    """Run an Iridium config on its saturation curve: the Iridium entry.

    On every run, in this order: the config is narrowed to its Iridium dials
    (:func:`iridium_dials_of`); the curve is checked against the inputs those dials imply
    (``check_curve_matches(saturation_inputs_for(dials), curve)``), so a curve computed for
    other inputs (another held spectrum, say) is never read; the panel factor (the scenario's
    panel over the curve's reference panel) is formed; the shared fleet-and-cost loop flies
    the full cadence (:func:`full_cadence_rule`); then the years, the readings and the IoT
    check, each class's block and the books are read from the curve and priced (the module
    docstring's steps), and the stated assumptions written.

    Args:
        config: A communications config with an ``iridium:`` block.
        curve: The saturation curve computed for the config's inputs (the one its
            ``iridium.saturation.curve_path`` names, loaded with
            :func:`communications.saturation_curve.load_saturation_curve`).

    Returns:
        The run's :class:`IridiumRun`: the shared fleet-and-cost record and the Iridium record.

    Raises:
        NotAnIridiumConfigError: If the config has no ``iridium:`` block.
        pydantic.ValidationError: If the config does not validate whole (a setting a
            ``model_copy`` carried past the validators), naming the field.
        SaturationCurveMismatchError: If the curve was computed for other inputs, naming the
            first field that differs.
        CurveBeyondLastRowError: If a year's living fleet, or a reported fleet, lies past a
            class's last row, naming the fleet, the class and the last row, and before them
            the year's fiscal year, or the reading's label, fleet and the settings that set
            it.
        ValueError: If the panel factor is not a positive finite number (a panel so small its
            ratio to the reference panel underflows to 0), naming ``iridium.aperture_m2``; or
            if the run's records would hold an infinity or a NaN (a panel, a price or a cost
            setting past what the model can compute: a panel of 1e-305 or 2.5e300 m^2, say,
            or a price of 5e-324 dollars), naming the first such field (the fleet-and-cost
            record walked first), its value and the settings its record scales with, each
            with its value (the panel, the five prices and the cost settings; the cost
            settings alone for the fleet-and-cost record). No run is returned.
        OverflowError: If the people at a fleet overflow to infinity and cannot become a
            count (a panel of about 1e308 m^2), before any record is built.
    """
    dials = iridium_dials_of(config)
    check_curve_matches(saturation_inputs_for(dials), curve)
    logger.debug("the saturation curve %s matches the run's inputs", curve.input_hash)
    panel_factor = _panel_factor(dials, curve)
    fleet = run_fleet_loop(
        config, full_cadence_rule, satellites_per_launch=config.satellite.satellites_per_launch
    )
    coverage_floor = config.coverage.satellites_for_full_coverage
    downlink_share = dials.saturation.downlink_share
    prices = MappingProxyType(
        {device_class: _class_price(dials.arpu, device_class) for device_class in DeviceClass}
    )
    books = _fixed_books(dials.arpu)
    years = _years(
        fleet,
        curve,
        coverage_floor=coverage_floor,
        downlink_share=downlink_share,
        panel_factor=panel_factor,
        prices=prices,
        books=books,
    )
    final = fleet.years[-1]
    cost_per_satellite_year_musd = per_satellite_annual_cost_musd(
        satellite_build_cost_musd=config.satellite.satellite_build_cost_musd,
        launch_cost_per_launch_musd=final.launch_cost_per_launch_musd,
        satellites_per_launch=config.satellite.satellites_per_launch,
        satellite_lifetime_years=config.satellite.satellite_lifetime_years,
    )
    readings = tuple(
        _reading(
            curve,
            reported,
            coverage_floor=coverage_floor,
            downlink_share=downlink_share,
            panel_factor=panel_factor,
            prices=prices,
        )
        for reported in _reported_fleets(
            config,
            fleet,
            coverage_floor=coverage_floor,
            cost_per_satellite_year_musd=cost_per_satellite_year_musd,
        )
    )
    classes = tuple(
        _class_record(
            curve,
            device_class,
            dials,
            panel_factor=panel_factor,
            price_usd_per_month=prices[device_class],
            final_living_fleet=final.living_fleet,
            cost_per_satellite_year_musd=cost_per_satellite_year_musd,
        )
        for device_class in DeviceClass
    )
    record = IridiumRecord(
        scenario_name=dials.scenario_name,
        spectrum_mhz=dials.spectrum_mhz,
        aperture_m2=dials.aperture_m2,
        satellites_per_launch=config.satellite.satellites_per_launch,
        operations_cost_musd=IRIDIUM_OPERATIONS_COST_MUSD,
        ecosystem_assumption=ECOSYSTEM_ASSUMPTION_NOTE,
        coverage_floor_reached_year=next(
            (year.year for year in fleet.years if _sells(year.living_fleet, coverage_floor)),
            None,
        ),
        cost_per_satellite_year_musd=cost_per_satellite_year_musd,
        classes=classes,
        years=years,
        fixed_books=books,
        saturation=SaturationRecord(
            curve_path=dials.saturation.curve_path,
            curve_schema_version=curve.schema_version,
            curve_version_stamp=curve.version_stamp,
            input_hash=curve.input_hash,
            downlink_share=downlink_share,
            panel_factor=panel_factor,
            readings=readings,
            band_saturation_numbers=MappingProxyType(
                {band.point.name: band.markers.saturation_number for band in curve.bands}
            ),
            iot_check=_iot_check(readings, dials, coverage_floor=coverage_floor),
            limits=curve.limits,
        ),
        assumptions=_assumptions(config, dials, curve, panel_factor=panel_factor),
    )
    run = IridiumRun(fleet=fleet, iridium=record)
    _refuse_a_number_that_is_not_finite(run, config, dials)
    logger.debug(
        "Iridium run: FY%d living fleet %d at $%.4fM a satellite-year; the floor reached %s",
        final.year,
        final.living_fleet,
        cost_per_satellite_year_musd,
        record.coverage_floor_reached_year,
    )
    return run


__all__ = [
    "COVERAGE_FLOOR_LABEL",
    "HORIZON_END_LABEL",
    "RETIRED_CAP_LABEL",
    "STEADY_STATE_LABEL_FORMAT",
    "BindingLimit",
    "ClassRates",
    "ClassReadingRecord",
    "ClassRecord",
    "ClassYearRecord",
    "FixedBooksRecord",
    "IotCheckRecord",
    "IotCheckRowRecord",
    "IridiumRecord",
    "IridiumRun",
    "MarginalIntervalRecord",
    "NotAnIridiumConfigError",
    "ReadingRecord",
    "SaturationRecord",
    "YearRecord",
    "derive_iridium_per_user_rates",
    "derive_per_satellite_capacity_gbps",
    "full_cadence_rule",
    "iridium_dials_of",
    "run_iridium_model",
]
