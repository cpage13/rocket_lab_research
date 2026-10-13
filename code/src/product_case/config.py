"""The product case's scenario: its frozen config, its loader, and each input's cell spec (box B0).

``code/scenarios/product_case.yaml`` is read through the shared
:func:`common.file_io.load_yaml_mapping` into :class:`ProductCaseConfig`, frozen, every block
``extra="forbid"`` and ``allow_inf_nan=False``, every number strict: an unknown key (an IoT
count among them, since no IoT count is ever a setting), a YAML boolean or a quoted number where
a number goes, and a number that is not finite are refused at load, naming the field. Its blocks:
the scenario's name, the engineering artifact's path (repository-relative), the reported years,
each class's prices but data IoT's (whose price is twice minimal-packet IoT's, the investor's
proportion, never a setting), each class's usage path, the market (draws, seed and the three
responses' ranges) and the usable floors. The validators refuse, naming the field: an end-price
list that does not open with its start price or does not fall strictly; a usage-scale list that
does not open at 1 or does not rise; a usage path whose length is not the reported years'; fewer
than two reported years or years out of order; a range whose low end is below 0 or above its
high end; a negative seed; draws below 9; a fill or robust floor outside (0, 1]; a margin floor
outside (0, 100) percent.

Every default is a named constant of :mod:`product_case.constants`, and the shipped scenario
holds exactly the defaults, its own label aside (a test ties the two). Each scenario value has
one :class:`~common.input_manifest.CellSpec` in :data:`SCENARIO_SPECS`, and each named constant
that is a model input one in :data:`CONSTANT_INPUTS` with its value: the artifact's input cells
are built from them by :func:`common.input_manifest._spec_cell`'s rule, each scenario value
handed to it by :func:`scenario_inputs` beside its default in a cell's form, so a value that
differs from its default is a scenario override (status ``scenario``, the scenario YAML its only
source) and a side run's price never inherits the investor's words. Every spec's status is one
of the shared statuses: the investor's values and the design's settings are ``scenario`` (each
rationale opens INVESTOR_SET or SCENARIO with its date), Iridium's customers and ARPU today
``certified`` (COMM-617, COMM-618). A field's description says what the field is; its basis is
its spec's.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from types import MappingProxyType
from typing import Final

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    ValidationInfo,
    field_validator,
    model_validator,
)

from common.file_io import load_yaml_mapping
from common.input_manifest import (
    AssumptionRole,
    CellSpec,
    InputScalar,
    InputValue,
    SourceStatus,
    SupportingClaim,
    _field_description,
)
from product_case.constants import (
    BROADBAND_ARPU_USD_MONTH,
    BROADBAND_CUSTOMERS_TODAY,
    BUSY_HOURS_PER_DAY,
    BYTES_PER_GB,
    BYTES_PER_MB,
    DATA_IOT_ANCHOR_ARPU_USD_MONTH,
    DATA_IOT_ANCHOR_CUSTOMERS,
    DATA_IOT_ANCHOR_SHARE,
    DATA_IOT_BURSTS_OUTSIDE_BUSY_HOURS_DEFAULT,
    DATA_IOT_BURSTS_PER_DAY_DEFAULT,
    DATA_IOT_MESSAGES_PER_DAY_DEFAULT,
    DATA_IOT_PRICE_MULTIPLE,
    DATA_IOT_SCALES_DEFAULT,
    DAYS_PER_MONTH,
    DRAWS_DEFAULT,
    ENGINEERING_ARTIFACT_PATH_DEFAULT,
    EPSILON_HIGH_DEFAULT,
    EPSILON_LOW_DEFAULT,
    ETA_HIGH_DEFAULT,
    ETA_LOW_DEFAULT,
    FILL_FLOOR_DEFAULT,
    GAMMA_HIGH_DEFAULT,
    GAMMA_LOW_DEFAULT,
    IOT_ARPU_USD_MONTH,
    IOT_CUSTOMERS_TODAY,
    MARGIN_FLOOR_PCT_DEFAULT,
    MIN_DRAWS,
    MIN_REPORTED_YEARS,
    MINIMAL_PACKET_IOT_END_PRICES_USD_MONTH_DEFAULT,
    MINIMAL_PACKET_IOT_MESSAGES_PER_DAY_DEFAULT,
    MINIMAL_PACKET_IOT_SCALES_DEFAULT,
    MINIMAL_PACKET_IOT_START_PRICE_USD_MONTH_DEFAULT,
    MOUNTED_TERMINAL_END_PRICES_USD_MONTH_DEFAULT,
    MOUNTED_TERMINAL_GB_PER_MONTH_DEFAULT,
    MOUNTED_TERMINAL_START_PRICE_USD_MONTH_DEFAULT,
    PERCENT,
    REPORTED_YEARS_DEFAULT,
    ROBUST_FLOOR_DEFAULT,
    SCENARIO_NAME_DEFAULT,
    SEED_DEFAULT,
    SMALL_TERMINAL_END_PRICES_USD_MONTH_DEFAULT,
    SMALL_TERMINAL_GB_PER_MONTH_DEFAULT,
    SMALL_TERMINAL_START_PRICE_USD_MONTH_DEFAULT,
    TERMINAL_CUSTOMERS_TODAY,
    USAGE_SCALE_START,
    VOICE_DATA_ARPU_USD_MONTH,
    VOICE_DATA_CUSTOMERS_TODAY,
)

logger = logging.getLogger(__name__)

_FROZEN_STRICT: Final[ConfigDict] = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
"""Every config block's settings: an unknown key and a number that is not finite are refused."""


def _falls_strictly(values: tuple[float, ...]) -> bool:
    """True when each value is strictly below the one before it."""
    return all(later < earlier for earlier, later in pairwise(values))


def _rises_strictly(values: tuple[float, ...]) -> bool:
    """True when each value is strictly above the one before it."""
    return all(later > earlier for earlier, later in pairwise(values))


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------


class ClassPriceDials(BaseModel):
    """One class's prices: its start price and the end prices the choice grid may take.

    A choice's price runs on a straight line from the start price in the first reported year
    to its end price in the last; the list of end prices opens with the start price (the
    choice that holds the price flat) and each later entry falls strictly below the one before
    (lower prices, the context: the run never picks them).
    """

    model_config = _FROZEN_STRICT

    start_usd_month: float = Field(
        gt=0,
        strict=True,
        description="The class's price a month in the first reported year, dollars.",
    )
    end_usd_month: tuple[StrictFloat, ...] = Field(
        min_length=1,
        description=(
            "The prices a month a choice may reach by the last reported year, dollars: the start "
            "price first, then each lower one."
        ),
    )

    @field_validator("end_usd_month")
    @classmethod
    def _end_prices_open_at_the_start_and_fall(
        cls, value: tuple[float, ...], info: ValidationInfo
    ) -> tuple[float, ...]:
        """Refuse an end-price list that does not open with the start price or fall strictly."""
        if any(price <= 0 for price in value):
            raise ValueError(f"every end price must be above 0, got {list(value)}")
        start = info.data.get("start_usd_month")
        if start is not None and value[0] != start:
            raise ValueError(
                f"the end prices must open with the start price {start!r} (the choice that holds "
                f"it flat), got {list(value)}"
            )
        if not _falls_strictly(value):
            raise ValueError(
                "each end price after the first must fall strictly below the one before "
                f"(the prices never rise), got {list(value)}"
            )
        return value


