"""B6, the product case's artifact (``product-case-v1``) and its promotion command.

:func:`build_product_case_artifact` maps a run in state ``picked`` (:mod:`product_case.engine`) to
the artifact, ADR 002's contract, every block frozen with finite numbers only: ``metadata`` (the
model, the schema, the scenario, the stamp, and the engineering artifact read: its path, schema,
stamp and the SHA-256 of the bytes parsed); ``inputs`` (every scenario value, every named constant
that is a model input and every value read from ``iridium-v7`` as an input cell: the scenario's by
the override rule, a value that differs from its default a scenario override; the engineering
values ``derived_estimate`` with one ``model_derivation`` source whose ref names the value's place
in ``iridium-v7`` by key and whose note is the file's SHA-256, a value read in each reported year
one cell per year keyed ``<field>.<year>``); ``network``; ``choices`` (every choice's summary);
``fronts``; ``pick``; ``headline`` (the pick at the central market, the four classes side by side
and the year's totals, every numeric leaf under ``headline.years`` a provenance cell from the
product case's own catalog, :data:`~product_case.constants.FORMULA_CATALOG`, but each year's
``year``; the market's three responses plain); ``spreads``; ``meta``
(the catalog's formulas, the validation results, the data dictionary by the shared walker, the
worked ``jq`` queries, the source-status summary); and the stated assumptions, each built from the
run where a value is the run's. No total of customers is published: people and devices never add.

The command, from ``code/``::

    uv run python -m product_case.json_output scenarios/product_case.yaml \\
        communications/models/product_case/default.json [--version-stamp STAMP]

It follows the Iridium command's conventions (:mod:`common.cli`): a relative output path anchored
at the repository root (:meth:`common.file_io.SourceCheckout.anchored`), a scenario path against
the working directory; the stamp today's ISO date unless given; status on stderr; an expected
failure one ``ERROR:`` line and exit status 1, a usage error exit status 2; the one artifact
written through :func:`common.file_io.write_files_with_rollback` (a symbolic-link or non-regular
destination refused, a failed write leaving the file as it was). It reads the engineering
artifact's bytes once, hashes them and parses the same bytes. It refuses, in this order: a scenario
it cannot read or that is invalid (an IoT count among the unknown keys it refuses); the default
artifact's path written from any scenario but ``code/scenarios/product_case.yaml`` (naming both
paths; a side run writes to a path of its own, outside the tracked folders), before the engineering
artifact is read; an engineering artifact missing, unreadable, not JSON or of another schema
(naming ``iridium-v7``), and the engineering view's other refusals (a null coverage floor year, a
reported year absent or before the floor, a zero room); a usage the offers refuse; a run in state
``no_usable_choice`` (naming the test the candidates' draws fail most); a run that breaks an
invariant or holds a number that is not finite (naming it and the settings it scales with); a
failed write.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final  # typing-acceptable: Any is pydantic Field's own return type

from pydantic import BaseModel, ConfigDict, Field

from common.cli import (
    EXIT_ERROR,
    EXIT_OK,
    CliArgumentParser,
    configure_cli_logging,
    describe_failure,
)
from common.file_io import (
    ModelFileError,
    SourceCheckout,
    artifact_write,
    locate_source_checkout,
    write_files_with_rollback,
)
from common.input_manifest import (
    AssumptionRole,
    InputCell,
    InputValue,
    SourceRef,
    SourceRefType,
    SourceStatus,
    _cell,
    _spec_cell,
)
from common.meta import (
    UNIT_JSON_SCHEMA_KEY,
    DataDictEntry,
    FormulaDefinition,
    QueryAppliesTo,
    QueryExample,
    SourceStatusSummary,
    ValidationResult,
    build_data_dictionary,
    summarize_source_statuses,
)
from common.provenance import ProvenanceCell
from product_case.checks import robust_floor_text
from product_case.config import (
    CONSTANT_INPUT_PREFIX,
    CONSTANT_INPUTS,
    SCENARIO_INPUT_PREFIX,
    load_product_case_config,
    scenario_inputs,
)
from product_case.constants import (
    DATA_IOT_ANCHOR_ARPU_USD_MONTH,
    DATA_IOT_ANCHOR_CUSTOMERS,
    DATA_IOT_PRICE_MULTIPLE,
    DEMAND_ANCHORS,
    DOLLARS_PER_MILLION,
    FORMULA_CATALOG,
    IOT_ARPU_USD_MONTH,
    IOT_CUSTOMERS_TODAY,
    MONTHS_PER_YEAR,
    PATH_SEPARATOR,
    PHONE_DEVICE_CLASS,
    PRODUCT_CASE_SCHEMA_VERSION,
    TERMINAL_CUSTOMERS_TODAY,
    TERMINAL_DEVICE_CLASS,
    ClassKind,
    PickBasis,
    ProductCaseFormula,
    ProductClass,
    RunState,
    SpreadField,
    SpreadNullReason,
    UsableTest,
)
from product_case.engine import ProductCaseRun, most_failed_test, run_product_case
from product_case.engineering import EngineeringView, engineering_view_from_bytes
from product_case.monte_carlo import (
    BasisSpread,
    ChoiceSummary,
    ClassOutcome,
    MarketOutcome,
    Spreads,
    YearOutcome,
)

logger = logging.getLogger(__name__)

MODEL_NAME: Final[str] = "product_case"
"""The artifact's model name (``metadata.model``)."""

DEFAULT_ARTIFACT_PATH: Final[str] = "communications/models/product_case/default.json"
"""The promoted product case, repository-relative: reserved for the shipped scenario."""

SHIPPED_SCENARIO_PATH: Final[str] = "code/scenarios/product_case.yaml"
"""The shipped scenario, repository-relative: the one scenario the default path is written from."""

_BLOCK: Final[ConfigDict] = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
"""Every block: frozen, no key the schema does not define, finite numbers only."""

_ENGINEERING: Final[str] = "inputs.engineering"
"""The prefix of the engineering input cells' paths."""


class NoUsableChoiceError(ValueError):
    """No candidate is usable in any draw: the run has no pick, so nothing is published."""


class ReservedPathError(ValueError):
    """The default artifact's path is written from a scenario other than the shipped one."""


def _plain(description: str, unit: str) -> Any:
    """A plain field's description with its unit declared for the data dictionary (``Field``'s
    own return type, ``Any``, so a default of any annotated field)."""
    return Field(description=description, json_schema_extra={UNIT_JSON_SCHEMA_KEY: unit})


# ---------------------------------------------------------------------------
# The artifact's blocks
# ---------------------------------------------------------------------------


class EngineeringArtifactBlock(BaseModel):
    """The engineering artifact the run read."""

    model_config = _BLOCK
    path: str = Field(description="The engineering artifact's path as the scenario names it.")
    schema_version: str = Field(description="Its schema, iridium-v7 (the product case's pin).")
    version_stamp: str = Field(description="Its version stamp.")
    sha256: str = Field(description="The SHA-256 of the bytes the run parsed, hex.")


class MetadataBlock(BaseModel):
    """The run's identity."""

    model_config = _BLOCK
    model: str = Field(description="The model this artifact belongs to: product_case.")
    schema_version: str = Field(description="The artifact's schema version, product-case-v1.")
    scenario_name: str = Field(description="The scenario's label.")
    source_scenario_path: str = Field(
        description="The scenario YAML run: repository-relative, or absolute outside it."
    )
    version_stamp: str = Field(description="The caller's stamp (today's ISO date by default).")
    engineering_artifact: EngineeringArtifactBlock = Field(
        description="The engineering artifact read: path, schema, stamp and SHA-256."
    )


