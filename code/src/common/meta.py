"""Shared cold-reader contract for the artifacts' meta blocks: its types and its walker.

The validation-check, data-dictionary, query-example, and formula-definition
models, their enums, and the source-status counter
(:func:`summarize_source_statuses`), used by the data-center space and ground
artifacts' ``meta`` blocks.

The one data-dictionary walker, :func:`build_data_dictionary`, with its unit
constants: every artifact that meets ADR 002's contract builds its
``meta.data_dictionary`` with it, from the artifact's typed model (a cell's
unit read from the cells themselves, any other leaf's from its field's
declaration).
"""

from __future__ import annotations

import inspect
import logging
import types
from collections import Counter
from collections.abc import Iterable
from enum import Enum, StrEnum
from typing import Any, Final, Union, get_args, get_origin  # typing-acceptable: introspection

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo

from common.input_manifest import InputCell, SourceStatus
from common.provenance import FieldPath, ProvenanceCell

logger = logging.getLogger(__name__)

COUNT_UNIT: Final[str] = "count"
"""Declared data-dictionary unit for a whole-number count field."""


class FieldKind(StrEnum):
    """The provenance class of one leaf field, published as a data-dictionary entry's
    ``source_class``.

    The field's position in the artifact decides it: an input the scenario
    sets (``INPUT``, under ``inputs``), a run-identity constant (``CONSTANT``,
    under ``metadata``), or a value the model computes (``DERIVED``, everything
    else).
    """

    INPUT = "input"
    CONSTANT = "constant"
    DERIVED = "derived"


class Severity(StrEnum):
    """Severity tier for a :class:`ValidationCheck`.

    ``CRITICAL``: model is invalid; do not quote.
    ``MAJOR``: a substantive defect that affects the headline.
    ``MINOR``: a soft check (range warning, secondary metric).
    """

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class ValidationSeverity(StrEnum):
    """Public validation severity emitted in ``meta.validation_results``."""

    OK = "pass"
    WARN = "warn"
    FAIL = "fail"


class QueryAppliesTo(StrEnum):
    """Which public model family a query example applies to."""

    SPACE = "space"
    GROUND = "ground"
    PRODUCT_CASE = "product_case"  # the product case's artifact (ADR 012)


class SourceStatusSummary(BaseModel):
    """Known-shape count of input assumptions by source-status value."""

    model_config = ConfigDict(frozen=True)

    certified: int = Field(
        ...,
        description="Certified source-backed input count.",
        json_schema_extra={"unit": COUNT_UNIT},
    )
    sourced_estimate: int = Field(
        ..., description="Sourced-estimate input count.", json_schema_extra={"unit": COUNT_UNIT}
    )
    derived_estimate: int = Field(
        ..., description="Derived-estimate input count.", json_schema_extra={"unit": COUNT_UNIT}
    )
    projection: int = Field(
        ..., description="Projection input count.", json_schema_extra={"unit": COUNT_UNIT}
    )
    extrapolation: int = Field(
        ..., description="Extrapolation input count.", json_schema_extra={"unit": COUNT_UNIT}
    )
    scenario: int = Field(
        ..., description="Scenario-authored input count.", json_schema_extra={"unit": COUNT_UNIT}
    )
    placeholder: int = Field(
        ...,
        description="Placeholder input count; must be zero in promoted artifacts.",
        json_schema_extra={"unit": COUNT_UNIT},
    )
    stale: int = Field(
        ...,
        description="Stale-source input count; must be zero in promoted artifacts.",
        json_schema_extra={"unit": COUNT_UNIT},
    )


def summarize_source_statuses(statuses: Iterable[SourceStatus]) -> SourceStatusSummary:
    """Count input assumptions by source status.

    The one counter behind every artifact's ``meta.source_status_summary``
    (the space model and the ground reference).

    Args:
        statuses: The source status of every input cell to count.

    Returns:
        The eight-way count; statuses absent from the input count zero.
    """
    counts = Counter(statuses)
    return SourceStatusSummary(
        certified=counts[SourceStatus.CERTIFIED],
        sourced_estimate=counts[SourceStatus.SOURCED_ESTIMATE],
        derived_estimate=counts[SourceStatus.DERIVED_ESTIMATE],
        projection=counts[SourceStatus.PROJECTION],
        extrapolation=counts[SourceStatus.EXTRAPOLATION],
        scenario=counts[SourceStatus.SCENARIO],
        placeholder=counts[SourceStatus.PLACEHOLDER],
        stale=counts[SourceStatus.STALE],
    )