def _small_terminal_prices() -> ClassPriceDials:
    """The small terminal's default prices."""
    return ClassPriceDials(
        start_usd_month=SMALL_TERMINAL_START_PRICE_USD_MONTH_DEFAULT,
        end_usd_month=SMALL_TERMINAL_END_PRICES_USD_MONTH_DEFAULT,
    )


def _mounted_terminal_prices() -> ClassPriceDials:
    """The mounted terminal's default prices."""
    return ClassPriceDials(
        start_usd_month=MOUNTED_TERMINAL_START_PRICE_USD_MONTH_DEFAULT,
        end_usd_month=MOUNTED_TERMINAL_END_PRICES_USD_MONTH_DEFAULT,
    )


def _minimal_packet_iot_prices() -> ClassPriceDials:
    """Minimal-packet IoT's default prices."""
    return ClassPriceDials(
        start_usd_month=MINIMAL_PACKET_IOT_START_PRICE_USD_MONTH_DEFAULT,
        end_usd_month=MINIMAL_PACKET_IOT_END_PRICES_USD_MONTH_DEFAULT,
    )


class PriceDials(BaseModel):
    """The prices of the three priced classes; data IoT pays twice minimal-packet IoT's price.

    Data IoT's price is not a setting: it is :data:`~product_case.constants.DATA_IOT_PRICE_MULTIPLE`
    times minimal-packet IoT's in every year and choice (the investor's proportion), so a
    scenario that sets one fails at load, naming it.
    """

    model_config = _FROZEN_STRICT

    small_terminal: ClassPriceDials = Field(
        default_factory=_small_terminal_prices,
        description="The small terminal's start and end prices.",
    )
    mounted_terminal: ClassPriceDials = Field(
        default_factory=_mounted_terminal_prices,
        description="The mounted terminal's start and end prices.",
    )
    minimal_packet_iot: ClassPriceDials = Field(
        default_factory=_minimal_packet_iot_prices,
        description="Minimal-packet IoT's start and end prices; data IoT pays twice them.",
    )


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------


def _check_scales(value: tuple[float, ...]) -> tuple[float, ...]:
    """Refuse a usage-scale list that does not open at 1 or does not rise strictly."""
    if value[0] != USAGE_SCALE_START:
        raise ValueError(
            f"the usage scales must open at {USAGE_SCALE_START:g} (the path itself), got "
            f"{list(value)}"
        )
    if not _rises_strictly(value):
        raise ValueError(f"the usage scales must rise strictly, got {list(value)}")
    return value


class TerminalUsageDials(BaseModel):
    """A terminal's data a month, in all, in each reported year.

    Its busy-hour part is the engineering usage's (so its seats are the engineering case's);
    the rest is off-peak data. A total below the busy-hour part is refused when the offers are
    built, which know the engineering artifact.
    """

    model_config = _FROZEN_STRICT

    gb_per_month: tuple[StrictFloat, ...] = Field(
        min_length=1,
        description=(
            "The terminal's data a month in all, GB (decimal), one value per reported year, in "
            "order."
        ),
    )

    @field_validator("gb_per_month")
    @classmethod
    def _positive(cls, value: tuple[float, ...]) -> tuple[float, ...]:
        """Refuse a monthly total that is not above 0."""
        if any(gb <= 0 for gb in value):
            raise ValueError(f"every monthly total must be above 0 GB, got {list(value)}")
        return value


def _small_terminal_usage() -> TerminalUsageDials:
    """The small terminal's default usage path."""
    return TerminalUsageDials(gb_per_month=SMALL_TERMINAL_GB_PER_MONTH_DEFAULT)


def _mounted_terminal_usage() -> TerminalUsageDials:
    """The mounted terminal's default usage path."""
    return TerminalUsageDials(gb_per_month=MOUNTED_TERMINAL_GB_PER_MONTH_DEFAULT)


class MinimalPacketIotUsageDials(BaseModel):
    """Minimal-packet IoT's usage: its messages a day per reported year and the usage scales.

    A usage a device sends, never a count of devices: minimal-packet IoT's customers come from
    the demand curve in every market and year.
    """

    model_config = _FROZEN_STRICT

    messages_per_day: tuple[StrictInt, ...] = Field(
        min_length=1,
        description=(
            "The messages a device sends a day, one value per reported year, in order, before "
            "a choice's usage scale."
        ),
    )
    scales: tuple[StrictFloat, ...] = Field(
        min_length=1,
        description=(
            "The usage scales a choice may take by the last reported year: the path's multiple "
            "then, rising on a straight line from 1 in the first reported year."
        ),
    )

    @field_validator("messages_per_day")
    @classmethod
    def _at_least_one_message(cls, value: tuple[int, ...]) -> tuple[int, ...]:
        """Refuse a year with no message (the service would divide by nothing)."""
        if any(messages < 1 for messages in value):
            raise ValueError(f"every year needs at least 1 message a day, got {list(value)}")
        return value

    @field_validator("scales")
    @classmethod
    def _scales_open_at_one_and_rise(cls, value: tuple[float, ...]) -> tuple[float, ...]:
        """Refuse scales that do not open at 1 or do not rise strictly."""
        return _check_scales(value)


def _minimal_packet_iot_usage() -> MinimalPacketIotUsageDials:
    """Minimal-packet IoT's default usage."""
    return MinimalPacketIotUsageDials(
        messages_per_day=MINIMAL_PACKET_IOT_MESSAGES_PER_DAY_DEFAULT,
        scales=MINIMAL_PACKET_IOT_SCALES_DEFAULT,
    )


class DataIotUsageDials(BaseModel):
    """Data IoT's usage: its messages a day, its bursts a day per reported year, their timing.

    The usage scale moves the bursts, never the messages. A usage a device sends, never a count
    of devices: data IoT's customers come from the demand curve in every market and year.
    """

    model_config = _FROZEN_STRICT

    messages_per_day: int = Field(
        ge=1,
        strict=True,
        description="The messages a device sends a day, in every reported year.",
    )
    bursts_per_day: tuple[StrictInt, ...] = Field(
        min_length=1,
        description=(
            "The 100 KB bursts a device sends a day, one value per reported year, in order, "
            "before a choice's usage scale."
        ),
    )
    bursts_outside_busy_hours: tuple[StrictBool, ...] = Field(
        min_length=1,
        description=(
            "Whether a year's bursts go outside the busy hours (spread over the off-peak hours) "
            "or at any hour, one flag per reported year, in order."
        ),
    )
    scales: tuple[StrictFloat, ...] = Field(
        min_length=1,
        description=(
            "The usage scales a choice may take by the last reported year: the bursts' multiple "
            "then, rising on a straight line from 1 in the first reported year."
        ),
    )

    @field_validator("bursts_per_day")
    @classmethod
    def _no_negative_bursts(cls, value: tuple[int, ...]) -> tuple[int, ...]:
        """Refuse a negative number of bursts."""
        if any(bursts < 0 for bursts in value):
            raise ValueError(f"bursts a day cannot be negative, got {list(value)}")
        return value

    @field_validator("scales")
    @classmethod
    def _scales_open_at_one_and_rise(cls, value: tuple[float, ...]) -> tuple[float, ...]:
        """Refuse scales that do not open at 1 or do not rise strictly."""
        return _check_scales(value)