class InputsBlock(BaseModel):
    """Every input as an input cell, keyed by its path under its block."""

    model_config = _BLOCK
    scenario: dict[str, InputCell] = Field(
        description="Each scenario value, keyed by its path in the scenario."
    )
    constants: dict[str, InputCell] = Field(
        description="Each named constant that is a model input, keyed by its path."
    )
    engineering: dict[str, InputCell] = Field(
        description=(
            "Each value read from iridium-v7: a value of each reported year keyed <field>.<year>, "
            "a value read once keyed by its name; each cell's source names its place there."
        )
    )


class NetworkYearBlock(BaseModel):
    """One reported year's network, from the engineering inputs alone."""

    model_config = _BLOCK
    year: int = Field(description="The fiscal year.")
    seats_small_terminal: float = _plain("S_small = s x P_small, unrounded.", "customers")
    seats_mounted_terminal: float = _plain(
        "S_mounted = (1 - s) x P_mounted, unrounded.", "customers"
    )
    network_scale: float = _plain("k = (S_small + S_mounted) / 418,100.", "-")


class NetworkBlock(BaseModel):
    """The network the product case sells on (method step 1)."""

    model_config = _BLOCK
    small_terminal_share: float = _plain(
        "s, the small terminal's share of the busy-hour beams (today's mix as beams).", "share"
    )
    years: list[NetworkYearBlock] = Field(description="Each reported year, in order.")


class EndPricesBlock(BaseModel):
    """A choice's price a month by the last reported year, per class."""

    model_config = _BLOCK
    small_terminal: float = _plain("The small terminal's end price.", "USD/month")
    mounted_terminal: float = _plain("The mounted terminal's end price.", "USD/month")
    minimal_packet_iot: float = _plain("Minimal-packet IoT's end price.", "USD/month")
    data_iot: float = _plain("Data IoT's end price, twice minimal-packet IoT's.", "USD/month")


class ChoiceBlock(BaseModel):
    """One choice of the grid and its summary over the draws and at the central market."""

    model_config = _BLOCK
    choice_id: int = Field(description="The choice's index in the grid's order.")
    end_prices: EndPricesBlock = Field(description="Each class's end price.")
    minimal_packet_scale: float = _plain("Minimal-packet IoT's usage scale by the last year.", "-")
    data_iot_scale: float = _plain("Data IoT's usage scale by the last year.", "-")
    at_start_prices: bool = Field(description="Every end price equal to its start price.")
    usable_draws: int = _plain("The draws in which the choice is usable.", "count")
    usable_share: float = _plain("Usable draws over the draws.", "share")
    median_summed_revenue_musd: float | None = _plain(
        "The median over its usable draws of the revenue summed over the reported years; null "
        "when none is usable.",
        "MUSD",
    )
    median_last_year_revenue_musd: float | None = _plain(
        "The median over its usable draws of the last reported year's revenue; null when none.",
        "MUSD/year",
    )
    central_revenue_musd: list[float] = _plain(
        "The revenue at the central market, one value per reported year, in order.", "MUSD/year"
    )
    central_summed_revenue_musd: float = _plain(
        "The central market's revenue summed over the reported years.", "MUSD"
    )
    central_usable: bool = Field(description="Whether the central market is usable for it.")
    draws_failing: dict[str, int] = _plain(
        "The draws failing each usable test (a draw may fail several).", "count"
    )


class FrontsBlock(BaseModel):
    """The two fronts: choice ids, most usable first."""

    model_config = _BLOCK
    all_prices: list[int] = Field(description="The front over every choice (the context).")
    at_start_prices: list[int] = Field(description="The candidates' front, the pick on it.")


class PickBlock(BaseModel):
    """The pick among the candidates."""

    model_config = _BLOCK
    choice_id: int = Field(description="The picked choice's id.")
    basis: PickBasis = Field(description="robust_floor_met or most_usable_fallback (warned).")
    usage_edges: list[ProductClass] = Field(
        description="The IoT classes whose usage scale is the grid's top (normally none)."
    )
    dominated_in_context_by: list[int] = Field(
        description=(
            "The front over every choice's members at least as usable as the pick with a median "
            "at least as high, one of the two higher."
        )
    )


class MarketBlock(BaseModel):
    """The headline's market, each response at the middle of its range."""

    model_config = _BLOCK
    gamma: float = _plain("The response to the network's scale.", "-")
    epsilon: float = _plain("The price response.", "-")
    eta: float = _plain("The service response.", "-")


class TerminalBlock(BaseModel):
    """A terminal's own cells in a headline year."""

    model_config = _BLOCK
    seats: ProvenanceCell = Field(description="Its seats, unrounded.")
    seats_filled: ProvenanceCell = Field(description="Its busy-hour downlink use.")
    busy_hour_gb_per_month: ProvenanceCell = Field(description="Its busy-hour data a month.")
    offpeak_gb_per_month: ProvenanceCell = Field(description="Its off-peak data a month.")
    active_rate_mbps: ProvenanceCell = Field(description="Its rate while active.")
    offpeak_downlink_use: ProvenanceCell = Field(
        description="Its off-peak load against the busy-hour budget of the same seats."
    )


class IotBlock(BaseModel):
    """An IoT class's own cells in a headline year: a usage, never a count."""

    model_config = _BLOCK
    messages_per_day: ProvenanceCell = Field(description="The messages a device sends a day.")
    bursts_per_day: ProvenanceCell = Field(description="The 100 KB bursts a device sends a day.")
    bursts_outside_busy_hours: bool | None = Field(
        description="Whether the bursts go off-peak; null for a class that sends none."
    )
    bytes_per_day: ProvenanceCell = Field(description="What a device sends a day.")
    uplink_use_busy: ProvenanceCell = Field(description="Its share of the busy-hour uplink.")
    uplink_use_offpeak: ProvenanceCell = Field(description="Its share of the off-peak uplink.")


class HeadlineClassBlock(BaseModel):
    """One class in a headline year, side by side with the others."""

    model_config = _BLOCK
    product_class: ProductClass = Field(description="The class.")
    kind: ClassKind = Field(description="terminal (sold up to its seats) or iot (uncapped).")
    price_usd_per_month: ProvenanceCell = Field(description="Its price a month.")
    service: ProvenanceCell = Field(description="Its service over the first reported year's.")
    demand: ProvenanceCell = Field(description="The demand curve's customers or devices.")
    customers: ProvenanceCell = Field(description="Its customers (a terminal) or devices (IoT).")
    revenue_musd: ProvenanceCell = Field(description="Its revenue a year.")
    price_per_unit: ProvenanceCell = Field(description="Its price a GB, a message or a MB.")
    terminal: TerminalBlock | None = Field(description="A terminal's block; null for IoT.")
    iot: IotBlock | None = Field(description="An IoT class's block; null for a terminal.")


class HeadlineTotalsBlock(BaseModel):
    """A headline year's totals (no total of customers: people and devices never add)."""

    model_config = _BLOCK
    revenue_musd: ProvenanceCell = Field(description="The year's revenue.")
    fleet_annual_cost_musd: ProvenanceCell = Field(description="The fleet's annual cost.")
    margin_pct: ProvenanceCell = Field(description="The margin, against the fleet's cost.")
    profit_musd: ProvenanceCell = Field(description="Revenue less the fleet's annual cost.")
    busy_hour_beams_filled: ProvenanceCell = Field(description="The busy-hour beams filled.")
    iot_uplink_use_busy: ProvenanceCell = Field(description="IoT's busy-hour uplink use.")
    iot_uplink_use_offpeak: ProvenanceCell = Field(description="IoT's off-peak uplink use.")
    access_use: ProvenanceCell = Field(description="IoT's random-access use of its room.")
    access_attempts_per_second_per_beam: ProvenanceCell = Field(
        description="IoT's random-access attempts a second a phone-class beam."
    )
    single_tone_use: ProvenanceCell = Field(description="IoT's single-tone time used.")
    gb_carried_per_year: ProvenanceCell = Field(description="The GB the four classes carry.")
    cost_per_gb_carried_usd: ProvenanceCell = Field(description="The fleet's cost per GB carried.")


