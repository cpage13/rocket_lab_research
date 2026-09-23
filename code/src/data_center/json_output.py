"""v8 output assembly + JSON serialiser for :class:`ValuationOutput`.

Three responsibilities:

* :func:`build_output` — assemble the complete v8 :class:`ValuationOutput`
  from a :class:`data_center.config.ValuationConfig`, the extended
  generation list, and the per-year ``physical`` / ``business`` maps the
  engine computes. The engine's :func:`data_center.engine.run_valuation`
  delegates the v8 assembly to this function (plan § 5 T51/T52).
* :func:`build_data_dictionary`: walk a built output (the space artifact
  or the ground reference) and return its path-sorted data dictionary. The
  dictionary is *generated*, not hand-maintained: a cell's unit is read
  from the cell itself, a non-cell field's unit from its declaration.
* :func:`render_json` — wrap ``model_dump_json(indent=2)`` so the CLI's
  ``--json`` path has one place to call.

The ``meta.query_examples`` block — the cold-reader contract — is the
fixed 12-entry list :func:`data_center.query_examples.build_query_examples`
builds for the run's anchor year; :func:`build_output` places it at
``meta.query_examples`` in every emitted :class:`ValuationOutput`.

``meta.validation_results`` is built by
:func:`data_center.validation.build_validation_results` (every V-rule, the
model invariants, and, for the canonical default only, the default guards);
its anchor-year checks read the run's anchor year
(:func:`data_center.config.anchor_year`), never a hardcoded calendar year.
"""

from __future__ import annotations

import inspect
import types
from collections.abc import Iterable
from enum import Enum
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Final, Union, get_args, get_origin  # typing-acceptable: introspection

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from common.meta import summarize_source_statuses
from data_center.config import ValuationConfig, anchor_year
from data_center.constants import USD_PER_MUSD
from data_center.generations import GenerationSpec
from data_center.input_manifest import (
    InputCell,
    build_input_manifest,
    generation_source_status,
)
from data_center.output import (
    SCHEMA_VERSION,
    ArtifactRole,
    BusinessBlock,
    BusinessYear,
    DataDictEntry,
    FormulaDefinition,
    GenerationSummary,
    MetaBlock,
    PhysicalBlock,
    PhysicalYear,
    RunMetadata,
    SpaceModelOutput,
    ValidationReport,
    ValuationOutput,
)
from data_center.provenance import FORMULAS, FieldPath, ProvenanceCell
from data_center.query_examples import build_query_examples
from data_center.validation import build_validation_results, compute_validation

MODEL_PACKAGE_NAME: Final[str] = "rklb-value"

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


def _source_class_for(path: str) -> str:
    """Best-effort provenance class for one leaf path.

    The v8 ``data_dictionary`` tags every field with a provenance class:
    fields under ``inputs.*`` are operator-set dials (``INPUT``); everything
    in ``physical`` / ``business`` is engine-computed (``DERIVED``);
    ``metadata`` fields are run-identity constants (``CONSTANT``).

    Args:
        path: The leaf's dotted field path.

    Returns:
        A provenance-class string: ``INPUT`` / ``DERIVED`` / ``CONSTANT``.
    """
    head = path.split(".", 1)[0]
    head = head[:-2] if head.endswith("[]") else head
    if head == "inputs":
        return "INPUT"
    if head == "metadata":
        return "CONSTANT"
    return "DERIVED"


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

    Shared by the space artifact and the ground reference. Returns a
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


# ---------------------------------------------------------------------------
# Generations dictionary
# ---------------------------------------------------------------------------


def _build_generations_dictionary(gens: list[GenerationSpec]) -> list[GenerationSummary]:
    """Build the compact ``meta.generations_dictionary`` view.

    Each entry's ``source_class`` is the generation's public source status
    (:func:`data_center.input_manifest.generation_source_status`), the same
    vocabulary the generation input cells publish.

    Args:
        gens: The extended generation list.

    Returns:
        One :class:`GenerationSummary` per generation.
    """
    return [
        GenerationSummary(
            name=g.name,
            year_available=g.year_available,
            die_count=g.die_count,
            kw_per_pkg=g.kw_per_pkg,
            pkg_mass_kg=g.kg_per_pkg,
            pkg_cost_musd=g.usd_per_pkg / USD_PER_MUSD,
            pf_per_pkg=g.pf_per_pkg,
            source_class=generation_source_status(g.source.sourcing),
            source_doc_path=g.source.doc_path,
        )
        for g in gens
    ]


def _model_version() -> str | None:
    """Return the installed package version when import metadata is available."""
    try:
        return version(MODEL_PACKAGE_NAME)
    except PackageNotFoundError:
        return None


# Formula-id prefixes owned by OTHER ventures that share the common FORMULAS
# registry. FORMULAS moved to common.provenance (Phase 0 of the comms build) and
# is shared; the communications model appends comms_-prefixed entries to it. The
# data-center artifact documents only its OWN formulas, so foreign entries are
# excluded here. Without this filter the promoted DC default JSON gains the comms
# formulas on every regeneration, silently breaking its exactness (the parity gate
# locks per-year values, not the meta.formula_definitions block).
_FOREIGN_VENTURE_FORMULA_PREFIXES: Final[tuple[str, ...]] = ("comms_",)


