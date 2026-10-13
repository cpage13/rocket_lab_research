"""Tests for the Iridium model (formerly Model B): L-band max-outcome, the MSS lane.

The end-to-end specification of the Iridium family, through the engine and the artifact. Every
Iridium run goes through the Iridium entry, ``run_iridium_model(config, curve)``: on the
committed saturation curve or, for dials it was not computed for and for the tripwire, on a
synthetic curve stamped for the dials (``conftest.py``). The suite covers each class's physics
(the class-to-SE mapping, the satellite's peak, people per beam, the downlink pool and the
per-user rates); IoT as capacity (ADR 011): each IoT class's engineering usage and its loads, the
worked capacity case, the edge views, each class's useful beams and IoT's room in every year and
at every reading; the entries' refusals and the identity check; the tripwire in its new form (an
Iridium run and a cellular run whose target the horizon never reaches share the fleet-and-cost
record whole, and that record's values are frozen); the headline, every class alone and side by
side, against the usage check's table (below; the terminals' revenue restated at the investor's
prices of 2026-10-07, $10 and $50: the small and mounted terminals within 5 percent, the phone
class within 1 percent; the fleets and costs exactly); the no-upgrade bracket; revenue rising
with the fleet; the floor rule; the three class prices and no government key; each class's
revenue its people at its price; a share that never launches; the downlink share; the panel
setting; every class in one run, in order; a fleet past a class's last row (the engine and the
command); a run that would hold a number that is not finite, refused naming the settings; the
readings and the reported fleets (the retired cap's reading its own constant); the marginal
intervals (hand-worked, and their verdicts on the committed curve at the investor's prices),
with d = 1's IoT room; a saturation number beside the cadence, never a cap; the scenario YAML;
the stated assumptions; the promoted export frozen on ``iridium-v7``; the drift guard that
regenerates the committed artifact byte for byte; and the artifact's models reading back their
own schema only.

Where the targets come from. The fleets and costs are exact arithmetic, worked beside them. The
people and revenue targets and the marginal chords come from the usage check: an independent
computation of the investor's usage (2026-10-04) made before the module was built, on a
prototype of its allocation (``check_usage_10_04_output.txt`` (local), in the investor's
records). "The usage check's table" is its per-class people and revenue at FY2031, FY2033,
FY2036, the steady state, the coverage floor and 2,000; "its rates" are each class's pool and
per-user rates; "its chords" are the prototype's marginal chords between rows and their
verdicts. A class's "first stop" is its first chord below cost: the phone class's is the usage
check's, and the two terminals' come from the prototype's own rows at the earlier prices
(``p6_targets_output.txt`` (local)). The bracket at 15 per launch comes from the investor's
table of the new defaults (``revenue_new_defaults_10_03_output.txt`` (local)). The IoT usage's
loads are worked by hand; the worked capacity case is the build's own print at full precision
(``A_capacity_print.txt`` (local)), equal to the product-case design's probe P6 to every
printed digit.

The values these tests freeze from the committed curve (people, the markers) move only with a
re-promotion of the curve, which re-freezes them on purpose (the re-promotion rule). Each class's
column is the whole fleet sold to that class alone; the classes run small terminal, mounted
terminal, phone class. The Iridium model is the MSS lane (purpose-built or in-chipset devices on
owned L-band), never the cellular unmodified-phone lane (the High-Bandwidth Cellular Pure Play
model).
"""

from __future__ import annotations

import dataclasses
import json
import logging
import math
import re
from collections.abc import Callable
from pathlib import Path

import pytest
from pydantic import ValidationError

from common.cli import EXIT_ERROR
from common.file_io import ARTIFACT_FILE_END, render_artifact_json
from communications import iridium, json_output
from communications.config import (
    CommsConfig,
    CoverageDials,
    IridiumArpuDials,
    IridiumDials,
    SatelliteDials,
    load_comms_config,
)
from communications.constants import (
    APERTURE_STACK_CAVEAT_NOTE,
    BASE_YEAR_DEFAULT,
    CLASS_SE_CENTRAL,
    CLASS_USAGE,
    ECOSYSTEM_ASSUMPTION_NOTE,
    HORIZON_YEARS_DEFAULT,
    IOT_ENGINEERING_USAGE,
    IRIDIUM_SCENARIO_NAME_DEFAULT,
    ORBIT_ALTITUDE_KM_SCENARIO,
    ORBIT_INCLINATION_DEG_SCENARIO,
    ORBIT_SCENARIO_BASIS,
    ORBIT_SCENARIO_SOURCE_STATUS,
    PANEL_RULE_LIMITS_NOTE,
    RETIRED_CAP_READING_FLEET,
    SATELLITES_PER_LAUNCH_MAX,
    SATELLITES_PER_LAUNCH_MIN,
    DeviceClass,
    IotClass,
    IotView,
)
from communications.engine import (
    CellularTrajectory,
    NotACellularConfigError,
    run_comms_model,
)
from communications.iridium import (
    COVERAGE_FLOOR_LABEL,
    HORIZON_END_LABEL,
    RETIRED_CAP_LABEL,
    BindingLimit,
    BindingLimitUnmeasuredError,
    ClassReadingRecord,
    ClassRecord,
    ClassYearRecord,
    IridiumRun,
    MarginalIntervalRecord,
    NotAnIridiumConfigError,
    derive_iridium_per_user_rates,
    derive_per_satellite_capacity_gbps,
    iot_room,
    iridium_dials_of,
    run_iridium_model,
)
from communications.json_output import (
    MODEL_NAME,
    IridiumModelArtifact,
    build_iridium_artifact,
    export_iridium_json,
    main,
)
from communications.saturation_curve import (
    CurveBeyondLastRowError,
    SaturationCurve,
    SaturationCurveError,
    SaturationCurveMismatchError,
    class_curve_of,
    read_fleet,
)

SMALL = DeviceClass.SMALL_TERMINAL_CLASS
MOUNTED = DeviceClass.MOUNTED_TERMINAL_CLASS
PHONE = DeviceClass.PHONE_CLASS
CLASS_ORDER = [SMALL, MOUNTED, PHONE]
"""Every block's class order (the charter's Presentation rule): small terminal, mounted terminal,
phone class."""

# ---------------------------------------------------------------------------
# Each class's physics (the usage check's rates), class order.
# ---------------------------------------------------------------------------
HELD_SPECTRUM_MHZ = 8.0
REFERENCE_PANEL_M2 = 25.0
DEFAULT_PANEL_M2 = 15.4
DEFAULT_PANEL_FACTOR = 0.616  # 15.4 / 25.
DEFAULT_DOWNLINK_SHARE = 0.67
CLASS_SE = (2.0, 2.5, 0.65)
PEAK_GBPS_AT_REFERENCE = (2.4, 3.0, 0.78)  # 8 x SE x 0.15.
PEAK_GBPS_AT_DEFAULT = (1.4784, 1.848, 0.48048)  # x 0.616.
BEAM_POOL_MBPS = (10.72, 13.4, 3.484)  # 8 x SE x 0.67.
PEAK_RATE_MBPS = (2.0, 5.0, 0.75)  # each class's rate while active.
OFFPEAK_RATE_MBPS = (10.0, 13.4, 3.484)  # min(pool, rate x peak / off-peak).
PEOPLE_PER_BEAM_AT_FULL_DOWNLINK = (320.0, 40.0, 832.0 / 3.0)  # 8 x SE / the busy-hour load.
CLASS_USAGE_SETTLED = ((2.0, 0.025, 0.005), (5.0, 0.10, 0.02), (0.75, 0.025, 0.005))
"""The investor's usage (2026-10-04), class order: each class's rate while active (Mbps), its
busy-hour share and its off-peak share, as literals (the off-peak shares of the mounted terminal
and the phone class reach no rate, since the pool binds, so only these literals pin them)."""

# ---------------------------------------------------------------------------
# The shipped scenario's fleet and cost (16 per launch, the all-in share, the flat $13.0M
# launch and $1.0M build, a five-year life): exact, since they do not read the curve.
# ---------------------------------------------------------------------------
MODEL_YEARS = tuple(range(2026, 2037))
COMMS_LAUNCHES = (0, 2, 3, 5, 9, 14, 22, 35, 51, 70, 90)
LIVING_FLEET = (0, 32, 80, 160, 304, 528, 848, 1_360, 2_096, 3_072, 4_288)
COVERAGE_FLOOR = 340
FLOOR_YEAR = 2031
LAUNCHES_THROUGH_FY2036 = 301
SATELLITES_THROUGH_FY2036 = 4_816
TOTAL_COST_MUSD = 8_729.0  # 4,816 x 1.0 + 301 x 13.0.
FY2036_REPLACEMENT_COST_MUSD = 406.0  # the FY2031 cohort: 224 x 1.0 + 14 x 13.0.
FY2031_COHORT_SATELLITES = 224
COST_PER_SATELLITE_YEAR_MUSD = 0.3625  # (1.0 + 13.0 / 16) / 5.
STEADY_STATE_FLEET = 7_200  # 90 x 16 x 5.
ANNUAL_COST_MUSD = {2031: 191.4, 2033: 493.0, 2036: 1_554.4}

# ---------------------------------------------------------------------------
# The prices (the investor, 2026-10-07: "Yes, let's use the $10 and $50"): the small terminal
# $10 and the mounted terminal $50 a month, held flat (the earlier prices were $15 and $100);
# the phone class $15, its floor. The usage check priced the terminals at the earlier prices, so
# their revenue targets below are its table's restated: its revenue over the earlier price is
# its people x 12, times the new price.
# ---------------------------------------------------------------------------
CLASS_PRICES = {SMALL: 10.0, MOUNTED: 50.0, PHONE: 15.0}
SMALL_RESTATED = 10.0 / 15.0  # the usage check's small terminal revenue at $15, restated at $10.
MOUNTED_RESTATED = 50.0 / 100.0  # its mounted terminal revenue at $100, restated at $50.

# ---------------------------------------------------------------------------
# The headline: each class alone, side by side (the usage check's table), each cell (people
# in millions, revenue $M a year), class order; each own margin is checked as its revenue
# against the fleet's cost. Tolerances: the directional classes' people and revenue within 5
# percent, the phone class's within 1 percent.
# ---------------------------------------------------------------------------
DIRECTIONAL_TOLERANCE = 0.05
PHONE_TOLERANCE = 0.01
HEADLINE_ROWS = (
    (
        "FY2031",
        528,
        191.4,
        ((4.14, 744.8 * SMALL_RESTATED), (0.53, 631.8 * MOUNTED_RESTATED), (3.56, 640.8)),
    ),
    (
        "FY2033",
        1_360,
        493.0,
        ((9.91, 1_783.9 * SMALL_RESTATED), (1.30, 1_554.1 * MOUNTED_RESTATED), (8.47, 1_524.3)),
    ),
    (
        "FY2036",
        4_288,
        1_554.4,
        ((24.65, 4_436.8 * SMALL_RESTATED), (3.57, 4_286.4 * MOUNTED_RESTATED), (20.81, 3_746.2)),
    ),
    (
        "steady state",
        7_200,
        2_610.0,
        ((33.79, 6_082.9 * SMALL_RESTATED), (5.29, 6_345.2 * MOUNTED_RESTATED), (28.59, 5_145.7)),
    ),
)
READING_TARGETS = (
    (
        340,
        123.25,
        ((2.73, 491.1 * SMALL_RESTATED), (0.34, 413.6 * MOUNTED_RESTATED), (2.34, 421.8)),
    ),
    (
        2_000,
        725.0,
        ((13.89, 2_500.3 * SMALL_RESTATED), (1.85, 2_223.2 * MOUNTED_RESTATED), (11.71, 2_107.0)),
    ),
)
HISTORICAL_FLEET_CAP = 2_000  # the cap the Iridium model inherited through iridium-v5 (ADR 005).

# The module's own values on the committed curve (the re-promotion rule re-freezes them).
FROZEN_PEOPLE = {
    2031: (4_139_229, 526_557, 3_560_271),
    2033: (9_941_462, 1_289_233, 8_470_209),
    2036: (24_607_046, 3_527_090, 20_823_193),
}
FROZEN_STEADY_STATE_PEOPLE = (33_755_488, 5_197_846, 28_622_500)
FROZEN_SATURATION_NUMBERS = (19_995, None, 20_652)
FROZEN_MOUNTED_NOT_REACHED_BY = 55_407
FROZEN_BAND_SATURATION_NUMBERS = {
    "taper": 13_810,
    "taper_and_spacing": 10_223,
    "density_10_per_km2": 19_751,
    "density_100_per_km2": 17_814,
    "grid_0p5_deg": 21_613,
    "beams_48": None,
}
SMALL_PEOPLE_AT_2000_DEFAULT_PANEL = 13_870_568  # an absolute people target at 15.4 m^2.

# ---------------------------------------------------------------------------
# The no-upgrade bracket (15 per launch; the investor's table of the new defaults, its second).
# ---------------------------------------------------------------------------
BRACKET_FLEETS = {2031: 495, 2033: 1_275, 2036: 4_020}
BRACKET_COSTS_MUSD = {2031: 184.8, 2033: 476.0, 2036: 1_500.8}
BRACKET_STEADY_STATE = (6_750, 2_520.0)
BRACKET_COST_PER_SATELLITE_YEAR_MUSD = (1.0 + 13.0 / 15) / 5  # 0.3733...

# ---------------------------------------------------------------------------
# The tripwire's frozen record: the cellular defaults with the subscriber target at 150,000,000
# (a 2,000-satellite fleet target the 0.18 share never reaches), flying every launch the cadence
# allows at 12 a launch on the default launch-cost curve, whose price moves with the whole-fleet
# cadence: the absolute pin on the shared loop's cadence-indexed launch price (the Iridium
# scenario flies a flat $13.0M launch, which would hide it). The values the review of 2026-10-12
# measured on the code, frozen here as new pins; before its rewrite the tripwire froze one value
# only, the cellular default's cash cost a person ($7.951337204338448, on the 10,000,000 target),
# which ``test_subscribers.py`` pins again.
# ---------------------------------------------------------------------------
TRIPWIRE_LIVING_FLEET = (0, 0, 12, 24, 48, 84, 132, 192, 288, 420, 576)
TRIPWIRE_TOTAL_COST_MUSD = 1594.5941525706626  # cumulative build and launch cash through FY2036.
TRIPWIRE_FY2036_REPLACEMENT_COST_MUSD = 79.51337204338448
"""The FY2036 cash replacement, $M: the FY2031 cohort's 36 satellites at $1.05M plus its 3
launches at the FY2036 whole-fleet cadence's price (90 launches, $13.904M), frozen exactly."""

# ---------------------------------------------------------------------------
# The marginal intervals' verdicts at full price at the investor's prices of 2026-10-07, each
# derived from the curve's people on consecutive rows x the price x 12 against $0.3625M a
# satellite-year (the usage check's chords, last paying through 8,010, 11,990 and 8,010, were at
# the earlier $15 and $100; the phone's holds), and each class's first stop at the prototype's
# endpoints at the new price (a terminal's: the prototype's own chord over 5,402 to 8,010 on its
# rows, at the earlier price, times the new price over it).
# ---------------------------------------------------------------------------
SMALL_MODULE_LAST_PAYING_ROW = 6_006  # the module's finer grid splits 5,402 to 8,010.
SMALL_PROTOTYPE_LAST_PAYING_ROW = 5_402
MOUNTED_LAST_PAYING_ROW = 5_402  # the module's rows and the prototypes' endpoints agree.
PHONE_LAST_PAYING_ROW = 8_010
FIRST_STOP_CHORDS = (
    (SMALL, 5_402, 8_010, 0.3257),  # the prototype's $0.4885M at $15 x 10 / 15.
    (MOUNTED, 5_402, 8_010, 0.3276),  # the prototype's $0.6552M at $100 x 50 / 100.
    (PHONE, 8_010, 10_000, 0.2902),
)