class HeadlineYearBlock(BaseModel):
    """One reported year of the headline."""

    model_config = _BLOCK
    year: int = Field(description="The fiscal year.")
    classes: list[HeadlineClassBlock] = Field(
        description="Small terminal, mounted terminal, minimal-packet IoT, data IoT."
    )
    totals: HeadlineTotalsBlock = Field(description="The year's totals.")


class HeadlineBlock(BaseModel):
    """The pick at the central market (a reading, not a gate)."""

    model_config = _BLOCK
    market: MarketBlock = Field(description="The central market.")
    usable: bool = Field(description="Whether the central market is usable for the pick.")
    failing_tests: list[UsableTest] = Field(description="The usable tests it fails.")
    years: list[HeadlineYearBlock] = Field(description="Each reported year, in order.")


class UsableDrawsSpread(BaseModel):
    """A field's spread over the pick's usable draws."""

    model_config = _BLOCK
    p10: float | None = _plain("The 10th percentile; null below 9 usable draws.", "per field")
    p50: float | None = _plain("The median; null below 9 usable draws.", "per field")
    p90: float | None = _plain("The 90th percentile; null below 9 usable draws.", "per field")
    headline_rank: float = _plain("The headline's mid-rank among the usable draws.", "share")
    null_reason: SpreadNullReason | None = Field(description="Why the percentiles are null.")


class AllDrawsSpread(BaseModel):
    """A field's spread over all draws, the usable test not applied."""

    model_config = _BLOCK
    p10: float = _plain("The 10th percentile.", "per field")
    p50: float = _plain("The median.", "per field")
    p90: float = _plain("The 90th percentile.", "per field")
    headline_rank: float = _plain("The headline's mid-rank among all draws.", "share")


class EverySeatBlock(BaseModel):
    """For a terminal's customers and revenue: the headline and the draws at every seat."""

    model_config = _BLOCK
    headline_sells_every_seat: bool = Field(description="Customers equal floor(seats).")
    usable_draws_share: float = _plain("The usable draws' share at every seat.", "share")
    all_draws_share: float = _plain("All draws' share at every seat.", "share")


class SpreadFieldBlock(BaseModel):
    """One headline value's spread in a reported year."""

    model_config = _BLOCK
    field: SpreadField = Field(description="The headline value it spreads.")
    usable_draws: UsableDrawsSpread = Field(description="Over the pick's usable draws.")
    all_draws: AllDrawsSpread = Field(description="Over all draws.")
    every_seat: EverySeatBlock | None = Field(
        description="A terminal's customers and revenue only; null otherwise."
    )


class SpreadYearBlock(BaseModel):
    """One reported year's spreads."""

    model_config = _BLOCK
    year: int = Field(description="The fiscal year.")
    fields: list[SpreadFieldBlock] = Field(description="Each spread field, in its order.")


class AllDrawsBasisBlock(BaseModel):
    """The all-draw basis's stated label (montecarlo M2)."""

    model_config = _BLOCK
    label: str = Field(description="What the all-draw spreads cover.")
    draws: int = _plain("All drawn markets.", "count")
    draws_past_iot_room: int = _plain(
        "The drawn markets in which the pick sells IoT past its uplink, access or single-tone "
        "room.",
        "count",
    )


class SpreadsBlock(BaseModel):
    """The pick's spreads over the drawn markets."""

    model_config = _BLOCK
    all_draws_basis: AllDrawsBasisBlock = Field(description="The all-draw basis's label.")
    years: list[SpreadYearBlock] = Field(description="Each reported year, in order.")


class MetaBlock(BaseModel):
    """ADR 002's cold-reader block."""

    model_config = _BLOCK
    formulas: list[FormulaDefinition] = Field(description="The product case's formula catalog.")
    validation_results: list[ValidationResult] = Field(
        description="The invariants, the believability checks and the run's warnings."
    )
    data_dictionary: list[DataDictEntry] = Field(description="Every leaf's meaning and unit.")
    query_examples: list[QueryExample] = Field(description="Worked jq queries.")
    source_status_summary: SourceStatusSummary = Field(
        description="The input cells counted by source status."
    )


class ProductCaseArtifact(BaseModel):
    """The product case's promoted artifact, ``product-case-v1``."""

    model_config = _BLOCK
    metadata: MetadataBlock = Field(description="The run's identity.")
    inputs: InputsBlock = Field(description="Every input as an input cell.")
    network: NetworkBlock = Field(description="The network sold on.")
    choices: list[ChoiceBlock] = Field(description="Every choice's summary, in the grid's order.")
    fronts: FrontsBlock = Field(description="The two fronts.")
    pick: PickBlock = Field(description="The pick.")
    headline: HeadlineBlock = Field(description="The pick at the central market.")
    spreads: SpreadsBlock = Field(description="The pick's spreads.")
    meta: MetaBlock = Field(description="Formulas, validation, dictionary, queries, statuses.")
    assumptions: list[str] = Field(description="The stated assumptions, one line each.")


# ---------------------------------------------------------------------------
# The cells
# ---------------------------------------------------------------------------

_ENGINEERING_SOURCE: Final[str] = "the engineering artifact (metadata.engineering_artifact)"
"""The source label of a value derived from the engineering artifact's inputs."""

_SOURCES: Final[Mapping[ProductCaseFormula, tuple[str, ...]]] = MappingProxyType(
    {
        ProductCaseFormula.PRICE_LINE: ("COMM-722",),
        ProductCaseFormula.SERVICE: ("COMM-724",),
        ProductCaseFormula.USAGE_LINE: ("COMM-724",),
        ProductCaseFormula.IOT_BYTES_PER_DAY: ("COMM-724", _ENGINEERING_SOURCE),
        ProductCaseFormula.PRICE_PER_UNIT: ("COMM-722", "COMM-724"),
        ProductCaseFormula.DEMAND_CURVE: ("COMM-617", "COMM-618", "COMM-723", "COMM-726"),
        ProductCaseFormula.SOLD: (
            "COMM-617",
            "COMM-618",
            "COMM-723",
            "COMM-726",
            _ENGINEERING_SOURCE,
        ),
        ProductCaseFormula.CLASS_REVENUE: ("COMM-722", "COMM-723"),
        ProductCaseFormula.REVENUE: ("COMM-722", "COMM-723"),
        ProductCaseFormula.MARGIN: ("COMM-722", "COMM-723", _ENGINEERING_SOURCE),
        ProductCaseFormula.PROFIT: ("COMM-722", "COMM-723", _ENGINEERING_SOURCE),
        ProductCaseFormula.SEATS: (_ENGINEERING_SOURCE,),
        ProductCaseFormula.FLEET_ANNUAL_COST: (_ENGINEERING_SOURCE,),
        ProductCaseFormula.TERMINAL_ACTIVE_RATE: (_ENGINEERING_SOURCE,),
        ProductCaseFormula.TERMINAL_BUSY_HOUR_DATA: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.TERMINAL_OFFPEAK_DATA: ("COMM-724",),
        ProductCaseFormula.TERMINAL_DOWNLINK_USE: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.BUSY_HOUR_BEAMS_FILLED: (_ENGINEERING_SOURCE, "COMM-723"),
        ProductCaseFormula.IOT_UPLINK_USE: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.ACCESS_USE: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.ACCESS_ATTEMPTS_PER_BEAM: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.SINGLE_TONE_USE: (_ENGINEERING_SOURCE, "COMM-724"),
        ProductCaseFormula.GB_CARRIED: ("COMM-724", _ENGINEERING_SOURCE),
        ProductCaseFormula.COST_PER_GB_CARRIED: ("COMM-724", _ENGINEERING_SOURCE),
    }
)
"""The ledger rows (and the engineering artifact) behind each headline formula's inputs."""


