"""The product case's named constants, its enums and its formula catalog (box B0).

Every value the product case's method uses that no scenario sets lives here: the demand
curve's anchors (Iridium's customers and ARPU today, COMM-617 and COMM-618, and data IoT's
anchor by the investor's proportion, COMM-726), the conventions (the 4 busy hours, 30 days a
month and decimal units, COMM-724), the unit conversions, the shipped scenario's defaults
(each ``*_DEFAULT``, which ``code/scenarios/product_case.yaml`` holds exactly, its own label
aside), the two schema versions, the enums every product-case list and record runs on, and
:data:`FORMULA_CATALOG`, one entry per formula of the method, from which the artifact's
``meta.formulas`` is built alone.

Each constant's docstring opens with its source class and says why that value:
``SOURCED_FACT`` (a certified ledger row), ``INVESTOR_SET`` (the date and the investor's
words, quoted, and where the words say less than the value, the approvals that made it the
value), ``SCENARIO`` (a modeling choice, with whose and when), ``DERIVED`` (computed from the
constants it names), or none for a definition, which says what it is instead: a unit
conversion, a schema version, a structural bound, a mapping, and four named here, a
scenario's default label and engineering artifact path (:data:`SCENARIO_NAME_DEFAULT` and
:data:`ENGINEERING_ARTIFACT_PATH_DEFAULT`, the run's identity), the formula catalog's path
separator (:data:`PATH_SEPARATOR`) and the engineering artifact's key of the phone class
(:data:`PHONE_DEVICE_CLASS`). A constant that is a model input also has a cell spec in
:mod:`product_case.config`, which carries its claim ID and status into the artifact's
``inputs.constants``; the definitions and the invariants' tolerance are not inputs and have
none.

IoT is never a count here: the anchors are the demand curve's starting points, today's
customers at today's prices, and every IoT customer the product case publishes comes from the
demand curve in every market and year, moving with the market, the price, the service and the
network's scale.

Every list of classes runs small terminal, mounted terminal, minimal-packet IoT, data IoT
(:class:`ProductClass`), never phone-first; the product case sells no phone class.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from common.meta import FormulaDefinition

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# The enums every product-case list and record runs on
# ---------------------------------------------------------------------------


class ProductClass(StrEnum):
    """The product case's four classes, in the order every product-case list runs.

    The two terminals sell to people, up to the seats the engineering network gives them; the
    two IoT classes sell to devices, uncapped, checked against IoT's room. Never phone-first:
    the product case sells no phone class.
    """

    SMALL_TERMINAL = "small_terminal"
    MOUNTED_TERMINAL = "mounted_terminal"
    MINIMAL_PACKET_IOT = "minimal_packet_iot"
    DATA_IOT = "data_iot"


class ClassKind(StrEnum):
    """How a class sells: a terminal up to its seats, an IoT class uncapped."""

    TERMINAL = "terminal"  # sold up to its seats; it fills busy-hour beams
    IOT = "iot"  # uncapped; its sales are checked against IoT's room, access and tone time


CLASS_KIND: Final[Mapping[ProductClass, ClassKind]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: ClassKind.TERMINAL,
        ProductClass.MOUNTED_TERMINAL: ClassKind.TERMINAL,
        ProductClass.MINIMAL_PACKET_IOT: ClassKind.IOT,
        ProductClass.DATA_IOT: ClassKind.IOT,
    }
)
"""Each class's kind (a read-only mapping, in :class:`ProductClass` order)."""

TERMINAL_DEVICE_CLASS: Final[Mapping[ProductClass, str]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: "small_terminal_class",
        ProductClass.MOUNTED_TERMINAL: "mounted_terminal_class",
    }
)
"""Each terminal class's device class in the engineering artifact (its ``device_class`` key),
whose people, beam pool and busy-hour load the product case reads (a read-only mapping)."""

PHONE_DEVICE_CLASS: Final[str] = "phone_class"
"""The engineering artifact's device class whose useful beams carry IoT (the phone rule: IoT
devices are low gain, so IoT's room rides the phone class's beams, ADR 011); the product case
reads those beams, L(t), and sells no phone."""


class UsableTest(StrEnum):
    """The tests a choice must pass in a market, in every reported year, to be usable."""

    FILL = "fill"  # the terminals' busy-hour beams filled at least the fill floor
    MARGIN = "margin"  # the year's margin at least the margin floor
    IOT_UPLINK_BUSY = "iot_uplink_busy"  # IoT's uplink use in the busy hours at most 1
    IOT_UPLINK_OFFPEAK = "iot_uplink_offpeak"  # IoT's uplink use off-peak at most 1
    RANDOM_ACCESS = "random_access"  # IoT's access use at most 1
    SINGLE_TONE_TIME = "single_tone_time"  # IoT's single-tone use at most 1
    REVENUE_RISING = "revenue_rising"  # revenue strictly rising from each year to the next


class PickBasis(StrEnum):
    """Why the pick is the pick: the robust floor met, or the most usable candidate, warned."""

    ROBUST_FLOOR_MET = "robust_floor_met"
    MOST_USABLE_FALLBACK = "most_usable_fallback"


class RunState(StrEnum):
    """Where a run ends: a pick, or no candidate usable in any draw (no pick, no headline)."""

    PICKED = "picked"
    NO_USABLE_CHOICE = "no_usable_choice"


class SpreadNullReason(StrEnum):
    """Why a spread's percentiles are null."""

    TOO_FEW_USABLE_DRAWS = "too_few_usable_draws"  # below the draws the exclusive method needs


class SpreadField(StrEnum):
    """The headline values the spreads cover, in the order the artifact lists them."""

    SMALL_TERMINAL_CUSTOMERS = "small_terminal.customers"
    SMALL_TERMINAL_REVENUE = "small_terminal.revenue_musd"
    MOUNTED_TERMINAL_CUSTOMERS = "mounted_terminal.customers"
    MOUNTED_TERMINAL_REVENUE = "mounted_terminal.revenue_musd"
    MINIMAL_PACKET_IOT_CUSTOMERS = "minimal_packet_iot.customers"
    MINIMAL_PACKET_IOT_REVENUE = "minimal_packet_iot.revenue_musd"
    DATA_IOT_CUSTOMERS = "data_iot.customers"
    DATA_IOT_REVENUE = "data_iot.revenue_musd"
    REVENUE = "revenue_musd"
    MARGIN = "margin_pct"
    IOT_UPLINK_USE_BUSY = "iot_uplink_use_busy"
    IOT_UPLINK_USE_OFFPEAK = "iot_uplink_use_offpeak"


# ---------------------------------------------------------------------------
# Schema versions
# ---------------------------------------------------------------------------

PRODUCT_CASE_SCHEMA_VERSION: Final[str] = "product-case-v1"
"""The schema version of the product case's artifact (``metadata.schema_version``)."""

ENGINEERING_SCHEMA_VERSION: Final[str] = "iridium-v7"
"""The one engineering artifact schema the product case reads (the pin): any other schema is
refused, so a schema bump of the engineering artifact lands only with a product-case change
that re-pins it, and the product case always states which engineering contract it read."""


# ---------------------------------------------------------------------------
# Unit conversions (definitions: they cite nothing)
# ---------------------------------------------------------------------------

BITS_PER_BYTE: Final[int] = 8
"""Bits in a byte."""

BITS_PER_MEGABIT: Final[int] = 1_000_000
"""Bits in a megabit (decimal), for the engineering artifact's rates in Mbps."""

SECONDS_PER_HOUR: Final[int] = 3_600
"""Seconds in an hour."""

HOURS_PER_DAY: Final[int] = 24
"""Hours in a day."""

SECONDS_PER_DAY: Final[int] = HOURS_PER_DAY * SECONDS_PER_HOUR
"""Seconds in a day, 86,400: a device's messages are spread over the whole day."""

MONTHS_PER_YEAR: Final[int] = 12
"""Months in a year: a monthly price times 12 is a year's revenue."""

DOLLARS_PER_MILLION: Final[int] = 1_000_000
"""Dollars in a million: revenue and cost are published in $M (``*_musd``)."""

PERCENT: Final[float] = 100.0
"""Percent in a whole: the margin is published in percent (``margin_pct``)."""


# ---------------------------------------------------------------------------
# The conventions (model inputs: each has a cell spec, COMM-724)
# ---------------------------------------------------------------------------

BUSY_HOURS_PER_DAY: Final[int] = 4
"""INVESTOR_SET (2026-10-04 19:59, asked to set the 4: "I'm not sure what you mean by four, but
that's okay. ... So for busy hours, it's fine"; COMM-724): the busy hours a day. A terminal's
busy-hour data a month is its engineering usage over these hours, so its busy-hour load and its
seats are the engineering case's; the rest of its data goes in the other hours."""

OFFPEAK_HOURS_PER_DAY: Final[int] = HOURS_PER_DAY - BUSY_HOURS_PER_DAY
"""DERIVED: the off-peak hours a day, 20, the day's hours less the busy hours; data IoT's bursts
outside the busy hours are spread over them."""

DAYS_PER_MONTH: Final[int] = 30
"""SCENARIO (round 1 of the product case's scratch exploration, 2026-10-06; COMM-724): a month is
30 days and a year 12 such months, never 365 days; the convention every monthly and yearly
figure of the product case uses."""

BYTES_PER_GB: Final[int] = 1_000_000_000
"""SCENARIO (round 1's convention, 2026-10-06; COMM-724): decimal units, a GB is 10^9 bytes."""


