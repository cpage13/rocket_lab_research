"""Shared input-cell vocabulary and cell builders.

The source-linked ``InputCell``, its enums, and the generic cell builders,
used by the data-center space model and the ground reference.

:func:`_spec_cell` is the one entry point for a scenario-valued input: it
attaches the input's source metadata (claim ID, status, rationale) only when
the run's value equals the default value that metadata describes. A value the
scenario changed is published as a scenario override
(:attr:`AssumptionRole.SCENARIO_OVERRIDE`, status ``scenario``) whose only
source is the scenario YAML, so an overridden value never inherits a claim
written for the default.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import NewType

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

InputPath = NewType("InputPath", str)
"""Stable public JSON path for one input assumption."""

type InputScalar = int | float | str | bool
type InputValue = InputScalar | list[InputScalar]

type ConfigFieldName = str
"""The name of one field of a config block (e.g. ``cadence_ceiling``), the key of
a block's per-field source-metadata table."""


class AssumptionRole(StrEnum):
    """Public role of one modeled input assumption.

    ``SCENARIO_OVERRIDE`` marks a value the scenario changed from the default:
    the default's claim, rationale, and role do not apply to it.
    """

    DEFAULT = "default"
    SENSITIVITY = "sensitivity"
    VALIDATION_ONLY = "validation_only"
    DERIVED_INPUT = "derived_input"
    SCENARIO_OVERRIDE = "scenario_override"


class SourceStatus(StrEnum):
    """Source-status taxonomy shared by public docs and model JSON."""

    CERTIFIED = "certified"
    SOURCED_ESTIMATE = "sourced_estimate"
    DERIVED_ESTIMATE = "derived_estimate"
    PROJECTION = "projection"
    EXTRAPOLATION = "extrapolation"
    SCENARIO = "scenario"
    PLACEHOLDER = "placeholder"
    STALE = "stale"


class SourceRefType(StrEnum):
    """Kind of public source reference attached to an input cell."""

    SOURCE_INDEX = "source_index"
    RESEARCH_DOC = "research_doc"
    MODEL_DERIVATION = "model_derivation"


class SourceRef(BaseModel):
    """One durable public source or derivation reference for an input."""

    model_config = ConfigDict(frozen=True)

    ref_type: SourceRefType = Field(..., description="Kind of source reference.")
    ref: str = Field(..., description="Durable document path, claim ID, or derivation path.")
    claim_id: str | None = Field(default=None, description="SOURCE_INDEX claim ID when relevant.")
    note: str | None = Field(default=None, description="What this reference supports.")


class InputCell(BaseModel):
    """One public input assumption leaf in the space-model JSON."""

    model_config = ConfigDict(frozen=True)

    path: str = Field(..., description="Stable public JSON path for this input.")
    label: str = Field(..., description="Short human-readable input label.")
    value: InputValue = Field(..., description="Input value as serialized JSON.")
    unit: str | None = Field(default=None, description="Unit string, or null for unitless values.")
    description: str = Field(..., description="Plain-language meaning of the input.")
    assumption_role: AssumptionRole = Field(..., description="How the model uses this input.")
    source_status: SourceStatus = Field(..., description="Evidence classification for this input.")
    source_refs: list[SourceRef] = Field(..., description="Public source references.")
    rationale: str = Field(..., description="Why this default is used.")
    notes: str | None = Field(default=None, description="Caveats or sensitivity guidance.")


@dataclass(frozen=True)
class CellSpec:
    """Source metadata describing one input's default value.

    Attributes:
        label: Short human-readable input label.
        unit: Unit string, or ``None`` for a unitless value.
        role: How the model uses the input.
        source_status: Evidence classification of the default value.
        claim_id: SOURCE_INDEX claim supporting the default value.
        source_note: What the claim supports.
        rationale: Why the default is used.
        notes: Caveats that hold for any value of the input.
        research_path: Optional research note backing the claim, cited
            beside the SOURCE_INDEX entry.
        research_note: What the research note supports.
    """

    label: str
    unit: str | None
    role: AssumptionRole
    source_status: SourceStatus
    claim_id: str
    source_note: str
    rationale: str
    notes: str | None = None
    research_path: str | None = None
    research_note: str | None = None


def _source_index_ref(claim_id: str, note: str) -> SourceRef:
    """Build a SOURCE_INDEX reference for an input cell."""
    return SourceRef(
        ref_type=SourceRefType.SOURCE_INDEX,
        ref=f"research/SOURCE_INDEX.md#{claim_id}",
        claim_id=claim_id,
        note=note,
    )


