"""Shared input-cell vocabulary used by both ventures.

The source-linked ``InputCell``, its enums, and the generic cell builders,
used by both the data-center and communications models.
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


class AssumptionRole(StrEnum):
    """Public role of one modeled input assumption."""

    DEFAULT = "default"
    SENSITIVITY = "sensitivity"
    VALIDATION_ONLY = "validation_only"
    DERIVED_INPUT = "derived_input"


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
    EXTERNAL_URL = "external_url"
    MODEL_DERIVATION = "model_derivation"


class SourceRef(BaseModel):
    """One durable public source or derivation reference for an input."""

    model_config = ConfigDict(frozen=True)

    ref_type: SourceRefType = Field(..., description="Kind of source reference.")
    ref: str = Field(..., description="Durable path, URL, claim ID, or derivation path.")
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
    """Metadata used to construct one input cell."""

    label: str
    unit: str | None
    role: AssumptionRole
    source_status: SourceStatus
    claim_id: str
    source_note: str
    rationale: str
    notes: str | None = None


def _source_index_ref(claim_id: str, note: str) -> SourceRef:
    """Build a SOURCE_INDEX reference for an input cell."""
    return SourceRef(
        ref_type=SourceRefType.SOURCE_INDEX,
        ref=f"research/SOURCE_INDEX.md#{claim_id}",
        claim_id=claim_id,
        note=note,
    )


def _research_ref(path: str, note: str, claim_id: str | None = None) -> SourceRef:
    """Build a research-document reference for an input cell."""
    return SourceRef(ref_type=SourceRefType.RESEARCH_DOC, ref=path, claim_id=claim_id, note=note)


def _field_description(model_cls: type[BaseModel], field_name: str) -> str:
    """Return the Pydantic field description for a config field."""
    description = model_cls.model_fields[field_name].description
    if description is None:
        return f"Scenario field {field_name}."
    return description


def _cell(path: str, value: InputValue, description: str, spec: CellSpec) -> InputCell:
    """Construct one source-linked input cell."""
    return InputCell(
        path=path,
        label=spec.label,
        value=value,
        unit=spec.unit,
        description=description,
        assumption_role=spec.role,
        source_status=spec.source_status,
        source_refs=[_source_index_ref(spec.claim_id, spec.source_note)],
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


def _int_value(cell: InputCell) -> int:
    """Return an input cell's scalar value as ``int``."""
    value = cell.value
    if isinstance(value, (bool, list)):
        raise TypeError(f"{cell.path} is not an integer scalar")
    return int(value)


def _number_value(cell: InputCell) -> float | int:
    """Return an input cell's scalar numeric value."""
    value = cell.value
    if isinstance(value, (bool, list, str)):
        raise TypeError(f"{cell.path} is not a numeric scalar")
    return value


def _float_value(cell: InputCell) -> float:
    """Return an input cell's scalar value as ``float``."""
    value = cell.value
    if isinstance(value, (bool, list)):
        raise TypeError(f"{cell.path} is not a numeric scalar")
    return float(value)


def _str_value(cell: InputCell) -> str:
    """Return an input cell's scalar value as ``str``."""
    value = cell.value
    if not isinstance(value, str):
        raise TypeError(f"{cell.path} is not a string scalar")
    return value


def _first_research_ref(cell: InputCell) -> str:
    """Return the first research-document ref attached to an input cell."""
    for ref in cell.source_refs:
        if ref.ref_type is SourceRefType.RESEARCH_DOC:
            return ref.ref
    return ""


__all__ = [
    "AssumptionRole",
    "CellSpec",
    "InputCell",
    "InputPath",
    "InputScalar",
    "InputValue",
    "SourceRef",
    "SourceRefType",
    "SourceStatus",
]
