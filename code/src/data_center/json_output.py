"""v8 output assembly + JSON serialiser for :class:`ValuationOutput`.

Three responsibilities:

* :func:`build_output` — assemble the complete v8 :class:`ValuationOutput`
  from a :class:`data_center.config.ValuationConfig`, the extended
  generation list, and the per-year ``physical`` / ``business`` maps the
  engine computes. The engine's :func:`data_center.engine.run_valuation`
  delegates the v8 assembly to this function (plan § 5 T51/T52).
* :func:`build_data_dictionary` — walk the typed :class:`ValuationOutput`
  model and return ``dict[FieldPath, DataDictEntry]`` keyed by dotted
  field path. The data dictionary is *generated*, not hand-maintained.
* :func:`render_json` — wrap ``model_dump_json(indent=2)`` so the CLI's
  ``--json`` path has one place to call.

The ``meta.query_examples`` block — the cold-reader contract — is the
fixed 12-entry :data:`data_center.query_examples.QUERY_EXAMPLES` list;
:func:`build_output` places it at ``meta.query_examples`` in every
emitted :class:`ValuationOutput`.
"""

from __future__ import annotations

import inspect
import types
from collections.abc import Iterable
from enum import Enum
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Final, Union, get_args, get_origin  # typing-acceptable: introspection

from pydantic import BaseModel

from data_center.config import ValuationConfig
from data_center.constants import USD_PER_MUSD
from data_center.generations import GenerationSpec
from data_center.input_manifest import InputCell, SourceStatus, build_input_manifest
from data_center.output import (
    SCHEMA_VERSION,
    BusinessBlock,
    BusinessYear,
    DataDictEntry,
    FormulaDefinition,
    GenerationSummary,
    MetaBlock,
    PhysicalBlock,
    PhysicalYear,
    RunMetadata,
    SourceStatusSummary,
    SpaceModelOutput,
    ValidationReport,
    ValidationResult,
    ValidationSeverity,
    ValuationOutput,
)
from data_center.provenance import FORMULAS, FieldPath, ProvenanceCell
from data_center.query_examples import QUERY_EXAMPLES
from data_center.validation import compute_validation

MODEL_PACKAGE_NAME: Final[str] = "rklb-value"
DEFAULT_ARTIFACT_ROLE: Final[str] = "draft"
PROMOTED_DEFAULT_ARTIFACT_ROLE: Final[str] = "promoted_default"
TARGET_YEAR: Final[str] = "2036"
DEPLOYED_KW_LOWER_BOUND: Final[float] = 60_000.0
DEPLOYED_KW_UPPER_BOUND: Final[float] = 75_000.0
DEFAULT_REVENUE_MULTIPLE: Final[float] = 1.5
DEFAULT_TARGET_LAUNCHES: Final[int] = 90
DEFAULT_SERVICE_LIFE_YEARS: Final[int] = 5

# ---------------------------------------------------------------------------
# Unit inference — every v8 leaf is a ProvenanceCell carrying its own `unit`,
# so the data-dictionary unit comes straight from the cell's declared unit
# where one exists. The name→unit table covers the non-cell leaves (config
# dials, generation specs, metadata) the walker still has to describe.
# ---------------------------------------------------------------------------