V6_REMOVED_KEYS = frozenset(
    {
        "annual_revenue_musd",
        "arpu_margin_vs_steady_state_cost_pct",
        "arpu_revenue_total_musd",
        "binding_regime",
        "build_completes_in_horizon",
        "built_fleet_annual_cost_musd",
        "cost_per_subscriber_annualized_usd",
        "count",
        "cumulative_launches_to_completion",
        "effective_satellites_per_launch",
        "final_year_cash_cost_per_subscriber_usd",
        "fleet_aggregate_capacity_gbps",
        "fleet_target",
        "full_coverage_reached_year",
        "government",
        "iot_devices",
        "mix_pct",
        "people_capacity_living_fleet_final_year",
        "people_capacity_target_fleet",
        "premium",
        "revenue_arpu_buckets",
        "standard",
        "stated_assumptions",
        "steady_state_annual_cost_musd",
        "subscribers_per_satellite",
        "subscribers_served",
        "total_build_and_hold_cost_musd",
        "total_connections",
    }
)
"""Every key name the ``iridium-v5`` artifact carried that ``iridium-v6`` carried nowhere, at any
depth (the committed v5 artifact against v6, 29 names), but ``iot``, which ``iridium-v7`` brought
back under a new meaning (each year's and each reading's IoT room, ADR 011), so 28 here: the
target, regime, completion and built-fleet fields, the per-person cost fields, the density, the
fleet aggregate, the served base, the living fleet's people capacity, the IoT passthrough's
``iot_devices``, the renamed cost and per-launch fields, and the four-bucket block with its inner
keys. (A later schema that brings one back under a new meaning names it here.)"""

YEAR_KEYS = ("year", "comms_launches_flown", "living_fleet", "annual_cost_musd", "classes", "iot")
"""Each ``years`` entry's keys in ``iridium-v7``, in order (IoT foundation v1)."""

CLASS_YEAR_KEYS = (
    "device_class",
    "useful_beams",
    "people_served",
    "revenue_musd",
    "own_margin_pct",
)
"""Each year's class line's keys in ``iridium-v7``, in order: the useful beams after the class."""

IOT_ROOM_KEYS = (
    "uplink_bits_per_second",
    "uplink_payload_bits_per_second",
    "access_attempts_per_second_low",
    "access_attempts_per_second_high",
    "single_tone_seconds_per_second",
    "classes",
)
"""An IoT room block's keys (each year's and each reading's ``iot``), in order."""

IOT_CLASS_CAPACITY_KEYS = (
    "iot_class",
    "devices_by_payload_bits",
    "devices_by_random_access",
    "devices_by_single_tone_time",
    "device_capacity",
    "binding_view",
)
"""One IoT class's capacity block's keys, in order."""

SATURATION_KEYS = (
    "curve_path",
    "curve_schema_version",
    "curve_version_stamp",
    "input_hash",
    "downlink_share",
    "panel_factor",
    "readings",
    "band_saturation_numbers",
    "limits",
)
"""The saturation block's keys in ``iridium-v7``, in order."""

READING_KEYS = ("label", "fleet", "fleet_annual_cost_musd", "classes", "iot")
"""Each reading's keys in ``iridium-v7``, in order: IoT's room after the classes."""

IOT_PHYSICS_FROZEN: dict[str, int | float] = {
    "iot_message_bytes": 340,
    "iot_burst_bytes": 100_000,
    "iot_mac_efficiency": 0.20,
    "iot_random_access_window_devices_low": 57,
    "iot_random_access_window_devices_high": 1_650,
    "iot_random_access_windows_per_second": 1,
    "iot_tone_hz": 3_750.0,
    "iot_message_airtime_low_s": 4.0,
    "iot_message_airtime_high_s": 7.0,
}
"""The physics block's nine IoT constants, frozen as IoT foundation v1 states them, in order after
the ecosystem assumption: the message and burst sizes (COMM-620; the investor's usage), the MAC
efficiency (COMM-659), the random-access window's two ends and its rate (COMM-654; an
assumption), the NB-IoT tone (COMM-714) and the message airtime's two ends (COMM-719)."""

IOT_KEYS_V7 = frozenset({"iot", "iot_class", "iot_classes", *IOT_PHYSICS_FROZEN})
"""Every key name ``iridium-v7`` writes that holds ``iot``, at any depth: each year's and each
reading's room (``iot``), the IoT classes and each capacity's class (``iot_classes``,
``iot_class``) and the physics block's nine constants, twelve in all. The frozen baseline holds
the file's such keys to exactly these, so no other IoT key (one for devices sold, a price,
revenue or the removed check, under any name) reaches the artifact unseen."""

SyntheticCurve = Callable[[IridiumDials], SaturationCurve]
"""The ``synthetic_saturation_curve`` fixture: Iridium dials in, a curve stamped for them out."""

ShortCurve = Callable[[IridiumDials, int], SaturationCurve]
"""The ``short_saturation_curve`` fixture: dials and a last row in, the curve cut at it."""


def _merged(base: dict[str, object], changes: dict[str, object]) -> dict[str, object]:
    """Return ``base`` with ``changes`` applied key by key: a nested block in ``changes`` replaces
    only the keys it names, at any depth, and keeps the rest of ``base``'s block."""
    merged = dict(base)
    for key, value in changes.items():
        current = merged.get(key)
        if isinstance(value, dict) and isinstance(current, dict):
            merged[key] = _merged(current, value)
        else:
            merged[key] = value
    return merged


def _iridium_scenario_with(scenario: Path, block: str, **fields: object) -> CommsConfig:
    """Load an Iridium scenario with some of one block's fields replaced (re-validated).

    Args:
        scenario: The scenario YAML to start from (the promoted ``iridium.yaml``).
        block: The top-level config block to edit (e.g. ``"satellite"``).
        **fields: The fields to set inside that block (a nested block merged key by key).

    Returns:
        The validated variant config.
    """
    data = load_comms_config(scenario).model_dump()
    return CommsConfig.model_validate(_merged(data, {block: fields}))


def _with_iridium(config: CommsConfig, **fields: object) -> CommsConfig:
    """Return a config with some of its Iridium dials replaced (re-validated), a nested block
    (``saturation``, ``arpu``) merged key by key, so its other settings keep the config's."""
    return CommsConfig.model_validate(_merged(config.model_dump(), {"iridium": fields}))


def _line_with(lines: tuple[str, ...], opening: str) -> str:
    """The one stated assumption that opens with the given words."""
    found = [line for line in lines if line.startswith(opening)]
    assert len(found) == 1, (opening, found)
    return found[0]


def _artifact_for(run: IridiumRun) -> IridiumModelArtifact:
    """Assemble a run's promoted artifact (no file IO)."""
    return build_iridium_artifact(
        fleet=run.fleet, iridium=run.iridium, source_scenario_path="test", version_stamp="test"
    )


def _year(run: IridiumRun, year: int) -> tuple[int, float, tuple[ClassYearRecord, ...]]:
    """A year's living fleet, annualized cost and class lines, read from the two records."""
    fleet_year = next(each for each in run.fleet.years if each.year == year)
    iridium_year = next(each for each in run.iridium.years if each.year == year)
    return fleet_year.living_fleet, fleet_year.annual_cost_this_year_musd, iridium_year.classes


def _within(value: float, target: float, tolerance: float) -> bool:
    """Whether a value lies within a relative tolerance of its target."""
    return abs(value / target - 1.0) <= tolerance


def _tolerance(device_class: DeviceClass) -> float:
    """The headline's tolerance for a class: 1 percent for the phone class, else 5."""
    return PHONE_TOLERANCE if device_class is PHONE else DIRECTIONAL_TOLERANCE


def _margin(revenue_musd: float, cost_musd: float) -> float:
    """The margin formula, percent, written out: (revenue - cost) / revenue x 100."""
    return (revenue_musd - cost_musd) / revenue_musd * 100.0


def _keys(document: object) -> set[str]:
    """Every key of a parsed JSON document, at any depth."""
    if isinstance(document, dict):
        return set(document) | {key for value in document.values() for key in _keys(value)}
    if isinstance(document, list):
        return {key for value in document for key in _keys(value)}
    return set()


# ---------------------------------------------------------------------------
# Each class's physics.
# ---------------------------------------------------------------------------


def test_the_class_spectral_efficiencies_are_the_three_centrals() -> None:
    """Objective: one home maps each class to its central spectral efficiency (the resolver
    and the device-class setting are retired), in class order.

    Expected outcome: ``CLASS_SE_CENTRAL`` gives 2.0, 2.5 and 0.65 for the small terminal, the
    mounted terminal and the phone class, in that order.
    """
    assert list(CLASS_SE_CENTRAL) == CLASS_ORDER
    assert tuple(CLASS_SE_CENTRAL.values()) == pytest.approx(CLASS_SE)


def test_per_satellite_capacity_worked_products() -> None:
    """Objective: the satellite's peak for each class, every beam lit and used and the band
    full time, at the reference panel and at the default panel (a factor of 0.616).

    Expected outcome: 2.4, 3.0 and 0.78 Gbps at 25 m^2; 1.4784, 1.848 and 0.48048 at 15.4 m^2
    (8 MHz x the class's SE x 0.15 x the panel factor).
    """
    for se, at_reference, at_default in zip(
        CLASS_SE, PEAK_GBPS_AT_REFERENCE, PEAK_GBPS_AT_DEFAULT, strict=True
    ):
        assert derive_per_satellite_capacity_gbps(HELD_SPECTRUM_MHZ, se, 1.0) == pytest.approx(
            at_reference
        )
        assert derive_per_satellite_capacity_gbps(
            HELD_SPECTRUM_MHZ, se, DEFAULT_PANEL_FACTOR
        ) == pytest.approx(at_default)


def test_people_per_useful_beam_at_each_class_usage(
    synthetic_saturation_curve: SyntheticCurve,
) -> None:
    """Objective: each class's people per useful beam is a beam's rate over the class's own
    busy-hour load (2026-10-04), read from the curve at d = 1 and the reference panel.

    Sample: the synthetic curve for the default dials (every row's capacity is its useful beams
    x 8 MHz x the class's SE), read at its first row, 342 satellites.

    Expected outcome: 320 people a beam for the small terminal (16 Mbps over 2 Mbps x 2.5
    percent), 40 for the mounted terminal (20 over 5 x 10 percent), 277.333 for the phone class
    (5.2 over 0.75 x 2.5 percent).
    """
    curve = synthetic_saturation_curve(IridiumDials())
    for device_class, per_beam in zip(CLASS_ORDER, PEOPLE_PER_BEAM_AT_FULL_DOWNLINK, strict=True):
        reading = read_fleet(curve, device_class, 342, downlink_share=1.0, panel_factor=1.0)
        assert reading.people / reading.useful_beams == pytest.approx(per_beam, rel=1e-12)


def test_per_user_rates_worked() -> None:
    """Objective: each class's downlink pool (W x SE x d) and per-user rates at its own usage.

    Expected outcome (the usage check's rates, d = 0.67): pools 10.72, 13.4 and 3.484 Mbps; peak
    rates 2.0, 5.0 and 0.75; off-peak 10.0 (the ratio binds), 13.4 and 3.484 (the pool binds).
    """
    for device_class, pool, peak, offpeak in zip(
        CLASS_ORDER, BEAM_POOL_MBPS, PEAK_RATE_MBPS, OFFPEAK_RATE_MBPS, strict=True
    ):
        rates = derive_iridium_per_user_rates(
            spectrum_mhz=HELD_SPECTRUM_MHZ,
            spectral_efficiency_bps_per_hz=CLASS_SE_CENTRAL[device_class],
            downlink_share=DEFAULT_DOWNLINK_SHARE,
            usage=CLASS_USAGE[device_class],
        )
        assert rates.beam_pool_mbps == pytest.approx(pool)
        assert rates.per_user_rate_peak_mbps == pytest.approx(peak)
        assert rates.per_user_rate_offpeak_mbps == pytest.approx(offpeak)


def test_per_user_offpeak_caps_at_the_beam_pool() -> None:
    """Objective: one beam's pool caps one person's off-peak rate.

    Sample: the mounted terminal's usage (5 Mbps, 10 and 2 percent, a 25 Mbps ratio rate) on its
    13.4 Mbps pool at d = 0.67; the same at d = 1 (a 20 Mbps pool).

    Expected outcome: the off-peak rate is the pool in both, 13.4 and 20.0 Mbps, below the 25
    Mbps the shares alone would give.
    """
    usage = CLASS_USAGE[MOUNTED]
    ratio_rate = usage.active_rate_mbps * usage.concurrency_peak / usage.concurrency_offpeak
    for downlink_share, pool in ((DEFAULT_DOWNLINK_SHARE, 13.4), (1.0, 20.0)):
        rates = derive_iridium_per_user_rates(
            spectrum_mhz=HELD_SPECTRUM_MHZ,
            spectral_efficiency_bps_per_hz=CLASS_SE_CENTRAL[MOUNTED],
            downlink_share=downlink_share,
            usage=usage,
        )
        assert rates.per_user_rate_offpeak_mbps == pytest.approx(pool)
        assert rates.per_user_rate_offpeak_mbps < ratio_rate


# ---------------------------------------------------------------------------
# IoT as capacity (ADR 011): each IoT class's engineering usage, its loads a day.
# ---------------------------------------------------------------------------
IOT_CLASS_ORDER = [IotClass.MINIMAL_PACKET_IOT, IotClass.DATA_IOT]
IOT_USAGE_LOADS = (
    (IotClass.MINIMAL_PACKET_IOT, 48, 0, 16_320, 130_560, 48, 48),
    (IotClass.DATA_IOT, 48, 4, 416_320, 3_330_560, 52, 48),
)
"""Each IoT class's engineering usage (the investor's, 2026-10-04) and its loads a day, worked by
hand, IoT class order: messages, bursts, bytes (48 x 340 = 16,320; 4 x 100,000 + 16,320 =
416,320), uplink bits (x 8), access attempts (one per message or burst) and single-tone messages
(every message, data IoT's included)."""


def test_each_iot_class_engineering_usage_and_its_loads_a_day() -> None:
    """Objective: the IoT capacity's reference usage, one entry per IoT class in its order, and
    the loads a day each derives (the bytes, the uplink bits, the access attempts and the
    single-tone messages), so a capacity read at it cannot drift from the usage.

    Sample: ``IOT_ENGINEERING_USAGE`` as shipped.

    Expected outcome: minimal-packet IoT then data IoT; minimal-packet IoT 48 messages and 0
    bursts a day, 16,320 bytes, 130,560 uplink bits, 48 access attempts and 48 single-tone
    messages; data IoT 48 messages and 4 bursts, 416,320 bytes, 3,330,560 bits, 52 attempts and
    48 single-tone messages.
    """
    assert list(IOT_ENGINEERING_USAGE) == IOT_CLASS_ORDER
    for iot_class, messages, bursts, volume, bits, attempts, tones in IOT_USAGE_LOADS:
        usage = IOT_ENGINEERING_USAGE[iot_class]
        assert (usage.messages_per_day, usage.bursts_per_day) == (messages, bursts)
        assert usage.bytes_per_day == volume
        assert usage.uplink_bits_per_day == bits
        assert usage.access_attempts_per_day == attempts
        assert usage.single_tone_messages_per_day == tones