_UNIT_PRICE_UNITS: Final[Mapping[ProductClass, str]] = MappingProxyType(
    {
        ProductClass.SMALL_TERMINAL: "USD/GB",
        ProductClass.MOUNTED_TERMINAL: "USD/GB",
        ProductClass.MINIMAL_PACKET_IOT: "USD/message",
        ProductClass.DATA_IOT: "USD/MB",
    }
)
"""Each class's price per unit's unit: a GB, a message, a MB."""

_OTHER_KINDS_USES: Final[Mapping[ClassKind, tuple[str, ...]]] = MappingProxyType(
    {
        ClassKind.TERMINAL: ("headline.years[].classes[].iot.", "inputs.constants.bytes_per_mb"),
        ClassKind.IOT: ("headline.years[].classes[].terminal.",),
    }
)
"""The uses a class's cell leaves out by its kind: a terminal's, the IoT block's paths and the
MB's size (data IoT's unit); an IoT class's, the terminal block's paths (an IoT class has no
seats)."""


def _cell_of(
    formula: ProductCaseFormula,
    value: float | int | None,
    unit: str,
    description: str,
    kind: ClassKind | None = None,
) -> ProvenanceCell:
    """A headline value as a provenance cell from the product case's catalog.

    ``common.provenance.cell`` reads the data center's catalog, so the product case builds its
    cells here: the formula's text and name from :data:`FORMULA_CATALOG`, its ``uses`` the
    entry's input paths (for a class's cell, those of its kind: :data:`_OTHER_KINDS_USES`), its
    sources the ledger rows behind them.
    """
    entry = FORMULA_CATALOG[formula]
    uses = [path for path in entry.input_path_pattern.split(PATH_SEPARATOR) if " " not in path]
    if kind is not None:
        uses = [path for path in uses if not path.startswith(_OTHER_KINDS_USES[kind])]
    return ProvenanceCell(
        value=value,
        unit=unit,
        formula=entry.formula_text,
        formula_name=entry.formula_id,
        uses=uses,
        sources=list(_SOURCES[formula]),
        description=description,
    )


def _whole(value: float) -> int:
    """A count the invariants held whole, published as an integer."""
    return round(value)


def _class_block(entry: ClassOutcome) -> HeadlineClassBlock:
    """One headline class's cells, each cell's uses its kind's."""

    def cell(
        formula: ProductCaseFormula, value: float | int | None, unit: str, description: str
    ) -> ProvenanceCell:
        """A cell of this class: :func:`_cell_of` at the class's kind."""
        return _cell_of(formula, value, unit, description, entry.kind)

    noun = "customers" if entry.kind is ClassKind.TERMINAL else "devices"
    unit_price = _UNIT_PRICE_UNITS[entry.product_class]
    terminal = None
    if entry.terminal is not None:
        block = entry.terminal
        terminal = TerminalBlock(
            seats=cell(ProductCaseFormula.SEATS, block.seats, "customers", "Its seats."),
            seats_filled=cell(
                ProductCaseFormula.TERMINAL_DOWNLINK_USE,
                block.seats_filled,
                "share",
                "Seats filled.",
            ),
            busy_hour_gb_per_month=cell(
                ProductCaseFormula.TERMINAL_BUSY_HOUR_DATA,
                block.busy_hour_gb_per_month,
                "GB/month",
                "The engineering usage's busy-hour data a month.",
            ),
            offpeak_gb_per_month=cell(
                ProductCaseFormula.TERMINAL_OFFPEAK_DATA,
                block.offpeak_gb_per_month,
                "GB/month",
                "The monthly total less the busy-hour part.",
            ),
            active_rate_mbps=cell(
                ProductCaseFormula.TERMINAL_ACTIVE_RATE,
                block.active_rate_mbps,
                "Mbps",
                "The engineering usage's rate while active.",
            ),
            offpeak_downlink_use=cell(
                ProductCaseFormula.TERMINAL_DOWNLINK_USE,
                block.offpeak_downlink_use,
                "share",
                "The off-peak load against the busy-hour budget of the same seats.",
            ),
        )
    iot = None
    if entry.iot is not None:
        usage = entry.iot
        iot = IotBlock(
            messages_per_day=cell(
                ProductCaseFormula.USAGE_LINE, usage.messages_per_day, "messages/day", "Messages."
            ),
            bursts_per_day=cell(
                ProductCaseFormula.USAGE_LINE, usage.bursts_per_day, "bursts/day", "Bursts."
            ),
            bursts_outside_busy_hours=usage.bursts_outside_busy_hours,
            bytes_per_day=cell(
                ProductCaseFormula.IOT_BYTES_PER_DAY, usage.bytes_per_day, "bytes/day", "Bytes."
            ),
            uplink_use_busy=cell(
                ProductCaseFormula.IOT_UPLINK_USE,
                usage.uplink_use_busy,
                "share",
                "Its term of the busy-hour uplink use.",
            ),
            uplink_use_offpeak=cell(
                ProductCaseFormula.IOT_UPLINK_USE,
                usage.uplink_use_offpeak,
                "share",
                "Its term of the off-peak uplink use.",
            ),
        )
    return HeadlineClassBlock(
        product_class=entry.product_class,
        kind=entry.kind,
        price_usd_per_month=cell(
            ProductCaseFormula.PRICE_LINE, entry.price_usd_per_month, "USD/month", "Its price."
        ),
        service=cell(ProductCaseFormula.SERVICE, entry.service, "-", "Its service."),
        demand=cell(ProductCaseFormula.DEMAND_CURVE, entry.demand, noun, "Its demand."),
        customers=cell(ProductCaseFormula.SOLD, _whole(entry.customers), noun, "Sold."),
        revenue_musd=cell(
            ProductCaseFormula.CLASS_REVENUE, entry.revenue_musd, "MUSD/year", "Its revenue."
        ),
        price_per_unit=cell(
            ProductCaseFormula.PRICE_PER_UNIT, entry.price_per_unit, unit_price, "Its unit price."
        ),
        terminal=terminal,
        iot=iot,
    )


def _year_block(year: YearOutcome) -> HeadlineYearBlock:
    """One headline year's cells."""
    totals = year.totals
    formula = ProductCaseFormula
    return HeadlineYearBlock(
        year=year.year,
        classes=[_class_block(entry) for entry in year.classes],
        totals=HeadlineTotalsBlock(
            revenue_musd=_cell_of(formula.REVENUE, totals.revenue_musd, "MUSD/year", "Revenue."),
            fleet_annual_cost_musd=_cell_of(
                formula.FLEET_ANNUAL_COST, totals.fleet_annual_cost_musd, "MUSD/year", "Cost."
            ),
            margin_pct=_cell_of(formula.MARGIN, totals.margin_pct, "percent", "The margin."),
            profit_musd=_cell_of(formula.PROFIT, totals.profit_musd, "MUSD/year", "Profit."),
            busy_hour_beams_filled=_cell_of(
                formula.BUSY_HOUR_BEAMS_FILLED, totals.busy_hour_beams_filled, "share", "Filled."
            ),
            iot_uplink_use_busy=_cell_of(
                formula.IOT_UPLINK_USE, totals.iot_uplink_use_busy, "share", "Busy-hour use."
            ),
            iot_uplink_use_offpeak=_cell_of(
                formula.IOT_UPLINK_USE, totals.iot_uplink_use_offpeak, "share", "Off-peak use."
            ),
            access_use=_cell_of(formula.ACCESS_USE, totals.access_use, "share", "Access use."),
            access_attempts_per_second_per_beam=_cell_of(
                formula.ACCESS_ATTEMPTS_PER_BEAM,
                totals.access_attempts_per_second_per_beam,
                "attempts/s/beam",
                "Attempts a second a beam.",
            ),
            single_tone_use=_cell_of(
                formula.SINGLE_TONE_USE, totals.single_tone_use, "share", "Single-tone use."
            ),
            gb_carried_per_year=_cell_of(
                formula.GB_CARRIED, totals.gb_carried_per_year, "GB/year", "GB carried."
            ),
            cost_per_gb_carried_usd=_cell_of(
                formula.COST_PER_GB_CARRIED, totals.cost_per_gb_carried_usd, "USD/GB", "Per GB."
            ),
        ),
    )