# Exact field-name → unit. Consulted before the suffix table so a specific
# name always wins over a generic suffix.
_NAME_TO_UNIT: Final[dict[str, str]] = {
    "fy": "year",
    "year_available": "year",
    "base_year": "year",
    "horizon_years": "year",
    "service_life_years": "year",
    "release_cadence_yr": "year/gen",
    "tjmax_lift_year": "year",
    "bus_flatten_after_yr": "year",
    "first_launch_year": "year",
    "value": "-",
    "schema_version": "-",
    "generated_at": "-",
    "mass_envelope_t": "t",
    "node_mass_fixed_t": "t",
    "kw_per_pkg": "kW/pkg",
    "kg_per_pkg": "kg/pkg",
    "kw_deployed_this_year": "kW",
    "kw_living_fleet": "kW",
    "pf_deployed_this_year": "PFLOPS",
    "pf_living_fleet": "PFLOPS",
    "pkg_mass_kg": "kg",
    "usd_per_pkg": "$/pkg",
    "die_count": "die",
    "pf_per_pkg": "PFLOPS",
    "pkg_cost_musd": "MUSD",
    "cadence_ceiling": "count",
    "launches_at_year_5": "count",
    "launches_at_year_10": "count",
    "r": "ratio",
    # v8 per-year cell fields (PhysicalYear / BusinessYear) — the cell
    # carries its own `unit`, but the data dictionary repeats it as a hint.
    "frontier_generation": "-",
    "gpus_per_node": "count",
    "kw_per_node": "kW",
    "pf_per_node": "PFLOPS",
    "pf_per_kw": "PFLOPS/kW",
    "binding_constraint": "-",
    "solar_area_per_pkg_m2": "m2",
    "volume_per_pkg_m3": "m3",
    "launches": "count",
    "nodes_deployed_this_year": "count",
    "living_fleet": "count",
    "kw_on_orbit": "kW",
    "pf_on_orbit": "PFLOPS",
    # v8 cost_breakdown sub-object cells (CostBreakdownBlock) — all $M.
    "compute": "MUSD",
    "bus": "MUSD",
    "solar": "MUSD",
    "radiator": "MUSD",
    "launch": "MUSD",
    "node_total": "MUSD",
}

# Ordered suffix table: more-specific suffixes win over generic ones.
_SUFFIX_TO_UNIT: Final[tuple[tuple[str, str], ...]] = (
    ("_cost_musd", "MUSD"),
    ("_musd_per_kw", "MUSD/kW"),
    ("_t_per_kw_pre", "t/kW"),
    ("_t_per_kw_post", "t/kW"),
    ("_t_per_kw", "t/kW"),
    ("_kg_m2", "kg/m2"),
    ("_per_kw", "/kW"),
    ("_musd", "MUSD"),
    ("_pct", "percent"),
    ("_m3", "m3"),
    ("_mm", "mm"),
    ("_kw", "kW"),
    ("_kg", "kg"),
    ("_t", "t"),
    ("_ratio", "ratio"),
    ("_years", "year"),
    ("_year", "year"),
    ("_yr", "year"),
)


def _unit_for(field_name: str, leaf_type: type[Any]) -> str:
    """Best-effort unit string for one non-cell leaf field.

    Resolution order: an exact field-name match in :data:`_NAME_TO_UNIT`
    wins first; then the most-specific suffix in :data:`_SUFFIX_TO_UNIT`;
    then ``'-'`` for booleans / numbers and ``''`` for strings.

    Args:
        field_name: The leaf field's name.
        leaf_type: The leaf's runtime type (for the numeric / string fallback).

    Returns:
        A unit string, or ``'-'`` / ``''`` for the unitless fallbacks.
    """
    name = field_name.lower()
    if name in _NAME_TO_UNIT:
        return _NAME_TO_UNIT[name]
    for suffix, unit in _SUFFIX_TO_UNIT:
        if name.endswith(suffix):
            return unit
    if leaf_type is bool or leaf_type is int or leaf_type is float:
        return "-"
    return ""


# ---------------------------------------------------------------------------
# Type + provenance-class inference for a leaf field.
# ---------------------------------------------------------------------------


def _wire_type(leaf_type: type[Any]) -> str:
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
    if inspect.isclass(leaf_type) and issubclass(leaf_type, Enum):
        return "string"
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
# Walking a Pydantic model tree.
# ---------------------------------------------------------------------------


def _is_basemodel(t: Any) -> bool:
    """True if ``t`` is a Pydantic BaseModel subclass."""
    return inspect.isclass(t) and issubclass(t, BaseModel)