# ---------------------------------------------------------------------------
# The demand curve's anchors: Iridium today, and data IoT by the investor's proportion
# ---------------------------------------------------------------------------

VOICE_DATA_CUSTOMERS_TODAY: Final[int] = 402_000
"""SOURCED_FACT (COMM-617, certified): Iridium's commercial voice-and-data subscribers at
year-end 2025, the small terminal's anchor on the demand curve (today's customers of that kind
at today's ARPU) and, with broadband, today's terminal customer mix behind the class split."""

BROADBAND_CUSTOMERS_TODAY: Final[int] = 16_100
"""SOURCED_FACT (COMM-617, certified): Iridium's commercial broadband subscribers at year-end
2025, the mounted terminal's anchor on the demand curve and the other half of today's mix."""

IOT_CUSTOMERS_TODAY: Final[int] = 1_998_000
"""SOURCED_FACT (COMM-617, certified): Iridium's commercial IoT subscribers at year-end 2025,
minimal-packet IoT's anchor on the demand curve; the curve's starting point, never a count the
product case sets."""

VOICE_DATA_ARPU_USD_MONTH: Final[float] = 47.0
"""SOURCED_FACT (COMM-618, certified): Iridium's commercial voice-and-data ARPU, dollars a month,
the small terminal's anchor price on the demand curve."""

BROADBAND_ARPU_USD_MONTH: Final[float] = 259.0
"""SOURCED_FACT (COMM-618, certified): Iridium's commercial broadband ARPU, dollars a month, the
mounted terminal's anchor price on the demand curve."""

IOT_ARPU_USD_MONTH: Final[float] = 7.78
"""SOURCED_FACT (COMM-618, certified): Iridium's commercial IoT ARPU, dollars a month,
minimal-packet IoT's anchor price on the demand curve."""

TERMINAL_CUSTOMERS_TODAY: Final[int] = VOICE_DATA_CUSTOMERS_TODAY + BROADBAND_CUSTOMERS_TODAY
"""DERIVED (COMM-617): Iridium's terminal customers today, 418,100 (voice and data plus
broadband); the network's scale k(t) is the terminals' seats over this base."""

DATA_IOT_ANCHOR_SHARE: Final[float] = 0.5
"""INVESTOR_SET (the investor's proportion, 2026-10-04: "You look for proportions, look at
research. It's not rocket science, extrapolate it out. Are they going to have as many as the
small, minimal pack IOT? No. Is it going to have more than the small terminal, double the price?
Yes"; COMM-726): data IoT's anchor is half of Iridium's IoT customers today. The words give the
bounds (fewer than minimal-packet IoT, more than the small terminal) and the doubled price; the
half is the investor's method that day, a proportion from the research: Iridium's tiers run close
to inverse proportion (IoT 1,998,000 at $7.78 against voice and data 402,000 at $47, COMM-617 and
COMM-618), so twice the price holds half the customers. It became the product case's value with
the code design the investor approved at its gate (2026-10-07 13:03: "So actually, I think we're
on yes. I think this is yes") and the plan (2026-10-12 20:27: "yes, approved, go ahead with the
plan"). It sets the demand curve's starting point only: data IoT's customers in every market and
year come from the curve."""

DATA_IOT_PRICE_MULTIPLE: Final[float] = 2.0
"""INVESTOR_SET (the investor's proportion, 2026-10-04: "Is it going to have more than the small
terminal, double the price? Yes"; kept in every IoT price the investor set: "data IoT ... $8.00,
the minimal packet is $4.00", 2026-10-04, then "Let's go with the three and six for now",
2026-10-06 19:52; COMM-722 and COMM-726): data IoT's price is twice minimal-packet IoT's in every
year (so data IoT's price is not a setting), and its anchor price twice Iridium's IoT ARPU
today."""

DATA_IOT_ANCHOR_CUSTOMERS: Final[float] = IOT_CUSTOMERS_TODAY * DATA_IOT_ANCHOR_SHARE
"""DERIVED (COMM-617 by the investor's proportion; COMM-726): data IoT's anchor customers,
999,000, half of Iridium's IoT customers today. Iridium reports one commercial IoT segment
(1,998,000 subscribers at $7.78 a month, COMM-617 and COMM-618); the product case takes it whole
as minimal-packet IoT's anchor and anchors data IoT beside it, so the two IoT classes start from
twice Iridium's IoT revenue today ($373.1M a year against $186.5M)."""

DATA_IOT_ANCHOR_ARPU_USD_MONTH: Final[float] = IOT_ARPU_USD_MONTH * DATA_IOT_PRICE_MULTIPLE
"""DERIVED (COMM-618 by the investor's proportion; COMM-726): data IoT's anchor price, $15.56 a
month, double Iridium's IoT ARPU today."""


@dataclass(frozen=True)
class DemandAnchor:
    """A class's starting point on the demand curve: its customers at its price today.

    Attributes:
        customers: N_c, the class's customers today (data IoT's by the investor's proportion).
        arpu_usd_month: A_c, the price they pay today, dollars a month.
    """

    customers: float
    arpu_usd_month: float


DEMAND_ANCHORS: Final[Mapping[ProductClass, DemandAnchor]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: DemandAnchor(
            float(VOICE_DATA_CUSTOMERS_TODAY), VOICE_DATA_ARPU_USD_MONTH
        ),
        ProductClass.MOUNTED_TERMINAL: DemandAnchor(
            float(BROADBAND_CUSTOMERS_TODAY), BROADBAND_ARPU_USD_MONTH
        ),
        ProductClass.MINIMAL_PACKET_IOT: DemandAnchor(
            float(IOT_CUSTOMERS_TODAY), IOT_ARPU_USD_MONTH
        ),
        ProductClass.DATA_IOT: DemandAnchor(
            DATA_IOT_ANCHOR_CUSTOMERS, DATA_IOT_ANCHOR_ARPU_USD_MONTH
        ),
    }
)
"""Each class's anchor (N_c, A_c), in :class:`ProductClass` order; the values keep their own
constants' tags (a read-only mapping)."""


# ---------------------------------------------------------------------------
# Structural bounds and the invariants' tolerance (definitions)
# ---------------------------------------------------------------------------

MIN_REPORTED_YEARS: Final[int] = 2
"""The fewest reported years a scenario may hold: the price and usage lines run from the first
reported year to the last, and revenue must rise between them (the design's D14)."""

MIN_DRAWS: Final[int] = 9
"""The fewest market draws a scenario may hold: below 9 values the exclusive method's 10th and
90th percentile cuts fall outside the data (the design's D10), so the spreads would mislead."""

USAGE_SCALE_START: Final[float] = 1.0
"""The first usage scale of every IoT class's list: the scenario's own path, unscaled; the
list rises from it ("we just increase usage", the investor, 2026-10-06)."""

RELATIVE_TOLERANCE: Final[float] = 1e-9
"""SCENARIO (the product-case code design's invariants, approved by the investor at its gate on
2026-10-07): the relative tolerance of the run's invariants (whole customers, a terminal never
past its seats, revenue equal to customers times price times 12), a billionth: well above the
rounding of double arithmetic (about 1e-16 relative a step), so float rounding alone never
refuses a run, and far below any quantity the product case publishes."""


# ---------------------------------------------------------------------------
# The shipped scenario's defaults (code/scenarios/product_case.yaml holds exactly these, its
# own label aside)
# ---------------------------------------------------------------------------

SCENARIO_NAME_DEFAULT: Final[str] = "A product-case scenario"
"""The label of a scenario that sets none (the artifact's ``metadata.scenario_name``): neutral,
so a side run that names nothing claims nothing about its prices or usage; the label is the run's
identity, not an input cell, so no override would mark it. The shipped scenario names itself
("The product case at the investor's prices, held flat")."""

ENGINEERING_ARTIFACT_PATH_DEFAULT: Final[str] = "communications/models/iridium/default.json"
"""The engineering artifact the product case reads, repository-relative: the promoted Iridium
artifact, which the Iridium command writes; a file location, not a sourced value."""

REPORTED_YEARS_DEFAULT: Final[tuple[int, ...]] = (2031, 2033, 2035, 2036)
"""SCENARIO (the 2026-10-05 product-case design; COMM-723): the reported fiscal years, FY2031
(the first year of service on the committed engineering artifact) to FY2036 (the horizon's
end); the method's years, on which the summed revenue and the usable test run."""

SMALL_TERMINAL_START_PRICE_USD_MONTH_DEFAULT: Final[float] = 10.0
"""INVESTOR_SET (2026-10-07, about 10:55: "Yes, let's use the $10 and $50. Let's do that";
COMM-722): the small terminal's price a month in the first reported year, held flat (2026-10-06
19:38: "The prices will not go down, but they will not go up"); the engineering model's small
terminal price too (one price list)."""

SMALL_TERMINAL_END_PRICES_USD_MONTH_DEFAULT: Final[tuple[float, ...]] = (10.0, 9.0, 8.0, 7.0, 6.0)
"""INVESTOR_SET for the first entry, the start price (2026-10-07: "Yes, let's use the $10 and
$50. Let's do that") held flat (2026-10-06 19:38: "The prices will not go down, but they will not
go up"); SCENARIO for the rest, context only (the product-case code design's rule, approved by the
investor at its gate on 2026-10-07; COMM-722 and COMM-723): steps of a tenth of the investor's
price down to the lowest step at or above the class's break-even alone in every reported year."""

MOUNTED_TERMINAL_START_PRICE_USD_MONTH_DEFAULT: Final[float] = 50.0
"""INVESTOR_SET (2026-10-07, about 10:55: "Yes, let's use the $10 and $50. Let's do that";
COMM-722): the mounted terminal's price a month in the first reported year, held flat (2026-10-06
19:38: "The prices will not go down, but they will not go up"); the engineering model's mounted
terminal price too (one price list)."""