def _data_iot_usage() -> DataIotUsageDials:
    """Data IoT's default usage."""
    return DataIotUsageDials(
        messages_per_day=DATA_IOT_MESSAGES_PER_DAY_DEFAULT,
        bursts_per_day=DATA_IOT_BURSTS_PER_DAY_DEFAULT,
        bursts_outside_busy_hours=DATA_IOT_BURSTS_OUTSIDE_BUSY_HOURS_DEFAULT,
        scales=DATA_IOT_SCALES_DEFAULT,
    )


class UsageDials(BaseModel):
    """Each class's usage path, one value per reported year (the four classes, in order)."""

    model_config = _FROZEN_STRICT

    small_terminal: TerminalUsageDials = Field(
        default_factory=_small_terminal_usage,
        description="The small terminal's data a month in all.",
    )
    mounted_terminal: TerminalUsageDials = Field(
        default_factory=_mounted_terminal_usage,
        description="The mounted terminal's data a month in all.",
    )
    minimal_packet_iot: MinimalPacketIotUsageDials = Field(
        default_factory=_minimal_packet_iot_usage,
        description="Minimal-packet IoT's messages a day and usage scales.",
    )
    data_iot: DataIotUsageDials = Field(
        default_factory=_data_iot_usage,
        description="Data IoT's messages and bursts a day, the bursts' timing and usage scales.",
    )


# ---------------------------------------------------------------------------
# The market and the floors
# ---------------------------------------------------------------------------


class ResponseRange(BaseModel):
    """The range one market response is drawn from, uniformly: its low end and its high end.

    The low end is at least 0, so in no drawn market does a bigger network, a lower price or
    more service bring fewer customers; the high end is at least the low end.
    """

    model_config = _FROZEN_STRICT

    low: float = Field(
        ge=0,
        strict=True,
        description=(
            "The response's low end, an exponent of at least 0 (a bigger network, a lower price "
            "or more service never brings fewer customers)."
        ),
    )
    high: float = Field(strict=True, description="The response's high end (an exponent).")

    @model_validator(mode="after")
    def _low_not_above_high(self) -> ResponseRange:
        """Refuse a range whose low end is above its high end."""
        if self.low > self.high:
            raise ValueError(f"the low end {self.low!r} is above the high end {self.high!r}")
        return self


class MarketDials(BaseModel):
    """The drawn markets: how many, the generator's seed, and each response's range.

    Each draw takes the network response gamma, the price response epsilon, then the service
    response eta, each uniform over its range, from one standard-library generator seeded with
    ``seed``; the central market sits at each range's middle.
    """

    model_config = _FROZEN_STRICT

    draws: int = Field(
        default=DRAWS_DEFAULT,
        ge=MIN_DRAWS,
        strict=True,
        description="The number of market draws.",
    )
    seed: int = Field(
        default=SEED_DEFAULT,
        ge=0,
        strict=True,
        description=(
            "The seed of the standard generator that draws the markets, at least 0 (the generator "
            "seeds from a whole number's size, so a negative seed would draw its positive's "
            "markets under another name)."
        ),
    )
    gamma: ResponseRange = Field(
        default_factory=lambda: ResponseRange(low=GAMMA_LOW_DEFAULT, high=GAMMA_HIGH_DEFAULT),
        description="The network response's range: customers grow as the network's scale to it.",
    )
    epsilon: ResponseRange = Field(
        default_factory=lambda: ResponseRange(low=EPSILON_LOW_DEFAULT, high=EPSILON_HIGH_DEFAULT),
        description="The price response's range: customers grow as today's price over ours to it.",
    )
    eta: ResponseRange = Field(
        default_factory=lambda: ResponseRange(low=ETA_LOW_DEFAULT, high=ETA_HIGH_DEFAULT),
        description="The service response's range: customers grow as the service to it.",
    )


class FloorDials(BaseModel):
    """The usable test's floors: the beams filled, the draws usable and the margin."""

    model_config = _FROZEN_STRICT

    fill: float = Field(
        default=FILL_FLOOR_DEFAULT,
        gt=0,
        le=1.0,
        strict=True,
        description=(
            "The least share of the terminals' busy-hour beams a usable choice fills in every "
            "reported year."
        ),
    )
    robust: float = Field(
        default=ROBUST_FLOOR_DEFAULT,
        gt=0,
        le=1.0,
        strict=True,
        description="The least share of the drawn markets in which the pick must be usable.",
    )
    margin_pct: float = Field(
        default=MARGIN_FLOOR_PCT_DEFAULT,
        gt=0,
        lt=PERCENT,
        strict=True,
        description=(
            "The least margin, percent, of the whole business a usable choice keeps in every "
            "reported year."
        ),
    )


# ---------------------------------------------------------------------------
# The config
# ---------------------------------------------------------------------------