def _is_cell(t: Any) -> bool:
    """True if ``t`` is a public cell type.

    The data-dictionary walker treats cells as leaves — they are public
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


def _walk(
    cls: type[BaseModel],
    prefix: str,
    out: dict[FieldPath, DataDictEntry],
) -> None:
    """Recurse into a Pydantic model class, emitting one DataDictEntry per leaf.

    Container fields (lists / dicts of BaseModels) flatten with a ``[]``
    suffix on the container's name. Pydantic BaseModel leaves recurse;
    primitive / enum leaves emit a single DataDictEntry.

    Args:
        cls: The Pydantic model class to walk.
        prefix: The dotted path prefix accumulated so far.
        out: The output map, mutated in place.
    """
    for name, info in cls.model_fields.items():
        path = f"{prefix}.{name}" if prefix else name
        ann = _unwrap_optional(info.annotation)

        # A ProvenanceCell IS the leaf — it is the model's output field. Do
        # not recurse into its machinery (value / unit / formula / ...);
        # describe the cell by its enclosing field's name + description.
        if _is_cell(ann):
            out[path] = DataDictEntry(
                path=path,
                description=info.description or "",
                unit=_unit_for(name, float),
                type="cell",
                source_class=_source_class_for(path),
            )
            continue

        if _is_basemodel(ann):
            _walk(ann, path, out)
            continue

        elem = _element_type(ann)
        if elem is not None and _is_cell(elem):
            out[f"{path}[]"] = DataDictEntry(
                path=f"{path}[]",
                description=info.description or "",
                unit=_unit_for(name, float),
                type="cell",
                source_class=_source_class_for(path),
            )
            continue
        if elem is not None and _is_basemodel(elem):
            _walk(elem, f"{path}[]", out)
            continue

        desc = info.description or ""
        leaf_type: type[Any]
        if elem is not None:
            leaf_type = elem if isinstance(elem, type) else type(elem)
        else:
            leaf_type = ann if isinstance(ann, type) else type(ann)
        if inspect.isclass(leaf_type) and issubclass(leaf_type, Enum):
            unit = "-"
        else:
            unit = _unit_for(name, leaf_type)
        out[path] = DataDictEntry(
            path=path,
            description=desc,
            unit=unit,
            type=_wire_type(leaf_type),
            source_class=_source_class_for(path),
        )


# ---------------------------------------------------------------------------
# Data dictionary
# ---------------------------------------------------------------------------


def build_data_dictionary(
    output_cls: type[BaseModel] = SpaceModelOutput,
) -> list[DataDictEntry]:
    """Walk a Pydantic output model and build the v8 data dictionary.

    Returns a path-sorted list of entries: leaf fields produce one entry;
    container fields (lists / dicts of BaseModels) flatten with a ``[]``
    suffix. Per-leaf ``description`` is the Pydantic ``Field`` description;
    ``unit`` is inferred from the field name; ``type`` is the wire type;
    ``source_class`` from the path position.

    Args:
        output_cls: The Pydantic model class to introspect.

    Returns:
        Data dictionary entries covering every leaf in the tree.
    """
    out: dict[FieldPath, DataDictEntry] = {}
    _walk(output_cls, "", out)
    return [out[path] for path in sorted(out)]


# ---------------------------------------------------------------------------
# Generations dictionary
# ---------------------------------------------------------------------------


def _build_generations_dictionary(gens: list[GenerationSpec]) -> list[GenerationSummary]:
    """Build the compact ``meta.generations_dictionary`` view.

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
            source_class=g.source.sourcing.value,
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


def _source_status_summary(output: SpaceModelOutput) -> SourceStatusSummary:
    """Count input assumptions by source-status value."""
    summary = dict.fromkeys(SourceStatus, 0)
    for cell in output.inputs.assumption_index.values():
        summary[cell.source_status] += 1
    return SourceStatusSummary(
        certified=summary[SourceStatus.CERTIFIED],
        sourced_estimate=summary[SourceStatus.SOURCED_ESTIMATE],
        derived_estimate=summary[SourceStatus.DERIVED_ESTIMATE],
        projection=summary[SourceStatus.PROJECTION],
        extrapolation=summary[SourceStatus.EXTRAPOLATION],
        scenario=summary[SourceStatus.SCENARIO],
        placeholder=summary[SourceStatus.PLACEHOLDER],
        stale=summary[SourceStatus.STALE],
    )


def _rule_to_validation_result(rule_name: str, result: bool, expected: str, observed: str) -> str:
    """Return a compact observed-result string for one validation."""
    verdict = "pass" if result else "fail"
    return f"{verdict}: expected {expected}; observed {observed}; rule={rule_name}"