def _headline_block(headline: MarketOutcome) -> HeadlineBlock:
    """The headline block."""
    market = headline.market
    return HeadlineBlock(
        market=MarketBlock(gamma=market.gamma, epsilon=market.epsilon, eta=market.eta),
        usable=headline.usable,
        failing_tests=list(headline.failing_tests),
        years=[_year_block(year) for year in headline.years],
    )


# ---------------------------------------------------------------------------
# The inputs
# ---------------------------------------------------------------------------


def _engineering_cell(
    key: str, place: str, value: InputValue, label: str, unit: str | None, sha256: str
) -> tuple[str, InputCell]:
    """One value read from ``iridium-v7``: its key and its input cell."""
    return key, InputCell(
        path=f"{_ENGINEERING}.{key}",
        label=label,
        value=value,
        unit=unit,
        description=f"{label}, as the engineering artifact publishes it ({place}).",
        assumption_role=AssumptionRole.DERIVED_INPUT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        source_refs=[
            SourceRef(
                ref_type=SourceRefType.MODEL_DERIVATION, ref=place, claim_id=None, note=sha256
            )
        ],
        rationale=(
            "Read from the engineering model's promoted artifact (iridium-v7) at the SHA-256 in "
            "the note; the product case never feeds that model."
        ),
    )


def _count_value(value: float) -> InputValue:
    """A people count as read: an integer when it is whole (the artifact's form)."""
    return int(value) if value.is_integer() else value


def _engineering_cells(view: EngineeringView) -> dict[str, InputCell]:
    """Every value the run read from ``iridium-v7``, keyed per reported year or by name."""
    sha = view.sha256
    small = TERMINAL_DEVICE_CLASS[ProductClass.SMALL_TERMINAL]
    mounted = TERMINAL_DEVICE_CLASS[ProductClass.MOUNTED_TERMINAL]
    cells: list[tuple[str, InputCell]] = []
    for year in view.years:
        at = f"years[year={year.year}]"
        cells += [
            _engineering_cell(
                f"living_fleet.{year.year}",
                f"{at}.living_fleet",
                year.living_fleet,
                f"Living fleet FY{year.year}",
                "satellites",
                sha,
            ),
            _engineering_cell(
                f"annual_cost_musd.{year.year}",
                f"{at}.annual_cost_musd",
                year.annual_cost_musd,
                f"Fleet annual cost FY{year.year}",
                "MUSD/year",
                sha,
            ),
            _engineering_cell(
                f"people_small_terminal.{year.year}",
                f"{at}.classes[device_class={small}].people_served",
                _count_value(year.people_small_terminal),
                f"Small terminal whole-fleet people FY{year.year}",
                "people",
                sha,
            ),
            _engineering_cell(
                f"people_mounted_terminal.{year.year}",
                f"{at}.classes[device_class={mounted}].people_served",
                _count_value(year.people_mounted_terminal),
                f"Mounted terminal whole-fleet people FY{year.year}",
                "people",
                sha,
            ),
            _engineering_cell(
                f"phone_useful_beams.{year.year}",
                f"{at}.classes[device_class={PHONE_DEVICE_CLASS}].useful_beams",
                year.phone_useful_beams,
                f"Phone-class useful beams FY{year.year}",
                "beams",
                sha,
            ),
            _engineering_cell(
                f"iot_payload_bits_per_second.{year.year}",
                f"{at}.iot.uplink_payload_bits_per_second",
                year.iot_payload_bits_per_second,
                f"IoT payload room FY{year.year}",
                "bits/s",
                sha,
            ),
            _engineering_cell(
                f"iot_access_attempts_per_second.{year.year}",
                f"{at}.iot.access_attempts_per_second_low",
                year.iot_access_attempts_per_second,
                f"IoT access room FY{year.year}",
                "attempts/s",
                sha,
            ),
            _engineering_cell(
                f"iot_single_tone_seconds_per_second.{year.year}",
                f"{at}.iot.single_tone_seconds_per_second",
                year.iot_single_tone_seconds_per_second,
                f"IoT single-tone room FY{year.year}",
                "tone-seconds/s",
                sha,
            ),
        ]
    for product_class, pool in (
        (ProductClass.SMALL_TERMINAL, view.small_terminal_pool),
        (ProductClass.MOUNTED_TERMINAL, view.mounted_terminal_pool),
    ):
        device = TERMINAL_DEVICE_CLASS[product_class]
        at = f"classes[device_class={device}]"
        cells += [
            _engineering_cell(
                f"{product_class}.device_class",
                f"{at}.device_class",
                device,
                f"The {product_class}'s engineering device class",
                None,
                sha,
            ),
            _engineering_cell(
                f"{product_class}.beam_pool_mbps",
                f"{at}.beam_pool_mbps",
                pool.beam_pool_mbps,
                f"The {product_class}'s beam pool",
                "Mbps",
                sha,
            ),
            _engineering_cell(
                f"{product_class}.active_user_rate_mbps",
                f"{at}.active_user_rate_mbps",
                pool.active_user_rate_mbps,
                f"The {product_class}'s rate while active",
                "Mbps",
                sha,
            ),
            _engineering_cell(
                f"{product_class}.concurrency_peak",
                f"{at}.concurrency_peak",
                pool.concurrency_peak,
                f"The {product_class}'s busy-hour share",
                "share",
                sha,
            ),
        ]
    cells += [
        _engineering_cell(
            "iot_message_bytes",
            "iridium_physics.iot_message_bytes",
            view.message_bytes,
            "IoT message size",
            "bytes",
            sha,
        ),
        _engineering_cell(
            "iot_burst_bytes",
            "iridium_physics.iot_burst_bytes",
            view.burst_bytes,
            "Data IoT burst size",
            "bytes",
            sha,
        ),
        _engineering_cell(
            "iot_message_airtime_high_s",
            "iridium_physics.iot_message_airtime_high_s",
            view.airtime_high_s,
            "Message single-tone airtime, high end",
            "s",
            sha,
        ),
        _engineering_cell(
            "coverage_floor_reached_year",
            "trajectory_summary.coverage_floor_reached_year",
            view.coverage_floor_reached_year,
            "Coverage floor year",
            "year",
            sha,
        ),
    ]
    return dict(cells)


def _inputs_block(run: ProductCaseRun, scenario_path: str) -> InputsBlock:
    """Every input cell: the scenario's by the override rule, the constants, the engineering."""
    scenario = {
        item.path: _spec_cell(
            f"{SCENARIO_INPUT_PREFIX}.{item.path}",
            item.value,
            item.default,
            item.description,
            item.spec,
            scenario_path,
        )
        for item in scenario_inputs(run.config)
    }
    constants = {
        key: _cell(f"{CONSTANT_INPUT_PREFIX}.{key}", item.value, item.description, item.spec)
        for key, item in CONSTANT_INPUTS.items()
    }
    return InputsBlock(
        scenario=scenario, constants=constants, engineering=_engineering_cells(run.engineering)
    )


# ---------------------------------------------------------------------------
# The Monte Carlo's blocks
# ---------------------------------------------------------------------------


def _usable_spread(basis: BasisSpread) -> UsableDrawsSpread:
    """A usable-draw spread block."""
    return UsableDrawsSpread(
        p10=basis.p10,
        p50=basis.p50,
        p90=basis.p90,
        headline_rank=basis.headline_rank,
        null_reason=basis.null_reason,
    )