class ProductCaseConfig(BaseModel):
    """The product case's scenario, frozen: the config every product-case run reads.

    Every field defaults to its named constant, so ``ProductCaseConfig()`` is the shipped
    scenario but its label, which is neutral (the shipped file names itself). A usage path holds
    one value per reported year; the years are at least two, in order. No IoT count is a
    setting: a scenario that sets one fails at load, naming the key.
    """

    model_config = _FROZEN_STRICT

    scenario_name: str = Field(
        default=SCENARIO_NAME_DEFAULT,
        min_length=1,
        description="The scenario's label: the run's identity, not an input.",
    )
    engineering_artifact_path: str = Field(
        default=ENGINEERING_ARTIFACT_PATH_DEFAULT,
        min_length=1,
        description=(
            "The engineering artifact the product case reads, repository-relative (an absolute "
            "path is allowed, so a test or a side run can point at another file)."
        ),
    )
    reported_years: tuple[StrictInt, ...] = Field(
        default=REPORTED_YEARS_DEFAULT,
        description="The reported fiscal years, in order: the method's years.",
    )
    prices: PriceDials = Field(default_factory=PriceDials, description="Each class's prices.")
    usage: UsageDials = Field(default_factory=UsageDials, description="Each class's usage path.")
    market: MarketDials = Field(
        default_factory=MarketDials, description="The drawn markets and their ranges."
    )
    floors: FloorDials = Field(default_factory=FloorDials, description="The usable test's floors.")

    @field_validator("reported_years")
    @classmethod
    def _two_or_more_years_in_order(cls, value: tuple[int, ...]) -> tuple[int, ...]:
        """Refuse fewer than two reported years, or years out of order."""
        if len(value) < MIN_REPORTED_YEARS:
            raise ValueError(
                f"at least {MIN_REPORTED_YEARS} reported years are needed (the lines run from "
                f"the first to the last), got {list(value)}"
            )
        if not _rises_strictly(value):  # compared as the integers they are, never as floats
            raise ValueError(f"the reported years must be in order, each once, got {list(value)}")
        return value

    @model_validator(mode="after")
    def _each_path_one_value_a_year(self) -> ProductCaseConfig:
        """Refuse a usage path whose length is not the reported years', naming the field."""
        paths: dict[str, int] = {
            "usage.small_terminal.gb_per_month": len(self.usage.small_terminal.gb_per_month),
            "usage.mounted_terminal.gb_per_month": len(self.usage.mounted_terminal.gb_per_month),
            "usage.minimal_packet_iot.messages_per_day": len(
                self.usage.minimal_packet_iot.messages_per_day
            ),
            "usage.data_iot.bursts_per_day": len(self.usage.data_iot.bursts_per_day),
            "usage.data_iot.bursts_outside_busy_hours": len(
                self.usage.data_iot.bursts_outside_busy_hours
            ),
        }
        years = len(self.reported_years)
        for field, length in paths.items():
            if length != years:
                raise ValueError(
                    f"{field} holds {length} values; it needs one per reported year ({years}: "
                    f"{', '.join(f'FY{year}' for year in self.reported_years)})"
                )
        return self


def load_product_case_config(path: str | Path) -> ProductCaseConfig:
    """Load and validate a :class:`ProductCaseConfig` from a scenario YAML file.

    The file is read through the shared :func:`common.file_io.load_yaml_mapping`; an empty
    file yields the default config.

    Args:
        path: The scenario YAML file.

    Returns:
        The validated, frozen config.

    Raises:
        common.file_io.ModelFileError: If the file is missing, unreadable, malformed, or not a
            YAML mapping.
        pydantic.ValidationError: If the content is not a valid config; the message names each
            failing field.
    """
    config = ProductCaseConfig.model_validate(load_yaml_mapping(Path(path)))
    logger.debug("loaded the product case's scenario %r from %s", config.scenario_name, path)
    return config


# ---------------------------------------------------------------------------
# The input cells' specs (D20): one per scenario value and per named constant that is an input
# ---------------------------------------------------------------------------

SCENARIO_INPUT_PREFIX: Final[str] = "inputs.scenario"
"""The artifact block of the scenario's input cells; a cell's path is this prefix and its
scenario key (:data:`SCENARIO_SPECS`'s keys)."""

CONSTANT_INPUT_PREFIX: Final[str] = "inputs.constants"
"""The artifact block of the named constants' input cells; a cell's path is this prefix and its
key in :data:`CONSTANT_INPUTS`."""

_PRICES_CLAIM: Final[str] = "COMM-722"
"""The source-ledger row of the product case's prices."""

_SETTINGS_CLAIM: Final[str] = "COMM-723"
"""The source-ledger row of the Monte Carlo's settings."""

_USAGE_CLAIM: Final[str] = "COMM-724"
"""The source-ledger row of the usage paths and conventions."""

_FLOORS_CLAIM: Final[str] = "COMM-725"
"""The source-ledger row of the usable floors."""

_DATA_IOT_ANCHOR_CLAIM: Final[str] = "COMM-726"
"""The source-ledger row of data IoT's anchor."""

_CUSTOMERS_CLAIM: Final[str] = "COMM-617"
"""The source-ledger row of Iridium's subscribers today (certified)."""

_ARPU_CLAIM: Final[str] = "COMM-618"
"""The source-ledger row of Iridium's ARPU today (certified)."""

_HELD_FLAT: Final[str] = (
    '(2026-10-06 19:38: "The prices will not go down, but they will not go up")'
)
"""The investor's words that hold every price flat, quoted in the price specs' rationales (the
sentence the constants' docstrings quote)."""

_TERMINAL_END_RULE: Final[str] = (
    "SCENARIO (the product-case code design's rule, approved by the investor on 2026-10-07) for "
    "the lower entries, context only, never the case's prices: steps of a tenth of the investor's "
    "price down to the lowest step at or above the class's break-even alone in every reported "
    "year, so that no context choice falls under the investor's floor on the committed "
    "engineering artifact."
)
"""The rule behind a terminal's lower end prices, quoted in their specs' rationales."""

_TERMINAL_PRICE_WORDS: Final[str] = (
    "(2026-10-07: \"Yes, let's use the $10 and $50. Let's do that\")"
)
"""The investor's words that set the two terminals' prices, quoted in their specs' rationales."""

_IOT_PRICE_WORDS: Final[str] = '(2026-10-06 19:52: "Let\'s go with the three and six for now")'
"""The investor's words that set the two IoT prices, quoted in their specs' rationales."""

_APPROVALS: Final[str] = (
    'the code design the investor approved at its gate (2026-10-07 13:03: "So actually, I think '
    'we\'re on yes. I think this is yes") and the plan (2026-10-12 20:27: "yes, approved, go ahead '
    'with the plan")'
)
"""The two approvals that made a value the product case's where the investor's words say less
than the value (a usage, a rough allotment, a question), quoted in those specs' rationales."""

_ENGINEERING_USAGE_WORDS: Final[str] = (
    '2026-10-04 13:33: "yes, go with the recommended column"; the 4 busy hours, 2026-10-04 19:59: '
    '"So for busy hours, it\'s fine"'
)
"""The investor's words behind a terminal's FY2031 total: the usage column and the busy hours."""

_ALLOTMENT_WORDS: Final[str] = (
    '2026-10-05: "for some of your bigger products, you get a 50% increase in your monthly '
    'allotment ... this is just a rough estimate right now"'
)
"""The investor's words behind a terminal's FY2035 total, quoted in full."""

_FY2036_USAGE_WORDS: Final[str] = '2026-10-12 15:56: "go with 9 GB, 90 GB and 13 bursts"'
"""The investor's words that set the product case's FY2036 usage."""

_RANGES_CHOICE: Final[str] = (
    "A modeling choice, which no market research grounds; approved by the investor with the "
    "product-case code design at its gate on 2026-10-07."
)
"""What grounds the three market responses' ranges, said in each range end's rationale."""


def _scenario_spec(
    label: str,
    unit: str | None,
    claim_id: str,
    source_note: str,
    rationale: str,
    *,
    notes: str | None = None,
    supporting: tuple[SupportingClaim, ...] = (),
) -> CellSpec:
    """One scenario value's spec: a default, status ``scenario``, its ledger row's claim."""
    return CellSpec(
        label=label,
        unit=unit,
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id=claim_id,
        source_note=source_note,
        rationale=rationale,
        notes=notes,
        supporting_claims=supporting,
    )