class ValidationCheck(BaseModel):
    """One engine-computed sanity check on the run.

    The cycle-1 validation type, reused verbatim for every wired V-rule. The
    ``meta.validation.rules`` block lists the V-rules alone; the complete
    public verdict list (every rule, the model invariants, and the default
    guards) is ``meta.validation_results``, where
    ``jq '.meta.validation_results[] | select(.severity != "pass")'`` shows
    every warning and failure.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        ...,
        description="Short identifier for the check (e.g. 'mass_util_in_range').",
    )
    what_it_tests: str = Field(
        ...,
        description="One-sentence statement of what the check ensures.",
    )
    expected: str = Field(
        ...,
        description=("Human-readable expected value or range, e.g. 'in [0.85, 1.0]' or '> 0'."),
    )
    computed: str = Field(
        ...,
        description="Human-readable computed value as a formatted string.",
    )
    pass_check: bool = Field(
        ...,
        description="Whether the check passed (computed satisfies expected).",
    )
    severity: Severity = Field(
        ...,
        description="Severity tier if the check failed (CRITICAL / MAJOR / MINOR).",
    )


class ValidationReport(BaseModel):
    """The ``meta.validation`` block: the full V-rule result list.

    A thin container so the validation block has a stable ``rules`` key
    a reader can address (``.meta.validation.rules[]``).
    """

    model_config = ConfigDict(frozen=True)

    rules: list[ValidationCheck] = Field(
        ...,
        description=(
            "All V-rule results in declaration order (16 rules: V1-V10 and "
            "V12-V17, V11 retired). The complete verdict list, rules plus the "
            "model invariants and default guards, is meta.validation_results: "
            "run `jq '.meta.validation_results[] | select(.severity != \"pass\")'` "
            "to find every warning or failure."
        ),
    )


class DataDictEntry(BaseModel):
    """One ``data_dictionary`` entry: the meaning of a single output field.

    Built by the ``build_data_dictionary`` helper from typed-model
    field-info introspection.
    """

    model_config = ConfigDict(frozen=True)

    path: FieldPath = Field(
        ...,
        description="Public JSON path this dictionary entry describes.",
    )
    description: str = Field(
        ...,
        description="One-sentence plain-English description of the field.",
    )
    unit: str = Field(
        ...,
        description=(
            "Unit string, e.g. 'MUSD', 'kW', 't', 'count', 'percent', or '-' for a unitless value."
        ),
    )
    type: str = Field(
        ...,
        description="The leaf value's wire type (e.g. 'number', 'integer', 'string').",
    )
    source_class: FieldKind = Field(
        ...,
        description="Provenance class of the field: input, constant, or derived.",
    )


class QueryExample(BaseModel):
    """One worked ``jq`` query in the ``meta.query_examples`` block.

    The ``query_examples`` block is the cold-reader contract: a cold agent
    runs these ``jq`` expressions to answer common questions without
    reverse-engineering the schema.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Stable key, e.g. 'headline_2036_revenue_central'.")
    question_answered: str = Field(..., description="Plain-language question this query answers.")
    jq_expression: str = Field(..., description="The exact jq expression.")
    expected_shape: str = Field(..., description="What the query result looks like.")
    important_paths: list[str] = Field(..., description="Important JSON paths touched.")
    applies_to: QueryAppliesTo = Field(..., description="Model family this query applies to.")


class FormulaDefinition(BaseModel):
    """One public formula-definition metadata entry."""

    model_config = ConfigDict(frozen=True)

    formula_id: str = Field(..., description="Stable formula identifier.")
    formula_text: str = Field(..., description="Human-readable formula text.")
    description: str = Field(..., description="What this formula computes.")
    input_path_pattern: str = Field(..., description="Input-path pattern this formula consumes.")
    output_path_pattern: str = Field(..., description="Output-path pattern this formula emits.")
    unit_behavior: str = Field(..., description="How units flow through the formula.")
    scenario_notes: str | None = Field(default=None, description="Scenario caveats.")


class ValidationResult(BaseModel):
    """One public validation-result metadata entry."""

    model_config = ConfigDict(frozen=True)

    validation_id: str = Field(..., description="Stable validation identifier.")
    severity: ValidationSeverity = Field(..., description="pass, warn, or fail.")
    what_tested: str = Field(..., description="Plain-language test description.")
    expected_condition: str = Field(..., description="Expected condition.")
    observed_result: str = Field(..., description="Observed result.")
    related_json_paths: list[str] = Field(..., description="Related JSON paths.")
    remediation_hint: str | None = Field(default=None, description="Suggested remediation.")