def _all_spread(basis: BasisSpread) -> AllDrawsSpread:
    """An all-draw spread block (its percentiles stand: a scenario holds 9 draws or more)."""
    if basis.p10 is None or basis.p50 is None or basis.p90 is None:
        raise ValueError("the all-draw percentiles are null: the scenario has fewer than 9 draws")
    return AllDrawsSpread(
        p10=basis.p10, p50=basis.p50, p90=basis.p90, headline_rank=basis.headline_rank
    )


def _spreads_block(spreads: Spreads) -> SpreadsBlock:
    """The spreads block with the all-draw basis's label (montecarlo M2)."""
    label = (
        "every drawn market, the usable test not applied: in "
        f"{spreads.draws_past_iot_room:,} of the {spreads.draws:,} drawn markets the pick sells "
        "IoT past its uplink, access or single-tone room in some reported year"
    )
    return SpreadsBlock(
        all_draws_basis=AllDrawsBasisBlock(
            label=label, draws=spreads.draws, draws_past_iot_room=spreads.draws_past_iot_room
        ),
        years=[
            SpreadYearBlock(
                year=year.year,
                fields=[
                    SpreadFieldBlock(
                        field=entry.field,
                        usable_draws=_usable_spread(entry.usable_draws),
                        all_draws=_all_spread(entry.all_draws),
                        every_seat=None
                        if entry.every_seat is None
                        else EverySeatBlock(
                            headline_sells_every_seat=entry.every_seat.headline_sells_every_seat,
                            usable_draws_share=entry.every_seat.usable_draws_share,
                            all_draws_share=entry.every_seat.all_draws_share,
                        ),
                    )
                    for entry in year.fields
                ],
            )
            for year in spreads.years
        ],
    )


def _choice_blocks(run: ProductCaseRun) -> list[ChoiceBlock]:
    """Every choice's summary."""
    return [
        ChoiceBlock(
            choice_id=summary.choice.choice_id,
            end_prices=EndPricesBlock(
                small_terminal=summary.choice.end_prices[ProductClass.SMALL_TERMINAL],
                mounted_terminal=summary.choice.end_prices[ProductClass.MOUNTED_TERMINAL],
                minimal_packet_iot=summary.choice.end_prices[ProductClass.MINIMAL_PACKET_IOT],
                data_iot=summary.choice.end_prices[ProductClass.DATA_IOT],
            ),
            minimal_packet_scale=summary.choice.minimal_packet_scale,
            data_iot_scale=summary.choice.data_iot_scale,
            at_start_prices=summary.choice.at_start_prices,
            usable_draws=summary.usable_draws,
            usable_share=summary.usable_share,
            median_summed_revenue_musd=summary.median_summed_revenue_musd,
            median_last_year_revenue_musd=summary.median_last_year_revenue_musd,
            central_revenue_musd=list(summary.central_revenue_musd),
            central_summed_revenue_musd=summary.central_summed_revenue_musd,
            central_usable=summary.central_usable,
            draws_failing={str(test): count for test, count in summary.draws_failing.items()},
        )
        for summary in run.choices
    ]


# ---------------------------------------------------------------------------
# The stated assumptions and the worked queries
# ---------------------------------------------------------------------------


def _money(value_musd: float) -> str:
    """$M with one decimal and thousands separators."""
    return f"${value_musd:,.1f}M"


_IOT_CLASS_NAMES: Final[Mapping[ProductClass, str]] = MappingProxyType(
    {ProductClass.MINIMAL_PACKET_IOT: "minimal-packet IoT", ProductClass.DATA_IOT: "data IoT"}
)
"""The two IoT classes as the stated lines name them (a usage edge is always an IoT class's)."""


def _usage_edge_clause(edges: Sequence[ProductClass], chosen: ChoiceSummary) -> str:
    """The clause the usage-stop line adds when the pick sits on an upper usage edge: each IoT
    class whose usage stops at the top of its list, with its scale there ("" when none does).

    Args:
        edges: The pick's usage edges, in class order (at most the two IoT classes).
        chosen: The pick's summary, whose choice holds the two usage scales.

    Returns:
        The clause, opening with "; ", or "" when the pick is on no upper usage edge.
    """
    scales = {
        ProductClass.MINIMAL_PACKET_IOT: chosen.choice.minimal_packet_scale,
        ProductClass.DATA_IOT: chosen.choice.data_iot_scale,
    }
    if not edges:
        return ""
    if len(edges) == 1:
        (only,) = edges
        return (
            f"; {_IOT_CLASS_NAMES[only]}'s usage stops at x{scales[only]:g}, the top of its usage "
            "list (an upper usage edge, warned)"
        )
    first, second = edges
    return (
        f"; {_IOT_CLASS_NAMES[first]}'s usage stops at x{scales[first]:g} and "
        f"{_IOT_CLASS_NAMES[second]}'s at x{scales[second]:g}, each the top of its usage list "
        "(upper usage edges, warned)"
    )


def _usage_stop_line(run: ProductCaseRun, chosen: ChoiceSummary) -> str:
    """The stated line on what stops the usage, as this run's pick came: by the robust floor, or,
    when no candidate reaches it, by the fallback (the design's D19), every number the run's.

    The robust branch names the three stops: the floor, the median's peak and the top of an IoT
    class's usage list. On either basis, a pick on an upper usage edge adds each IoT class whose
    usage stops at the top of its list, with its scale (:func:`_usage_edge_clause`; the artifact
    warns of it, ``warning.pick_on_upper_usage_edge``).

    Args:
        run: A run with a pick.
        chosen: The pick's summary.

    Returns:
        The line.

    Raises:
        ValueError: If the run has no pick.
    """
    pick = run.pick
    if pick is None:
        raise ValueError("a run with no pick has no usage to state")
    config = run.config
    floor = robust_floor_text(config)
    if pick.basis is PickBasis.ROBUST_FLOOR_MET:
        why = (
            "What stops the usage: the pick's IoT usage rises while its median summed revenue "
            f"rises and its usable draws stay at or above {floor}, and stops at whichever comes "
            "first: that floor, the median's peak, or the top of an IoT class's usage list, where "
            "the pick then sits on an upper usage edge, warned; every candidate shares the "
            "terminals' fill, so IoT's own failures may take only the draws between the fill's "
            "share and that floor."
        )
    else:
        why = (
            f"What stops the usage: no candidate reaches {floor}, so the pick is the most usable "
            "candidate, the first on the candidates' front, ties to the higher median, and its "
            "usage is that candidate's; the run warns of it and never lowers a price."
        )
    edges = _usage_edge_clause(pick.usage_edges, chosen)
    return (
        f"{why} This run's pick: minimal-packet IoT x{chosen.choice.minimal_packet_scale:g} and "
        f"data IoT x{chosen.choice.data_iot_scale:g}, usable in {chosen.usable_draws:,} of "
        f"{config.market.draws:,} draws ({pick.basis}){edges}."
    )