IOT_WORKED_ROOMS = (
    (
        2031,
        528,
        19_160.469197388542,
        (32_879_365_142.718735, 6_575_873_028.543747, 1_092_146.744251147, 31_614_774.175691094),
        13_488_970.31496153,
        (
            ((4_351_680_680.653951, 1_965_864_139.6520646, 3_468_592_366.7043934), 1_965_864_139),
            ((170_588_558.58059296, 1_814_643_821.2172902, 3_468_592_366.7043934), 170_588_558),
        ),
    ),
    (
        2036,
        4_288,
        112_065.11747154818,
        (192_303_741_581.17667, 38_460_748_316.23534, 6_387_711.695878246, 184_907_443.8280545),
        78_893_842.6999699,
        (
            ((25_451_965_797.50868, 11_497_881_052.580843, 20_286_988_122.849403), 11_497_881_052),
            ((997_732_709.9715161, 10_613_428_663.920776, 20_286_988_122.849403), 997_732_709),
        ),
    ),
)
"""The worked capacity case, the build's own print at full precision (``A_capacity_print.txt``
(local), equal to the product-case design's probe P6 to every printed digit): per year, the
fleet, the phone class's useful beams (x 0.616), the room (uplink bits, payload bits, access low
and high a second), the single-tone seconds a second, and per IoT class its three views (payload
bits, random access, single-tone time) and its capacity."""
IOT_BINDING_VIEWS = (IotView.RANDOM_ACCESS, IotView.PAYLOAD_BITS)
"""The view that binds each IoT class at the shipped settings: random access for minimal-packet
IoT, payload bits for data IoT."""


def _room_at(
    curve: SaturationCurve, fleet: int, *, downlink_share: float, at_or_above_floor: bool
) -> iridium.IotRoomRecord:
    """The IoT room at a fleet of the shipped settings: the phone class's useful beams read from a
    curve at d and the default panel (15.4 / 25, the run's own division), then the room."""
    beams = read_fleet(
        curve,
        PHONE,
        fleet,
        downlink_share=downlink_share,
        panel_factor=DEFAULT_PANEL_M2 / REFERENCE_PANEL_M2,
    ).useful_beams
    return iot_room(
        beams,
        spectrum_mhz=HELD_SPECTRUM_MHZ,
        downlink_share=downlink_share,
        at_or_above_floor=at_or_above_floor,
    )