# ---------------------------------------------------------------------------
# Units: each cell's own unit, or the unit declared once on a non-cell field.
# ---------------------------------------------------------------------------

UNIT_JSON_SCHEMA_KEY: Final[str] = "unit"
"""Key under a non-cell field's ``json_schema_extra`` that declares its unit."""

UNITLESS: Final[str] = "-"
"""Data-dictionary unit for a unitless number, flag, or enum (and a cell whose
unit is null)."""

TEXT_UNIT: Final[str] = ""
"""Data-dictionary unit for free text."""

PER_CELL_UNIT: Final[str] = "per cell (read each cell's unit)"
"""Data-dictionary unit for a container whose cells carry different units
(the flat ``inputs.assumption_index``)."""


def _cell_unit(cells: list[BaseModel]) -> str:
    """Return the data-dictionary unit for the cells found at one path.

    The unit is the cells' own declared ``unit`` (a null unit reads
    :data:`UNITLESS`). When the cells at one path disagree, the entry says
    so (:data:`PER_CELL_UNIT`) rather than picking one.

    Args:
        cells: Every :class:`ProvenanceCell` or :class:`InputCell` at the
            path across the walked output.

    Returns:
        The shared unit, :data:`PER_CELL_UNIT`, or :data:`UNITLESS` when the
        output holds no cell at the path.
    """
    units = {
        UNITLESS if unit is None else unit
        for unit in (c.unit for c in cells if isinstance(c, (ProvenanceCell, InputCell)))
    }
    if not units:
        return UNITLESS
    if len(units) == 1:
        return units.pop()
    return PER_CELL_UNIT


def _declared_unit(info: FieldInfo) -> str | None:
    """Return the unit a non-cell field declares in its ``json_schema_extra``."""
    extra = info.json_schema_extra
    if isinstance(extra, dict):
        unit = extra.get(UNIT_JSON_SCHEMA_KEY)
        if isinstance(unit, str):
            return unit
    return None


# ---------------------------------------------------------------------------
# Type + provenance-class inference for a leaf field.
# ---------------------------------------------------------------------------


def _wire_type(leaf_type: Any) -> str:
    """Return the JSON wire type for a leaf Python type.

    Args:
        leaf_type: The leaf's Python type.

    Returns:
        One of ``'integer'``, ``'number'``, ``'boolean'``, ``'string'``.
    """
    if leaf_type is bool:
        return "boolean"
    if leaf_type is int:
        return "integer"
    if leaf_type is float:
        return "number"
    return "string"


def _source_class_for(path: str) -> FieldKind:
    """Provenance class of one leaf path, from its top-level block.

    The ``data_dictionary`` tags every field with a :class:`FieldKind`:
    fields under ``inputs.*`` are scenario-set inputs (``input``);
    ``metadata`` fields are run-identity constants (``constant``); everything
    else (``physical``, ``business``, ``meta``, and the ground reference's
    computed blocks) is model-derived (``derived``).

    Args:
        path: The leaf's dotted field path.

    Returns:
        The field's :class:`FieldKind`.
    """
    head = path.split(".", 1)[0]
    head = head[:-2] if head.endswith("[]") else head
    if head == "inputs":
        return FieldKind.INPUT
    if head == "metadata":
        return FieldKind.CONSTANT
    return FieldKind.DERIVED


# ---------------------------------------------------------------------------
# Walking a Pydantic output instance.
# ---------------------------------------------------------------------------


def _is_basemodel(t: Any) -> bool:
    """True if ``t`` is a Pydantic BaseModel subclass."""
    return inspect.isclass(t) and issubclass(t, BaseModel)


def _is_cell(t: Any) -> bool:
    """True if ``t`` is a public cell type.

    The data-dictionary walker treats cells as leaves: they are public
    fields, not nested records to recurse into.
    """
    return inspect.isclass(t) and issubclass(t, (ProvenanceCell, InputCell))