def _assumptions(run: ProductCaseRun, headline: MarketOutcome, spreads: Spreads) -> list[str]:
    """The stated assumptions, one line each, every value the run's or a named constant's."""
    config, view = run.config, run.engineering
    pick = run.pick
    if pick is None:
        raise ValueError("a run with no pick has no stated assumptions")
    chosen = next(s for s in run.choices if s.choice.choice_id == pick.choice_id)
    first, last = view.years[0], view.years[-1]
    anchors = DEMAND_ANCHORS
    iot_today = IOT_CUSTOMERS_TODAY * IOT_ARPU_USD_MONTH * MONTHS_PER_YEAR / DOLLARS_PER_MILLION
    data_anchor = (
        DATA_IOT_ANCHOR_CUSTOMERS * DATA_IOT_ANCHOR_ARPU_USD_MONTH * MONTHS_PER_YEAR
    ) / DOLLARS_PER_MILLION
    market = config.market
    prices = config.prices
    last_year = headline.years[-1]
    minimal = next(
        e for e in last_year.classes if e.product_class is ProductClass.MINIMAL_PACKET_IOT
    )
    data = next(e for e in last_year.classes if e.product_class is ProductClass.DATA_IOT)
    if minimal.iot is None or data.iot is None:
        raise ValueError("the headline's IoT classes carry no usage block")
    return [
        "Each class's customers come from the demand curve D = N x k^gamma x (A / p)^epsilon x "
        "v^eta, anchored on Iridium's customers and ARPU today (COMM-617, COMM-618): the small "
        f"terminal {anchors[ProductClass.SMALL_TERMINAL].customers:,.0f} at "
        f"${anchors[ProductClass.SMALL_TERMINAL].arpu_usd_month:g}, the mounted terminal "
        f"{anchors[ProductClass.MOUNTED_TERMINAL].customers:,.0f} at "
        f"${anchors[ProductClass.MOUNTED_TERMINAL].arpu_usd_month:g}, minimal-packet IoT "
        f"{IOT_CUSTOMERS_TODAY:,} at ${IOT_ARPU_USD_MONTH:g} (Iridium's one reported commercial "
        "IoT segment, taken whole).",
        "Data IoT is anchored beside that segment at the investor's proportion (2026-10-04), half "
        f"the count at double the ARPU, {DATA_IOT_ANCHOR_CUSTOMERS:,.0f} at "
        f"${DATA_IOT_ANCHOR_ARPU_USD_MONTH:g} (COMM-726), so the two IoT classes start from twice "
        "Iridium's IoT revenue today, a run rate at today's count and ARPU "
        f"({_money(iot_today + data_anchor)} a year against {_money(iot_today)}).",
        "The network's scale k is the terminals' seats over Iridium's "
        f"{TERMINAL_CUSTOMERS_TODAY:,} terminal customers today, the seats read from the "
        f"engineering artifact: k = {first.network_scale:.1f} in FY{first.year} and "
        f"{last.network_scale:.1f} in FY{last.year}.",
        "The prices are held flat in nominal dollars at the scenario's start prices (the small "
        f"terminal ${prices.small_terminal.start_usd_month:g}, the mounted terminal "
        f"${prices.mounted_terminal.start_usd_month:g}, minimal-packet IoT "
        f"${prices.minimal_packet_iot.start_usd_month:g}, data IoT "
        f"${DATA_IOT_PRICE_MULTIPLE * prices.minimal_packet_iot.start_usd_month:g}); inflation is "
        "not modeled.",
        "The market's three responses are drawn independently and uniformly over their ranges "
        f"(gamma {market.gamma.low:g} to {market.gamma.high:g}, epsilon {market.epsilon.low:g} to "
        f"{market.epsilon.high:g}, eta {market.eta.low:g} to {market.eta.high:g}; "
        f"{market.draws:,} draws, seed {market.seed}), so each class's customers at the central "
        "market are its median over the population of markets and, in the "
        f"{market.draws:,} drawn markets, within sampling error of it.",
        "IoT is uncapped: each IoT class sells every device its demand curve gives, bounded by its "
        "uplink room, its random access and its single-tone time, which the usable test checks; "
        "no IoT count is ever set.",
        _usage_stop_line(run, chosen),
        "Each IoT class's usage and time basis differ from the engineering capacity's: the "
        "engineering artifact counts each class's devices alone at its reference usage, averaged "
        "over the day; the product case sells at the pick's usage by period "
        f"({minimal.iot.messages_per_day:,} messages a day for minimal-packet IoT and "
        f"{data.iot.bursts_per_day:,} bursts a day for data IoT in FY{last_year.year}), so its "
        "devices are never divided by that capacity.",
        "IoT's room rides the phone class's useful beams, the beams lit over inhabited cells: "
        f"{first.phone_useful_beams:,.0f} in FY{first.year} and {last.phone_useful_beams:,.0f} "
        f"in FY{last.year}, read from the engineering artifact. So the room counts no beam over "
        "oceans or empty land, a conservative basis: the beams there are upside the case does not "
        "count. On its beams the room is the whole uplink in its share of the frame after the MAC "
        "efficiency, with the random-access window and the single-tone room; the terminals' own "
        "upload is not subtracted.",
        "The all-draw spreads cover every drawn market, the usable test not applied: in "
        f"{spreads.draws_past_iot_room:,} of the {spreads.draws:,} drawn markets the pick sells "
        "IoT past its uplink, access or single-tone room in some reported year.",
        "People and devices are never added: no total of customers is published; bytes add "
        "across the classes in the GB carried.",
        "Government is left out of revenue.",
        f"The engineering inputs are read from {view.path} ({view.schema_version}, stamp "
        f"{view.version_stamp}) at SHA-256 {view.sha256}; the product case never feeds the "
        "engineering model.",
    ]