SCENARIO_SPECS: Final[Mapping[str, CellSpec]] = MappingProxyType(
    {
        "reported_years": _scenario_spec(
            "Reported years",
            "fiscal year",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the four reported years.",
            "SCENARIO (the 2026-10-05 product-case design): FY2031, the first year of service, "
            "to FY2036, the horizon's end; the summed revenue and the usable test run on them.",
        ),
        "prices.small_terminal.start_usd_month": _scenario_spec(
            "Small terminal start price",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: the small terminal's, held flat.",
            f"INVESTOR_SET {_TERMINAL_PRICE_WORDS}, it was $15; held flat {_HELD_FLAT}; the "
            "engineering model's small terminal price too (one price list).",
        ),
        "prices.small_terminal.end_usd_month": _scenario_spec(
            "Small terminal end prices",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: the start price, then the context's lower end prices.",
            f"INVESTOR_SET for the first entry, the start price {_TERMINAL_PRICE_WORDS} held flat "
            f"{_HELD_FLAT}; " + _TERMINAL_END_RULE,
            supporting=(SupportingClaim(_SETTINGS_CLAIM, "The choice grid the end prices span."),),
        ),
        "prices.mounted_terminal.start_usd_month": _scenario_spec(
            "Mounted terminal start price",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: the mounted terminal's, held flat.",
            f"INVESTOR_SET {_TERMINAL_PRICE_WORDS}, it was $100; held flat {_HELD_FLAT}; the "
            "engineering model's mounted terminal price too (one price list).",
        ),
        "prices.mounted_terminal.end_usd_month": _scenario_spec(
            "Mounted terminal end prices",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: the start price, then the context's lower end prices.",
            f"INVESTOR_SET for the first entry, the start price {_TERMINAL_PRICE_WORDS} held flat "
            f"{_HELD_FLAT}; " + _TERMINAL_END_RULE,
            supporting=(SupportingClaim(_SETTINGS_CLAIM, "The choice grid the end prices span."),),
        ),
        "prices.minimal_packet_iot.start_usd_month": _scenario_spec(
            "Minimal-packet IoT start price",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: minimal-packet IoT's, held flat; data IoT pays twice it.",
            f"INVESTOR_SET {_IOT_PRICE_WORDS}, held flat {_HELD_FLAT}.",
            notes=(
                "Data IoT pays twice this price in every year and choice (the investor's "
                "proportion, 2026-10-04); its price is not a setting."
            ),
        ),
        "prices.minimal_packet_iot.end_usd_month": _scenario_spec(
            "Minimal-packet IoT end prices",
            "USD/month",
            _PRICES_CLAIM,
            "The product case's prices: minimal-packet IoT's start price, held flat.",
            f"INVESTOR_SET {_IOT_PRICE_WORDS}: the start price held flat {_HELD_FLAT}, its one end "
            "price; the grid holds no lower IoT price.",
        ),
        "usage.small_terminal.gb_per_month": _scenario_spec(
            "Small terminal data a month, in all",
            "GB/month",
            _USAGE_CLAIM,
            "The usage paths: the small terminal's data a month in each reported year.",
            "INVESTOR_SET for FY2031, FY2035 and FY2036; SCENARIO for FY2033. FY2031's 5.4 GB is "
            f"the engineering usage the investor approved ({_ENGINEERING_USAGE_WORDS}): 2 Mbps "
            "while active, 2.5 percent active at the busy hour and 0.5 percent off-peak, 2.7 GB a "
            "month over the 4 busy hours and 2.7 GB over the 20 off-peak hours. FY2035's 8.1 GB is "
            f"5.4 GB with the investor's bigger allotment ({_ALLOTMENT_WORDS}). FY2036's 9 GB "
            f"({_FY2036_USAGE_WORDS}). FY2033's 6.7 GB is about half-way (round 1's 2.7 + 4.0 GB). "
            "The words of 2026-10-04 and 2026-10-05 give a usage and a rough allotment, not these "
            f"totals; the totals became the product case's values with {_APPROVALS}. The busy-hour "
            "part is the engineering usage's; the rest is off-peak.",
        ),
        "usage.mounted_terminal.gb_per_month": _scenario_spec(
            "Mounted terminal data a month, in all",
            "GB/month",
            _USAGE_CLAIM,
            "The usage paths: the mounted terminal's data a month in each reported year.",
            "INVESTOR_SET for FY2031, FY2035 and FY2036; SCENARIO for FY2033. FY2031's 54 GB is "
            f"the engineering usage the investor approved ({_ENGINEERING_USAGE_WORDS}): 5 Mbps "
            "while active, 10 percent active at the busy hour and 2 percent off-peak, 27 GB a "
            "month over the 4 busy hours and 27 GB over the 20 off-peak hours. FY2035's 81 GB is "
            f"54 GB with the investor's bigger allotment ({_ALLOTMENT_WORDS}). FY2036's 90 GB "
            f"({_FY2036_USAGE_WORDS}). FY2033's 67 GB is about half-way (round 1's 27 + 40 GB). "
            "The words of 2026-10-04 and 2026-10-05 give a usage and a rough allotment, not these "
            f"totals; the totals became the product case's values with {_APPROVALS}. The busy-hour "
            "part is the engineering usage's; the rest is off-peak.",
        ),
        "usage.minimal_packet_iot.messages_per_day": _scenario_spec(
            "Minimal-packet IoT messages a day",
            "messages/day",
            _USAGE_CLAIM,
            "The usage paths: minimal-packet IoT's messages a day, before a choice's scale.",
            "SCENARIO (round 1 of the product case's scratch exploration, 2026-10-06): 48, the "
            "engineering usage, doubling to 96 by FY2035 and held; each choice multiplies it by "
            "its usage scale's line factor (768 a day by FY2036 at x8, which the investor "
            'accepted on 2026-10-07: "I\'m fine with the number of messages per day").',
            notes="A usage a device sends, never a count of devices.",
        ),
        "usage.minimal_packet_iot.scales": _scenario_spec(
            "Minimal-packet IoT usage scales",
            "multiple",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the usage scales of minimal-packet IoT.",
            "SCENARIO (round 3's 1, 2 and 4 of the scratch exploration, 2026-10-06, extended so "
            "the usable test, not the grid, stops the usage; approved by the investor with the "
            "code design on 2026-10-07).",
        ),
        "usage.data_iot.messages_per_day": _scenario_spec(
            "Data IoT messages a day",
            "messages/day",
            _USAGE_CLAIM,
            "The usage paths: data IoT's messages a day, the same in every year.",
            "INVESTOR_SET (the investor's usage table, frozen 2026-10-04 12:31: \"This looks good "
            "... we'll kind of freeze it here\"): the engineering usage's 48 messages of 340 bytes "
            "a day, beside the bursts the table gave data IoT; the words freeze the table as a "
            f"whole, and the 48 became the product case's value with {_APPROVALS}. The usage scale "
            "moves the bursts, not the messages.",
        ),
        "usage.data_iot.bursts_per_day": _scenario_spec(
            "Data IoT bursts a day",
            "bursts/day",
            _USAGE_CLAIM,
            "The usage paths: data IoT's 100 KB bursts a day, before a choice's scale.",
            "INVESTOR_SET for FY2031's 8 (2026-10-05: \"My thinking is $8 is quite expensive for "
            "just 4 bursts of 100 kilobytes a day. So let's say we just doubled that\") and "
            f"FY2036's 13 ({_FY2036_USAGE_WORDS}); SCENARIO for FY2033's 10 and FY2035's 12 (round "
            "1 of the scratch exploration). The 2026-10-05 words were thinking aloud (\"we don't "
            f"have to change anything\"); the 8 became the product case's value with {_APPROVALS}.",
            notes="A usage a device sends, never a count of devices.",
        ),
        "usage.data_iot.bursts_outside_busy_hours": _scenario_spec(
            "Data IoT bursts outside the busy hours",
            None,
            _USAGE_CLAIM,
            "The usage paths: when data IoT's bursts go.",
            'INVESTOR_SET for FY2033 to FY2036 (2026-10-05: "Could the data IoT at the higher '
            "price do bursts like 12 or 24 bursts a day? Maybe you could say excluding peak time "
            "or something like that\"): outside the busy hours from FY2033; SCENARIO for FY2031's, "
            "at any hour (round 1 of the scratch exploration). The words asked a question; the "
            f"timing became the product case's value with {_APPROVALS}.",
        ),
        "usage.data_iot.scales": _scenario_spec(
            "Data IoT usage scales",
            "multiple",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the usage scales of data IoT.",
            "SCENARIO (round 3's 1, 2 and 4 of the scratch exploration, 2026-10-06, extended so "
            "the usable test, not the grid, stops the usage; approved by the investor with the "
            "code design on 2026-10-07).",
        ),
        "market.draws": _scenario_spec(
            "Market draws",
            "draws",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the number of drawn markets.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06; approved by the investor "
            "with the product-case code design at its gate on 2026-10-07). What 2,000 draws buy: "
            "another seed or draw count moves the drawn markets, never the central market; the "
            "headline, the pick read there, moves only when the pick does (it holds at seeds 1 to "
            "5, the same choice usable in 1,719 to 1,754 of the 2,000 draws, the plan's probe, "
            "local).",
        ),
        "market.seed": _scenario_spec(
            "Market seed",
            None,
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the generator's seed.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): one seed, so every run "
            "draws the same markets; another seed moves the drawn markets, never the central one "
            "(the pick holds at seeds 1 to 5).",
        ),
        "market.gamma.low": _scenario_spec(
            "Network response, low end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the network response's range.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): at 0.5 customers grow as "
            "the square root of the network's scale, so four times the network only doubles them. "
            + _RANGES_CHOICE,
        ),
        "market.gamma.high": _scenario_spec(
            "Network response, high end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the network response's range.",
            "SCENARIO (round 2, 2026-10-06): at 1.0 customers grow in proportion to the network's "
            "scale, the investor's \"If we are getting eight times the network overall, we should "
            'be getting about eight times the revenue. That is just an approximation" '
            "(2026-10-06); at the range's middle, 0.75, eight times the network brings 4.76 times "
            "the customers. " + _RANGES_CHOICE,
        ),
        "market.epsilon.low": _scenario_spec(
            "Price response, low end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the price response's range.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): at 0.5 a price half "
            "today's brings 1.41 times the customers and the revenue falls 29 percent. The range "
            "is centred on 1 (its high end's rationale says what that middle does). "
            + _RANGES_CHOICE,
        ),
        "market.epsilon.high": _scenario_spec(
            "Price response, high end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the price response's range.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): at 1.5 a price half "
            "today's brings 2.83 times the customers and the revenue rises 41 percent. The range "
            "is centred on 1, so at the central market, where the headline is read, the price "
            "response is exactly 1: for a given usage an uncapped class's price change shows there "
            "as customers, not revenue, and a terminal at its seats shows it as revenue; the "
            "headline also moves with a price through the usage the pick then takes. "
            + _RANGES_CHOICE,
        ),
        "market.eta.low": _scenario_spec(
            "Service response, low end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the service response's range.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): at 0 more service brings "
            "no customers. " + _RANGES_CHOICE,
        ),
        "market.eta.high": _scenario_spec(
            "Service response, high end",
            "exponent",
            _SETTINGS_CLAIM,
            "The Monte Carlo's settings: the service response's range.",
            "SCENARIO (round 2 of the scratch exploration, 2026-10-06): at 0.5 half again the "
            "service brings 22 percent more customers and twice the service 41 percent more; at "
            "the range's middle, 0.25, half again the service brings 11 percent more. "
            + _RANGES_CHOICE,
        ),
        "floors.fill": _scenario_spec(
            "Fill floor",
            "share of busy-hour beams",
            _FLOORS_CLAIM,
            "The usable floors: the share of the terminals' busy-hour beams filled.",
            "SCENARIO (round 2's reading of the investor's \"We do not want half our network "
            'used", 2026-10-06).',
        ),
        "floors.robust": _scenario_spec(
            "Robust floor",
            "share of draws",
            _FLOORS_CLAIM,
            "The usable floors: the share of the drawn markets the pick must be usable in.",
            "SCENARIO (round 2's reading of the investor's \"Take the clearly usable ones and "
            'then pick where you are", 2026-10-06).',
        ),
        "floors.margin_pct": _scenario_spec(
            "Margin floor",
            "percent",
            _FLOORS_CLAIM,
            "The usable floors: the whole business's margin in every reported year.",
            'INVESTOR_SET ("at least 50%", 2026-10-06; confirmed 2026-10-07 on the whole '
            "business: \"I think about a 50% floor for margin ... You wouldn't want to go below "
            'that for sure").',
            notes=(
                "The floor's other two parts are read where they live, not tested here: each "
                "class alone at or above break-even, and the engineering model's own margins, "
                "published."
            ),
        ),
    }
)
"""One cell spec per scenario value, keyed by its path in the scenario (a read-only mapping):
each describes the shipped default, so a run's value that differs from it is a scenario
override. The scenario's name and the engineering artifact's path are the run's identity, in
the artifact's ``metadata``, not inputs."""