MOUNTED_TERMINAL_END_PRICES_USD_MONTH_DEFAULT: Final[tuple[float, ...]] = (50.0, 45.0, 40.0)
"""INVESTOR_SET for the first entry, the start price (2026-10-07: "Yes, let's use the $10 and
$50. Let's do that") held flat (2026-10-06 19:38: "The prices will not go down, but they will not
go up"); SCENARIO for the rest, context only (the product-case code design's rule, approved by the
investor at its gate on 2026-10-07; COMM-722 and COMM-723): steps of a tenth of the investor's
price down to the lowest step at or above the class's break-even alone in every reported year."""

MINIMAL_PACKET_IOT_START_PRICE_USD_MONTH_DEFAULT: Final[float] = 3.0
"""INVESTOR_SET (2026-10-06 19:52: "Let's go with the three and six for now"; COMM-722):
minimal-packet IoT's price a month, held flat (2026-10-06 19:38: "The prices will not go down, but
they will not go up"); data IoT pays twice it."""

MINIMAL_PACKET_IOT_END_PRICES_USD_MONTH_DEFAULT: Final[tuple[float, ...]] = (3.0,)
"""INVESTOR_SET (2026-10-06 19:52: "Let's go with the three and six for now", held flat, 19:38:
"The prices will not go down, but they will not go up"; COMM-722): minimal-packet IoT's one end
price, its start price; the grid holds no lower IoT price."""

SMALL_TERMINAL_GB_PER_MONTH_DEFAULT: Final[tuple[float, ...]] = (5.4, 6.7, 8.1, 9.0)
"""INVESTOR_SET for FY2031, FY2035 and FY2036; SCENARIO for FY2033 (COMM-724): the small
terminal's data a month in all, in each reported year; its busy-hour part is the engineering
usage's and the rest goes off-peak. FY2031's 5.4 GB is the engineering usage the investor approved
(2026-10-04 13:33: "yes, go with the recommended column": 2 Mbps while active, 2.5 percent active
at the busy hour and 0.5 percent off-peak) over the 4 busy hours (2026-10-04 19:59: "So for busy
hours, it's fine") and the 20 off-peak hours, 2.7 GB each. FY2035's 8.1 GB is 5.4 GB with the
investor's bigger allotment (2026-10-05: "for some of your bigger products, you get a 50% increase
in your monthly allotment ... this is just a rough estimate right now"). FY2036's 9 GB the investor
set (2026-10-12 15:56: "go with 9 GB, 90 GB and 13 bursts"). FY2033's 6.7 GB is about half-way
(round 1's 2.7 + 4.0 GB). The words of 2026-10-04 and 2026-10-05 give a usage and a rough
allotment, not these totals; the totals became the product case's values with the code design the
investor approved at its gate (2026-10-07 13:03, Q1 to Q5 yes: "So actually, I think we're on yes.
I think this is yes") and the plan (2026-10-12 20:27: "yes, approved, go ahead with the plan"),
which keeps FY2035 at 8.1 GB."""

MOUNTED_TERMINAL_GB_PER_MONTH_DEFAULT: Final[tuple[float, ...]] = (54.0, 67.0, 81.0, 90.0)
"""INVESTOR_SET for FY2031, FY2035 and FY2036; SCENARIO for FY2033 (COMM-724): the mounted
terminal's data a month in all, in each reported year; its busy-hour part is the engineering
usage's and the rest goes off-peak. FY2031's 54 GB is the engineering usage the investor approved
(2026-10-04 13:33: "yes, go with the recommended column": 5 Mbps while active, 10 percent active at
the busy hour and 2 percent off-peak) over the 4 busy hours (2026-10-04 19:59: "So for busy hours,
it's fine") and the 20 off-peak hours, 27 GB each. FY2035's 81 GB is 54 GB with the investor's
bigger allotment (2026-10-05: "for some of your bigger products, you get a 50% increase in your
monthly allotment ... this is just a rough estimate right now"). FY2036's 90 GB the investor set
(2026-10-12 15:56: "go with 9 GB, 90 GB and 13 bursts"). FY2033's 67 GB is about half-way (round
1's 27 + 40 GB). The words of 2026-10-04 and 2026-10-05 give a usage and a rough allotment, not
these totals; the totals became the product case's values with the code design the investor
approved at its gate (2026-10-07 13:03, Q1 to Q5 yes: "So actually, I think we're on yes. I think
this is yes") and the plan (2026-10-12 20:27: "yes, approved, go ahead with the plan"), which keeps
FY2035 at 81 GB."""

MINIMAL_PACKET_IOT_MESSAGES_PER_DAY_DEFAULT: Final[tuple[int, ...]] = (48, 72, 96, 96)
"""SCENARIO (round 1 of the scratch exploration, 2026-10-06; COMM-724): minimal-packet IoT's
messages a day in each reported year, before a choice's usage scale: 48, the engineering usage,
doubling to 96 by FY2035 and held; a usage a device sends, never a count of devices."""

MINIMAL_PACKET_IOT_SCALES_DEFAULT: Final[tuple[float, ...]] = (1.0, 2.0, 4.0, 8.0, 16.0)
"""SCENARIO (round 3's 1, 2 and 4, 2026-10-06, extended so the usable test, not the grid, stops
the usage, approved by the investor with the code design on 2026-10-07; COMM-723): the usage
scales a choice may take for minimal-packet IoT by the last reported year, each step doubling."""

DATA_IOT_MESSAGES_PER_DAY_DEFAULT: Final[int] = 48
"""INVESTOR_SET (the investor's usage table, frozen 2026-10-04 12:31: "This looks good ... we'll
kind of freeze it here"; COMM-724): data IoT's messages a day in every year, the engineering
usage's 48 messages of 340 bytes, beside its bursts; the usage scale moves its bursts, not its
messages. The table gave data IoT its bursts on top of those messages and the words freeze the
table as a whole; the 48 became the product case's value with the code design the investor
approved at its gate (2026-10-07 13:03) and the plan (2026-10-12 20:27: "yes, approved, go ahead
with the plan")."""

DATA_IOT_BURSTS_PER_DAY_DEFAULT: Final[tuple[int, ...]] = (8, 10, 12, 13)
"""INVESTOR_SET for FY2031's 8 (2026-10-05: "My thinking is $8 is quite expensive for just 4
bursts of 100 kilobytes a day. So let's say we just doubled that") and FY2036's 13 (2026-10-12
15:56: "go with 9 GB, 90 GB and 13 bursts"); SCENARIO for FY2033's 10 and FY2035's 12 (round 1 of
the scratch exploration); COMM-724: data IoT's 100 KB bursts a day in each reported year, before a
choice's usage scale; a usage a device sends, never a count of devices. The 2026-10-05 words were
thinking aloud ("we don't have to change anything"); the 8 became the product case's value with
the code design the investor approved at its gate (2026-10-07 13:03) and the plan (2026-10-12
20:27: "yes, approved, go ahead with the plan")."""

DATA_IOT_BURSTS_OUTSIDE_BUSY_HOURS_DEFAULT: Final[tuple[bool, ...]] = (False, True, True, True)
"""INVESTOR_SET for FY2033 to FY2036 (2026-10-05: "Could the data IoT at the higher price do
bursts like 12 or 24 bursts a day? Maybe you could say excluding peak time or something like
that"; COMM-724): from FY2033 data IoT's bursts go outside the busy hours, spread over the 20
off-peak hours; SCENARIO for FY2031's, at any hour (round 1). The words asked a question; the
timing became the product case's value with the code design the investor approved at its gate
(2026-10-07 13:03) and the plan (2026-10-12 20:27: "yes, approved, go ahead with the plan")."""

DATA_IOT_SCALES_DEFAULT: Final[tuple[float, ...]] = (1.0, 2.0, 4.0, 8.0)
"""SCENARIO (round 3's 1, 2 and 4, 2026-10-06, extended so the usable test, not the grid, stops
the usage, approved by the investor with the code design on 2026-10-07; COMM-723): the usage
scales a choice may take for data IoT by the last reported year, each step doubling."""

DRAWS_DEFAULT: Final[int] = 2_000
"""SCENARIO (round 2 of the scratch exploration, 2026-10-06, approved by the investor with the
product-case code design at its gate on 2026-10-07; COMM-723): the market draws. What 2,000 buy:
the pick holds across seeds (at seeds 1 to 5 it is the same choice, usable in 1,719 to 1,754 of
the 2,000 draws, the plan's probe pB2, local), and the headline, read at the central market, moves
with neither the draws nor the seed; the spreads' 10th and 90th percentiles need at least 9
(:data:`MIN_DRAWS`)."""

SEED_DEFAULT: Final[int] = 20_261_006
"""SCENARIO (round 2, 2026-10-06; COMM-723): the seed of the standard generator that draws the
markets, so every run draws the same markets (round 3's stream); another seed moves the drawn
markets and can move the pick near a floor, never the central market (the pick holds at seeds 1 to
5, :data:`DRAWS_DEFAULT`)."""

GAMMA_LOW_DEFAULT: Final[float] = 0.5
"""SCENARIO (round 2, 2026-10-06; COMM-723): the network response's low end, 0.5: customers grow
as the square root of the network's scale, so four times the network only doubles them. No market
research grounds the three ranges: they are a modeling choice, approved by the investor with the
product-case code design at its gate on 2026-10-07."""