QUERY_EXAMPLES: Final[tuple[QueryExample, ...]] = (
    QueryExample(
        name="headline_last_year_revenue_and_margin",
        question_answered="What does the network sell in the last reported year, at what margin?",
        jq_expression=(
            ".headline.years[-1] | {year, revenue_musd: .totals.revenue_musd.value, "
            "margin_pct: .totals.margin_pct.value}"
        ),
        expected_shape="{year: int, revenue_musd: number, margin_pct: number}",
        important_paths=[
            "headline.years[].totals.revenue_musd",
            "headline.years[].totals.margin_pct",
        ],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
    QueryExample(
        name="classes_side_by_side_last_year",
        question_answered="Each class's customers and revenue in the last reported year?",
        jq_expression=(
            "[.headline.years[-1].classes[] | {product_class, customers: .customers.value, "
            "revenue_musd: .revenue_musd.value}]"
        ),
        expected_shape="[4 objects: {product_class: string, customers: int, revenue_musd: number}]",
        important_paths=[
            "headline.years[].classes[].customers",
            "headline.years[].classes[].revenue_musd",
        ],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
    QueryExample(
        name="pick_and_basis",
        question_answered="Which choice is the pick, on what basis, at which usage edges?",
        jq_expression=".pick | {choice_id, basis, usage_edges}",
        expected_shape="{choice_id: int, basis: string, usage_edges: [string]}",
        important_paths=["pick.choice_id", "pick.basis", "pick.usage_edges"],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
    QueryExample(
        name="pick_usable_share",
        question_answered="In what share of the drawn markets is the pick usable?",
        jq_expression=(
            ".pick.choice_id as $id | .choices[] | select(.choice_id == $id) | "
            "{usable_draws, usable_share}"
        ),
        expected_shape="{usable_draws: int, usable_share: number}",
        important_paths=["choices[].usable_draws", "choices[].usable_share"],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
    QueryExample(
        name="spreads_last_year",
        question_answered="The last reported year's spreads, over the usable and all draws?",
        jq_expression=".spreads.years[-1].fields[] | {field, usable_draws, all_draws}",
        expected_shape=(
            "one object a spread field: {field: string, usable_draws: {...}, all_draws: {...}}"
        ),
        important_paths=["spreads.years[].fields[]"],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
    QueryExample(
        name="engineering_artifact_read",
        question_answered="Which engineering artifact did the run read, at what hash?",
        jq_expression=(
            ".metadata.engineering_artifact | {path, schema_version, version_stamp, sha256}"
        ),
        expected_shape=(
            "{path: string, schema_version: string, version_stamp: string, sha256: string}"
        ),
        important_paths=["metadata.engineering_artifact"],
        applies_to=QueryAppliesTo.PRODUCT_CASE,
    ),
)
"""The worked ``jq`` queries the artifact carries (each run by a test)."""


# ---------------------------------------------------------------------------
# The artifact
# ---------------------------------------------------------------------------


def build_product_case_artifact(
    run: ProductCaseRun, *, source_scenario_path: str, version_stamp: str
) -> ProductCaseArtifact:
    """Map a run in state ``picked`` to the ``product-case-v1`` artifact.

    The data dictionary is built by the shared walker on the finished model, then set.

    Args:
        run: The run (:func:`~product_case.engine.run_product_case`).
        source_scenario_path: The scenario's path for the metadata and the scenario cells.
        version_stamp: The stamp.

    Returns:
        The artifact.

    Raises:
        NoUsableChoiceError: If the run has no pick (state ``no_usable_choice``).
        pydantic.ValidationError: If a block would hold a number that is not finite.
    """
    pick, headline, spreads = run.pick, run.headline, run.spreads
    if run.state is not RunState.PICKED or pick is None or headline is None or spreads is None:
        raise NoUsableChoiceError("a run in state no_usable_choice has no artifact to publish")
    view = run.engineering
    inputs = _inputs_block(run, source_scenario_path)
    statuses = [
        cell.source_status
        for block in (inputs.scenario, inputs.constants, inputs.engineering)
        for cell in block.values()
    ]
    artifact = ProductCaseArtifact(
        metadata=MetadataBlock(
            model=MODEL_NAME,
            schema_version=PRODUCT_CASE_SCHEMA_VERSION,
            scenario_name=run.config.scenario_name,
            source_scenario_path=source_scenario_path,
            version_stamp=version_stamp,
            engineering_artifact=EngineeringArtifactBlock(
                path=view.path,
                schema_version=view.schema_version,
                version_stamp=view.version_stamp,
                sha256=view.sha256,
            ),
        ),
        inputs=inputs,
        network=NetworkBlock(
            small_terminal_share=view.small_terminal_share,
            years=[
                NetworkYearBlock(
                    year=year.year,
                    seats_small_terminal=year.seats_small_terminal,
                    seats_mounted_terminal=year.seats_mounted_terminal,
                    network_scale=year.network_scale,
                )
                for year in view.years
            ],
        ),
        choices=_choice_blocks(run),
        fronts=FrontsBlock(
            all_prices=list(run.fronts.all_prices),
            at_start_prices=list(run.fronts.at_start_prices),
        ),
        pick=PickBlock(
            choice_id=pick.choice_id,
            basis=pick.basis,
            usage_edges=list(pick.usage_edges),
            dominated_in_context_by=list(pick.dominated_in_context_by),
        ),
        headline=_headline_block(headline),
        spreads=_spreads_block(spreads),
        meta=MetaBlock(
            formulas=list(FORMULA_CATALOG.values()),
            validation_results=list(run.validation_results),
            data_dictionary=[],
            query_examples=list(QUERY_EXAMPLES),
            source_status_summary=summarize_source_statuses(statuses),
        ),
        assumptions=_assumptions(run, headline, spreads),
    )
    dictionary = build_data_dictionary(artifact)
    return artifact.model_copy(
        update={"meta": artifact.meta.model_copy(update={"data_dictionary": dictionary})}
    )


# ---------------------------------------------------------------------------
# The command
# ---------------------------------------------------------------------------


def _refuse_reserved_default(checkout: SourceCheckout, scenario: Path, output: Path) -> None:
    """Refuse the default artifact's path written from any scenario but the shipped one."""
    default = checkout.anchored(DEFAULT_ARTIFACT_PATH)
    shipped = checkout.anchored(SHIPPED_SCENARIO_PATH)
    if output.resolve() == default.resolve() and scenario.resolve() != shipped.resolve():
        raise ReservedPathError(
            f"{DEFAULT_ARTIFACT_PATH} is written only from {SHIPPED_SCENARIO_PATH}, not from "
            f"{checkout.repo_relative(scenario)}: a side run writes to a path of its own, outside "
            "the tracked folders"
        )


def _read_engineering_bytes(path: Path) -> bytes:
    """The engineering artifact's bytes, read once."""
    try:
        return path.read_bytes()
    except OSError as error:
        raise ModelFileError(
            path, f"cannot read the engineering artifact ({error.strerror or error})"
        ) from error


def export_product_case_json(
    scenario_path: str | Path, output_path: str | Path, version_stamp: str | None = None
) -> Path:
    """Run a product-case scenario on its engineering artifact and write the artifact.

    Args:
        scenario_path: The scenario YAML (against the working directory).
        output_path: Where to write (relative = repository-root anchored).
        version_stamp: The stamp; today's ISO date by default.

    Returns:
        The path written: the output anchored at the root when relative, not resolved.

    Raises:
        common.file_io.ModelFileError: If the module is not in a source checkout, the scenario
            or the engineering artifact cannot be read, or the write fails.
        ValueError: An invalid scenario; the reserved default path from another scenario; an
            engineering artifact the view refuses; a usage the offers refuse; a run with no usable
            choice; an invariant broken or a number not finite.
    """
    checkout = locate_source_checkout(__file__)
    scenario = Path(scenario_path)
    config = load_product_case_config(scenario)
    out = checkout.anchored(output_path)
    _refuse_reserved_default(checkout, scenario, out)
    data = _read_engineering_bytes(checkout.anchored(config.engineering_artifact_path))
    view = engineering_view_from_bytes(
        data, path=config.engineering_artifact_path, reported_years=config.reported_years
    )
    run = run_product_case(config, view)
    if run.state is RunState.NO_USABLE_CHOICE:
        raise NoUsableChoiceError(
            f"no choice at the start prices is usable in any of the {config.market.draws:,} draws; "
            f"the test their draws fail most is {most_failed_test(run)}"
        )
    stamp = version_stamp if version_stamp is not None else date.today().isoformat()
    artifact = build_product_case_artifact(
        run, source_scenario_path=checkout.repo_relative(scenario), version_stamp=stamp
    )
    write_files_with_rollback([artifact_write(out, artifact)])
    for warning in run.warnings:
        logger.warning("%s: %s", warning.validation_id, warning.observed_result)
    logger.info("promoted the product case to %s", out)
    return out


def _build_parser() -> CliArgumentParser:
    """The command's parser (usage errors exit with EXIT_USAGE)."""
    parser = CliArgumentParser(
        prog="python -m product_case.json_output",
        description=(
            "Run the product case from a scenario YAML on the engineering artifact it names and "
            "write its promoted JSON (relative output paths anchor to the repository root)."
        ),
    )
    parser.add_argument("scenario", help="Scenario YAML, e.g. scenarios/product_case.yaml.")
    parser.add_argument(
        "output", help="Output JSON, e.g. communications/models/product_case/default.json."
    )
    parser.add_argument(
        "--version-stamp", default=None, help="Provenance stamp; defaults to today's ISO date."
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point; returns the exit status.

    Args:
        argv: The arguments (defaults to ``sys.argv[1:]``).

    Returns:
        :data:`~common.cli.EXIT_OK`, or :data:`~common.cli.EXIT_ERROR` after one ``ERROR:`` line
        for an expected failure (every refusal the module docstring lists); usage errors exit
        through :class:`~common.cli.CliArgumentParser` with status 2.
    """
    configure_cli_logging()
    args = _build_parser().parse_args(None if argv is None else list(argv))
    scenario = Path(args.scenario)
    try:
        export_product_case_json(scenario, args.output, args.version_stamp)
    except (ModelFileError, ValueError, ArithmeticError) as error:
        logger.error("could not promote %s: %s", scenario, describe_failure(error, scenario))
        return EXIT_ERROR
    return EXIT_OK


__all__ = [
    "DEFAULT_ARTIFACT_PATH",
    "MODEL_NAME",
    "QUERY_EXAMPLES",
    "SHIPPED_SCENARIO_PATH",
    "NoUsableChoiceError",
    "ProductCaseArtifact",
    "ReservedPathError",
    "build_product_case_artifact",
    "export_product_case_json",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