@dataclass(frozen=True)
class ScenarioInput:
    """One scenario value ready for its input cell: the run's value beside the default it is
    compared with, both in the form an input cell holds.

    The config holds a list setting as a tuple and an input cell holds a list, and
    :func:`common.input_manifest._spec_cell` compares the run's value with the default by ``==``:
    a tuple against a list never compares equal, so a builder that turned only one side would
    publish the investor's defaults as scenario overrides, their claims and words dropped. Here
    both sides are lists (fresh ones, so nothing reaches the config), so the shipped values stay
    defaults.

    Attributes:
        path: The value's path in the scenario, a key of :data:`SCENARIO_SPECS`; its input
            cell's path is :data:`SCENARIO_INPUT_PREFIX` and this.
        value: The run's value, a list where the config holds a tuple.
        default: The code default at the same path, in the same form.
        description: What the field is, its config field's description.
        spec: The value's cell spec, describing the default.
    """

    path: str
    value: InputValue
    default: InputValue
    description: str
    spec: CellSpec


def _input_value(value: object, path: str) -> InputValue:
    """A config leaf in an input cell's form: a tuple as a list of its scalars, a scalar as is."""
    if isinstance(value, tuple):
        return [_input_scalar(item, path) for item in value]
    return _input_scalar(value, path)