GAMMA_HIGH_DEFAULT: Final[float] = 1.0
"""SCENARIO (round 2, 2026-10-06; COMM-723): the network response's high end, 1.0: customers grow
in proportion to the network's scale, the investor's "If we are getting eight times the network
overall, we should be getting about eight times the revenue. That is just an approximation"
(2026-10-06); at the range's middle, 0.75, eight times the network brings 4.76 times the
customers. A modeling choice (no market research grounds it), approved with the code design on
2026-10-07."""

EPSILON_LOW_DEFAULT: Final[float] = 0.5
"""SCENARIO (round 2, 2026-10-06; COMM-723): the price response's low end, 0.5: customers grow as
the square root of today's price over the class's, so a price half today's brings 1.41 times the
customers and the revenue falls 29 percent. The range, 0.5 to 1.5, is centred on 1
(:data:`EPSILON_HIGH_DEFAULT` says what that middle does). A modeling choice (no market research
grounds it), approved with the code design on 2026-10-07."""

EPSILON_HIGH_DEFAULT: Final[float] = 1.5
"""SCENARIO (round 2, 2026-10-06; COMM-723): the price response's high end, 1.5: a price half
today's brings 2.83 times the customers and the revenue rises 41 percent (a price a third lower,
1.84 times the customers). The range is centred on 1, so at the central market, where the
headline is read, the price response is exactly 1: for a given usage an uncapped class's price
change shows there as customers, not revenue, and a terminal at its seats shows it as revenue; the
headline moves with a price only through the usage the pick then takes (the design's D7, ADR 012).
A modeling choice (no market research grounds it), approved with the code design on 2026-10-07."""

ETA_LOW_DEFAULT: Final[float] = 0.0
"""SCENARIO (round 2, 2026-10-06; COMM-723): the service response's low end, 0: more service brings
no customers. A modeling choice (no market research grounds it), approved with the code design on
2026-10-07."""

ETA_HIGH_DEFAULT: Final[float] = 0.5
"""SCENARIO (round 2, 2026-10-06; COMM-723): the service response's high end, 0.5: half again the
service brings 22 percent more customers and twice the service 41 percent more; at the range's
middle, 0.25, half again the service brings 11 percent more. A modeling choice (no market research
grounds it), approved with the code design on 2026-10-07."""

FILL_FLOOR_DEFAULT: Final[float] = 0.75
"""SCENARIO (round 2's reading of the investor's "We do not want half our network used",
2026-10-06; COMM-725): the share of the terminals' busy-hour beams a usable choice fills in
every reported year."""

ROBUST_FLOOR_DEFAULT: Final[float] = 0.75
"""SCENARIO (round 2's reading of the investor's "Take the clearly usable ones and then pick where
you are", 2026-10-06; COMM-725): the share of the drawn markets in which the pick must be usable;
the pick is the most median revenue among the candidates that reach it."""

MARGIN_FLOOR_PCT_DEFAULT: Final[float] = 50.0
"""INVESTOR_SET ("at least 50%", 2026-10-06; confirmed 2026-10-07 on the whole business: "I think
about a 50% floor for margin"; COMM-725): the whole business's margin a usable choice keeps in
every reported year, in percent."""


# ---------------------------------------------------------------------------
# The formula catalog: one entry per formula of the method
# ---------------------------------------------------------------------------


class ProductCaseFormula(StrEnum):
    """The product case's formulas, the key type of :data:`FORMULA_CATALOG`.

    Each value is its catalog entry's ``formula_id`` and the ``formula_name`` of every
    provenance cell it computes. The members run in the method's order: the reported years and
    the network (step 1), the offers (step 2), the demand curve and the sales (steps 3 and 4), a
    year's numbers (step 5), usable (step 6), each choice over the draws (step 7), the grid, the
    fronts and the pick (step 8), the headline and the spreads (step 9), then the source-status
    summary of the run's inputs.
    """

    REPORTED_YEARS = "reported_years"
    CLASS_SPLIT = "class_split"
    SEATS = "seats"
    NETWORK_SCALE = "network_scale"
    IOT_ROOMS_READ = "iot_rooms_read"
    FLEET_ANNUAL_COST = "fleet_annual_cost"
    TERMINAL_ACTIVE_RATE = "terminal_active_rate"
    TERMINAL_BUSY_HOUR_DATA = "terminal_busy_hour_data"
    TERMINAL_OFFPEAK_DATA = "terminal_offpeak_data"
    PRICE_LINE = "price_line"
    USAGE_LINE = "usage_line"
    IOT_BYTES_PER_DAY = "iot_bytes_per_day"
    SERVICE = "service"
    PER_DEVICE_LOADS = "per_device_loads"
    TERMINAL_DOWNLINK_USE = "terminal_downlink_use"
    PRICE_PER_UNIT = "price_per_unit"
    DEMAND_CURVE = "demand_curve"
    SOLD = "sold"
    CLASS_REVENUE = "class_revenue"
    BUSY_HOUR_BEAMS_FILLED = "busy_hour_beams_filled"
    REVENUE = "revenue"
    MARGIN = "margin"
    PROFIT = "profit"
    IOT_UPLINK_USE = "iot_uplink_use"
    ACCESS_USE = "access_use"
    ACCESS_ATTEMPTS_PER_BEAM = "access_attempts_per_beam"
    SINGLE_TONE_USE = "single_tone_use"
    GB_CARRIED = "gb_carried"
    COST_PER_GB_CARRIED = "cost_per_gb_carried"
    USABLE = "usable"
    CHOICE_GRID = "choice_grid"
    USABLE_DRAWS = "usable_draws"
    DRAWS_FAILING = "draws_failing"
    MEDIAN_SUMMED_REVENUE = "median_summed_revenue"
    MEDIAN_LAST_YEAR_REVENUE = "median_last_year_revenue"
    CENTRAL_SUMMED_REVENUE = "central_summed_revenue"
    FRONT = "front"
    PICK = "pick"
    DOMINATED_IN_CONTEXT_BY = "dominated_in_context_by"
    CENTRAL_MARKET = "central_market"
    HEADLINE = "headline"
    PERCENTILES = "percentiles"
    MID_RANK = "mid_rank"
    EVERY_SEAT_SHARES = "every_seat_shares"
    DRAWS_PAST_IOT_ROOM = "draws_past_iot_room"
    SOURCE_STATUS_SUMMARY = "source_status_summary"


PATH_SEPARATOR: Final[str] = "; "
"""How a catalog entry's ``output_path_pattern`` (and ``input_path_pattern``) separates the paths
it names. A definition, not an input. Each path is written as the data-dictionary walker
(:func:`common.meta.build_data_dictionary`) writes the artifact's leaves, and a test of every
published number reads it so: dotted field names; a list's or a map's records or cells as ``[]``
after its name (``headline.years[].totals``); a list or a map of plain values as one leaf at its
own name (``choices[].draws_failing``, ``choices[].central_revenue_musd``); never ``*``. A path
that ends at a record, a list of records or a map names every leaf under it
(``headline.market``, ``meta.source_status_summary``). An input is named by its input path, the
key of its cell in ``inputs.scenario``, ``inputs.constants`` or ``inputs.engineering`` (maps of
cells, which the walker lists as ``inputs.scenario[]`` and the like); a path that is a prefix of
input paths names each of them (``inputs.scenario.usage``), and a value read in each reported
year is named once, without its year (``inputs.engineering.people_small_terminal``). Two
patterns are prose, saying what an entry reads or publishes outside the artifact's leaves."""


def _entry(
    formula: ProductCaseFormula,
    *,
    text: str,
    description: str,
    inputs: tuple[str, ...],
    outputs: tuple[str, ...],
    units: str,
    notes: str | None = None,
) -> tuple[ProductCaseFormula, FormulaDefinition]:
    """Build one catalog entry, its paths joined by :data:`PATH_SEPARATOR`."""
    return formula, FormulaDefinition(
        formula_id=formula.value,
        formula_text=text,
        description=description,
        input_path_pattern=PATH_SEPARATOR.join(inputs),
        output_path_pattern=PATH_SEPARATOR.join(outputs),
        unit_behavior=units,
        scenario_notes=notes,
    )


_HEADLINE_CLASS: Final[str] = "headline.years[].classes[]"
"""The data-dictionary path of a headline class entry (the four classes side by side)."""

_HEADLINE_TOTALS: Final[str] = "headline.years[].totals"
"""The data-dictionary path of a headline year's totals."""

_SPREAD_FIELD: Final[str] = "spreads.years[].fields[]"
"""The data-dictionary path of one spread field's entry."""