def _unwrap_optional(t: Any) -> Any:
    """If ``t`` is ``X | None`` / ``Optional[X]``, return ``X`` (else ``t``)."""
    origin = get_origin(t)
    if origin is Union or origin is types.UnionType:
        args = [a for a in get_args(t) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return t


def _element_type(t: Any) -> Any | None:
    """If ``t`` is a list / tuple / set, return the element type (else None).

    For ``dict[K, V]`` returns the value type (the model keys data by name).
    """
    origin = get_origin(t)
    if origin in (list, tuple, set, frozenset, Iterable):
        args = get_args(t)
        if args:
            return _unwrap_optional(args[0])
    if origin is dict:
        args = get_args(t)
        if len(args) >= 2:
            return _unwrap_optional(args[1])
    return None


def _container_items(values: list[Any]) -> list[BaseModel]:
    """Flatten the list or dict values found at one container path."""
    items: list[BaseModel] = []
    for value in values:
        members = value.values() if isinstance(value, dict) else value
        items.extend(item for item in members if isinstance(item, BaseModel))
    return items


def _walk(
    cls: type[BaseModel],
    prefix: str,
    instances: list[BaseModel],
    out: dict[FieldPath, DataDictEntry],
) -> None:
    """Recurse into a model class and its instances, one DataDictEntry per leaf.

    Container fields (lists / dicts of models or cells) flatten with a ``[]``
    suffix on the container's name. A cell is a leaf whose unit is read from
    the cells themselves (:func:`_cell_unit`) across every instance at the
    path; any other leaf takes the unit its field declares
    (:func:`_declared_unit`), else :data:`UNITLESS` for numbers, flags, and
    enums and :data:`TEXT_UNIT` for text.

    Args:
        cls: The Pydantic model class to walk.
        prefix: The dotted path prefix accumulated so far.
        instances: Every instance of ``cls`` at ``prefix`` in the output.
        out: The output map, mutated in place.
    """
    for name, info in cls.model_fields.items():
        path = f"{prefix}.{name}" if prefix else name
        ann = _unwrap_optional(info.annotation)
        values = [getattr(instance, name) for instance in instances]
        present = [value for value in values if value is not None]
        description = info.description or ""
        source_class = _source_class_for(path)

        if _is_cell(ann):
            out[path] = DataDictEntry(
                path=path,
                description=description,
                unit=_cell_unit(present),
                type="cell",
                source_class=source_class,
            )
            continue

        if _is_basemodel(ann):
            _walk(ann, path, present, out)
            continue

        elem = _element_type(ann)
        if elem is not None and _is_cell(elem):
            out[f"{path}[]"] = DataDictEntry(
                path=f"{path}[]",
                description=description,
                unit=_cell_unit(_container_items(present)),
                type="cell",
                source_class=source_class,
            )
            continue
        if elem is not None and _is_basemodel(elem):
            _walk(elem, f"{path}[]", _container_items(present), out)
            continue

        leaf_type = elem if elem is not None else ann
        declared = _declared_unit(info)
        is_enum = inspect.isclass(leaf_type) and issubclass(leaf_type, Enum)
        if declared is not None:
            unit = declared
        elif leaf_type in (bool, int, float) or is_enum:
            unit = UNITLESS
        else:
            unit = TEXT_UNIT
        out[path] = DataDictEntry(
            path=path,
            description=description,
            unit=unit,
            type=_wire_type(leaf_type),
            source_class=source_class,
        )


# ---------------------------------------------------------------------------
# Data dictionary
# ---------------------------------------------------------------------------


def build_data_dictionary(output: BaseModel) -> list[DataDictEntry]:
    """Walk a built output and generate its data dictionary.

    The one walker every artifact that meets ADR 002's contract builds its
    ``meta.data_dictionary`` with. Returns a
    path-sorted list of entries: leaf fields produce one entry; container
    fields (lists / dicts of models or cells) flatten with a ``[]`` suffix.
    Per-leaf ``description`` is the Pydantic ``Field`` description; a cell's
    ``unit`` is the unit its cells declare in the output (so the dictionary
    and the cells cannot disagree), a non-cell leaf's unit is the unit its
    field declares; ``type`` is the wire type; ``source_class`` follows the
    path position.

    Args:
        output: A built output model (its cells supply the units).

    Returns:
        Data dictionary entries covering every leaf in the tree.
    """
    out: dict[FieldPath, DataDictEntry] = {}
    _walk(type(output), "", [output], out)
    return [out[path] for path in sorted(out)]


__all__ = [
    "COUNT_UNIT",
    "PER_CELL_UNIT",
    "TEXT_UNIT",
    "UNITLESS",
    "UNIT_JSON_SCHEMA_KEY",
    "DataDictEntry",
    "FieldKind",
    "FormulaDefinition",
    "QueryAppliesTo",
    "QueryExample",
    "Severity",
    "SourceStatusSummary",
    "ValidationCheck",
    "ValidationReport",
    "ValidationResult",
    "ValidationSeverity",
    "build_data_dictionary",
    "summarize_source_statuses",
]
