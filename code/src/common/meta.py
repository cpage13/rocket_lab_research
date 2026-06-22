"""Shared cold-reader contract types used by both ventures' meta blocks.

The validation-check, data-dictionary, query-example, and formula-definition
models, plus their enums, used by both ventures' `meta` blocks.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from common.provenance import FieldPath


class FieldKind(StrEnum):
    """The semantic kind of one leaf field in the output JSON.

    Used in the ``data_dictionary`` so a reader knows what a number *is*:
    a dial they set (``INPUT``), a model constant (``CONSTANT``), a level
    prevailing in a year (``STATE``), a per-year flow (``FLOW``), a running
    total (``STOCK``), or a function of other fields (``DERIVED``).
    """

    INPUT = "input"
    CONSTANT = "constant"
    STATE = "state"
    FLOW = "flow"
    STOCK = "stock"
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
    BOTH = "both"


class SourceStatusSummary(BaseModel):
    """Known-shape count of input assumptions by source-status value."""

    model_config = ConfigDict(frozen=True)

    certified: int = Field(..., description="Certified source-backed input count.")
    sourced_estimate: int = Field(..., description="Sourced-estimate input count.")
    derived_estimate: int = Field(..., description="Derived-estimate input count.")
    projection: int = Field(..., description="Projection input count.")
    extrapolation: int = Field(..., description="Extrapolation input count.")
    scenario: int = Field(..., description="Scenario-authored input count.")
    placeholder: int = Field(
        ..., description="Placeholder input count; must be zero in promoted artifacts."
    )
    stale: int = Field(
        ..., description="Stale-source input count; must be zero in promoted artifacts."
    )


class ValidationCheck(BaseModel):
    """One engine-computed sanity check on the run.

    The cycle-1 validation type, reused verbatim for V1–V17. The
    ``meta.validation.rules`` block lets a reader run
    ``jq '.meta.validation.rules[] | select(.pass_check == false)'`` and
    see every failed check without reading the engine.
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
            "All V-rule results in declaration order (V1..V17). Run "
            "`jq '.meta.validation.rules[] | select(.pass_check==false)'` "
            "to find any failure."
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
    source_class: str = Field(
        ...,
        description=("Provenance class of the field: INPUT / CONSTANT / DERIVED."),
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

    @property
    def jq(self) -> str:
        """Return the jq expression for existing test and renderer helpers."""
        return self.jq_expression


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


__all__ = [
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
]