def _input_scalar(value: object, path: str) -> InputScalar:
    """A config scalar as an input cell holds it; anything else is a spec naming no leaf."""
    if isinstance(value, (bool, int, float, str)):
        return value
    raise TypeError(f"{path} names no scalar or list of scalars of the config: {type(value)!r}")


def _leaf(config: BaseModel, path: str) -> tuple[BaseModel, str, object]:
    """The block that holds a dotted path's leaf, the leaf's field name and its value."""
    *blocks, name = path.split(".")
    block = config
    for key in blocks:
        nested = getattr(block, key)
        if not isinstance(nested, BaseModel):
            raise TypeError(f"{path}: {key} is not a config block")
        block = nested
    return block, name, getattr(block, name)


def scenario_inputs(config: ProductCaseConfig) -> tuple[ScenarioInput, ...]:
    """Each scenario value of a run with its default, description and spec, ready for its cell.

    Walks :data:`SCENARIO_SPECS` in order, reading each path on the run's config and on the code
    defaults (``ProductCaseConfig()``), both sides in an input cell's form (a tuple as a list),
    so :func:`common.input_manifest._spec_cell` sees a value equal to its default as the
    default, with its claim and the investor's words, and any other value as a scenario
    override. The scenario's name and the engineering artifact's path are the run's identity,
    not inputs, and have no entry.

    Args:
        config: The run's config.

    Returns:
        One :class:`ScenarioInput` per scenario value, in :data:`SCENARIO_SPECS`'s order.
    """
    defaults = ProductCaseConfig()
    entries: list[ScenarioInput] = []
    for path, spec in SCENARIO_SPECS.items():
        block, name, value = _leaf(config, path)
        _, _, default = _leaf(defaults, path)
        entries.append(
            ScenarioInput(
                path=path,
                value=_input_value(value, path),
                default=_input_value(default, path),
                description=_field_description(type(block), name),
                spec=spec,
            )
        )
    return tuple(entries)


@dataclass(frozen=True)
class ConstantInput:
    """A named constant the product case publishes as an input cell under ``inputs.constants``.

    Attributes:
        value: The constant's value, from :mod:`product_case.constants`.
        description: What the value is.
        spec: Its source metadata: status, claim, rationale.
    """

    value: int | float
    description: str
    spec: CellSpec


def _constant(
    value: int | float,
    description: str,
    label: str,
    unit: str | None,
    status: SourceStatus,
    claim_id: str,
    source_note: str,
    rationale: str,
    *,
    supporting: tuple[SupportingClaim, ...] = (),
) -> ConstantInput:
    """One named constant's input: its value, what it is, and its spec (a default)."""
    return ConstantInput(
        value=value,
        description=description,
        spec=CellSpec(
            label=label,
            unit=unit,
            role=AssumptionRole.DEFAULT,
            source_status=status,
            claim_id=claim_id,
            source_note=source_note,
            rationale=rationale,
            supporting_claims=supporting,
        ),
    )


_ANCHOR_RATIONALE: Final[str] = (
    "SOURCED_FACT: the demand curve's starting point for the class, today's customers of that "
    "kind at today's price; the curve grows them with the network's scale, the price and the "
    "service."
)
"""The rationale every certified anchor shares."""

_DATA_IOT_ANCHOR_RATIONALE: Final[str] = (
    "INVESTOR_SET (the investor's proportion, 2026-10-04: \"You look for proportions, look at "
    "research. It's not rocket science, extrapolate it out. Are they going to have as many as the "
    "small, minimal pack IOT? No. Is it going to have more than the small terminal, double the "
    "price? Yes\"): half of Iridium's IoT customers today at double their ARPU, on COMM-617 and "
    "COMM-618. The words give the bounds and the doubled price; the half is the investor's method "
    "that day, a proportion from the research: Iridium's tiers run close to inverse proportion "
    "(IoT 1,998,000 at $7.78 against voice and data 402,000 at $47), so twice the price holds half "
    f"the customers; it became the product case's value with {_APPROVALS}. Iridium reports one "
    "commercial IoT segment (1,998,000 "
    "at $7.78, COMM-617, COMM-618); the product case takes it whole as minimal-packet IoT's "
    "anchor and anchors data IoT beside it, so the two IoT classes start from twice Iridium's IoT "
    "revenue today, a run rate at today's count and ARPU ($373.1M a year against $186.5M). The "
    "curve's starting point, never a count of devices: data IoT's customers in every market and "
    "year come from the demand curve."
)
"""The rationale of data IoT's two anchor values (montecarlo M1's sentence)."""