def test_the_worked_iot_capacity_case_at_fy2031_and_fy2036(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: IoT's room on the phone class's useful beams and each IoT class's capacity
    alone, by the three views at their conservative ends, the least rounded down (ADR 011).

    Sample: the committed curve at the shipped settings (8 MHz, d = 0.67, the 15.4 m^2 panel), at
    FY2031's living fleet (528) and FY2036's (4,288).

    Expected outcome: the beams, the room and each view within 1e-9 of the build's own print
    (P6's values); the capacities exactly (FY2031: 1,965,864,139 and 170,588,558; FY2036:
    11,497,881,052 and 997,732,709), each the least view rounded down, random access binding
    minimal-packet IoT and payload bits data IoT; the classes in IoT class order.
    """
    for _, fleet, beams, room_values, tone, classes in IOT_WORKED_ROOMS:
        room = _room_at(
            committed_saturation_curve,
            fleet,
            downlink_share=DEFAULT_DOWNLINK_SHARE,
            at_or_above_floor=True,
        )
        assert read_fleet(
            committed_saturation_curve,
            PHONE,
            fleet,
            downlink_share=DEFAULT_DOWNLINK_SHARE,
            panel_factor=DEFAULT_PANEL_M2 / REFERENCE_PANEL_M2,
        ).useful_beams == pytest.approx(beams, rel=1e-9)
        assert (
            room.uplink_bits_per_second,
            room.uplink_payload_bits_per_second,
            room.access_attempts_per_second_low,
            room.access_attempts_per_second_high,
        ) == pytest.approx(room_values, rel=1e-9)
        assert room.single_tone_seconds_per_second == pytest.approx(tone, rel=1e-9)
        assert [entry.iot_class for entry in room.classes] == IOT_CLASS_ORDER
        for entry, (views, capacity), binding in zip(
            room.classes, classes, IOT_BINDING_VIEWS, strict=True
        ):
            published = (
                entry.devices_by_payload_bits,
                entry.devices_by_random_access,
                entry.devices_by_single_tone_time,
            )
            assert published == pytest.approx(views, rel=1e-9)
            assert entry.device_capacity == capacity
            assert entry.binding_view is binding
            assert all(value is not None for value in published)
            assert entry.device_capacity == math.floor(min(v for v in published if v is not None))


def test_the_iot_room_below_the_floor_and_at_an_empty_fleet(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: the room is published at every fleet, while each class's five capacity fields
    are null below the coverage floor (IoT needs continuous coverage); a fleet of 0 has a room of
    0.0.

    Sample: the committed curve at the shipped settings, at FY2030's living fleet (304, below the
    340 floor) read as below the floor and, for the room alone, as at it; and at a fleet of 0.

    Expected outcome: at 304 below the floor the room equals the room read at it (positive), and
    every class's five fields are None; at 0 every room field is 0.0 and every class's five
    fields None.
    """
    below = _room_at(
        committed_saturation_curve,
        304,
        downlink_share=DEFAULT_DOWNLINK_SHARE,
        at_or_above_floor=False,
    )
    read_as_sold = _room_at(
        committed_saturation_curve,
        304,
        downlink_share=DEFAULT_DOWNLINK_SHARE,
        at_or_above_floor=True,
    )
    empty = _room_at(
        committed_saturation_curve,
        0,
        downlink_share=DEFAULT_DOWNLINK_SHARE,
        at_or_above_floor=False,
    )
    nulls = (None, None, None, None, None)
    for room in (below, empty):
        assert [entry.iot_class for entry in room.classes] == IOT_CLASS_ORDER
        for entry in room.classes:
            assert dataclasses.astuple(entry)[1:] == nulls
    assert dataclasses.replace(below, classes=()) == dataclasses.replace(read_as_sold, classes=())
    assert below.uplink_payload_bits_per_second > 0.0
    assert (
        empty.uplink_bits_per_second,
        empty.uplink_payload_bits_per_second,
        empty.access_attempts_per_second_low,
        empty.access_attempts_per_second_high,
        empty.single_tone_seconds_per_second,
    ) == (0.0, 0.0, 0.0, 0.0, 0.0)


def test_at_full_downlink_each_iot_capacity_is_zero_with_the_payload_view_binding(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: d = 1 leaves the uplink no time, so the payload and tone rooms are 0 and each
    IoT class's capacity is 0, the payload view binding (the tie between the two zero views goes
    to the earlier in ``IotView``'s order), while the access room is still read.

    Sample: the committed curve at d = 1 and the default panel, at 4,288 satellites.

    Expected outcome: uplink, payload and tone rooms 0.0; the access room positive; each class's
    payload and tone views 0.0, its access view positive, its capacity 0 and ``payload_bits``
    binding.
    """
    room = _room_at(committed_saturation_curve, 4_288, downlink_share=1.0, at_or_above_floor=True)
    assert (
        room.uplink_bits_per_second,
        room.uplink_payload_bits_per_second,
        room.single_tone_seconds_per_second,
    ) == (0.0, 0.0, 0.0)
    assert room.access_attempts_per_second_low > 0.0
    for entry in room.classes:
        assert (entry.devices_by_payload_bits, entry.devices_by_single_tone_time) == (0.0, 0.0)
        assert entry.devices_by_random_access is not None and entry.devices_by_random_access > 0.0
        assert (entry.device_capacity, entry.binding_view) == (0, IotView.PAYLOAD_BITS)


TIE_DOWNLINK_SHARE = 0.81296875
"""The downlink share at which minimal-packet IoT's random-access and single-tone views meet at 8
MHz: W (1 - d) = 57 devices a window x 3,750 Hz x 7 s = 1,496,250 Hz, so 1 - d = 0.18703125."""


def test_a_tie_between_views_binds_the_earlier_in_the_view_order() -> None:
    """Objective: when two views give the same least devices, the one earlier in ``IotView``'s
    order (payload bits, random access, single-tone time) binds, for constructed views and for
    the real input that ties two least views.

    Sample: constructed views: payload and access equal and least; access and tone equal and
    least; payload and tone equal and least; all three equal. Then ``iot_room`` at 8 MHz and
    d = 0.81296875, where minimal-packet IoT's random-access and single-tone views meet, at 1,
    1,000 and 4,096 phone-class beams, where the two come out bit-equal (102,600 devices a beam).

    Expected outcome: payload bits, random access, payload bits, payload bits; at the real tie
    minimal-packet IoT's two views equal and below its payload view, random access binding, and
    the capacity that view rounded down.
    """
    cases = (
        ((5.0, 5.0, 9.0), IotView.PAYLOAD_BITS),
        ((9.0, 5.0, 5.0), IotView.RANDOM_ACCESS),
        ((5.0, 9.0, 5.0), IotView.PAYLOAD_BITS),
        ((5.0, 5.0, 5.0), IotView.PAYLOAD_BITS),
    )
    for values, binding in cases:
        views = dict(zip(IotView, values, strict=True))
        assert iridium._binding_view(views) is binding, values
    uplink_width_hz = (1.0 - TIE_DOWNLINK_SHARE) * HELD_SPECTRUM_MHZ * 1e6
    assert uplink_width_hz == pytest.approx(57 * 3_750.0 * 7.0)
    for beams in (1.0, 1_000.0, 4_096.0):
        entry = iot_room(
            beams,
            spectrum_mhz=HELD_SPECTRUM_MHZ,
            downlink_share=TIE_DOWNLINK_SHARE,
            at_or_above_floor=True,
        ).classes[0]
        assert entry.iot_class is IotClass.MINIMAL_PACKET_IOT
        access, tone = entry.devices_by_random_access, entry.devices_by_single_tone_time
        assert access is not None and entry.devices_by_payload_bits is not None
        assert access == tone, (beams, access, tone)
        assert access < entry.devices_by_payload_bits
        assert entry.binding_view is IotView.RANDOM_ACCESS
        assert entry.device_capacity == math.floor(access)


def test_an_iot_room_past_what_a_float_holds_leaves_the_capacity_unrounded() -> None:
    """Objective: the capacity is rounded down only from a finite least view, so a room past what
    a float holds never raises an ``OverflowError`` from rounding; the view that is not finite
    stays in the record, where the run's last step refuses it naming the field.

    Sample: phone-class useful beams of 1e305 at the shipped settings, at or above the floor.

    Expected outcome: no exception; every class's capacity None and one of its views not finite.
    """
    room = iot_room(
        1e305,
        spectrum_mhz=HELD_SPECTRUM_MHZ,
        downlink_share=DEFAULT_DOWNLINK_SHARE,
        at_or_above_floor=True,
    )
    for entry in room.classes:
        assert entry.device_capacity is None
        views = (
            entry.devices_by_payload_bits,
            entry.devices_by_random_access,
            entry.devices_by_single_tone_time,
        )
        assert not all(view is not None and math.isfinite(view) for view in views)


def test_each_class_useful_beams_and_the_iot_room_in_every_year(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: each people class's busy-hour useful beams are published in every year, below
    the coverage floor too (beams are physical), from the reading that gives its people; each
    year carries IoT's room on its phone-class beams, each IoT class's capacity null below the
    floor (IoT needs continuous coverage).

    Sample: the shipped scenario on the committed curve (fleets 0, 32, 80, 160, 304, then 528 to
    4,288 from FY2031, the floor year).

    Expected outcome: every year's beams for every class equal ``read_fleet``'s at the year's
    living fleet, d and the panel factor (the same reading, exactly), 0.0 at a fleet of 0 and
    above 0 after; each year's IoT block equals ``iot_room`` at its phone-class beams, the room
    0.0 at a fleet of 0; FY2026 to FY2030 publish the room with every class's five capacity
    fields null, FY2031 on both capacities; FY2036's beams and IoT block equal the horizon-end
    reading's, both at 4,288 satellites (capacities 11,497,881,052 and 997,732,709).
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    panel_factor = run.iridium.saturation.panel_factor
    for fleet_year, iridium_year in zip(run.fleet.years, run.iridium.years, strict=True):
        for line in iridium_year.classes:
            assert (
                line.useful_beams
                == read_fleet(
                    committed_saturation_curve,
                    line.device_class,
                    fleet_year.living_fleet,
                    downlink_share=DEFAULT_DOWNLINK_SHARE,
                    panel_factor=panel_factor,
                ).useful_beams
            )
            assert line.useful_beams > 0.0 or fleet_year.living_fleet == 0
        sold = fleet_year.year >= FLOOR_YEAR
        assert iridium_year.iot == iot_room(
            iridium_year.classes[2].useful_beams,
            spectrum_mhz=HELD_SPECTRUM_MHZ,
            downlink_share=DEFAULT_DOWNLINK_SHARE,
            at_or_above_floor=sold,
        )
        for entry in iridium_year.iot.classes:
            if sold:
                assert entry.device_capacity is not None and entry.device_capacity > 0
            else:
                assert dataclasses.astuple(entry)[1:] == (None, None, None, None, None)
    first = run.iridium.years[0]
    assert [line.useful_beams for line in first.classes] == [0.0, 0.0, 0.0]
    assert dataclasses.astuple(first.iot)[:5] == (0.0, 0.0, 0.0, 0.0, 0.0)
    horizon, fy2036 = run.iridium.saturation.readings[2], run.iridium.years[-1]
    assert horizon.fleet == run.fleet.years[-1].living_fleet == LIVING_FLEET[-1]
    assert [line.useful_beams for line in fy2036.classes] == [
        line.useful_beams for line in horizon.classes
    ]
    assert fy2036.iot == horizon.iot
    assert [entry.device_capacity for entry in fy2036.iot.classes] == [11_497_881_052, 997_732_709]


def test_each_reading_carries_the_iot_room_and_both_capacities(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: each reported fleet carries IoT's room on its phone-class useful beams and, at
    or above the coverage floor, each IoT class's capacity alone.

    Sample: the shipped scenario's four readings (340, 2,000, 4,288 and 7,200 satellites, each at
    or above the floor).

    Expected outcome: each reading's IoT block equals ``iot_room`` at its phone-class beams, in
    IoT class order, with both capacities published and rising with the fleet.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    readings = run.iridium.saturation.readings
    assert [reading.fleet for reading in readings] == [340, 2_000, 4_288, STEADY_STATE_FLEET]
    for reading in readings:
        assert reading.iot == iot_room(
            reading.classes[2].useful_beams,
            spectrum_mhz=HELD_SPECTRUM_MHZ,
            downlink_share=DEFAULT_DOWNLINK_SHARE,
            at_or_above_floor=True,
        )
        assert [entry.iot_class for entry in reading.iot.classes] == IOT_CLASS_ORDER
    for index in range(len(IOT_CLASS_ORDER)):
        capacities = [reading.iot.classes[index].device_capacity for reading in readings]
        assert all(capacity is not None for capacity in capacities)
        assert capacities == sorted(capacities), capacities
        assert len(set(capacities)) == len(capacities), capacities


# ---------------------------------------------------------------------------
# The two entries and the identity check.
# ---------------------------------------------------------------------------


def test_hb_cellular_default_has_no_iridium_block() -> None:
    """Objective: the High-Bandwidth Cellular Pure Play model stays untouched: the default
    config has no ``iridium:`` block and runs through the cellular entry, whose record carries
    no Iridium field (the interim v5 block left with the density path).

    Expected outcome: ``CommsConfig().iridium`` is None; the cellular run's record has no field
    named for Iridium or a built fleet.
    """
    assert CommsConfig().iridium is None
    run = run_comms_model(CommsConfig())
    fields = {field.name for field in dataclasses.fields(CellularTrajectory)}
    assert "iridium" not in fields
    assert "built_fleet_annual_cost_musd" not in fields
    assert run.cellular.fleet_target == COVERAGE_FLOOR


def test_the_cellular_entry_refuses_an_iridium_config(iridium_yaml: Path) -> None:
    """Objective: each family has its own entry: the cellular entry refuses a config of the
    Iridium family with a typed error naming the Iridium entry, so no Iridium config runs
    without its saturation curve.

    Sample: the default Iridium dials; the shipped Iridium scenario.

    Expected outcome: each raises NotACellularConfigError (a ValueError) whose message names
    ``communications.iridium.run_iridium_model(config, curve)``.
    """
    for config in (CommsConfig(iridium=IridiumDials()), load_comms_config(iridium_yaml)):
        with pytest.raises(NotACellularConfigError) as refused:
            run_comms_model(config)
        assert "communications.iridium.run_iridium_model(config, curve)" in str(refused.value)
        assert isinstance(refused.value, ValueError)


def test_the_iridium_entry_refuses_a_cellular_config_with_the_familys_message(
    committed_saturation_curve: SaturationCurve,
) -> None:
    """Objective: the Iridium entry narrows its config before anything else, so a config of
    the cellular family is refused with the family's typed error and the command's message,
    before any check of the curve.

    Sample: the default config (no ``iridium:`` block) with the committed curve.

    Expected outcome: NotAnIridiumConfigError (a ValueError) with the message word for word,
    not a mismatch of the curve.
    """
    with pytest.raises(NotAnIridiumConfigError) as refused:
        run_iridium_model(CommsConfig(), committed_saturation_curve)
    assert str(refused.value) == (
        "the scenario does not select the Iridium model: it needs a top-level "
        "'iridium:' block (see scenarios/iridium.yaml)"
    )
    assert isinstance(refused.value, ValueError)


def test_every_iridium_path_refuses_a_setting_a_model_copy_slipped_past_the_validators(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: pydantic's ``model_copy`` does not validate, so the narrowing every Iridium
    path calls (``iridium_dials_of``) re-validates the config whole and a copied config cannot
    carry a setting the validators refuse into a run.

    Sample: the shipped scenario; a copy whose coverage floor is 500 (the Iridium path pins it
    at 340); a copy whose phone class price is -1.0 (built without validation).

    Expected outcome: the shipped config narrows to its own dials; each slipped copy raises a
    ValidationError naming the field, from the narrowing and from the Iridium entry alike.
    """
    config = load_comms_config(iridium_yaml)
    assert config.iridium is not None
    assert iridium_dials_of(config) == config.iridium
    floor = config.model_copy(update={"coverage": CoverageDials(satellites_for_full_coverage=500)})
    assert floor.coverage.satellites_for_full_coverage == 500
    negative = IridiumArpuDials.model_construct(
        **{**config.iridium.arpu.model_dump(), "phone_class_price_usd_month": -1.0}
    )
    price = config.model_copy(
        update={"iridium": config.iridium.model_copy(update={"arpu": negative})}
    )
    for slipped, field in (
        (floor, "coverage.satellites_for_full_coverage"),
        (price, "phone_class_price_usd_month"),
    ):
        with pytest.raises(ValidationError, match=field):
            iridium_dials_of(slipped)
        with pytest.raises(ValidationError, match=field):
            run_iridium_model(slipped, committed_saturation_curve)


def test_the_iridium_entry_runs_only_on_a_curve_computed_for_its_inputs(
    committed_saturation_curve: SaturationCurve, synthetic_saturation_curve: SyntheticCurve
) -> None:
    """Objective: the identity check runs inside the Iridium entry on every run, before the
    run: a config reads only a curve computed for its own inputs.

    Sample: an Iridium config at 10.5 MHz with the committed curve (computed for the held
    spectrum the shipped scenario sets), then with a synthetic curve stamped for 10.5 MHz; the
    default Iridium dials with that 10.5 MHz curve.

    Expected outcome: the 10.5 MHz config with the committed curve raises
    SaturationCurveMismatchError naming ``spectrum_mhz``, 10.5 for this run and the curve's own
    value (read from its parameters); with its own curve it runs, the phone class's satellite
    peak at 10.5 MHz and the default panel 0.630630 Gbps (10.5 x 0.65 x 0.15 x 0.616); the
    default dials with the 10.5 MHz curve are refused in turn, naming ``spectrum_mhz`` again.
    """
    wider = IridiumDials(spectrum_mhz=10.5)
    committed_spectrum = committed_saturation_curve.parameters.spectrum_mhz
    with pytest.raises(SaturationCurveMismatchError) as refused:
        run_iridium_model(CommsConfig(iridium=wider), committed_saturation_curve)
    assert (
        f"spectrum_mhz is 10.5 for this run but {committed_spectrum} in the curve's parameters"
    ) in str(refused.value)
    wider_curve = synthetic_saturation_curve(wider)
    run = run_iridium_model(CommsConfig(iridium=wider), wider_curve)
    phone = run.iridium.classes[2]
    assert phone.per_satellite_capacity_gbps == pytest.approx(10.5 * 0.65 * 0.15 * 0.616)
    with pytest.raises(SaturationCurveMismatchError, match=r"spectrum_mhz is 8\.0 for this run"):
        run_iridium_model(CommsConfig(iridium=IridiumDials()), wider_curve)


def test_iridium_class_physics_frozen_at_the_default(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: every class's block at the default (the shipped scenario: 15.4 m^2, 16 per
    launch, d = 0.67) on the committed curve: its price, usage and physics, its markers read
    from the curve, and the limit that binds at the horizon's end.

    Expected outcome: in class order, prices $10, $50 and $15; each class's usage its named
    constants and the investor's literals (2 Mbps, 2.5 and 0.5 percent; 5 Mbps, 10 and 2
    percent; 0.75 Mbps, 2.5 and 0.5 percent); SE 2.0, 2.5 and 0.65; the satellite's peak
    1.4784, 1.848 and 0.48048 Gbps; pools
    10.72, 13.4 and 3.484 Mbps; peak rates 2.0, 5.0 and 0.75; off-peak 10.0, 13.4 and 3.484;
    the maximum use the curve's times 0.616 and every marker the curve's own (the saturation
    numbers 19,995, not reached by 55,407, and 20,652); every class bound by the launch cadence
    at the horizon's end (4,288 satellites, below every saturation number).
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    curves = {entry.device_class: entry for entry in committed_saturation_curve.classes}
    prices = tuple(CLASS_PRICES[device_class] for device_class in CLASS_ORDER)
    blocks = run.iridium.classes
    assert [block.device_class for block in blocks] == CLASS_ORDER
    for index, block in enumerate(blocks):
        usage = CLASS_USAGE[block.device_class]
        markers = curves[block.device_class].markers
        assert block.price_usd_per_month == prices[index]
        block_usage = (
            block.active_user_rate_mbps,
            block.concurrency_peak,
            block.concurrency_offpeak,
        )
        assert block_usage == (
            usage.active_rate_mbps,
            usage.concurrency_peak,
            usage.concurrency_offpeak,
        )
        assert block_usage == CLASS_USAGE_SETTLED[index]
        assert block.spectral_efficiency_bps_per_hz == CLASS_SE[index]
        assert block.per_satellite_capacity_gbps == pytest.approx(PEAK_GBPS_AT_DEFAULT[index])
        assert block.beam_pool_mbps == pytest.approx(BEAM_POOL_MBPS[index])
        assert block.per_user_rate_peak_mbps == pytest.approx(PEAK_RATE_MBPS[index])
        assert block.per_user_rate_offpeak_mbps == pytest.approx(OFFPEAK_RATE_MBPS[index])
        assert block.maximum_use_beams == pytest.approx(
            markers.maximum_use_beams * DEFAULT_PANEL_FACTOR, rel=1e-12
        )
        assert block.saturation_number == markers.saturation_number
        assert block.saturation_number == FROZEN_SATURATION_NUMBERS[index]
        assert block.saturation_not_reached_by == markers.saturation_not_reached_by
        assert block.elasticity_under_0p25_fleet == markers.elasticity_under_0p25_fleet
        assert block.fleet_at_90pct_of_maximum_use == markers.fleet_at_90pct_of_maximum_use
        assert block.binding_limit_at_horizon_end is BindingLimit.LAUNCH_CADENCE
    assert blocks[1].saturation_not_reached_by == FROZEN_MOUNTED_NOT_REACHED_BY


# ---------------------------------------------------------------------------
# The tripwire in its new form.
# ---------------------------------------------------------------------------


def test_iridium_and_cellular_runs_share_the_fleet_and_cost_records(
    synthetic_saturation_curve: SyntheticCurve,
) -> None:
    """THE EQUALITY TRIPWIRE: an Iridium run and a cellular run share the fleet-and-cost record.

    Objective: prove the shared machinery (the cadence share, the cohort cliff, the build,
    launch and replacement cost lines and the annualized cost) on config defaults. With no
    target the Iridium path flies the full cadence, so it is compared with a cellular run whose
    fleet target the horizon never reaches: both fly every launch the cadence allows. The
    config defaults' launch price moves with the cadence, so the comparison also exercises the
    per-cohort cost lock-in.

    Sample: the Iridium dials at their defaults (the 0.18 share, 12 per launch, the default
    cost curve, the default prices) on a synthetic curve stamped for them; the cellular
    defaults with the subscriber target at 150,000,000 (a 2,000-satellite fleet target, which
    the 0.18 share's fleet never reaches).

    Expected outcome: first the premise, every year's cellular living fleet below its target;
    then the two shared records equal whole (every year with its cohort cost lines, and every
    cost total), compared as records, so a future shared field joins with no edit here; and the
    shared record's own values frozen, so a change that moves both families alike (a launch
    priced at another year's cadence, say) fails here: the living fleets 0, 0, 12, 24, 48, 84,
    132, 192, 288, 420 and 576, the total cost $1,594.59M and the FY2036 cash replacement
    $79.51337204338448M exactly. The families' own records are not compared.
    """
    cellular_config = CommsConfig.model_validate(
        {"subscribers": {"subscribers_at_full_coverage": 150_000_000}}
    )
    cellular = run_comms_model(cellular_config)
    target = cellular.cellular.fleet_target
    assert all(year.living_fleet < target for year in cellular.fleet.years), (
        "the premise: the cellular run never reaches its target, so it flies every launch"
    )
    dials = IridiumDials()
    iridium = run_iridium_model(CommsConfig(iridium=dials), synthetic_saturation_curve(dials))
    assert iridium.fleet == cellular.fleet
    shared = cellular.fleet
    assert [year.living_fleet for year in shared.years] == list(TRIPWIRE_LIVING_FLEET)
    assert shared.total_cost_through_final_year_musd == pytest.approx(TRIPWIRE_TOTAL_COST_MUSD)
    assert shared.final_year_replacement_cost_musd == TRIPWIRE_FY2036_REPLACEMENT_COST_MUSD


# ---------------------------------------------------------------------------
# The headline, the bracket, and the fleet and cost lines.
# ---------------------------------------------------------------------------


def test_the_headline_every_class_alone_side_by_side(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the headline (the investor's usage, d = 0.67, the 15.4 m^2 panel, 16 per launch,
    the all-in share): each class alone, side by side, at FY2031, FY2033, FY2036 and the steady
    state beyond the horizon, against the usage check's table.

    Expected outcome: the fleets and fleet costs exactly (528, 1,360, 4,288 and 7,200; $191.4M,
    $493.0M, $1,554.4M and $2,610.0M); each class's people and revenue within its tolerance (5
    percent for the small and mounted terminals, 1 for the phone class); each class's own margin
    its own revenue against the whole fleet's cost; the four rows in class order.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    steady = run.iridium.saturation.readings[3]
    for label, fleet, cost_musd, cells in HEADLINE_ROWS:
        if label == "steady state":
            assert (steady.fleet, steady.fleet_annual_cost_musd) == pytest.approx(
                (fleet, cost_musd)
            )
            lines = [
                (line.device_class, line.people, line.revenue_musd, line.own_margin_pct)
                for line in steady.classes
            ]
        else:
            living, annual_cost, year_lines = _year(run, int(label[2:]))
            assert living == fleet
            assert annual_cost == pytest.approx(cost_musd)
            lines = [
                (line.device_class, line.people_served, line.revenue_musd, line.own_margin_pct)
                for line in year_lines
            ]
        assert [line[0] for line in lines] == CLASS_ORDER
        for (device_class, people, revenue, margin), (people_m, revenue_musd) in zip(
            lines, cells, strict=True
        ):
            tolerance = _tolerance(device_class)
            assert _within(people / 1e6, people_m, tolerance), (label, device_class, people)
            assert _within(revenue, revenue_musd, tolerance), (label, device_class, revenue)
            assert margin == pytest.approx(_margin(revenue, cost_musd))


def test_the_no_upgrade_bracket_at_fifteen_per_launch(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the bracket without the Neutron block upgrade, 15 satellites per launch, and
    its stated assumptions say so.

    Expected outcome (the investor's table of the new defaults, its second table; exact): 495,
    1,275 and 4,020 satellites at FY2031, FY2033 and FY2036 and 6,750 at the steady state;
    $184.8M, $476.0M, $1,500.8M and $2,520.0M a year; $0.3733M a satellite-year; the stated
    per-launch line says this run flies 15, beside the validated 16 with the block upgrade and
    15 without it.
    """
    config = _iridium_scenario_with(iridium_yaml, "satellite", satellites_per_launch=15)
    run = run_iridium_model(config, committed_saturation_curve)
    per_launch = _line_with(
        run.iridium.assumptions, "Satellites per launch is a direct scenario setting"
    )
    assert "this run flies 15." in per_launch
    assert "The validated counts are 16 with the Neutron block upgrade" in per_launch
    assert "and 15 without the upgrade" in per_launch
    for year, fleet in BRACKET_FLEETS.items():
        living, annual_cost, _ = _year(run, year)
        assert living == fleet
        assert annual_cost == pytest.approx(BRACKET_COSTS_MUSD[year])
    steady = run.iridium.saturation.readings[3]
    assert (steady.fleet, steady.fleet_annual_cost_musd) == pytest.approx(BRACKET_STEADY_STATE)
    assert run.iridium.cost_per_satellite_year_musd == pytest.approx(
        BRACKET_COST_PER_SATELLITE_YEAR_MUSD
    )


def test_every_year_replaces_only_its_retiring_cohort(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the fleet and cost lines of the full cadence: every launch the cadence share
    allows flies, with no target, completion or hold, and each year counts as replacement only
    the cohort retiring that year (the cohort one life earlier).

    Expected outcome: each year flies 0, 2, 3, 5, 9, 14, 22, 35, 51, 70 and 90 launches of 16 and
    holds 0, 32, 80, 160, 304, 528, 848, 1,360, 2,096, 3,072 and 4,288 living satellites; each
    year's replaced satellites equal the deployment five years earlier (none before FY2031);
    301 launches and 4,816 satellites through FY2036 at a cash cost of $8,729.0M; the FY2036
    cash replacement $406.0M (the FY2031 cohort's 224 satellites); $0.3625M a satellite-year.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    years = run.fleet.years
    assert [year.year for year in years] == list(MODEL_YEARS)
    assert [year.comms_launches_flown_this_year for year in years] == list(COMMS_LAUNCHES)
    assert [year.living_fleet for year in years] == list(LIVING_FLEET)
    deployed = [year.satellites_deployed_this_year for year in years]
    assert deployed == [launches * 16 for launches in COMMS_LAUNCHES]
    for index, year in enumerate(years):
        retiring = deployed[index - 5] if index >= 5 else 0
        assert year.satellites_replaced_this_year == retiring
    assert sum(year.comms_launches_flown_this_year for year in years) == LAUNCHES_THROUGH_FY2036
    assert sum(deployed) == SATELLITES_THROUGH_FY2036
    assert run.fleet.total_cost_through_final_year_musd == pytest.approx(TOTAL_COST_MUSD)
    assert years[-1].satellites_replaced_this_year == FY2031_COHORT_SATELLITES
    assert run.fleet.final_year_replacement_cost_musd == pytest.approx(FY2036_REPLACEMENT_COST_MUSD)
    assert run.iridium.cost_per_satellite_year_musd == pytest.approx(COST_PER_SATELLITE_YEAR_MUSD)


def test_long_satellite_life_publishes_no_cash_replacement(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: a satellite life longer than the horizon publishes no 0.0 cash cost as a real
    figure: with a 10-year life no cohort retires by FY2036, so the final year replaces nothing.

    Expected outcome: the final-year cash replacement is None; the annualized basis carries the
    real cost, the 4,816 satellites at (1.0 + 13.0 / 16) / 10 = $872.9M a year.
    """
    config = _iridium_scenario_with(iridium_yaml, "satellite", satellite_lifetime_years=10)
    summary = _artifact_for(
        run_iridium_model(config, committed_saturation_curve)
    ).trajectory_summary
    assert summary.final_year_replacement_cost_musd is None
    assert summary.living_fleet_final_year == SATELLITES_THROUGH_FY2036
    assert summary.final_year_annual_cost_musd == pytest.approx(872.9)


# ---------------------------------------------------------------------------
# Revenue and the floor rule.
# ---------------------------------------------------------------------------


def test_every_class_revenue_rises_every_year_from_the_floor_year(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: every seat sold on the fleet the cadence builds, so revenue rises with the
    fleet.

    Expected outcome: from FY2031 to FY2036 every class's people and revenue rise every year.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    sold = [year for year in run.iridium.years if year.year >= FLOOR_YEAR]
    for index in range(len(CLASS_ORDER)):
        revenue = [year.classes[index].revenue_musd for year in sold]
        people = [year.classes[index].people_served for year in sold]
        assert all(later > earlier for earlier, later in zip(revenue, revenue[1:])), revenue
        assert all(later > earlier for earlier, later in zip(people, people[1:])), people


def test_below_the_floor_nothing_is_sold_and_the_cost_accrues(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the floor rule: nothing is sold in a year whose living fleet is below the
    coverage floor (340), and from the first year at it every class is sold in full; for IoT,
    the room is published in every year while each IoT class's capacity is null below the floor
    (IoT needs continuous coverage).

    Expected outcome: FY2026 to FY2030 (0, 32, 80, 160 and 304 satellites) have every class's
    people 0, revenue 0.0 and a null margin, while their annualized cost accrues (above 0.0 from
    FY2027), and IoT's room is published (0.0 at the fleet of 0, above 0.0 after) with every IoT
    class's five capacity fields null; the floor is reached in FY2031, from which every class has
    its own margin and both IoT classes their capacity.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    assert run.iridium.coverage_floor_reached_year == FLOOR_YEAR
    for fleet_year, iridium_year in zip(run.fleet.years, run.iridium.years, strict=True):
        if fleet_year.year < FLOOR_YEAR:
            assert fleet_year.living_fleet < COVERAGE_FLOOR
            assert all(
                (line.people_served, line.revenue_musd, line.own_margin_pct) == (0, 0.0, None)
                for line in iridium_year.classes
            )
            if fleet_year.year > BASE_YEAR_DEFAULT:
                assert fleet_year.annual_cost_this_year_musd > 0.0
            room = iridium_year.iot
            assert (room.uplink_payload_bits_per_second > 0.0) is (fleet_year.living_fleet > 0)
            assert all(dataclasses.astuple(entry)[1:] == (None,) * 5 for entry in room.classes)
        else:
            assert all(line.own_margin_pct is not None for line in iridium_year.classes)
            assert all(entry.device_capacity is not None for entry in iridium_year.iot.classes)


def test_the_three_class_prices_and_no_government_key(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the engineering config carries the three people classes' prices, exact, and
    no other (IoT is capacity in this model, its prices the product case's, ADR 011); and the
    artifact carries no government key anywhere (government is left out of revenue).

    Expected outcome: the ``arpu`` block's fields are the small terminal's, the mounted
    terminal's and the phone class's prices, in that order, defaulting to $10, $50 and $15; no
    key of the shipped scenario's artifact, at any depth, names government.
    """
    prices = IridiumArpuDials()
    assert list(IridiumArpuDials.model_fields) == [
        "small_terminal_class_price_usd_month",
        "mounted_terminal_class_price_usd_month",
        "phone_class_price_usd_month",
    ]
    assert (
        prices.small_terminal_class_price_usd_month,
        prices.mounted_terminal_class_price_usd_month,
        prices.phone_class_price_usd_month,
    ) == (10.0, 50.0, 15.0)
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    payload = json.loads(render_artifact_json(_artifact_for(run)))
    assert not any("government" in key for key in _keys(payload))


def test_each_class_revenue_is_its_people_times_its_price(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: each class's revenue is its served people times its price times 12, and its own
    margin is its own revenue against the year's whole-fleet cost.

    Sample: the shipped scenario.

    Expected outcome: in every year every class's revenue is its people x its price x 12 / 1e6,
    and in every sold year its own margin its own revenue against the year's cost.
    """
    config = load_comms_config(iridium_yaml)
    base = run_iridium_model(config, committed_saturation_curve)
    for fleet_year, iridium_year in zip(base.fleet.years, base.iridium.years, strict=True):
        for line in iridium_year.classes:
            assert line.revenue_musd == pytest.approx(
                line.people_served * CLASS_PRICES[line.device_class] * 12 / 1e6
            )
            if line.revenue_musd > 0.0:
                assert line.own_margin_pct == pytest.approx(
                    _margin(line.revenue_musd, fleet_year.annual_cost_this_year_musd)
                )


def test_the_prices_are_validated() -> None:
    """Objective: every price is above 0 and at most $5,000 a month (the three classes'
    prices).

    Expected outcome: each price at 0 and at 5,000.01 is refused at construction naming the
    field; each at 5,000 is accepted.
    """
    for field in IridiumArpuDials.model_fields:
        for bad in (0.0, 5_000.01):
            with pytest.raises(ValidationError, match=field):
                IridiumArpuDials.model_validate({field: bad})
        assert getattr(IridiumArpuDials.model_validate({field: 5_000.0}), field) == 5_000.0


def test_near_zero_share_does_not_publish_a_full_margin_on_an_empty_fleet(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: a share that never launches (0.001: every year's comms launches round to 0)
    publishes nothing that does not exist: no margin without revenue, no U at a fleet of 0, and
    no inf or NaN.

    Expected outcome: every year's fleet 0, cost 0.0, people 0, revenue 0.0 and null margins,
    and its IoT room 0.0 with both IoT capacities null; the floor never reached (null); the
    cost per satellite-year still defined ($0.3625M); the horizon-end and steady-state readings
    at 0 with useful beams 0.0, share 0.0, people 0, revenue 0.0, a null U and null margins, and
    the same empty IoT room; the coverage-floor and 2,000 readings equal the all-in run's; the
    JSON holds no infinity or NaN.
    """
    all_in = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    config = _iridium_scenario_with(iridium_yaml, "comms_cadence", share_of_fleet=0.001)
    run = run_iridium_model(config, committed_saturation_curve)
    assert all(year.living_fleet == 0 for year in run.fleet.years)
    assert all(year.annual_cost_this_year_musd == 0.0 for year in run.fleet.years)
    for year in run.iridium.years:
        assert all(
            (line.people_served, line.revenue_musd, line.own_margin_pct) == (0, 0.0, None)
            for line in year.classes
        )
    assert run.iridium.coverage_floor_reached_year is None
    assert run.iridium.cost_per_satellite_year_musd == pytest.approx(COST_PER_SATELLITE_YEAR_MUSD)
    readings = run.iridium.saturation.readings
    assert readings[:2] == all_in.iridium.saturation.readings[:2]
    for reading in readings[2:]:
        assert (reading.fleet, reading.fleet_annual_cost_musd) == (0, 0.0)
        assert all(
            line == ClassReadingRecord(line.device_class, 0.0, 0.0, None, 0, 0.0, None)
            for line in reading.classes
        )
    empty_room = iot_room(
        0.0,
        spectrum_mhz=HELD_SPECTRUM_MHZ,
        downlink_share=DEFAULT_DOWNLINK_SHARE,
        at_or_above_floor=False,
    )
    assert dataclasses.astuple(empty_room)[:5] == (0.0, 0.0, 0.0, 0.0, 0.0)
    assert all(dataclasses.astuple(entry)[1:] == (None,) * 5 for entry in empty_room.classes)
    for iot in (*(year.iot for year in run.iridium.years), *(r.iot for r in readings[2:])):
        assert iot == empty_room

    def refuse(constant: str) -> float:
        raise AssertionError(f"the JSON holds {constant}")

    json.loads(render_artifact_json(_artifact_for(run)), parse_constant=refuse)


# ---------------------------------------------------------------------------
# The downlink share, the panel, the class order.
# ---------------------------------------------------------------------------


def test_halving_the_downlink_share_halves_people_capacity_and_the_pool_only(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: d scales people, each class's capacity and the pool (ADR 008), the off-peak
    per-user rate following the pool only where the pool caps it and the busy-hour per-user rate
    not moving, while the rest of the frame, 1 - d, scales IoT's uplink, payload and single-tone
    rooms and IoT's random-access room moves with neither: what the stated line on d says.

    Sample: the shipped scenario at d = 0.67 and at d = 0.335, read at the 2,000 reading.

    Expected outcome: at half d every class's people at 2,000 are half (within one person's
    rounding), its capacity there (``read_fleet``) half and its pool half; its off-peak rate at
    each d the lower of its pool and its own rate x busy-hour share over off-peak share (at 0.67
    the small terminal's own ratio caps it, 10.0 Mbps; at 0.335 every pool does); its busy-hour
    rate, useful beams, the share of maximum use, U, maximum use, the satellite's peak and the
    markers unchanged. IoT's
    uplink, payload and single-tone rooms there grow by (1 - 0.335) / (1 - 0.67), about 2.015,
    and its two access rooms stay equal, so minimal-packet IoT's capacity (random access binding
    at both) is unchanged and data IoT's payload view (binding at both) grows by that ratio.
    """
    config = load_comms_config(iridium_yaml)
    full = run_iridium_model(config, committed_saturation_curve)
    half_config = _with_iridium(config, saturation={"downlink_share": 0.335})
    half = run_iridium_model(half_config, committed_saturation_curve)
    for index, device_class in enumerate(CLASS_ORDER):
        full_reading = full.iridium.saturation.readings[1].classes[index]
        half_reading = half.iridium.saturation.readings[1].classes[index]
        assert abs(half_reading.people - full_reading.people / 2) <= 1
        assert half_reading.useful_beams == full_reading.useful_beams
        assert half_reading.share_of_maximum_use == full_reading.share_of_maximum_use
        assert half_reading.ocean_factor == full_reading.ocean_factor
        capacities = [
            read_fleet(
                committed_saturation_curve,
                device_class,
                2_000,
                downlink_share=share,
                panel_factor=DEFAULT_PANEL_FACTOR,
            ).capacity_gbps
            for share in (0.67, 0.335)
        ]
        assert capacities[1] == pytest.approx(capacities[0] / 2)
        full_block, half_block = full.iridium.classes[index], half.iridium.classes[index]
        assert half_block.beam_pool_mbps == pytest.approx(full_block.beam_pool_mbps / 2)
        usage = CLASS_USAGE[device_class]
        own_ratio = usage.active_rate_mbps * usage.concurrency_peak / usage.concurrency_offpeak
        for block in (full_block, half_block):
            assert block.per_user_rate_offpeak_mbps == min(block.beam_pool_mbps, own_ratio)
        assert half_block.per_user_rate_offpeak_mbps == half_block.beam_pool_mbps
        assert half_block.per_user_rate_peak_mbps == full_block.per_user_rate_peak_mbps
        assert half_block.per_satellite_capacity_gbps == full_block.per_satellite_capacity_gbps
        assert half_block.maximum_use_beams == full_block.maximum_use_beams
        markers = (
            "saturation_number",
            "saturation_not_reached_by",
            "elasticity_under_0p25_fleet",
            "fleet_at_90pct_of_maximum_use",
        )
        for marker in markers:
            assert getattr(half_block, marker) == getattr(full_block, marker), marker
    small_at_shipped_d = full.iridium.classes[0]
    assert small_at_shipped_d.per_user_rate_offpeak_mbps == 10.0 < small_at_shipped_d.beam_pool_mbps
    uplink_growth = (1.0 - 0.335) / (1.0 - 0.67)
    full_room = full.iridium.saturation.readings[1].iot
    half_room = half.iridium.saturation.readings[1].iot
    for room_field in (
        "uplink_bits_per_second",
        "uplink_payload_bits_per_second",
        "single_tone_seconds_per_second",
    ):
        assert getattr(half_room, room_field) == pytest.approx(
            getattr(full_room, room_field) * uplink_growth, rel=1e-12
        ), room_field
    assert half_room.access_attempts_per_second_low == full_room.access_attempts_per_second_low
    assert half_room.access_attempts_per_second_high == full_room.access_attempts_per_second_high
    (full_minimal, full_data), (half_minimal, half_data) = full_room.classes, half_room.classes
    assert full_minimal.binding_view is half_minimal.binding_view is IotView.RANDOM_ACCESS
    assert half_minimal.device_capacity == full_minimal.device_capacity
    assert full_data.binding_view is half_data.binding_view is IotView.PAYLOAD_BITS
    assert full_data.devices_by_payload_bits is not None
    assert half_data.devices_by_payload_bits == pytest.approx(
        full_data.devices_by_payload_bits * uplink_growth, rel=1e-12
    )


def test_the_panel_setting_scales_people_beams_capacity_and_maximum_use_linearly(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the panel is one linear setting on the curve (the 60 m^2 what-if rewritten):
    the default 15.4 m^2 reads 0.616 times the 25 m^2 reference panel, and nothing else moves.

    Sample: the shipped scenario at 15.4 m^2 and at 25 m^2, read at the 2,000 reading; the same
    at 16 m^2.

    Expected outcome: at 15.4 m^2 every class's useful beams, maximum use and satellite peak
    are 0.616 times its 25 m^2 values and its people too (within rounding), the small
    terminal's people 13,870,568 (an absolute target); satellites per launch, the fleet,
    the saturation numbers and U unchanged; the stack caveat in the assumptions above 15.4 m^2
    (at 16 m^2) and not at it.
    """
    config = load_comms_config(iridium_yaml)
    default = run_iridium_model(config, committed_saturation_curve)
    reference = run_iridium_model(
        _with_iridium(config, aperture_m2=REFERENCE_PANEL_M2), committed_saturation_curve
    )
    assert default.iridium.saturation.panel_factor == pytest.approx(DEFAULT_PANEL_FACTOR)
    assert reference.iridium.saturation.panel_factor == 1.0
    for index in range(len(CLASS_ORDER)):
        at_default = default.iridium.saturation.readings[1].classes[index]
        at_reference = reference.iridium.saturation.readings[1].classes[index]
        assert at_default.useful_beams == pytest.approx(
            DEFAULT_PANEL_FACTOR * at_reference.useful_beams, rel=1e-12
        )
        assert abs(at_default.people - DEFAULT_PANEL_FACTOR * at_reference.people) <= 1
        assert at_default.ocean_factor == at_reference.ocean_factor
        default_block = default.iridium.classes[index]
        reference_block = reference.iridium.classes[index]
        assert default_block.maximum_use_beams == pytest.approx(
            DEFAULT_PANEL_FACTOR * reference_block.maximum_use_beams, rel=1e-12
        )
        assert default_block.per_satellite_capacity_gbps == pytest.approx(
            DEFAULT_PANEL_FACTOR * reference_block.per_satellite_capacity_gbps
        )
        assert default_block.saturation_number == reference_block.saturation_number
    assert default.iridium.saturation.readings[1].classes[0].people == (
        SMALL_PEOPLE_AT_2000_DEFAULT_PANEL
    )
    assert default.fleet == reference.fleet
    assert default.iridium.satellites_per_launch == reference.iridium.satellites_per_launch == 16
    assert APERTURE_STACK_CAVEAT_NOTE not in default.iridium.assumptions
    above = run_iridium_model(_with_iridium(config, aperture_m2=16.0), committed_saturation_curve)
    assert APERTURE_STACK_CAVEAT_NOTE in above.iridium.assumptions


def test_every_class_in_one_run_in_class_order(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: one run reports every class side by side, never phone-first.

    Expected outcome: the class blocks, every year's class lines and every reading's class
    lines run small terminal, mounted terminal, phone class, and so do the artifact's class
    blocks, its years' lines and its readings' lines.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    assert [block.device_class for block in run.iridium.classes] == CLASS_ORDER
    for year in run.iridium.years:
        assert [line.device_class for line in year.classes] == CLASS_ORDER
    for reading in run.iridium.saturation.readings:
        assert [line.device_class for line in reading.classes] == CLASS_ORDER
    payload = json.loads(render_artifact_json(_artifact_for(run)))
    order = [device_class.value for device_class in CLASS_ORDER]
    assert [block["device_class"] for block in payload["classes"]] == order
    for year in payload["years"]:
        assert [line["device_class"] for line in year["classes"]] == order
    for reading in payload["saturation"]["readings"]:
        assert [line["device_class"] for line in reading["classes"]] == order


# ---------------------------------------------------------------------------
# A fleet past a class's last row.
# ---------------------------------------------------------------------------


def test_a_fleet_past_a_class_last_row_fails_naming_the_year_the_class_and_the_last_row(
    tmp_path: Path,
    iridium_yaml: Path,
    short_saturation_curve: ShortCurve,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Objective: a curve is never extrapolated or clamped: the first year whose living fleet
    lies past a class's last row fails with the typed error naming that year's fleet, the class
    and the last row, through the engine and through the command.

    Sample: the shipped scenario's dials on the synthetic curve cut short at 3,025 satellites
    (the realized fleet of the 3,000 request); FY2034 holds 2,096 and FY2035 3,072. For the
    command, its ``load_saturation_curve`` is replaced to return that curve (no file can carry a
    short curve past the loader's completeness check and the identity check).

    Expected outcome: the Iridium entry raises CurveBeyondLastRowError naming FY2035, 3,072
    satellites, the small terminal (read first) and its last row, 3,025; the command exits with
    EXIT_ERROR, writes no artifact, and logs exactly one ERROR line naming the same.
    """
    config = load_comms_config(iridium_yaml)
    assert config.iridium is not None
    short = short_saturation_curve(config.iridium, 3_025)
    with pytest.raises(CurveBeyondLastRowError) as refused:
        run_iridium_model(config, short)
    message = str(refused.value)
    for named in ("FY2035", "small_terminal_class", "last row is at 3025", "at 3072 satellites"):
        assert named in message
    monkeypatch.setattr(json_output, "load_saturation_curve", lambda path: short)
    out_path = tmp_path / "short.json"
    assert main([str(iridium_yaml), str(out_path)]) == EXIT_ERROR
    assert not out_path.exists()
    errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
    assert len(errors) == 1
    for named in ("FY2035", "small_terminal_class", "3025", "3072"):
        assert named in errors[0]


def test_a_reading_past_a_class_last_row_fails_naming_the_reading_and_its_settings(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: a reported fleet past a class's last row is refused (a curve is never
    extrapolated), and the refusal names the reading, its fleet and the settings that set it, as
    a year's refusal names its year: every modeled year can read while the
    steady state beyond the horizon lies past the curve.

    Sample: the shipped scenario with a 20-year life (its bound) and the cadence's year-10 anchor
    at 126 launches, both in bounds: FY2036 flies 126 comms launches and its living fleet reads,
    while the steady state, 126 x 16 x 20 = 40,320 satellites, lies past the small terminal's
    last committed row, 40,000.

    Expected outcome: the Iridium entry raises CurveBeyondLastRowError naming the reading's label
    (the steady state beyond the 10-year horizon), its fleet, FY2036's 126 comms launches, the 16
    satellites per launch and the 20-year life with the settings behind each, and then the
    reading's own message (the small terminal and its last row).
    """
    data = load_comms_config(iridium_yaml).model_dump()
    data["satellite"]["satellite_lifetime_years"] = 20
    data["cadence"]["launches_at_year_10"] = 126
    config = CommsConfig.model_validate(data)
    with pytest.raises(CurveBeyondLastRowError) as refused:
        run_iridium_model(config, committed_saturation_curve)
    message = str(refused.value)
    assert message.startswith(
        f"the steady state, beyond the {HORIZON_YEARS_DEFAULT}-year horizon (40320 satellites, "
        "FY2036's 126 comms launches (set by cadence.* and comms_cadence.share_of_fleet) x 16 "
        "satellites per launch (satellite.satellites_per_launch) x the 20-year life "
        "(satellite.satellite_lifetime_years)): "
    ), message
    for named in ("small_terminal_class", "last row is at 40000", "at 40320 satellites"):
        assert named in message


NonFiniteSettings = tuple[tuple[tuple[str, ...], float], ...]
"""Settings written beside a non-finite case's own setting: each a config path and its value."""


@pytest.mark.parametrize(
    ("setting", "value", "also", "first_field"),
    [
        (
            ("iridium", "aperture_m2"),
            2.5e300,
            (),
            "iridium.years[1].iot.uplink_bits_per_second is inf",
        ),
        (
            ("iridium", "aperture_m2"),
            2.5e300,
            ((("iridium", "saturation", "downlink_share"), 1.0),),
            "iridium.years[1].iot.uplink_bits_per_second is nan",
        ),
        (
            ("iridium", "arpu", "phone_class_price_usd_month"),
            5e-324,
            (),
            "iridium.years[5].classes[2].own_margin_pct is -inf",
        ),
        (
            ("satellite", "satellite_build_cost_musd"),
            1e308,
            (),
            "fleet.years[1].build_cost_this_year_musd is inf",
        ),
    ],
    ids=[
        "a panel so large the IoT room overflows",
        "a panel so large the IoT room is not a number at full downlink",
        "a subnormal price",
        "a build cost that overflows the fleet's costs",
    ],
)
def test_a_run_that_would_hold_a_number_that_is_not_finite_is_refused_naming_the_settings(
    iridium_yaml: Path,
    committed_saturation_curve: SaturationCurve,
    setting: tuple[str, ...],
    value: float,
    also: NonFiniteSettings,
    first_field: str,
) -> None:
    """Objective: a run the Iridium entry returns holds only finite numbers (before the fix these
    settings, each valid at load, returned records holding inf, -inf or NaN, which only the
    artifact's models refused, naming an artifact field rather than the setting).

    Sample (each case's first field re-derived by running it, 2026-10-13): the shipped scenario
    with, in turn, a panel of 2.5e300 m^2 (people stay finite; the IoT room's uplink bits a
    second overflow first, in FY2027, the room's first field walked before its capacity views);
    the same panel with the band in full-time downlink, d = 1 (the uplink's product overflows
    before its zero share, so the room's uplink is NaN); a phone class price of 5e-324 dollars
    (its margin overflows to -inf); and a satellite build cost of 1e308 $M (the fleet-and-cost
    record's costs overflow).

    Expected outcome: a ValueError (the type itself) naming the first field that is not finite
    (the fleet-and-cost record walked first) and its value, then the settings its record scales
    with, each with its value: for the Iridium record the panel, the three prices (exactly the
    three people classes', in class order) and the cost settings; for the fleet-and-cost record
    the cost settings alone.
    """
    data = load_comms_config(iridium_yaml).model_dump()
    for path, written in ((setting, value), *also):
        node = data
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = written
    config = CommsConfig.model_validate(data)
    with pytest.raises(ValueError, match="not a finite number") as refused:
        run_iridium_model(config, committed_saturation_curve)
    assert type(refused.value) is ValueError
    message = str(refused.value)
    assert message.startswith(f"the run's {first_field}, not a finite number: ")
    assert f"{'.'.join(setting)} ({value!r})" in message
    assert "satellite.satellite_build_cost_musd (" in message
    assert "launch_cost.high_cadence_cost_musd (" in message
    if setting[0] == "satellite":
        assert "iridium." not in message
    else:
        assert "iridium.aperture_m2 (" in message
        assert re.findall(r"iridium\.arpu\.(\w+) \(", message) == [
            "small_terminal_class_price_usd_month",
            "mounted_terminal_class_price_usd_month",
            "phone_class_price_usd_month",
        ]


# ---------------------------------------------------------------------------
# The readings at the reported fleets.
# ---------------------------------------------------------------------------


def test_the_readings_at_the_reported_fleets(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the four reported fleets and their costs, every class at each.

    Expected outcome: the readings run the coverage floor (340, $123.25M), the retired cap
    (2,000, $725.0M), the horizon-end reach (4,288 at the final year's $1,554.4M) and the steady
    state beyond the 10-year horizon (7,200, $2,610.0M); at 340 and 2,000 every class within the
    headline's tolerances of the usage check's table; the 4,288 reading equals the FY2036 year;
    at the 0.18
    share the horizon-end and steady-state fleets are 768 and 1,280.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    readings = run.iridium.saturation.readings
    assert [reading.label for reading in readings] == [
        COVERAGE_FLOOR_LABEL,
        RETIRED_CAP_LABEL,
        HORIZON_END_LABEL,
        f"the steady state, beyond the {HORIZON_YEARS_DEFAULT}-year horizon",
    ]
    assert [(reading.fleet, reading.fleet_annual_cost_musd) for reading in readings] == (
        pytest.approx([(340, 123.25), (2_000, 725.0), (4_288, 1_554.4), (7_200, 2_610.0)])
    )
    for reading, (fleet, cost_musd, cells) in zip(readings[:2], READING_TARGETS, strict=True):
        assert (reading.fleet, reading.fleet_annual_cost_musd) == pytest.approx((fleet, cost_musd))
        for line, (people_m, revenue_musd) in zip(reading.classes, cells, strict=True):
            tolerance = _tolerance(line.device_class)
            assert _within(line.people / 1e6, people_m, tolerance), (fleet, line)
            assert _within(line.revenue_musd, revenue_musd, tolerance), (fleet, line)
            assert line.own_margin_pct == pytest.approx(_margin(line.revenue_musd, cost_musd))
    _, _, fy2036 = _year(run, 2036)
    for reading_line, year_line in zip(readings[2].classes, fy2036, strict=True):
        assert (reading_line.people, reading_line.revenue_musd, reading_line.own_margin_pct) == (
            year_line.people_served,
            year_line.revenue_musd,
            year_line.own_margin_pct,
        )
    shared = _iridium_scenario_with(iridium_yaml, "comms_cadence", share_of_fleet=0.18)
    shared_run = run_iridium_model(shared, committed_saturation_curve)
    fleets = [reading.fleet for reading in shared_run.iridium.saturation.readings]
    assert fleets == [340, 2_000, 768, 1_280]


def test_the_retired_cap_reading_is_its_own_constant_at_the_historical_cap(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the retired cap's reading stays at the 2,000-satellite fleet cap the Iridium
    model inherited from the cellular family through ``iridium-v5`` (ADR 005), whatever the
    cellular family's live fleet cap becomes: the reading is its own named constant, not that
    live default.

    Sample: the named constant; the shipped scenario's run.

    Expected outcome: the constant equals the historical cap, 2,000; the run's second reading,
    labeled the retired cap, reads that fleet.
    """
    assert RETIRED_CAP_READING_FLEET == HISTORICAL_FLEET_CAP
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    reading = run.iridium.saturation.readings[1]
    assert (reading.label, reading.fleet) == (RETIRED_CAP_LABEL, HISTORICAL_FLEET_CAP)


# ---------------------------------------------------------------------------
# The marginal intervals.
# ---------------------------------------------------------------------------


def test_the_marginal_intervals_against_hand_worked_chords(
    iridium_yaml: Path, synthetic_saturation_curve: SyntheticCurve
) -> None:
    """Objective: the marginal intervals: from 0 to the first row, then between consecutive
    rows, each the people one more satellite adds at its revenue a satellite-year against the
    cost per satellite-year, every interval listed, so one that pays after a first stop shows.

    Sample: the shipped scenario at d = 1 and the 25 m^2 reference panel (people are the
    capacity x 1,000 / the load, 20,000 a Gbps for the small terminal), on the synthetic curve
    with the small terminal's first four rows reworked to hold 1,368,000, 1,942,000, 2,192,000
    and 3,018,000 people at 342, 506, 756 and 992 satellites; the small terminal's $10 a month
    (the investor's price of 2026-10-07) is $0.00012M a person a year, and a satellite-year
    costs $0.3625M (so an interval pays from about 3,021 people a satellite).

    Expected outcome: 0 to 342 adds 4,000 people a satellite, $0.48M, paying; 342 to 506 3,500,
    $0.42M, paying; 506 to 756 1,000, $0.12M, not paying; 756 to 992 3,500, $0.42M, paying again;
    then 992 to 1,482 continues from the synthetic rows; every class lists one interval per row.
    Also, d = 1 leaves the uplink no time, so in every year from the floor year and at every
    reading IoT's uplink, payload and tone rooms are 0.0 while its access room is read, and each
    IoT class's capacity is 0 with ``payload_bits`` binding.
    """
    config = _with_iridium(
        load_comms_config(iridium_yaml),
        aperture_m2=REFERENCE_PANEL_M2,
        saturation={"downlink_share": 1.0},
    )
    assert config.iridium is not None
    curve = synthetic_saturation_curve(config.iridium)
    people = {342: 1_368_000.0, 506: 1_942_000.0, 756: 2_192_000.0, 992: 3_018_000.0}
    small = curve.classes[0]
    rows = tuple(
        row.model_copy(update={"capacity_gbps": people[row.fleet] / 20_000.0})
        if row.fleet in people
        else row
        for row in small.rows
    )
    reworked = curve.model_copy(
        update={"classes": (small.model_copy(update={"rows": rows}), *curve.classes[1:])}
    )
    run = run_iridium_model(config, reworked)
    intervals = run.iridium.classes[0].marginal_intervals
    expected = (
        (0, 342, 4_000.0, 0.48, True),
        (342, 506, 3_500.0, 0.42, True),
        (506, 756, 1_000.0, 0.12, False),
        (756, 992, 3_500.0, 0.42, True),
    )
    for interval, (lower, upper, added, revenue, pays) in zip(intervals, expected, strict=False):
        assert interval == MarginalIntervalRecord(
            lower, upper, pytest.approx(added), pytest.approx(revenue), pays
        )
    assert intervals[4].lower_fleet == 992
    for block, entry in zip(run.iridium.classes, reworked.classes, strict=True):
        assert [interval.upper_fleet for interval in block.marginal_intervals] == [
            row.fleet for row in entry.rows
        ]
    sold_rooms = [year.iot for year in run.iridium.years if year.year >= FLOOR_YEAR]
    for room in (*sold_rooms, *(reading.iot for reading in run.iridium.saturation.readings)):
        zero_rooms = (
            room.uplink_bits_per_second,
            room.uplink_payload_bits_per_second,
            room.single_tone_seconds_per_second,
        )
        assert zero_rooms == (0.0, 0.0, 0.0), room
        assert room.access_attempts_per_second_low > 0.0
        for entry in room.classes:
            assert (entry.device_capacity, entry.binding_view) == (0, IotView.PAYLOAD_BITS)


def test_the_marginal_interval_verdicts_on_the_committed_curve(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the published verdicts at full price on the curve's own rows at the investor's
    prices of 2026-10-07 (the small terminal $10, the mounted terminal $50, the phone class
    $15), and the chords at the prototype's first-stop endpoints formed from the module's rows.

    Expected outcome (each verdict derived from the curve's people x the price x 12 against the
    cost per satellite-year): the small terminal, on the module's finer grid, pays on every
    interval through 6,006 and on none from 6,006 on (the module splits the prototype's 5,402
    to 8,010 at 6,006; at the earlier $15 it paid through 8,010, as the usage check's chords
    show); the mounted terminal pays through 5,402 and on none from 5,402 on (at the earlier
    $100, through 14,042); the phone class (at its $15 floor) through 8,010, its first below
    cost 8,010 to 10,000 within 1 percent of the prototype's $0.2902M (the phone verdicts must
    hold). Each first-stop chord at the prototype's endpoints is below cost and within its
    class's tolerance of the prototype's at the new price ($0.3257M, $0.3276M, $0.2902M).
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    cost = run.iridium.cost_per_satellite_year_musd
    last_paying = {
        SMALL: SMALL_MODULE_LAST_PAYING_ROW,
        MOUNTED: MOUNTED_LAST_PAYING_ROW,
        PHONE: PHONE_LAST_PAYING_ROW,
    }
    for block in run.iridium.classes:
        for interval in block.marginal_intervals:
            assert interval.pays is (interval.upper_fleet <= last_paying[block.device_class]), (
                block.device_class,
                interval,
            )
    phone_stop = next(
        interval
        for interval in run.iridium.classes[2].marginal_intervals
        if interval.lower_fleet == PHONE_LAST_PAYING_ROW
    )
    assert phone_stop.upper_fleet == 10_000
    assert _within(phone_stop.revenue_per_satellite_year_musd, 0.2902, PHONE_TOLERANCE)
    for device_class, lower, upper, prototype in FIRST_STOP_CHORDS:
        people = [
            read_fleet(
                committed_saturation_curve,
                device_class,
                fleet,
                downlink_share=DEFAULT_DOWNLINK_SHARE,
                panel_factor=DEFAULT_PANEL_FACTOR,
            ).people
            for fleet in (lower, upper)
        ]
        chord = (people[1] - people[0]) / (upper - lower) * CLASS_PRICES[device_class] * 12 / 1e6
        assert chord < cost, (device_class, chord)
        assert _within(chord, prototype, _tolerance(device_class)), (device_class, chord)
    bounds = [
        (interval.lower_fleet, interval.upper_fleet)
        for interval in run.iridium.classes[0].marginal_intervals
    ]
    assert (SMALL_PROTOTYPE_LAST_PAYING_ROW, SMALL_MODULE_LAST_PAYING_ROW) in bounds
    assert (SMALL_MODULE_LAST_PAYING_ROW, 8_010) in bounds


def test_a_saturation_number_is_reported_beside_the_cadence_never_a_cap(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: a class's saturation number is reported beside the cadence and never sizes,
    caps, stops or slows the build (ADR 005).

    Sample: the shipped scenario over a 30-year horizon with a 10-year life, so the living fleet
    passes the small terminal's and the phone class's saturation numbers (19,995 and 20,652)
    and reaches 24,000, still inside every class's last row.

    Expected outcome: every year flies every launch the cadence share allows; the living fleet
    keeps growing past both numbers; the small terminal and the phone class read spectrum as the
    limit at the horizon's end and the mounted terminal (not reached by 55,407) the launch
    cadence; people are read past the numbers, still rising.
    """
    data = load_comms_config(iridium_yaml).model_dump()
    data["metadata"] = {"base_year": BASE_YEAR_DEFAULT, "horizon_years": 30}
    data["satellite"]["satellite_lifetime_years"] = 10
    run = run_iridium_model(CommsConfig.model_validate(data), committed_saturation_curve)
    assert all(
        year.satellites_deployed_this_year == year.comms_launches_flown_this_year * 16
        for year in run.fleet.years
    )
    living = [year.living_fleet for year in run.fleet.years]
    assert living[-1] == 24_000
    small_number, phone_number = FROZEN_SATURATION_NUMBERS[0], FROZEN_SATURATION_NUMBERS[2]
    assert phone_number is not None and small_number is not None
    past = [index for index, fleet in enumerate(living) if fleet > phone_number]
    assert len(past) > 1
    assert all(living[i] <= living[j] for i, j in zip(past, past[1:]))
    assert [block.binding_limit_at_horizon_end for block in run.iridium.classes] == [
        BindingLimit.SPECTRUM,
        BindingLimit.LAUNCH_CADENCE,
        BindingLimit.SPECTRUM,
    ]
    people = [run.iridium.years[index].classes[0].people_served for index in past]
    assert people == sorted(people)
    assert people[-1] > people[0]


NOT_REACHED_LABELS = {SMALL: 36_900, MOUNTED: 55_407}
"""The synthetic curve's not-reached-by fleets (it places no saturation number on any class):
each class's last midpoint, by hand: the small terminal sqrt(34,040 x 40,000) = 36,899.86, so
36,900; the mounted terminal sqrt(47,961 x 64,009) = 55,407.0 (219 x 253)."""

HAND_PRICE_USD_PER_MONTH = 10.0
"""The price the binding-limit tests build a block at: any price, since the limit reads none."""


def class_record_at(
    curve: SaturationCurve, device_class: DeviceClass, final_living_fleet: int
) -> ClassRecord:
    """One class's block built by the run's own ``_class_record`` at the default dials, the
    default panel factor, the shipped cost per satellite-year and the given final living fleet."""
    return iridium._class_record(
        curve,
        device_class,
        IridiumDials(),
        panel_factor=DEFAULT_PANEL_FACTOR,
        price_usd_per_month=HAND_PRICE_USD_PER_MONTH,
        final_living_fleet=final_living_fleet,
        cost_per_satellite_year_musd=COST_PER_SATELLITE_YEAR_MUSD,
    )


@pytest.mark.parametrize("device_class", [SMALL, MOUNTED])
def test_a_final_fleet_at_the_not_reached_by_fleet_reads_the_launch_cadence(
    synthetic_saturation_curve: SyntheticCurve, device_class: DeviceClass
) -> None:
    """Objective: a class whose curve reaches no saturation number reads the launch cadence as
    its binding limit at the horizon's end up to and at the fleet its curve names it not reached
    by, the last midpoint at which its rows measure the elasticity of capacity (ADR 005).

    Sample: the synthetic curve for the default dials (L = N x B, no saturation number on any
    class), each class's block built by ``_class_record`` with the final living fleet at its
    label: the small terminal 36,900, the mounted terminal 55,407 (each worked by hand).

    Expected outcome: the curve and the block carry that label and no saturation number; the
    binding limit is the launch cadence.
    """
    curve = synthetic_saturation_curve(IridiumDials())
    label = NOT_REACHED_LABELS[device_class]
    markers = class_curve_of(curve, device_class).markers
    assert markers.saturation_number is None
    assert markers.saturation_not_reached_by == label
    record = class_record_at(curve, device_class, label)
    assert record.saturation_number is None
    assert record.saturation_not_reached_by == label
    assert record.binding_limit_at_horizon_end is BindingLimit.LAUNCH_CADENCE


@pytest.mark.parametrize("device_class", [SMALL, MOUNTED])
def test_a_final_fleet_past_the_not_reached_by_fleet_is_refused(
    synthetic_saturation_curve: SyntheticCurve, device_class: DeviceClass
) -> None:
    """Objective: a class whose curve reaches no saturation number, its final living fleet past
    the fleet its curve names it not reached by, is refused with a typed error naming the class,
    the fleet and the label: the rows measure the elasticity no further, so which limit binds
    there is unknown, never guessed.

    Sample: as the test above, the final living fleet one satellite past each label (36,901 for
    the small terminal, 55,408 for the mounted terminal), both inside the class's last row.

    Expected outcome: ``BindingLimitUnmeasuredError``, a ``SaturationCurveError`` (so a
    ValueError, which the commands report on one line), its message naming the class, the
    label and the fleet.
    """
    curve = synthetic_saturation_curve(IridiumDials())
    label = NOT_REACHED_LABELS[device_class]
    assert label + 1 < class_curve_of(curve, device_class).rows[-1].fleet
    with pytest.raises(BindingLimitUnmeasuredError) as refused:
        class_record_at(curve, device_class, label + 1)
    assert isinstance(refused.value, SaturationCurveError)
    message = str(refused.value)
    assert f"the {device_class.value} curve reaches no saturation number" in message
    assert f"not reached by {label} satellites" in message
    assert f"living fleet of {label + 1} satellites lies past it" in message


# ---------------------------------------------------------------------------
# The scenario YAML, the stated assumptions, the promoted export.
# ---------------------------------------------------------------------------


def test_iridium_yaml_scenario_loads_and_runs(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the Iridium scenario YAML loads at its shipped settings and runs on the
    promoted curve.

    Expected outcome: the label "Iridium L-band max-outcome (every device class)", the 15.4 m^2
    panel, 16 per launch, d = 0.67, the three prices, the all-in share and the flat costs (a
    $13.0M launch at both cadence anchors and a $1.0M build); no metadata block (the default
    factory gives 2026 and a 10-year horizon); its run reaches 4,288 satellites at FY2036 with
    every class side by side.
    """
    config = load_comms_config(iridium_yaml)
    assert config.iridium is not None
    assert config.iridium.scenario_name == IRIDIUM_SCENARIO_NAME_DEFAULT
    assert IRIDIUM_SCENARIO_NAME_DEFAULT == "Iridium L-band max-outcome (every device class)"
    assert config.iridium.aperture_m2 == DEFAULT_PANEL_M2
    assert config.iridium.spectrum_mhz == HELD_SPECTRUM_MHZ
    assert config.iridium.saturation.downlink_share == DEFAULT_DOWNLINK_SHARE
    assert config.iridium.arpu == IridiumArpuDials()
    assert config.satellite.satellites_per_launch == 16
    assert config.comms_cadence.share_of_fleet == 1.0
    launch = config.launch_cost
    assert (launch.low_cadence_cost_musd, launch.high_cadence_cost_musd) == (13.0, 13.0)
    assert config.satellite.satellite_build_cost_musd == 1.0
    assert config.metadata.base_year == BASE_YEAR_DEFAULT
    assert config.metadata.horizon_years == HORIZON_YEARS_DEFAULT
    run = run_iridium_model(config, committed_saturation_curve)
    assert run.fleet.years[-1].living_fleet == LIVING_FLEET[-1]
    assert [block.device_class for block in run.iridium.classes] == CLASS_ORDER


def test_iridium_assumptions_states_ecosystem_and_ops(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the stated assumptions, rewritten for the switch.

    Expected outcome: the lines state the ecosystem assumption first, its MSS-lane statements
    among it (the phone class's tier is in-chipset, and no unmodified phone is reached), and
    operations at zero; the curve,
    the reuse calibration (0.15 at the 25 m^2 reference panel, an estimate, COMM-410 and
    COMM-411), d (each people figure and each class's downlink pool scale with it, the off-peak
    per-user rate follows the pool only where the pool caps it, and the satellite's peak and the
    busy-hour per-user rates do not move; IoT's uplink, payload and single-tone rooms with 1 - d
    and its random-access room with neither, so an IoT class's capacity follows its binding
    view), and the panel with the rule's measured limits
    (``PANEL_RULE_LIMITS_NOTE``: every class carries at least what the rule gives below the
    reference panel); the cadence fleet with no target and no cap; this run's 16 per launch
    beside the validated counts (16 with the block upgrade and its two conditions, 15 without
    it); every seat of the three people classes sold; the class
    prices held flat (the small terminal $10, the mounted terminal $50 and the phone class $15 a
    month) and the phone class's floor, $15, apart from its price; a haircut as a division with
    every margin re-derived; each class's own margin with no IoT clause; each class's usage; IoT
    as two device classes on the phone class's useful beams, those lit over inhabited cells, so
    IoT over oceans and empty land is not counted (a conservative basis), each class with its
    capacity alone at its engineering usage and never a count sold or revenue (ADR 011); the
    floor rule, IoT's capacity null below the floor; the
    room's formulas and constants with their claim IDs (COMM-659, COMM-654, COMM-714 and
    COMM-719), each view at its conservative end; the whole IoT uplink, no people class's upload
    subtracted (the phone class's on the beams IoT rides among them); each capacity at its
    engineering usage over the day, never divided by the product case's devices; government left
    out of revenue; the readings, a reading below the floor selling nothing with each IoT
    class's capacity null there; the refusals of a
    fleet past a class's last row and of a final fleet past a no-number class's label (ADR 005);
    the limits; no line calls the margin gross; no stack caveat at the default.
    """
    run = run_iridium_model(load_comms_config(iridium_yaml), committed_saturation_curve)
    lines = run.iridium.assumptions
    assert lines[0] == ECOSYSTEM_ASSUMPTION_NOTE
    for statement in ("in-chipset", "unmodified"):
        assert statement in lines[0], statement
    assert any(PANEL_RULE_LIMITS_NOTE in line for line in lines)
    joined = " ".join(lines).lower()
    for statement in (
        "operations cost is assumed zero",
        "promoted saturation curve (saturation-v1)",
        "the reuse calibration is 0.15 gbps per mhz per unit of spectral efficiency at the 25 "
        "m^2 reference panel, an estimate (comm-410, comm-411)",
        "the downlink share d is 0.67, the time-division duplex band's downlink time share (adr "
        "008): each people figure and each class's downlink pool (w x se x d) scale with it; each "
        "class's off-peak per-user rate follows the pool only where the pool caps it; the "
        "satellite's peak and each class's busy-hour per-user rate (its rate while active) do not "
        "move with d. the uplink holds the rest of the frame, 1 - d.",
        "iot's uplink, payload and single-tone rooms scale with 1 - d and its random-access room "
        "with neither, so an iot class's capacity follows 1 - d while its payload or single-tone "
        "view binds and does not move with d while its random-access view binds.",
        "a panel factor of 0.616",
        "every class carries at least what the rule gives",
        "no fleet target and no cap",
        "this run flies 16",
        "16 with the neutron block upgrade",
        "rod-held base",
        "15 without the upgrade",
        "every seat is sold: each year each people class (the small terminal, the mounted "
        "terminal and the phone class) serves every person its living fleet carries",
        "the small terminal $10, the mounted terminal $50 and the phone class $15 a month",
        "the phone class's floor is the investor's $15 a month",
        "re-derived against the same fleet cost, never divided or averaged",
        "the small terminal 2 mbps while active",
        "the mounted terminal 5 mbps",
        "the phone class 0.75 mbps",
        "iot is two device classes, minimal-packet iot and data iot",
        "in the uplink's share of the frame, 1 - d. those are the beams lit over inhabited cells, "
        "the phone class's ocean factor of the fleet's beams (each reading publishes it), so iot "
        "over oceans and empty land is not counted: a conservative basis.",
        "each iot class's device capacity alone at its engineering usage (minimal-packet iot 48 "
        "messages of 340 bytes a day; data iot 4 bursts of 100 kb a day beside 48 messages)",
        "the two capacities never add",
        "a capacity is never a count sold and never revenue",
        "the product case's (adr 011)",
        "nothing is sold in a year whose living fleet is below it, and each iot class's "
        "capacity is null there (iot needs continuous coverage)",
        "every class is sold in full and both iot capacities are published",
        "iot's room, at each year's and each reading's phone-class useful beams l, the held "
        "width w (8 mhz), the phone class's central spectral efficiency se (0.65)",
        "the uplink bits a second, l x w x se x (1 - d)",
        "times a 20 percent mac efficiency (comm-659)",
        "a random-access window of 57 to 1,650 devices (comm-654) x an assumed 1 window a second",
        "l x w over the 3.75 khz nb-iot tone (comm-714) x (1 - d)",
        "the random-access window's low end (57) and the message airtime's high end (7 s of 4 to "
        "7 s, comm-719)",
        "iot's room is the whole iot uplink: no people class's own upload (the small terminal's, "
        "the mounted terminal's, or the phone class's on the beams iot rides) is subtracted from "
        "it.",
        "each iot class's capacity is read at its engineering usage, averaged over the day",
        "so neither is divided by the other",
        "government is left out of revenue",
        "the retired cap, kept for comparison",
        "a reading below the coverage floor sells nothing, and each iot class's capacity there "
        "is null.",
        "never a build target or a cap",
        "a fleet past a class's last computed row is refused, never extrapolated or clamped",
        "so is a run whose final year's living fleet passes the fleet a class with no saturation "
        "number is not reached by",
    ):
        assert statement in joined, statement
    margin = _line_with(lines, "Each class's own margin is its own revenue")
    assert margin.endswith("null in a year with no revenue."), margin
    assert "gross" not in joined
    assert "every people and capacity figure" not in joined
    assert "every downlink capacity figure" not in joined
    assert "the terminals' own upload" not in joined
    assert "(its floor)" not in joined
    assert "exact in beams" not in joined
    assert APERTURE_STACK_CAVEAT_NOTE not in lines


def test_the_per_launch_and_price_lines_state_the_run_beside_the_validated_values(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the stated per-launch and price lines are built from the run, so a setting the
    config accepts never publishes a line written for the shipped values: the
    run's own satellites per launch beside the validated counts and the bounds' one home, and
    the run's own phone price beside the investor's floor, never the price called the floor.

    Sample: the shipped scenario, then the same at 15 satellites per launch (the no-upgrade
    bracket) and a phone class price of $20 a month (above its floor, a value the config
    accepts).

    Expected outcome: the shipped run's per-launch line says it flies 16 and the variant's 15,
    each beside the bounds 1 to 16 (the config's own bounds, the named constants) and the
    validated counts, 16 with the block upgrade (COMM-713) and 15 without (COMM-712); the
    variant's price line states the phone class at $20 a month and its floor at the investor's
    $15, and no line says "(its floor)" of a configured price.
    """
    shipped = load_comms_config(iridium_yaml)
    data = shipped.model_dump()
    data["satellite"]["satellites_per_launch"] = 15
    data["iridium"]["arpu"]["phone_class_price_usd_month"] = 20.0
    variant = CommsConfig.model_validate(data)
    assert (SATELLITES_PER_LAUNCH_MIN, SATELLITES_PER_LAUNCH_MAX) == (1, 16)
    for accepted in (SATELLITES_PER_LAUNCH_MIN, SATELLITES_PER_LAUNCH_MAX):
        assert SatelliteDials(satellites_per_launch=accepted).satellites_per_launch == accepted
    for refused in (SATELLITES_PER_LAUNCH_MIN - 1, SATELLITES_PER_LAUNCH_MAX + 1):
        with pytest.raises(ValidationError, match="satellites_per_launch"):
            SatelliteDials(satellites_per_launch=refused)
    validated = (
        "The validated counts are 16 with the Neutron block upgrade assumed from the first "
        "launch, for the stack kept in the fairing's cylinder at calculation C's pitch on a "
        "rod-held base (COMM-713), and 15 without the upgrade, the mass-bound count today "
        "(COMM-712)."
    )
    for config, flies in ((shipped, 16), (variant, 15)):
        lines = run_iridium_model(config, committed_saturation_curve).iridium.assumptions
        per_launch = _line_with(lines, "Satellites per launch is a direct scenario setting")
        assert per_launch == (
            "Satellites per launch is a direct scenario setting (bounds 1 to 16); this run "
            f"flies {flies}. {validated}"
        )
    lines = run_iridium_model(variant, committed_saturation_curve).iridium.assumptions
    prices = _line_with(lines, "Each class's price is held flat")
    assert prices.startswith(
        "Each class's price is held flat: the small terminal $10, the mounted terminal $50 and "
        "the phone class $20 a month. The phone class's floor is the investor's $15 a month, "
        "which no price haircut goes below."
    )
    assert "(its floor)" not in " ".join(lines)


def test_a_phone_price_below_the_floor_is_named_in_the_price_line(
    iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: a phone class price below the investor's floor, which the config accepts (the
    floor is a stated value, not a config bound), publishes a price line that says the run is
    below the floor, never the floor beside a price that breaks it and nothing more.

    Sample: the shipped scenario with the phone class at $12 a month (below the $15 floor); the
    same at $15 (the floor itself) and at $20 (above it).

    Expected outcome: at $12 the price line states the phone class at $12, the floor at the
    investor's $15, and that this run sets the phone class below that floor, at $12 a month (a
    scenario setting, not a haircut);
    at $15 and at $20 the floor's sentence ends where it did and no line says the run is below
    the floor.
    """
    shipped = load_comms_config(iridium_yaml)
    below = _with_iridium(shipped, arpu={"phone_class_price_usd_month": 12.0})
    lines = run_iridium_model(below, committed_saturation_curve).iridium.assumptions
    assert _line_with(lines, "Each class's price is held flat").startswith(
        "Each class's price is held flat: the small terminal $10, the mounted terminal $50 and "
        "the phone class $12 a month. The phone class's floor is the investor's $15 a month, "
        "which no price haircut goes below; this run sets the phone class below that floor, at "
        "$12 a month (a scenario setting, not a haircut). A lower price or a smaller market is a "
        "division in the conclusions"
    )
    for price in (15.0, 20.0):
        at_or_above = _with_iridium(shipped, arpu={"phone_class_price_usd_month": price})
        lines = run_iridium_model(at_or_above, committed_saturation_curve).iridium.assumptions
        line = _line_with(lines, "Each class's price is held flat")
        assert (
            f"the phone class ${price:g} a month. The phone class's floor is the investor's $15 a "
            "month, which no price haircut goes below. A lower price"
        ) in line, line
        assert "below that floor" not in " ".join(lines), price


def test_promoted_json_export_writes_frozen_baseline(
    tmp_path: Path, iridium_yaml: Path, committed_saturation_curve: SaturationCurve
) -> None:
    """Objective: the promoted-JSON writer end to end (the scenario YAML in, the artifact file
    out), frozen on iridium-v7 (IoT as capacity, ADR 011).

    Expected outcome: the file exists with provenance 'iridium', the stamp and schema
    iridium-v7; the top level in the foundation's order, ``iot_classes`` after ``classes``; the
    trajectory summary exact ($8,729.0M through FY2036, $1,554.4M final-year annualized, $406.0M
    replacement, 4,288 living, 301 launches, the floor reached in FY2031, $0.3625M a
    satellite-year); the orbit block; the physics (8 MHz, 15.4 m^2, 16 per launch, operations
    0.0, the ecosystem note) and its nine IoT constants after it, in order (340 bytes, 100,000
    bytes, 0.20, 57, 1,650, 1 a second, 3,750 Hz, 4 and 7 s); the class blocks in order with
    their prices and saturation numbers; ``iot_classes`` at the engineering usage (48, 0,
    130,560, 48 and 48; 48, 4, 3,330,560, 52 and 48); the years' fleet, cost and frozen people at
    FY2031, FY2033 and FY2036, each year's and each class line's fields in the foundation's
    order; FY2031's and FY2036's IoT rooms and capacities, the build's own print's values, with
    their binding views (1,965,864,139 and 170,588,558; 11,497,881,052 and 997,732,709; random
    access, then payload bits); FY2036's phone class useful beams the print's; the steady
    state's frozen people; the saturation block's identity (the committed curve's path, schema,
    stamp and hash), d, the panel factor, the band saturation numbers and the curve's limits,
    its fields and each reading's in the foundation's order; none of the 28 key names the v6
    schema removed and v7 did not bring back, at any depth (``V6_REMOVED_KEYS``); and every key
    name holding ``iot``, at any depth, one of the twelve v7 writes (``IOT_KEYS_V7``), so the
    file carries no other IoT key (none of guard N2's among them).
    """
    out_path = tmp_path / "iridium_default.json"
    written = export_iridium_json(iridium_yaml, out_path, version_stamp="test-stamp")
    assert written == out_path
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert list(payload) == [
        "provenance",
        "trajectory_summary",
        "orbit_scenario",
        "iridium_physics",
        "classes",
        "iot_classes",
        "years",
        "saturation",
        "assumptions",
    ]
    assert payload["provenance"] == {
        "model_name": MODEL_NAME,
        "schema_version": "iridium-v7",
        "scenario_name": IRIDIUM_SCENARIO_NAME_DEFAULT,
        "source_scenario_path": "code/scenarios/iridium.yaml",
        "version_stamp": "test-stamp",
    }
    assert payload["trajectory_summary"] == pytest.approx(
        {
            "total_cost_through_final_year_musd": TOTAL_COST_MUSD,
            "final_year_annual_cost_musd": ANNUAL_COST_MUSD[2036],
            "final_year_replacement_cost_musd": FY2036_REPLACEMENT_COST_MUSD,
            "living_fleet_final_year": LIVING_FLEET[-1],
            "cumulative_launches_final_year": LAUNCHES_THROUGH_FY2036,
            "coverage_floor_reached_year": FLOOR_YEAR,
            "cost_per_satellite_year_musd": COST_PER_SATELLITE_YEAR_MUSD,
        }
    )
    assert payload["orbit_scenario"] == {
        "altitude_km": ORBIT_ALTITUDE_KM_SCENARIO,
        "inclination_deg": ORBIT_INCLINATION_DEG_SCENARIO,
        "source_status": ORBIT_SCENARIO_SOURCE_STATUS.value,
        "basis": ORBIT_SCENARIO_BASIS,
    }
    physics = {
        "spectrum_mhz": HELD_SPECTRUM_MHZ,
        "aperture_m2": DEFAULT_PANEL_M2,
        "satellites_per_launch": 16,
        "operations_cost_musd": 0.0,
        "ecosystem_assumption": ECOSYSTEM_ASSUMPTION_NOTE,
        **IOT_PHYSICS_FROZEN,
    }
    assert payload["iridium_physics"] == physics
    assert list(payload["iridium_physics"]) == list(physics)
    classes = payload["classes"]
    assert [block["device_class"] for block in classes] == [each.value for each in CLASS_ORDER]
    assert [block["price_usd_per_month"] for block in classes] == [
        CLASS_PRICES[device_class] for device_class in CLASS_ORDER
    ]
    assert [block["saturation_number"] for block in classes] == list(FROZEN_SATURATION_NUMBERS)
    assert classes[1]["saturation_not_reached_by"] == FROZEN_MOUNTED_NOT_REACHED_BY
    assert [len(block["marginal_intervals"]) for block in classes] == [24, 26, 24]
    assert payload["iot_classes"] == [
        {
            "iot_class": iot_class.value,
            "messages_per_day": messages,
            "bursts_per_day": bursts,
            "uplink_bits_per_day": bits,
            "access_attempts_per_day": attempts,
            "single_tone_messages_per_day": tones,
        }
        for iot_class, messages, bursts, _, bits, attempts, tones in IOT_USAGE_LOADS
    ]
    years = {year["year"]: year for year in payload["years"]}
    assert [year["living_fleet"] for year in payload["years"]] == list(LIVING_FLEET)
    assert [year["comms_launches_flown"] for year in payload["years"]] == list(COMMS_LAUNCHES)
    for year, people in FROZEN_PEOPLE.items():
        assert years[year]["annual_cost_musd"] == pytest.approx(ANNUAL_COST_MUSD[year])
        assert [line["people_served"] for line in years[year]["classes"]] == list(people)
    for year in payload["years"]:
        assert list(year) == list(YEAR_KEYS)
        assert all(list(line) == list(CLASS_YEAR_KEYS) for line in year["classes"])
    for year_number, fleet, beams, room_values, tone, iot_classes in IOT_WORKED_ROOMS:
        iot = years[year_number]["iot"]
        assert years[year_number]["living_fleet"] == fleet
        assert years[year_number]["classes"][2]["useful_beams"] == pytest.approx(beams, rel=1e-9)
        assert list(iot) == list(IOT_ROOM_KEYS)
        assert (
            iot["uplink_bits_per_second"],
            iot["uplink_payload_bits_per_second"],
            iot["access_attempts_per_second_low"],
            iot["access_attempts_per_second_high"],
        ) == pytest.approx(room_values, rel=1e-9)
        assert iot["single_tone_seconds_per_second"] == pytest.approx(tone, rel=1e-9)
        for entry, iot_class, (views, capacity), binding in zip(
            iot["classes"], IOT_CLASS_ORDER, iot_classes, IOT_BINDING_VIEWS, strict=True
        ):
            assert list(entry) == list(IOT_CLASS_CAPACITY_KEYS)
            assert entry["iot_class"] == iot_class.value
            published = (
                entry["devices_by_payload_bits"],
                entry["devices_by_random_access"],
                entry["devices_by_single_tone_time"],
            )
            assert published == pytest.approx(views, rel=1e-9)
            assert (entry["device_capacity"], entry["binding_view"]) == (capacity, binding.value)
    saturation = payload["saturation"]
    assert list(saturation) == list(SATURATION_KEYS)
    assert all(list(reading) == list(READING_KEYS) for reading in saturation["readings"])
    steady = saturation["readings"][3]
    assert steady["fleet"] == STEADY_STATE_FLEET
    assert [line["people"] for line in steady["classes"]] == list(FROZEN_STEADY_STATE_PEOPLE)
    assert saturation["curve_path"] == "communications/models/iridium/saturation_curve.json"
    assert saturation["curve_schema_version"] == committed_saturation_curve.schema_version
    assert saturation["curve_version_stamp"] == committed_saturation_curve.version_stamp
    assert saturation["input_hash"] == committed_saturation_curve.input_hash
    assert saturation["downlink_share"] == DEFAULT_DOWNLINK_SHARE
    assert saturation["panel_factor"] == pytest.approx(DEFAULT_PANEL_FACTOR)
    assert saturation["band_saturation_numbers"] == FROZEN_BAND_SATURATION_NUMBERS
    assert saturation["limits"] == list(committed_saturation_curve.limits)
    assert len(V6_REMOVED_KEYS) == 28
    returned = sorted(_keys(payload) & V6_REMOVED_KEYS)
    assert returned == [], returned
    assert len(IOT_KEYS_V7) == 12
    assert {key for key in _keys(payload) if "iot" in key.lower()} == IOT_KEYS_V7


def test_regenerated_default_artifact_matches_committed(
    tmp_path: Path, iridium_yaml: Path, promoted_iridium_artifact: Path
) -> None:
    """Regenerating the promoted Iridium artifact reproduces the committed file.

    Objective: the committed communications/models/iridium/default.json is exactly
    what the current code writes from scenarios/iridium.yaml on the committed curve (the
    conclusion quotes it). Expected: a fresh export, stamped with the committed version
    stamp, parses to the same JSON document, key for key and value for value (compared first,
    for a readable difference), and is the same file byte for byte, so an integer written as a
    float, a boolean as a number or a key moved fails too.
    """
    committed = json.loads(promoted_iridium_artifact.read_text(encoding="utf-8"))
    written = export_iridium_json(
        iridium_yaml,
        tmp_path / "default.json",
        version_stamp=committed["provenance"]["version_stamp"],
    )
    regenerated = json.loads(written.read_text(encoding="utf-8"))
    assert regenerated == committed
    assert written.read_bytes() == promoted_iridium_artifact.read_bytes()


def test_the_artifact_models_read_back_their_own_schema_only(
    promoted_iridium_artifact: Path,
) -> None:
    """Objective: the artifact's models are the contract of ``iridium-v7`` alone: the committed
    file reads back through them whole, while a file stating another schema, or carrying a key
    the schema does not define, is refused rather than read as ``iridium-v7``.

    Sample: the committed ``default.json``; the same stated as ``iridium-v6``; the same with a key
    the schema does not define at the top level, and then inside FY2031's IoT room.

    Expected outcome: the committed file validates, states ``iridium-v7`` and renders back to the
    same text (with the file's one closing newline); the relabeled file raises one ValidationError
    located at ``provenance.schema_version``; each unknown key one ``extra_forbidden`` error
    located at it.
    """
    text = promoted_iridium_artifact.read_text(encoding="utf-8")
    artifact = IridiumModelArtifact.model_validate_json(text)
    assert artifact.provenance.schema_version == "iridium-v7"
    assert render_artifact_json(artifact) + ARTIFACT_FILE_END == text
    relabeled = json.loads(text)
    relabeled["provenance"]["schema_version"] = "iridium-v6"
    with pytest.raises(ValidationError) as refused:
        IridiumModelArtifact.model_validate(relabeled)
    assert [error["loc"] for error in refused.value.errors()] == [("provenance", "schema_version")]
    for location in (
        ("a_key_v7_does_not_define",),
        ("years", 5, "iot", "a_key_v7_does_not_define"),
    ):
        widened = json.loads(text)
        node = widened
        for key in location[:-1]:
            node = node[key]
        node[location[-1]] = 1
        with pytest.raises(ValidationError) as refused:
            IridiumModelArtifact.model_validate(widened)
        found = [(error["loc"], error["type"]) for error in refused.value.errors()]
        assert found == [(location, "extra_forbidden")], found