def _build_formula_definitions() -> list[FormulaDefinition]:
    """Build public formula metadata from the authoritative formula table.

    Documents only data-center formulas: entries in the shared FORMULAS registry
    that belong to another venture (see :data:`_FOREIGN_VENTURE_FORMULA_PREFIXES`)
    are excluded, so the promoted DC artifact stays exact as the shared registry
    grows.
    """
    return [
        FormulaDefinition(
            formula_id=formula_id,
            formula_text=spec.formula,
            description=spec.description,
            input_path_pattern="See each ProvenanceCell.uses entry.",
            output_path_pattern="Search cells where formula_name equals this formula_id.",
            unit_behavior="Output units are carried by each ProvenanceCell.unit.",
            scenario_notes=None,
        )
        for formula_id, spec in sorted(FORMULAS.items())
        if not formula_id.startswith(_FOREIGN_VENTURE_FORMULA_PREFIXES)
    ]


# ---------------------------------------------------------------------------
# v8 output assembly
# ---------------------------------------------------------------------------


def build_output(
    *,
    config: ValuationConfig,
    extended_gens: list[GenerationSpec],
    physical_by_year: dict[str, PhysicalYear],
    business_by_year: dict[str, BusinessYear],
    generated_at: str,
    source_scenario_path: str,
    artifact_role: ArtifactRole = ArtifactRole.DRAFT,
) -> SpaceModelOutput:
    """Assemble the complete v8 :class:`SpaceModelOutput`.

    The engine computes the per-year ``physical`` / ``business`` maps and
    calls this function to wrap them in the five-block v8 artifact —
    building the ``metadata`` / ``inputs`` / ``meta`` blocks and running
    the validation rules against the assembled output.

    Args:
        config: The validated :class:`ValuationConfig`.
        extended_gens: The generation list extended to cover the horizon.
        physical_by_year: Per-year :class:`PhysicalYear`, keyed by
            JSON-string fiscal year.
        business_by_year: Per-year :class:`BusinessYear`, keyed by
            JSON-string fiscal year.
        generated_at: ISO-8601 UTC timestamp for the run.
        source_scenario_path: Repository-relative path to the scenario YAML.
        artifact_role: Artifact role to stamp in metadata.

    Returns:
        A frozen v8 :class:`SpaceModelOutput` with the validation report
        computed against the assembled artifact.
    """
    md = config.metadata
    metadata = RunMetadata(
        schema_version=SCHEMA_VERSION,
        scenario_name=config.scenario_name,
        base_year=md.base_year,
        horizon_years=md.horizon_years,
        workload_type=md.workload_type,
        operator_model=md.operator_model,
        radiator_architecture=md.radiator_architecture,
        deployment_philosophy=md.deployment_philosophy,
        generated_at=generated_at,
        model_package=MODEL_PACKAGE_NAME,
        model_version=_model_version(),
        artifact_role=artifact_role,
        source_scenario_path=source_scenario_path,
    )

    inputs = build_input_manifest(
        config=config,
        extended_gens=extended_gens,
        source_scenario_path=source_scenario_path,
    )

    physical = PhysicalBlock(years=physical_by_year)
    business = BusinessBlock(years=business_by_year)

    # Build the artifact with an empty data dictionary and validation report,
    # generate the dictionary from the populated output (its cells supply the
    # units), run the rules against the populated output, then swap the
    # report and the public verdict list in. Every rule stays a pure function
    # of SpaceModelOutput. ``query_examples`` is the fixed cold-reader
    # contract from ``query_examples.py``.
    pre_meta = MetaBlock(
        validation=ValidationReport(rules=[]),
        data_dictionary=[],
        formula_definitions=_build_formula_definitions(),
        validation_results=[],
        generations_dictionary=_build_generations_dictionary(extended_gens),
        query_examples=build_query_examples(anchor_year(md.base_year, md.horizon_years)),
        source_status_summary=summarize_source_statuses(
            cell.source_status for cell in inputs.assumption_index.values()
        ),
        schema_version_notes=(
            "v8 space output with Phase-2 InputManifest, source-status summary, "
            "formula definitions, validation_results, and query examples."
        ),
    )
    pre_output = SpaceModelOutput(
        metadata=metadata,
        inputs=inputs,
        physical=physical,
        business=business,
        meta=pre_meta,
    )
    meta = pre_meta.model_copy(update={"data_dictionary": build_data_dictionary(pre_output)})
    pre_output = pre_output.model_copy(update={"meta": meta})
    rules = compute_validation(pre_output)
    meta = meta.model_copy(update={"validation": ValidationReport(rules=rules)})
    output_with_rules = pre_output.model_copy(update={"meta": meta})
    meta = meta.model_copy(
        update={"validation_results": build_validation_results(output_with_rules)}
    )
    return output_with_rules.model_copy(update={"meta": meta})


def render_json(output: ValuationOutput) -> str:
    """Serialise a :class:`ValuationOutput` as indented JSON.

    Wraps ``model_dump_json(indent=2)``. The returned string is what the
    CLI's ``--json`` path emits.

    Args:
        output: The v8 valuation output to serialise.

    Returns:
        The artifact as an indented JSON string.
    """
    return output.model_dump_json(indent=2)


__all__ = ["build_data_dictionary", "build_output", "render_json"]