def _validation_result(
    *,
    validation_id: str,
    passed: bool,
    what_tested: str,
    expected_condition: str,
    observed_result: str,
    related_json_paths: list[str],
    remediation_hint: str | None = None,
) -> ValidationResult:
    """Construct one public validation result."""
    return ValidationResult(
        validation_id=validation_id,
        severity=ValidationSeverity.OK if passed else ValidationSeverity.FAIL,
        what_tested=what_tested,
        expected_condition=expected_condition,
        observed_result=observed_result,
        related_json_paths=related_json_paths,
        remediation_hint=None if passed else remediation_hint,
    )


def _numeric_cell_value(cell: ProvenanceCell) -> float:
    """Return a provenance cell's value as a float."""
    value = cell.value
    if isinstance(value, bool) or value is None or isinstance(value, str):
        raise TypeError(f"{cell.description} is not numeric")
    return float(value)


def _integer_cell_value(cell: ProvenanceCell) -> int:
    """Return a provenance cell's value as an integer."""
    value = cell.value
    if isinstance(value, bool) or value is None or isinstance(value, str):
        raise TypeError(f"{cell.description} is not an integer")
    return int(value)


def _build_validation_results(output: SpaceModelOutput) -> list[ValidationResult]:
    """Build Phase-2 public validation metadata from the final output."""
    results: list[ValidationResult] = []
    for rule in output.meta.validation.rules:
        severity = ValidationSeverity.OK
        if not rule.pass_check:
            severity = (
                ValidationSeverity.WARN
                if rule.severity.value == "minor"
                else ValidationSeverity.FAIL
            )
        results.append(
            ValidationResult(
                validation_id=rule.name,
                severity=severity,
                what_tested=rule.what_it_tests,
                expected_condition=rule.expected,
                observed_result=rule.computed,
                related_json_paths=[],
                remediation_hint=None if rule.pass_check else "Review model inputs and formulas.",
            )
        )

    business_year = output.business.years[TARGET_YEAR]
    deployed_kw = _numeric_cell_value(business_year.kw_deployed_this_year)
    deployed_ok = DEPLOYED_KW_LOWER_BOUND <= deployed_kw <= DEPLOYED_KW_UPPER_BOUND
    results.append(
        _validation_result(
            validation_id="default_2036_deployed_capacity_around_70mw",
            passed=deployed_ok,
            what_tested="Default 2036 newly deployed capacity is around 70 MW/year.",
            expected_condition=(
                f"{DEPLOYED_KW_LOWER_BOUND:g} <= kw_deployed_this_year <= "
                f"{DEPLOYED_KW_UPPER_BOUND:g}"
            ),
            observed_result=_rule_to_validation_result(
                "default_2036_deployed_capacity_around_70mw",
                deployed_ok,
                "around 70 MW/year",
                f"{deployed_kw:g} kW/year",
            ),
            related_json_paths=[f'business.years."{TARGET_YEAR}".kw_deployed_this_year'],
            remediation_hint="Check cadence and per-node power assumptions.",
        )
    )

    living_kw = _numeric_cell_value(business_year.kw_living_fleet)
    cohort_ok = living_kw > deployed_kw
    results.append(
        _validation_result(
            validation_id="living_fleet_distinct_from_deployed_year_cohort",
            passed=cohort_ok,
            what_tested="Living fleet capacity is distinct from same-year deployment.",
            expected_condition="kw_living_fleet > kw_deployed_this_year",
            observed_result=_rule_to_validation_result(
                "living_fleet_distinct_from_deployed_year_cohort",
                cohort_ok,
                "living fleet above deployed-year cohort",
                f"{living_kw:g} kW living vs {deployed_kw:g} kW deployed",
            ),
            related_json_paths=[
                f'business.years."{TARGET_YEAR}".kw_living_fleet',
                f'business.years."{TARGET_YEAR}".kw_deployed_this_year',
            ],
            remediation_hint="Check cohort cliff and living-fleet rollup.",
        )
    )

    first_r = output.inputs.r_band.central[0].r
    r_ok = first_r == DEFAULT_REVENUE_MULTIPLE
    results.append(
        _validation_result(
            validation_id="default_revenue_multiple_is_1_5x",
            passed=r_ok,
            what_tested="Default central R-band starts at 1.5x.",
            expected_condition=f"central R at base year == {DEFAULT_REVENUE_MULTIPLE:g}",
            observed_result=_rule_to_validation_result(
                "default_revenue_multiple_is_1_5x",
                r_ok,
                f"{DEFAULT_REVENUE_MULTIPLE:g}",
                f"{first_r:g}",
            ),
            related_json_paths=["inputs.config.revenue.central"],
            remediation_hint="Check default scenario R-band anchors.",
        )
    )

    launches = _integer_cell_value(business_year.launches)
    launches_ok = launches == DEFAULT_TARGET_LAUNCHES
    results.append(
        _validation_result(
            validation_id="target_cadence_is_90_launches",
            passed=launches_ok,
            what_tested="2036 target cadence is 90 launches/year.",
            expected_condition=f"launches == {DEFAULT_TARGET_LAUNCHES}",
            observed_result=_rule_to_validation_result(
                "target_cadence_is_90_launches",
                launches_ok,
                str(DEFAULT_TARGET_LAUNCHES),
                str(launches),
            ),
            related_json_paths=[
                "inputs.config.cadence.launches_at_year_10",
                f'business.years."{TARGET_YEAR}".launches',
            ],
            remediation_hint="Check cadence anchors.",
        )
    )

    service_life = output.inputs.fleet.service_life_years
    service_ok = service_life == DEFAULT_SERVICE_LIFE_YEARS
    results.append(
        _validation_result(
            validation_id="default_service_life_is_five_years",
            passed=service_ok,
            what_tested="Default service life is five years.",
            expected_condition=f"service_life_years == {DEFAULT_SERVICE_LIFE_YEARS}",
            observed_result=_rule_to_validation_result(
                "default_service_life_is_five_years",
                service_ok,
                str(DEFAULT_SERVICE_LIFE_YEARS),
                str(service_life),
            ),
            related_json_paths=["inputs.config.fleet.service_life_years"],
            remediation_hint="Check default scenario fleet block.",
        )
    )

    source_summary = output.meta.source_status_summary
    release_status_ok = source_summary.placeholder == 0 and source_summary.stale == 0
    results.append(
        _validation_result(
            validation_id="release_critical_inputs_have_no_placeholder_or_stale_status",
            passed=release_status_ok,
            what_tested="Source-status summary has no placeholder or stale default inputs.",
            expected_condition="placeholder == 0 and stale == 0",
            observed_result=_rule_to_validation_result(
                "release_critical_inputs_have_no_placeholder_or_stale_status",
                release_status_ok,
                "no placeholder/stale statuses",
                str(source_summary.model_dump()),
            ),
            related_json_paths=["inputs.assumption_index", "meta.source_status_summary"],
            remediation_hint="Update source metadata before promotion.",
        )
    )
    return results


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
    artifact_role: str = DEFAULT_ARTIFACT_ROLE,
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

    # Build the artifact with a temporary empty validation report, run the
    # rules against the populated output, then swap the report in. Computing
    # against the populated output keeps every rule a pure function of
    # SpaceModelOutput. ``query_examples`` is the fixed cold-reader
    # contract from ``query_examples.py``.
    data_dictionary = build_data_dictionary(SpaceModelOutput)
    pre_meta = MetaBlock(
        validation=ValidationReport(rules=[]),
        data_dictionary=data_dictionary,
        formula_definitions=_build_formula_definitions(),
        validation_results=[],
        generations_dictionary=_build_generations_dictionary(extended_gens),
        query_examples=QUERY_EXAMPLES,
        source_status_summary=SourceStatusSummary(
            certified=0,
            sourced_estimate=0,
            derived_estimate=0,
            projection=0,
            extrapolation=0,
            scenario=0,
            placeholder=0,
            stale=0,
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
    source_summary = _source_status_summary(pre_output)
    meta_with_summary = pre_meta.model_copy(update={"source_status_summary": source_summary})
    pre_output = pre_output.model_copy(update={"meta": meta_with_summary})
    rules = compute_validation(pre_output)
    final_meta = meta_with_summary.model_copy(update={"validation": ValidationReport(rules=rules)})
    output_with_rules = pre_output.model_copy(update={"meta": final_meta})
    validation_results = _build_validation_results(output_with_rules)
    final_meta = final_meta.model_copy(update={"validation_results": validation_results})
    return output_with_rules.model_copy(update={"meta": final_meta})


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