FORMULA_CATALOG: Final[Mapping[ProductCaseFormula, FormulaDefinition]] = MappingProxyType(
    dict(
        (
            _entry(
                ProductCaseFormula.REPORTED_YEARS,
                text=(
                    "the reported fiscal years t0 < ... < t1, as the scenario sets them; each "
                    "reported year's entry in the network, the headline and the spreads carries "
                    "its year"
                ),
                description=(
                    "The years the method runs on, in order: the price and usage lines run from "
                    "the first to the last, and the summed revenue and the usable test over them."
                ),
                inputs=("inputs.scenario.reported_years",),
                outputs=("network.years[].year", "headline.years[].year", "spreads.years[].year"),
                units="fiscal year",
            ),
            _entry(
                ProductCaseFormula.CLASS_SPLIT,
                text=(
                    "s = (n_v / u_small) / ((n_v / u_small) + (n_b / u_mounted)), with n_v = "
                    "N_v / (N_v + N_b) and n_b = 1 - n_v today's terminal mix (N_v 402,000 voice "
                    "and data, N_b 16,100 broadband, COMM-617) and u_c = beam_pool_mbps / "
                    "(active_user_rate_mbps x concurrency_peak), a terminal class's people a beam "
                    "in the engineering artifact"
                ),
                description=(
                    "The class split: the small terminal's share of the busy-hour beams, today's "
                    "terminal mix turned into beam shares through each class's people a beam (the "
                    "engineering case's split); the mounted terminal holds the rest, 1 - s."
                ),
                inputs=(
                    "inputs.constants.anchors.small_terminal.customers",
                    "inputs.constants.anchors.mounted_terminal.customers",
                    "inputs.engineering.small_terminal",
                    "inputs.engineering.mounted_terminal",
                ),
                outputs=("network.small_terminal_share",),
                units="a share of the terminals' beams (unitless, 0 to 1)",
            ),
            _entry(
                ProductCaseFormula.SEATS,
                text=(
                    "S_small(t) = s x P_small(t); S_mounted(t) = (1 - s) x P_mounted(t), "
                    "unrounded, with P_c(t) the engineering artifact's whole-fleet people of the "
                    "class in year t (years[].classes[].people_served)"
                ),
                description=(
                    "Each terminal's seats: its share of the fleet's beams times the people the "
                    "whole fleet carries for that class alone."
                ),
                inputs=(
                    "network.small_terminal_share",
                    "inputs.engineering.people_small_terminal",
                    "inputs.engineering.people_mounted_terminal",
                ),
                outputs=(
                    "network.years[].seats_small_terminal",
                    "network.years[].seats_mounted_terminal",
                    f"{_HEADLINE_CLASS}.terminal.seats",
                ),
                units="people (seats), unrounded",
            ),
            _entry(
                ProductCaseFormula.NETWORK_SCALE,
                text=(
                    "k(t) = (S_small(t) + S_mounted(t)) / 418,100, Iridium's terminal customers "
                    "today (COMM-617)"
                ),
                description=(
                    "The network's scale: the terminals' seats over Iridium's terminal customers "
                    "today, how many times today's terminal network the fleet carries."
                ),
                inputs=(
                    "network.years[].seats_small_terminal",
                    "network.years[].seats_mounted_terminal",
                    "inputs.constants.terminal_customers_today",
                ),
                outputs=("network.years[].network_scale",),
                units="a multiple of today's terminal base (unitless)",
            ),
            _entry(
                ProductCaseFormula.IOT_ROOMS_READ,
                text=(
                    "R(t) = years[].iot.uplink_payload_bits_per_second; A(t) = "
                    "years[].iot.access_attempts_per_second_low; T(t) = "
                    "years[].iot.single_tone_seconds_per_second; L(t) = the phone class's "
                    "years[].classes[].useful_beams; each read as the engineering artifact "
                    "publishes it for year t"
                ),
                description=(
                    "IoT's three rooms, payload bits, random access at the window's low end and "
                    "single-tone time, and the phone class's useful beams IoT rides, read from the "
                    "engineering artifact; the product case recomputes none of them."
                ),
                inputs=("the engineering artifact (iridium-v7), at its recorded SHA-256",),
                outputs=(
                    "inputs.engineering.iot_payload_bits_per_second",
                    "inputs.engineering.iot_access_attempts_per_second",
                    "inputs.engineering.iot_single_tone_seconds_per_second",
                    "inputs.engineering.phone_useful_beams",
                ),
                units="bits a second; attempts a second; tone-seconds a second; beams",
            ),
            _entry(
                ProductCaseFormula.FLEET_ANNUAL_COST,
                text=(
                    "C(t) = years[].annual_cost_musd, the engineering artifact's annualized build "
                    "and launch cost of year t's living fleet (operations zero)"
                ),
                description=(
                    "The fleet's annual cost, read from the engineering artifact: the cost every "
                    "margin and the cost per GB carried are measured against."
                ),
                inputs=("inputs.engineering.annual_cost_musd",),
                outputs=(f"{_HEADLINE_TOTALS}.fleet_annual_cost_musd",),
                units="$M a year",
            ),
            _entry(
                ProductCaseFormula.TERMINAL_ACTIVE_RATE,
                text=(
                    "r_active = classes[].active_user_rate_mbps, the engineering usage's rate "
                    "while active for the terminal's device class"
                ),
                description="A terminal's rate while active, read from the engineering artifact.",
                inputs=(
                    "inputs.engineering.small_terminal.active_user_rate_mbps",
                    "inputs.engineering.mounted_terminal.active_user_rate_mbps",
                ),
                outputs=(f"{_HEADLINE_CLASS}.terminal.active_rate_mbps",),
                units="Mbps",
            ),
            _entry(
                ProductCaseFormula.TERMINAL_BUSY_HOUR_DATA,
                text=(
                    "busy GB a month = r_active x 10^6 x c_busy x 4 h x 3,600 s x 30 days / 8 / "
                    "10^9, with c_busy the engineering usage's busy-hour share "
                    "(classes[].concurrency_peak)"
                ),
                description=(
                    "A terminal's busy-hour data a month: the engineering usage over the 4 busy "
                    "hours, so its busy-hour load and its seats are the engineering case's."
                ),
                inputs=(
                    "inputs.engineering.small_terminal.active_user_rate_mbps",
                    "inputs.engineering.small_terminal.concurrency_peak",
                    "inputs.engineering.mounted_terminal.active_user_rate_mbps",
                    "inputs.engineering.mounted_terminal.concurrency_peak",
                    "inputs.constants.busy_hours_per_day",
                    "inputs.constants.days_per_month",
                    "inputs.constants.bytes_per_gb",
                ),
                outputs=(f"{_HEADLINE_CLASS}.terminal.busy_hour_gb_per_month",),
                units="GB a month (decimal)",
            ),
            _entry(
                ProductCaseFormula.TERMINAL_OFFPEAK_DATA,
                text=(
                    "off-peak GB a month(t) = the scenario's data a month in all(t) - the busy "
                    "GB a month; a monthly total below the busy-hour part is refused"
                ),
                description="A terminal's off-peak data a month: the rest of its monthly data.",
                inputs=(
                    "inputs.scenario.usage.small_terminal.gb_per_month",
                    "inputs.scenario.usage.mounted_terminal.gb_per_month",
                ),
                outputs=(f"{_HEADLINE_CLASS}.terminal.offpeak_gb_per_month",),
                units="GB a month (decimal)",
            ),
            _entry(
                ProductCaseFormula.PRICE_LINE,
                text=(
                    "p(t) = p_start + (p_end - p_start) x (t - t0) / (t1 - t0), with t a reported "
                    "fiscal year, t0 the first and t1 the last; data IoT's p(t) = 2 x "
                    "minimal-packet IoT's p(t)"
                ),
                description=(
                    "A class's price a month in a reported year, on the straight line from its "
                    "start price (the investor's) in the first reported year to the choice's end "
                    "price in the last; a candidate's end prices equal its start prices, so its "
                    "prices are flat."
                ),
                inputs=(
                    "inputs.scenario.prices.small_terminal.start_usd_month",
                    "inputs.scenario.prices.mounted_terminal.start_usd_month",
                    "inputs.scenario.prices.minimal_packet_iot.start_usd_month",
                    "choices[].end_prices",
                    "inputs.constants.data_iot_price_multiple",
                ),
                outputs=(f"{_HEADLINE_CLASS}.price_usd_per_month",),
                units="dollars a month",
            ),
            _entry(
                ProductCaseFormula.USAGE_LINE,
                text=(
                    "f(t) = 1 + (scale - 1) x (t - t0) / (t1 - t0); minimal-packet IoT's messages "
                    "a day m(t) = round_half_up(m_path(t) x f(t)) and data IoT's bursts a day "
                    "b(t) = round_half_up(b_path(t) x f(t)), with round_half_up(x) = floor(x + "
                    "0.5) and the product taken exactly, the scale at its decimal value, so an "
                    "exact half rounds up (50 at x1.15 in the last year: 57.5, so 58); data IoT's "
                    "messages a day are its one scenario value in every year (x8 in FY2033 of "
                    "2031 to 2036: 72 x 3.8 = 273.6, so 274)"
                ),
                description=(
                    "Each IoT class's usage in a reported year: its scenario path times the "
                    "choice's usage scale's line factor, 1 in the first reported year and the "
                    "scale in the last, in whole messages and bursts, rounded half up."
                ),
                inputs=(
                    "inputs.scenario.usage.minimal_packet_iot.messages_per_day",
                    "inputs.scenario.usage.data_iot.messages_per_day",
                    "inputs.scenario.usage.data_iot.bursts_per_day",
                    "choices[].minimal_packet_scale",
                    "choices[].data_iot_scale",
                ),
                outputs=(
                    f"{_HEADLINE_CLASS}.iot.messages_per_day",
                    f"{_HEADLINE_CLASS}.iot.bursts_per_day",
                ),
                units="messages a day; bursts a day (whole)",
            ),
            _entry(
                ProductCaseFormula.IOT_BYTES_PER_DAY,
                text=(
                    "B(t) = m(t) x 340 + b(t) x 100,000 bytes a day, the message and burst sizes "
                    "the engineering artifact publishes (iridium_physics.iot_message_bytes, "
                    "iridium_physics.iot_burst_bytes)"
                ),
                description="What an IoT device sends a day, its messages and its bursts.",
                inputs=(
                    "inputs.engineering.iot_message_bytes",
                    "inputs.engineering.iot_burst_bytes",
                ),
                outputs=(f"{_HEADLINE_CLASS}.iot.bytes_per_day",),
                units="bytes a day",
            ),
            _entry(
                ProductCaseFormula.SERVICE,
                text=(
                    "v_c(t) = data a month in all(t) / data a month in all(t0) for a terminal; "
                    "B(t) / B(t0) for an IoT class, at the same choice"
                ),
                description=(
                    "What a customer gets in a reported year over what it got in the first, the "
                    "service term of the demand curve."
                ),
                inputs=(
                    "inputs.scenario.usage",
                    f"{_HEADLINE_CLASS}.iot.bytes_per_day",
                ),
                outputs=(f"{_HEADLINE_CLASS}.service",),
                units="a ratio to the first reported year (unitless)",
            ),
            _entry(
                ProductCaseFormula.PER_DEVICE_LOADS,
                text=(
                    "a terminal: r_busy = busy GB x 10^9 x 8 / (4 x 3,600 x 30) and r_off(t) = "
                    "off-peak GB(t) x 10^9 x 8 / (20 x 3,600 x 30) bits a second; an IoT device: "
                    "uplink bits a second m x 340 x 8 / 86,400 plus its bursts' b x 100,000 x 8 / "
                    "86,400 in both periods, or, when its bursts go outside the busy hours, 0 in "
                    "the busy hours and b x 100,000 x 8 / 72,000 off-peak; random-access attempts "
                    "a second the same way, one per message or burst; single-tone messages a "
                    "second m / 86,400"
                ),
                description=(
                    "What one customer or device loads the network with in each period: a "
                    "terminal's downlink rates, an IoT device's uplink bits, access attempts and "
                    "tone messages a second."
                ),
                inputs=(
                    f"{_HEADLINE_CLASS}.terminal.busy_hour_gb_per_month",
                    f"{_HEADLINE_CLASS}.terminal.offpeak_gb_per_month",
                    f"{_HEADLINE_CLASS}.iot.messages_per_day",
                    f"{_HEADLINE_CLASS}.iot.bursts_per_day",
                    f"{_HEADLINE_CLASS}.iot.bursts_outside_busy_hours",
                ),
                outputs=(
                    "none published: terminal_downlink_use, iot_uplink_use, access_use and "
                    "single_tone_use read them",
                ),
                units="bits a second; attempts a second; messages a second",
            ),
            _entry(
                ProductCaseFormula.TERMINAL_DOWNLINK_USE,
                text=(
                    "busy-hour downlink use = customers x r_busy / (S x r_busy), the seats filled; "
                    "off-peak downlink use = customers x r_off(t) / (S x r_busy), the load against "
                    "the busy-hour budget of the same seats"
                ),
                description=(
                    "How much of a terminal's own busy-hour downlink budget its customers use, in "
                    "the busy hours and off-peak."
                ),
                inputs=(f"{_HEADLINE_CLASS}.customers", f"{_HEADLINE_CLASS}.terminal.seats"),
                outputs=(
                    f"{_HEADLINE_CLASS}.terminal.seats_filled",
                    f"{_HEADLINE_CLASS}.terminal.offpeak_downlink_use",
                ),
                units="a share of the budget (unitless; above 1 is past it)",
            ),
            _entry(
                ProductCaseFormula.PRICE_PER_UNIT,
                text=(
                    "a terminal: p(t) / its data a month in all (dollars a GB); minimal-packet "
                    "IoT: p(t) / (m(t) x 30) (dollars a message); data IoT: p(t) / (B(t) x 30 / "
                    "10^6) (dollars a MB)"
                ),
                description="What a customer pays for each unit of what it gets.",
                inputs=(
                    f"{_HEADLINE_CLASS}.price_usd_per_month",
                    "inputs.scenario.usage",
                    f"{_HEADLINE_CLASS}.iot.bytes_per_day",
                ),
                outputs=(f"{_HEADLINE_CLASS}.price_per_unit",),
                units="dollars a GB, a message or a MB (the cell's unit)",
            ),
            _entry(
                ProductCaseFormula.DEMAND_CURVE,
                text=(
                    "D_c(t) = N_c x k(t)^gamma x (A_c / p_c(t))^epsilon x v_c(t)^eta, with (N_c, "
                    "A_c) the class's anchor (today's customers and ARPU, COMM-617 and COMM-618; "
                    "data IoT 999,000 at $15.56 by the investor's proportion, COMM-726) and "
                    "(gamma, epsilon, eta) the market"
                ),
                description=(
                    "A class's demand in one market: today's customers, grown with the network's "
                    "scale, the price against today's and the service."
                ),
                inputs=(
                    "inputs.constants.anchors",
                    "network.years[].network_scale",
                    f"{_HEADLINE_CLASS}.price_usd_per_month",
                    f"{_HEADLINE_CLASS}.service",
                    "headline.market",
                ),
                outputs=(f"{_HEADLINE_CLASS}.demand",),
                units="customers (people or devices), unrounded",
            ),
            _entry(
                ProductCaseFormula.SOLD,
                text=(
                    "a terminal sells floor(min(D, S)); an IoT class sells floor(D), uncapped, its "
                    "sales checked against IoT's room, access and tone time by the usable test"
                ),
                description=(
                    "A class's customers in one market: whole people, never past a terminal's "
                    "seats; whole devices for an IoT class, always from the demand curve."
                ),
                inputs=(f"{_HEADLINE_CLASS}.demand", f"{_HEADLINE_CLASS}.terminal.seats"),
                outputs=(f"{_HEADLINE_CLASS}.customers",),
                units="customers (people or devices), whole",
            ),
            _entry(
                ProductCaseFormula.CLASS_REVENUE,
                text="revenue_c(t) = customers x p_c(t) x 12 / 10^6",
                description="A class's revenue in a year.",
                inputs=(f"{_HEADLINE_CLASS}.customers", f"{_HEADLINE_CLASS}.price_usd_per_month"),
                outputs=(f"{_HEADLINE_CLASS}.revenue_musd",),
                units="$M a year",
            ),
            _entry(
                ProductCaseFormula.BUSY_HOUR_BEAMS_FILLED,
                text=("F(t) = s x sold_small / S_small + (1 - s) x sold_mounted / S_mounted"),
                description=(
                    "The share of the terminals' busy-hour beams their customers fill, each "
                    "terminal weighted by its share of the beams."
                ),
                inputs=(
                    "network.small_terminal_share",
                    f"{_HEADLINE_CLASS}.customers",
                    f"{_HEADLINE_CLASS}.terminal.seats",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.busy_hour_beams_filled",),
                units="a share of the busy-hour beams (unitless, 0 to 1)",
            ),
            _entry(
                ProductCaseFormula.REVENUE,
                text="Rev(t) = the sum over the four classes of customers x p_c(t) x 12 / 10^6",
                description="The year's revenue, the four classes summed.",
                inputs=(f"{_HEADLINE_CLASS}.revenue_musd",),
                outputs=(f"{_HEADLINE_TOTALS}.revenue_musd", "choices[].central_revenue_musd"),
                units="$M a year",
            ),
            _entry(
                ProductCaseFormula.MARGIN,
                text="margin(t) = (1 - C(t) / Rev(t)) x 100",
                description=(
                    "The year's full-cost margin: revenue less the fleet's annualized build and "
                    "launch cost, over revenue (never called gross)."
                ),
                inputs=(
                    f"{_HEADLINE_TOTALS}.revenue_musd",
                    f"{_HEADLINE_TOTALS}.fleet_annual_cost_musd",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.margin_pct",),
                units="percent",
            ),
            _entry(
                ProductCaseFormula.PROFIT,
                text="profit(t) = Rev(t) - C(t)",
                description="The year's profit against the fleet's full annualized cost.",
                inputs=(
                    f"{_HEADLINE_TOTALS}.revenue_musd",
                    f"{_HEADLINE_TOTALS}.fleet_annual_cost_musd",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.profit_musd",),
                units="$M a year",
            ),
            _entry(
                ProductCaseFormula.IOT_UPLINK_USE,
                text=(
                    "U_period(t) = the sum over the two IoT classes of customers x that period's "
                    "uplink bits a second / R(t), for the busy hours and off-peak; each class's "
                    "own use is its term of the sum"
                ),
                description=(
                    "How much of IoT's payload room its devices use, in the busy hours and "
                    "off-peak (IoT's room is the whole uplink, the terminals' upload not "
                    "subtracted)."
                ),
                inputs=(
                    f"{_HEADLINE_CLASS}.customers",
                    "inputs.engineering.iot_payload_bits_per_second",
                ),
                outputs=(
                    f"{_HEADLINE_TOTALS}.iot_uplink_use_busy",
                    f"{_HEADLINE_TOTALS}.iot_uplink_use_offpeak",
                    f"{_HEADLINE_CLASS}.iot.uplink_use_busy",
                    f"{_HEADLINE_CLASS}.iot.uplink_use_offpeak",
                ),
                units="a share of the room (unitless; above 1 is past it)",
            ),
            _entry(
                ProductCaseFormula.ACCESS_USE,
                text=(
                    "access use(t) = the larger period's sum over the two IoT classes of "
                    "customers x attempts a second, over A(t)"
                ),
                description=(
                    "How much of IoT's random-access room its devices use, in the busier period."
                ),
                inputs=(
                    f"{_HEADLINE_CLASS}.customers",
                    "inputs.engineering.iot_access_attempts_per_second",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.access_use",),
                units="a share of the room (unitless; above 1 is past it)",
            ),
            _entry(
                ProductCaseFormula.ACCESS_ATTEMPTS_PER_BEAM,
                text=(
                    "the larger period's sum over the two IoT classes of customers x attempts a "
                    "second, over L(t)"
                ),
                description=(
                    "IoT's random-access attempts a second a beam, beside the window's 57 a beam "
                    "(COMM-654) that A(t) holds."
                ),
                inputs=(
                    f"{_HEADLINE_CLASS}.customers",
                    "inputs.engineering.phone_useful_beams",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.access_attempts_per_second_per_beam",),
                units="attempts a second a beam",
            ),
            _entry(
                ProductCaseFormula.SINGLE_TONE_USE,
                text=(
                    "tone use(t) = the sum over the two IoT classes of customers x messages a "
                    "second x 7 s (the message airtime's high end, COMM-719), over T(t)"
                ),
                description="How much of IoT's single-tone time its devices' messages use.",
                inputs=(
                    f"{_HEADLINE_CLASS}.customers",
                    "inputs.engineering.iot_message_airtime_high_s",
                    "inputs.engineering.iot_single_tone_seconds_per_second",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.single_tone_use",),
                units="a share of the room (unitless; above 1 is past it)",
            ),
            _entry(
                ProductCaseFormula.GB_CARRIED,
                text=(
                    "G(t) = the sum over the four classes of the GB they carry in a year: a "
                    "terminal's customers x its data a month in all x 12, an IoT class's devices x "
                    "B(t) x 30 x 12 / 10^9"
                ),
                description=(
                    "The GB the fleet carries in a year for the four classes: bytes add across "
                    "classes, people and devices never do."
                ),
                inputs=(
                    f"{_HEADLINE_CLASS}.customers",
                    "inputs.scenario.usage",
                    f"{_HEADLINE_CLASS}.iot.bytes_per_day",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.gb_carried_per_year",),
                units="GB a year (decimal)",
            ),
            _entry(
                ProductCaseFormula.COST_PER_GB_CARRIED,
                text="cost per GB(t) = C(t) x 10^6 / G(t)",
                description="The fleet's annual cost over the GB it carries in the year.",
                inputs=(
                    f"{_HEADLINE_TOTALS}.fleet_annual_cost_musd",
                    f"{_HEADLINE_TOTALS}.gb_carried_per_year",
                ),
                outputs=(f"{_HEADLINE_TOTALS}.cost_per_gb_carried_usd",),
                units="dollars a GB",
            ),
            _entry(
                ProductCaseFormula.USABLE,
                text=(
                    "a choice in one market is usable when, in every reported year, F(t) >= the "
                    "fill floor, margin(t) >= the margin floor, U_busy(t) <= 1, U_offpeak(t) <= 1, "
                    "access use(t) <= 1 and tone use(t) <= 1, and Rev(t) rises strictly from each "
                    "reported year to the next; a market records each test it fails"
                ),
                description=(
                    "Whether a choice works in a market: the network mostly used, the margin "
                    "healthy, IoT within its room, revenue rising."
                ),
                inputs=(
                    "inputs.scenario.floors.fill",
                    "inputs.scenario.floors.margin_pct",
                    _HEADLINE_TOTALS,
                ),
                outputs=("headline.usable", "headline.failing_tests", "choices[].central_usable"),
                units="a flag, and the tests failed",
            ),
            _entry(
                ProductCaseFormula.CHOICE_GRID,
                text=(
                    "the choices in one fixed order: the small terminal's end prices, then the "
                    "mounted terminal's, then minimal-packet IoT's, then minimal-packet IoT's "
                    "usage scales, then data IoT's (the last varying fastest); choice_id is the "
                    "index; data IoT's end price is twice minimal-packet IoT's; a choice is a "
                    "candidate (at_start_prices) when every end price equals its start price"
                ),
                description=(
                    "What the product case may sell, before any market: each end price and usage "
                    "scale combined, the candidates holding the investor's prices flat."
                ),
                inputs=(
                    "inputs.scenario.prices.small_terminal.end_usd_month",
                    "inputs.scenario.prices.mounted_terminal.end_usd_month",
                    "inputs.scenario.prices.minimal_packet_iot.end_usd_month",
                    "inputs.scenario.usage.minimal_packet_iot.scales",
                    "inputs.scenario.usage.data_iot.scales",
                ),
                outputs=(
                    "choices[].choice_id",
                    "choices[].end_prices.small_terminal",
                    "choices[].end_prices.mounted_terminal",
                    "choices[].end_prices.minimal_packet_iot",
                    "choices[].end_prices.data_iot",
                    "choices[].minimal_packet_scale",
                    "choices[].data_iot_scale",
                    "choices[].at_start_prices",
                ),
                units="an index; dollars a month; usage multiples",
            ),
            _entry(
                ProductCaseFormula.USABLE_DRAWS,
                text=(
                    "usable draws = the number of drawn markets in which the choice is usable (the "
                    "usable test applied in each drawn market); usable share = usable draws / "
                    "draws"
                ),
                description=(
                    "How many of the drawn markets a choice works in. The draws' own usable flags "
                    "are not published, only these counts and the central market's flag."
                ),
                inputs=("inputs.scenario.market", "inputs.scenario.floors"),
                outputs=("choices[].usable_draws", "choices[].usable_share"),
                units="draws; a share of the draws",
            ),
            _entry(
                ProductCaseFormula.DRAWS_FAILING,
                text=(
                    "for each usable test, the number of drawn markets that fail it (a market may "
                    "fail several)"
                ),
                description="Which tests a choice fails, and in how many markets.",
                inputs=("inputs.scenario.market", "inputs.scenario.floors"),
                outputs=("choices[].draws_failing",),
                units="draws",
            ),
            _entry(
                ProductCaseFormula.MEDIAN_SUMMED_REVENUE,
                text=(
                    "statistics.median of Rev(t) summed over the reported years, over the choice's "
                    "usable draws; null when none is usable"
                ),
                description="A choice's typical revenue over the reported years where it works.",
                inputs=(f"{_HEADLINE_TOTALS}.revenue_musd",),
                outputs=("choices[].median_summed_revenue_musd",),
                units="$M over the reported years",
            ),
            _entry(
                ProductCaseFormula.MEDIAN_LAST_YEAR_REVENUE,
                text=(
                    "statistics.median of Rev(t1), the last reported year's revenue, over the "
                    "choice's usable draws; null when none is usable"
                ),
                description="A choice's typical last-year revenue where it works.",
                inputs=(f"{_HEADLINE_TOTALS}.revenue_musd",),
                outputs=("choices[].median_last_year_revenue_musd",),
                units="$M a year",
            ),
            _entry(
                ProductCaseFormula.CENTRAL_SUMMED_REVENUE,
                text="the sum over the reported years of Rev(t) at the central market",
                description=(
                    "A choice's revenue over the reported years in the one market every choice is "
                    "read in."
                ),
                inputs=("choices[].central_revenue_musd",),
                outputs=("choices[].central_summed_revenue_musd",),
                units="$M over the reported years",
            ),
            _entry(
                ProductCaseFormula.FRONT,
                text=(
                    "sort the choices with at least one usable draw by usable share, then median "
                    "summed revenue, both descending, then the grid's order; a choice joins the "
                    "front when its median is strictly above every earlier member's; members are "
                    "listed most usable first"
                ),
                description=(
                    "The choices no other choice beats on both usable share and median revenue "
                    "(of exact ties the earliest in the grid's order stands for them): over every "
                    "choice (all_prices, the context: what lower prices would do) and over the "
                    "candidates (at_start_prices, on which the pick lies)."
                ),
                inputs=(
                    "choices[].usable_share",
                    "choices[].median_summed_revenue_musd",
                    "choices[].choice_id",
                ),
                outputs=("fronts.all_prices", "fronts.at_start_prices"),
                units="choice ids",
            ),
            _entry(
                ProductCaseFormula.PICK,
                text=(
                    "among the candidates usable in at least the robust floor's share of the "
                    "draws, the highest median summed revenue, ties to the higher usable share, "
                    "then the earlier choice (robust_floor_met); when none reaches the floor, the "
                    "first member of the candidates' front, warned (most_usable_fallback); when no "
                    "candidate is usable in any draw, no pick (no_usable_choice); usage_edges are "
                    "the IoT classes whose usage scale is the top of the grid"
                ),
                description=(
                    "The adopted case: the investor's prices held flat, with the IoT usage the "
                    "market supports. What stops the usage: every candidate holds the same "
                    "terminal prices, so all fail the terminals' fill in the same weak markets; "
                    "more IoT usage fails IoT's room, access or tone time in more of the filled "
                    "markets and drops the strongest of them; so the usage rises only while its "
                    "usable share stays at or above the robust floor and its median still rises, "
                    "and the floor or the median's peak stops it, whichever comes first. A change "
                    "that moves the terminals' fill or an IoT price can move the usage, in steps."
                ),
                inputs=(
                    "choices[].usable_share",
                    "choices[].median_summed_revenue_musd",
                    "fronts.at_start_prices",
                    "inputs.scenario.floors.robust",
                ),
                outputs=("pick.choice_id", "pick.basis", "pick.usage_edges"),
                units="a choice id, its basis and the classes at a usage edge",
                notes=(
                    "The run never lowers a price: the pick is always a candidate, and lower "
                    "prices appear only in the front over every choice, as context."
                ),
            ),
            _entry(
                ProductCaseFormula.DOMINATED_IN_CONTEXT_BY,
                text=(
                    "the members of fronts.all_prices at least as usable as the pick with a median "
                    "summed revenue at least as high, one of the two higher; empty when the pick "
                    "is on that front"
                ),
                description=(
                    "The context choices, at lower prices, that beat the pick: any choice that "
                    "beats it is beaten or matched by one of these."
                ),
                inputs=("fronts.all_prices", "pick.choice_id"),
                outputs=("pick.dominated_in_context_by",),
                units="choice ids",
            ),
            _entry(
                ProductCaseFormula.CENTRAL_MARKET,
                text=(
                    "gamma = (gamma_low + gamma_high) / 2; epsilon = (epsilon_low + epsilon_high) "
                    "/ 2; eta = (eta_low + eta_high) / 2"
                ),
                description=(
                    "The central market, each response at the middle of its range: with the "
                    "responses drawn independently and uniformly, each class's customers there are "
                    "its median over the population of markets (in the drawn sample, within "
                    "sampling error)."
                ),
                inputs=(
                    "inputs.scenario.market.gamma",
                    "inputs.scenario.market.epsilon",
                    "inputs.scenario.market.eta",
                ),
                outputs=("headline.market.gamma", "headline.market.epsilon", "headline.market.eta"),
                units="the responses' exponents (unitless)",
            ),
            _entry(
                ProductCaseFormula.HEADLINE,
                text=(
                    "the pick evaluated at the central market through the same evaluation as the "
                    "draws (one market), each reported year's classes and totals by their own "
                    "formulas"
                ),
                description=(
                    "The headline: the adopted case in the typical market, a reading, not a gate "
                    "(an unusable central market is published and warned)."
                ),
                inputs=("pick.choice_id", "headline.market"),
                outputs=("headline.years[]",),
                units="per its cells",
            ),
            _entry(
                ProductCaseFormula.PERCENTILES,
                text=(
                    "per reported year and spread field, over the pick's usable draws (null below "
                    "9 usable draws, reason too_few_usable_draws) and over all draws: the 50th by "
                    "statistics.median, the 10th and 90th by statistics.quantiles(values, n=10) "
                    "(the exclusive method)"
                ),
                description="The spread of the pick's outcomes over the drawn markets.",
                inputs=("pick.choice_id", "inputs.scenario.market"),
                outputs=(
                    f"{_SPREAD_FIELD}.usable_draws.p10",
                    f"{_SPREAD_FIELD}.usable_draws.p50",
                    f"{_SPREAD_FIELD}.usable_draws.p90",
                    f"{_SPREAD_FIELD}.usable_draws.null_reason",
                    f"{_SPREAD_FIELD}.all_draws.p10",
                    f"{_SPREAD_FIELD}.all_draws.p50",
                    f"{_SPREAD_FIELD}.all_draws.p90",
                ),
                units="the spread field's own unit",
            ),
            _entry(
                ProductCaseFormula.MID_RANK,
                text=(
                    "rank = the share of the basis's draws strictly below the headline value plus "
                    "half the share equal to it"
                ),
                description="Where the headline sits among the drawn markets.",
                inputs=("headline.years[]", f"{_SPREAD_FIELD}.field"),
                outputs=(
                    f"{_SPREAD_FIELD}.usable_draws.headline_rank",
                    f"{_SPREAD_FIELD}.all_draws.headline_rank",
                ),
                units="a share of the draws (unitless, 0 to 1)",
            ),
            _entry(
                ProductCaseFormula.EVERY_SEAT_SHARES,
                text=(
                    "for a terminal's customers and revenue: whether the headline sells every seat "
                    "(customers = floor(S)), and the share of each basis's draws that do"
                ),
                description=(
                    "How often a terminal is sold out: where it is, its rank among ties at its "
                    "seats says little."
                ),
                inputs=(f"{_HEADLINE_CLASS}.customers", f"{_HEADLINE_CLASS}.terminal.seats"),
                outputs=(
                    f"{_SPREAD_FIELD}.every_seat.headline_sells_every_seat",
                    f"{_SPREAD_FIELD}.every_seat.usable_draws_share",
                    f"{_SPREAD_FIELD}.every_seat.all_draws_share",
                ),
                units="a flag; shares of the draws",
            ),
            _entry(
                ProductCaseFormula.DRAWS_PAST_IOT_ROOM,
                text=(
                    "the number of drawn markets, all of them, the usable test not applied, in "
                    "which the pick's IoT uplink use in the busy hours or off-peak, or its access "
                    "use, is above 1 in at least one reported year (a market counts once; the tone "
                    "test is not in the count)"
                ),
                description=(
                    "The all-draw basis's label: in how many markets the pick sells IoT past its "
                    "room or access, markets the usable draws leave out."
                ),
                inputs=("pick.choice_id", "inputs.scenario.market"),
                outputs=("spreads.all_draws_basis",),
                units="draws",
            ),
            _entry(
                ProductCaseFormula.SOURCE_STATUS_SUMMARY,
                text=(
                    "the number of the run's input cells in each source status, by "
                    "common.meta.summarize_source_statuses over every input cell"
                ),
                description=(
                    "How the run's inputs are sourced: a count of input cells per status, "
                    "certified, scenario and derived estimates among them."
                ),
                inputs=("inputs.scenario", "inputs.constants", "inputs.engineering"),
                outputs=("meta.source_status_summary",),
                units="input cells",
            ),
        )
    )
)
"""The product case's formula catalog: one :class:`~common.meta.FormulaDefinition` per formula of
the method (a read-only mapping, keyed by :class:`ProductCaseFormula`, in the method's order).
The artifact's ``meta.formulas`` is built from it alone; every provenance cell the artifact
publishes names one of its keys as its ``formula_name``; each entry's ``output_path_pattern``
names the paths it computes, plain fields among them, in the walker's form
(:data:`PATH_SEPARATOR` says it and separates them).
:data:`common.provenance.FORMULAS` stays the data center's catalog."""


__all__ = [
    "BITS_PER_BYTE",
    "BITS_PER_MEGABIT",
    "BROADBAND_ARPU_USD_MONTH",
    "BROADBAND_CUSTOMERS_TODAY",
    "BUSY_HOURS_PER_DAY",
    "BYTES_PER_GB",
    "CLASS_KIND",
    "DATA_IOT_ANCHOR_ARPU_USD_MONTH",
    "DATA_IOT_ANCHOR_CUSTOMERS",
    "DATA_IOT_ANCHOR_SHARE",
    "DATA_IOT_BURSTS_OUTSIDE_BUSY_HOURS_DEFAULT",
    "DATA_IOT_BURSTS_PER_DAY_DEFAULT",
    "DATA_IOT_MESSAGES_PER_DAY_DEFAULT",
    "DATA_IOT_PRICE_MULTIPLE",
    "DATA_IOT_SCALES_DEFAULT",
    "DAYS_PER_MONTH",
    "DEMAND_ANCHORS",
    "DOLLARS_PER_MILLION",
    "DRAWS_DEFAULT",
    "ENGINEERING_ARTIFACT_PATH_DEFAULT",
    "ENGINEERING_SCHEMA_VERSION",
    "EPSILON_HIGH_DEFAULT",
    "EPSILON_LOW_DEFAULT",
    "ETA_HIGH_DEFAULT",
    "ETA_LOW_DEFAULT",
    "FILL_FLOOR_DEFAULT",
    "FORMULA_CATALOG",
    "GAMMA_HIGH_DEFAULT",
    "GAMMA_LOW_DEFAULT",
    "HOURS_PER_DAY",
    "IOT_ARPU_USD_MONTH",
    "IOT_CUSTOMERS_TODAY",
    "MARGIN_FLOOR_PCT_DEFAULT",
    "MINIMAL_PACKET_IOT_END_PRICES_USD_MONTH_DEFAULT",
    "MINIMAL_PACKET_IOT_MESSAGES_PER_DAY_DEFAULT",
    "MINIMAL_PACKET_IOT_SCALES_DEFAULT",
    "MINIMAL_PACKET_IOT_START_PRICE_USD_MONTH_DEFAULT",
    "MIN_DRAWS",
    "MIN_REPORTED_YEARS",
    "MONTHS_PER_YEAR",
    "MOUNTED_TERMINAL_END_PRICES_USD_MONTH_DEFAULT",
    "MOUNTED_TERMINAL_GB_PER_MONTH_DEFAULT",
    "MOUNTED_TERMINAL_START_PRICE_USD_MONTH_DEFAULT",
    "OFFPEAK_HOURS_PER_DAY",
    "PATH_SEPARATOR",
    "PERCENT",
    "PHONE_DEVICE_CLASS",
    "PRODUCT_CASE_SCHEMA_VERSION",
    "RELATIVE_TOLERANCE",
    "REPORTED_YEARS_DEFAULT",
    "ROBUST_FLOOR_DEFAULT",
    "SCENARIO_NAME_DEFAULT",
    "SECONDS_PER_DAY",
    "SECONDS_PER_HOUR",
    "SEED_DEFAULT",
    "SMALL_TERMINAL_END_PRICES_USD_MONTH_DEFAULT",
    "SMALL_TERMINAL_GB_PER_MONTH_DEFAULT",
    "SMALL_TERMINAL_START_PRICE_USD_MONTH_DEFAULT",
    "TERMINAL_CUSTOMERS_TODAY",
    "TERMINAL_DEVICE_CLASS",
    "USAGE_SCALE_START",
    "VOICE_DATA_ARPU_USD_MONTH",
    "VOICE_DATA_CUSTOMERS_TODAY",
    "ClassKind",
    "DemandAnchor",
    "PickBasis",
    "ProductCaseFormula",
    "ProductClass",
    "RunState",
    "SpreadField",
    "SpreadNullReason",
    "UsableTest",
]