CONSTANT_INPUTS: Final[Mapping[str, ConstantInput]] = MappingProxyType(
    {
        "anchors.small_terminal.customers": _constant(
            VOICE_DATA_CUSTOMERS_TODAY,
            "The small terminal's anchor customers: Iridium's voice-and-data subscribers today.",
            "Small terminal anchor customers",
            "customers",
            SourceStatus.CERTIFIED,
            _CUSTOMERS_CLAIM,
            "Iridium's commercial voice-and-data subscribers, year-end 2025.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.small_terminal.arpu_usd_month": _constant(
            VOICE_DATA_ARPU_USD_MONTH,
            "The small terminal's anchor price: Iridium's voice-and-data ARPU today.",
            "Small terminal anchor ARPU",
            "USD/month",
            SourceStatus.CERTIFIED,
            _ARPU_CLAIM,
            "Iridium's commercial voice-and-data ARPU.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.mounted_terminal.customers": _constant(
            BROADBAND_CUSTOMERS_TODAY,
            "The mounted terminal's anchor customers: Iridium's broadband subscribers today.",
            "Mounted terminal anchor customers",
            "customers",
            SourceStatus.CERTIFIED,
            _CUSTOMERS_CLAIM,
            "Iridium's commercial broadband subscribers, year-end 2025.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.mounted_terminal.arpu_usd_month": _constant(
            BROADBAND_ARPU_USD_MONTH,
            "The mounted terminal's anchor price: Iridium's broadband ARPU today.",
            "Mounted terminal anchor ARPU",
            "USD/month",
            SourceStatus.CERTIFIED,
            _ARPU_CLAIM,
            "Iridium's commercial broadband ARPU.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.minimal_packet_iot.customers": _constant(
            IOT_CUSTOMERS_TODAY,
            "Minimal-packet IoT's anchor customers: Iridium's IoT subscribers today.",
            "Minimal-packet IoT anchor customers",
            "devices",
            SourceStatus.CERTIFIED,
            _CUSTOMERS_CLAIM,
            "Iridium's commercial IoT subscribers, year-end 2025.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.minimal_packet_iot.arpu_usd_month": _constant(
            IOT_ARPU_USD_MONTH,
            "Minimal-packet IoT's anchor price: Iridium's IoT ARPU today.",
            "Minimal-packet IoT anchor ARPU",
            "USD/month",
            SourceStatus.CERTIFIED,
            _ARPU_CLAIM,
            "Iridium's commercial IoT ARPU.",
            _ANCHOR_RATIONALE,
        ),
        "anchors.data_iot.customers": _constant(
            DATA_IOT_ANCHOR_CUSTOMERS,
            "Data IoT's anchor customers: half of Iridium's IoT subscribers today.",
            "Data IoT anchor customers",
            "devices",
            SourceStatus.SCENARIO,
            _DATA_IOT_ANCHOR_CLAIM,
            "Data IoT's anchor, by the investor's proportion.",
            _DATA_IOT_ANCHOR_RATIONALE,
            supporting=(SupportingClaim(_CUSTOMERS_CLAIM, "Iridium's IoT subscribers today."),),
        ),
        "anchors.data_iot.arpu_usd_month": _constant(
            DATA_IOT_ANCHOR_ARPU_USD_MONTH,
            "Data IoT's anchor price: twice Iridium's IoT ARPU today.",
            "Data IoT anchor ARPU",
            "USD/month",
            SourceStatus.SCENARIO,
            _DATA_IOT_ANCHOR_CLAIM,
            "Data IoT's anchor, by the investor's proportion.",
            _DATA_IOT_ANCHOR_RATIONALE,
            supporting=(SupportingClaim(_ARPU_CLAIM, "Iridium's IoT ARPU today."),),
        ),
        "terminal_customers_today": _constant(
            TERMINAL_CUSTOMERS_TODAY,
            "Iridium's terminal customers today, voice and data plus broadband: the base the "
            "network's scale is measured against.",
            "Terminal customers today",
            "customers",
            SourceStatus.CERTIFIED,
            _CUSTOMERS_CLAIM,
            "Iridium's commercial voice-and-data and broadband subscribers, year-end 2025.",
            "SOURCED_FACT (the sum of two certified counts): the network's scale is the "
            "terminals' seats over this base, how many times today's terminal network the fleet "
            "carries.",
        ),
        "data_iot_anchor_share": _constant(
            DATA_IOT_ANCHOR_SHARE,
            "Data IoT's anchor customers as a share of Iridium's IoT customers today.",
            "Data IoT anchor share",
            "share",
            SourceStatus.SCENARIO,
            _DATA_IOT_ANCHOR_CLAIM,
            "Data IoT's anchor, by the investor's proportion.",
            _DATA_IOT_ANCHOR_RATIONALE,
        ),
        "data_iot_price_multiple": _constant(
            DATA_IOT_PRICE_MULTIPLE,
            "Data IoT's price as a multiple of minimal-packet IoT's, and its anchor price as a "
            "multiple of Iridium's IoT ARPU today.",
            "Data IoT price multiple",
            "multiple",
            SourceStatus.SCENARIO,
            _PRICES_CLAIM,
            "The product case's prices: data IoT at double minimal-packet IoT's price.",
            "INVESTOR_SET (the investor's proportion, 2026-10-04: \"Is it going to have more than "
            'the small terminal, double the price? Yes"; kept in every IoT price the investor set: '
            '"data IoT ... $8.00, the minimal packet is $4.00", 2026-10-04, then "Let\'s go with '
            'the three and six for now", 2026-10-06 19:52): data IoT pays twice minimal-packet '
            "IoT's price in every year and choice, so its price is not a setting.",
            supporting=(
                SupportingClaim(_DATA_IOT_ANCHOR_CLAIM, "The same multiple on data IoT's anchor."),
            ),
        ),
        "busy_hours_per_day": _constant(
            BUSY_HOURS_PER_DAY,
            "The busy hours a day.",
            "Busy hours a day",
            "hours/day",
            SourceStatus.SCENARIO,
            _USAGE_CLAIM,
            "The usage paths' conventions: the 4 busy hours.",
            "INVESTOR_SET (2026-10-04 19:59, asked to set the 4: \"I'm not sure what you mean by "
            "four, but that's okay. ... So for busy hours, it's fine\"): a terminal's busy-hour "
            "data is its engineering usage over these hours, so its seats are the engineering "
            "case's.",
        ),
        "days_per_month": _constant(
            DAYS_PER_MONTH,
            "The days in a month.",
            "Days a month",
            "days/month",
            SourceStatus.SCENARIO,
            _USAGE_CLAIM,
            "The usage paths' conventions: 30 days a month.",
            "SCENARIO (round 1's convention, 2026-10-06): a month is 30 days and a year 12 such "
            "months.",
        ),
        "bytes_per_gb": _constant(
            BYTES_PER_GB,
            "The bytes in a GB.",
            "Bytes a GB",
            "bytes/GB",
            SourceStatus.SCENARIO,
            _USAGE_CLAIM,
            "The usage paths' conventions: decimal units.",
            "SCENARIO (round 1's convention, 2026-10-06): decimal units, a GB is 10^9 bytes.",
        ),
        "bytes_per_mb": _constant(
            BYTES_PER_MB,
            "The bytes in a MB.",
            "Bytes a MB",
            "bytes/MB",
            SourceStatus.SCENARIO,
            _USAGE_CLAIM,
            "The usage paths' conventions: decimal units.",
            "SCENARIO (round 1's convention, 2026-10-06): decimal units, a MB is 10^6 bytes, as a "
            "GB is 10^9; data IoT's price per unit is in dollars a MB.",
        ),
    }
)
"""One input per named constant that is a model input, keyed by its path under
``inputs.constants`` (a read-only mapping): the anchors, Iridium's terminal customers today, data
IoT's proportion and the four conventions (the busy hours, the days a month, and the decimal GB
and MB). Unit conversions, the schema versions and the invariants' tolerance are definitions, not
inputs."""


__all__ = [
    "CONSTANT_INPUTS",
    "CONSTANT_INPUT_PREFIX",
    "SCENARIO_INPUT_PREFIX",
    "SCENARIO_SPECS",
    "ClassPriceDials",
    "ConstantInput",
    "DataIotUsageDials",
    "FloorDials",
    "MarketDials",
    "MinimalPacketIotUsageDials",
    "PriceDials",
    "ProductCaseConfig",
    "ResponseRange",
    "ScenarioInput",
    "TerminalUsageDials",
    "UsageDials",
    "load_product_case_config",
    "scenario_inputs",
]