def _research_ref(path: str, note: str | None, claim_id: str | None = None) -> SourceRef:
    """Build a research-document reference for an input cell."""
    return SourceRef(ref_type=SourceRefType.RESEARCH_DOC, ref=path, claim_id=claim_id, note=note)


def _field_description(model_cls: type[BaseModel], field_name: str) -> str:
    """Return the Pydantic field description for a config field."""
    description = model_cls.model_fields[field_name].description
    if description is None:
        return f"Scenario field {field_name}."
    return description


def _cell(path: str, value: InputValue, description: str, spec: CellSpec) -> InputCell:
    """Construct one source-linked input cell from its default-value metadata.

    The cell cites ``spec``'s SOURCE_INDEX claim and, when ``spec`` names
    one, the research note behind it.
    """
    refs = [_source_index_ref(spec.claim_id, spec.source_note)]
    if spec.research_path is not None:
        refs.append(_research_ref(spec.research_path, spec.research_note, spec.claim_id))
    return InputCell(
        path=path,
        label=spec.label,
        value=value,
        unit=spec.unit,
        description=description,
        assumption_role=spec.role,
        source_status=spec.source_status,
        source_refs=refs,
        rationale=spec.rationale,
        notes=spec.notes,
    )


def _scenario_ref(path: str) -> SourceRef:
    """Build the source-scenario reference used by scenario-level cells."""
    return SourceRef(
        ref_type=SourceRefType.RESEARCH_DOC,
        ref=path,
        claim_id=None,
        note="Scenario YAML value used for this model run.",
    )


def _with_scenario_ref(cell: InputCell, scenario_path: str) -> InputCell:
    """Attach the scenario YAML path alongside the claim-ledger reference."""
    return cell.model_copy(
        update={"source_refs": [*cell.source_refs, _scenario_ref(scenario_path)]}
    )


def _override_cell(
    path: str,
    value: InputValue,
    default_value: InputValue | None,
    description: str,
    spec: CellSpec,
    scenario_path: str,
) -> InputCell:
    """Construct the input cell for a value the scenario changed from the default.

    The cell keeps the input's label, unit, description, and caveat notes but
    none of the default's source metadata: its role is
    :attr:`AssumptionRole.SCENARIO_OVERRIDE`, its status is
    :attr:`SourceStatus.SCENARIO`, and its only source is the scenario YAML.

    Args:
        path: Stable public JSON path of the input.
        value: The scenario's value.
        default_value: The default value at this path, or ``None`` when the
            default has no value there (for example an R anchor year the
            default band does not carry).
        description: Plain-language meaning of the input.
        spec: The default's cell metadata (only its label, unit, and notes
            carry over).
        scenario_path: Repository-relative scenario YAML path.

    Returns:
        A frozen scenario-override :class:`InputCell`.
    """
    default_text = (
        "the default has no value at this path"
        if default_value is None
        else f"the default is {default_value!r}"
    )
    return InputCell(
        path=path,
        label=spec.label,
        value=value,
        unit=spec.unit,
        description=description,
        assumption_role=AssumptionRole.SCENARIO_OVERRIDE,
        source_status=SourceStatus.SCENARIO,
        source_refs=[_scenario_ref(scenario_path)],
        rationale=(
            f"Scenario override: this run sets {value!r} ({default_text}). The "
            "default's source claim and rationale do not cover the overridden "
            "value; the scenario YAML is its only source."
        ),
        notes=spec.notes,
    )


def _spec_cell(
    path: str,
    value: InputValue,
    default_value: InputValue | None,
    description: str,
    spec: CellSpec,
    scenario_path: str,
) -> InputCell:
    """Construct a scenario-valued input cell, marking a changed value as an override.

    When ``value`` equals ``default_value`` the cell carries ``spec``'s claim,
    status, role, and rationale plus the scenario YAML reference. Otherwise it
    is a scenario override (:func:`_override_cell`).

    Args:
        path: Stable public JSON path of the input.
        value: The scenario's value.
        default_value: The default value at this path, or ``None`` when the
            default has none.
        description: Plain-language meaning of the input.
        spec: Source metadata describing the default value.
        scenario_path: Repository-relative scenario YAML path.

    Returns:
        A frozen :class:`InputCell`.
    """
    if default_value is not None and value == default_value:
        return _with_scenario_ref(_cell(path, value, description, spec), scenario_path)
    return _override_cell(path, value, default_value, description, spec, scenario_path)


__all__ = [
    "AssumptionRole",
    "CellSpec",
    "ConfigFieldName",
    "InputCell",
    "InputPath",
    "InputScalar",
    "InputValue",
    "SourceRef",
    "SourceRefType",
    "SourceStatus",
]
