"""The comms meta enrichment: the data-dictionary walk, the formula and validation builders.

The comms analog of :mod:`data_center.json_output`, adapted to the comms
lean-engine split (plan P5.0). The Phase-3 engine assembles a COMPLETE five-key
:class:`communications.output.CommsModelOutput` with a LEAN ``meta`` block (the
validation report empty, the source-status summary and schema notes populated,
the four enrichment fields empty). This module's :func:`enrich_comms_output`
takes that lean output and returns an enriched copy whose ``meta`` block carries
the introspection-driven ``data_dictionary``, the ``formula_definitions``
catalog, the executable validation ``rules``, the public ``validation_results``,
and the ``query_examples`` cold-reader contract. The serializer lives in
:mod:`communications.engine` (``render_comms_json``); this module is the
meta-enrichment surface only.

The formula catalog is SCOPED to the comms namespace (the ``comms_``-prefixed
formula ids), excluding the data-center formulas that share the one
``common.provenance.FORMULAS`` registry. This mirrors, in reverse, the
data-center artifact's exclusion of the comms namespace (commit 8efb6e0): each
venture's promoted artifact documents only its OWN formulas, so neither is
reverse-contaminated as the shared registry grows.

The enrichment is a PURE function of the input output: it reads cells and builds
the meta scaffold; it computes NO new space-side or ground-side number and emits
NO verdict, conclusion label, market-capture, or heavier-vehicle value.
"""

from __future__ import annotations

import inspect
import logging
import types
from collections.abc import Iterable
from enum import Enum
from typing import (  # typing-acceptable: introspection
    Any,
    Final,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel

from common.input_manifest import InputCell
from common.meta import (
    DataDictEntry,
    FormulaDefinition,
    QueryAppliesTo,
    QueryExample,
    Severity,
    ValidationReport,
    ValidationResult,
    ValidationSeverity,
)
from common.provenance import FORMULAS, FieldPath, ProvenanceCell
from communications.output import CommsModelOutput
from communications.validation import compute_comms_validation

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Named constants (the "no bare literals" rule).
# ---------------------------------------------------------------------------

TARGET_YEAR: Final[str] = "2036"
"""The default-scenario steady-state year string the query examples key off. The
per-run steady-state year is ``config.metadata.steady_state_year``; ``TARGET_YEAR``
is the default-scenario constant the worked jq examples hard-code (mirroring the DC
query_examples). A non-default scenario's reader adapts the year in the expression."""

# Formula-id prefix OWNED by the comms venture. The shared FORMULAS registry
# (in common.provenance) holds both the data-center and the comms formulas; the
# comms artifact documents only its OWN formulas, so the data-center entries are
# excluded here. This is the reverse of the DC json_output's exclusion of the
# comms namespace (commit 8efb6e0): each venture's catalog is namespace-scoped so
# neither artifact is reverse-contaminated as the shared registry grows.
_COMMS_FORMULA_PREFIX: Final[str] = "comms_"
"""The formula-id prefix the comms formula catalog includes (excludes DC formulas)."""

# ---------------------------------------------------------------------------
# Unit-inference tables (retuned for comms units).
# ---------------------------------------------------------------------------

_NAME_TO_UNIT: Final[dict[str, str]] = {
    "value": "-",
    "schema_version": "-",
    "generated_at": "-",
    "year": "year",
    "base_year": "year",
    "horizon_years": "year",
    "steady_state_year": "year",
    "satellites_per_launch": "count",
    "binding_constraint": "-",
    "mass_bound_count": "count",
    "volume_bound_count": "count",
    "launches": "count",
    "broadband_satellites_deployed_this_year": "count",
    "direct_to_cell_satellites_deployed_this_year": "count",
    "broadband_living_fleet": "count",
    "direct_to_cell_living_fleet": "count",
    "cumulative_satellites_built": "count",
    "learning_curve_multiplier": "ratio",
    "capability": "Mbps",
    "per_beam_capacity_mbps": "Mbps",
    "naive_capacity_mbps": "Mbps",
    "spectrum_to_acquire_mhz": "MHz",
    "arpu_collectable_revenue_usd": "USD",
    "total_served": "subs",
    "antenna": "MUSD",
    "comms_electronics": "MUSD",
    "solar": "MUSD",
    "radiator_bus": "MUSD",
    "minor_component": "MUSD",
    "build_cost": "MUSD",
    "build_cost_after_learning": "MUSD",
    "launch_cost_per_satellite": "MUSD",
    "satellite_total": "MUSD",
    "cost_annual_per_satellite_musd": "MUSD",
}

# Ordered suffix table: more-specific suffixes win over generic ones.
_SUFFIX_TO_UNIT: Final[tuple[tuple[str, str], ...]] = (
    ("_per_customer_usd", "USD"),
    ("_per_sub_year", "USD"),
    ("_usd_per_year", "USD"),
    ("_revenue_usd", "USD"),
    ("_usd", "USD"),
    ("_fleet_musd", "MUSD"),
    ("_cost_musd", "MUSD"),
    ("_musd", "MUSD"),
    ("_mhz", "MHz"),
    ("_mbps", "Mbps"),
    ("_served", "subs"),
    ("_m3", "m3"),
    ("_t", "t"),
    ("_kw", "kW"),
    ("_pct", "percent"),
    ("_ratio", "ratio"),
    ("_years", "year"),
    ("_year", "year"),
)


def _unit_for(field_name: str, leaf_type: type[Any]) -> str:
    """Best-effort unit string for one non-cell leaf field.

    Resolution order: an exact field-name match in :data:`_NAME_TO_UNIT` wins
    first; then the most-specific suffix in :data:`_SUFFIX_TO_UNIT`; then ``'-'``
    for booleans / numbers and ``''`` for strings.

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

    Fields under ``inputs.*`` are author-set dials (``INPUT``); ``metadata.*``
    fields are run-identity constants (``CONSTANT``); everything in ``physical`` /
    ``business`` / ``meta`` is engine-computed (``DERIVED``).

    Args:
        path: The leaf's dotted field path.

    Returns:
        A provenance-class string: ``INPUT`` / ``CONSTANT`` / ``DERIVED``.
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
    """True if ``t`` is a public cell type (ProvenanceCell or InputCell).

    The data-dictionary walker treats cells as leaves: they are public output
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

    Container fields (lists / dicts of BaseModels) flatten with a ``[]`` suffix on
    the container's name. Pydantic BaseModel leaves recurse; cell types and
    primitive / enum leaves emit a single DataDictEntry. The comms per-year maps
    (``physical.years`` / ``business.years``) flatten to ``physical.years[]`` /
    ``business.years[]`` (the dict VALUE type), so the dictionary has one entry per
    distinct leaf SHAPE, not one per calendar year.

    Args:
        cls: The Pydantic model class to walk.
        prefix: The dotted path prefix accumulated so far.
        out: The output map, mutated in place.
    """
    for name, info in cls.model_fields.items():
        path = f"{prefix}.{name}" if prefix else name
        ann = _unwrap_optional(info.annotation)

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


def build_comms_data_dictionary(
    output_cls: type[BaseModel] = CommsModelOutput,
) -> list[DataDictEntry]:
    """Walk a comms output model and build the data dictionary.

    Returns a path-sorted list of entries: leaf fields produce one entry;
    container fields (dicts / lists of BaseModels) flatten with a ``[]`` suffix.
    Per-leaf ``description`` is the Pydantic ``Field`` description; ``unit`` is
    inferred from the field name; ``type`` is the wire type; ``source_class`` from
    the path position. The comms analog of the DC
    :func:`data_center.json_output.build_data_dictionary`.

    Args:
        output_cls: The Pydantic model class to introspect (defaults to
            :class:`communications.output.CommsModelOutput`).

    Returns:
        Data-dictionary entries covering every leaf in the tree, path-sorted.
    """
    out: dict[FieldPath, DataDictEntry] = {}
    _walk(output_cls, "", out)
    return [out[path] for path in sorted(out)]


def _build_formula_definitions() -> list[FormulaDefinition]:
    """Build the public comms formula catalog from the FORMULAS registry.

    One :class:`FormulaDefinition` per ``comms_``-prefixed entry in
    :data:`common.provenance.FORMULAS`, sorted by formula id. The comms model
    shares the one FORMULAS registry with the data center; this catalog is SCOPED
    to the comms namespace (see :data:`_COMMS_FORMULA_PREFIX`) so the comms
    artifact documents only its own formulas and is not reverse-contaminated by
    the data-center formulas as the shared registry grows (the reverse of the DC
    json_output's exclusion of the comms namespace, commit 8efb6e0).

    Returns:
        The comms formula catalog, one entry per comms formula, id-sorted.
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
        if formula_id.startswith(_COMMS_FORMULA_PREFIX)
    ]


def _build_comms_validation_results(output: CommsModelOutput) -> list[ValidationResult]:
    """Map the engine-internal validation checks to public validation results.

    Reads ``output.meta.validation.rules`` (the :class:`ValidationCheck` list that
    :func:`communications.validation.compute_comms_validation` produced and the
    enrichment wired into ``meta.validation``) and emits one public
    :class:`ValidationResult` per check, mapping the check severity to the public
    ``pass`` / ``warn`` / ``fail`` vocabulary: a passing check -> ``OK``; a failing
    ``minor`` check -> ``WARN``; a failing ``critical`` / ``major`` check ->
    ``FAIL`` (the DC mapping). Unlike the DC builder, this version appends NO
    ad-hoc default-scenario assertions: ALL comms checks live in
    :mod:`communications.validation`'s rule list, and this builder only
    RE-PRESENTS them as public results.

    Args:
        output: The comms output with ``meta.validation.rules`` populated.

    Returns:
        One public :class:`ValidationResult` per engine check, in rule order.
    """
    results: list[ValidationResult] = []
    for rule in output.meta.validation.rules:
        severity = ValidationSeverity.OK
        if not rule.pass_check:
            severity = (
                ValidationSeverity.WARN
                if rule.severity == Severity.MINOR
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
                remediation_hint=(
                    None if rule.pass_check else "Review model inputs, formulas, and source status."
                ),
            )
        )
    return results


# ---------------------------------------------------------------------------
# The comms query examples (the cold-reader contract).
# ---------------------------------------------------------------------------


QUERY_EXAMPLES: Final[list[QueryExample]] = [
    QueryExample(
        name="list_default_inputs_and_source_statuses",
        question_answered="Which default inputs were used, and how are they source-classed?",
        jq_expression=(
            ".inputs.assumption_index | to_entries | "
            "map({path: .key, value: .value.value, unit: .value.unit, "
            "source_status: .value.source_status})"
        ),
        expected_shape="list of {path, value, unit, source_status}",
        important_paths=["inputs.assumption_index"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="steady_state_customer_band_2036",
        question_answered="What is the steady-state direct-to-cell served-customer band?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}".total_served | '
            "{low: .low.value, mid: .mid.value, high: .high.value}"
        ),
        expected_shape="object {low, mid, high} subscriber counts",
        important_paths=[f'business.years."{TARGET_YEAR}".total_served'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="steady_state_cost_per_customer_band_2036",
        question_answered="What is the steady-state annual cost to serve one customer (a band)?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}".cost_annual_per_customer_usd | '
            "{low: .low.value, mid: .mid.value, high: .high.value}"
        ),
        expected_shape="object {low, mid, high} USD/yr per-customer costs",
        important_paths=[f'business.years."{TARGET_YEAR}".cost_annual_per_customer_usd'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="steady_state_priced_cost_band_2036",
        question_answered="What is the steady-state priced per-customer cost (cost x 1.5)?",
        jq_expression=(
            f'.business.years."{TARGET_YEAR}".priced_cost_per_customer_usd | '
            "{low: .low.value, mid: .mid.value, high: .high.value}"
        ),
        expected_shape="object {low, mid, high} USD/yr priced costs",
        important_paths=[f'business.years."{TARGET_YEAR}".priced_cost_per_customer_usd'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="direct_to_cell_living_fleet_2036",
        question_answered="How many direct-to-cell satellites are in the steady-state fleet?",
        jq_expression=f'.business.years."{TARGET_YEAR}".direct_to_cell_living_fleet.value',
        expected_shape="single integer satellite count",
        important_paths=[f'business.years."{TARGET_YEAR}".direct_to_cell_living_fleet'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="spectrum_requirement",
        question_answered="How much spectrum must the constellation acquire (a requirement, MHz)?",
        jq_expression=f'.physical.years."{TARGET_YEAR}".spectrum_to_acquire_mhz.value',
        expected_shape="single number (MHz); a requirement, never a cost line",
        important_paths=[f'physical.years."{TARGET_YEAR}".spectrum_to_acquire_mhz'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="per_beam_capacity_vs_naive_cross_check",
        question_answered="Empirical per-beam capacity vs the naive cross-check (Mbps)?",
        jq_expression=(
            f'.physical.years."{TARGET_YEAR}" | '
            "{empirical: .per_beam_capacity_mbps.value, "
            "naive_cross_check: .naive_capacity_mbps.value}"
        ),
        expected_shape="object {empirical, naive_cross_check} Mbps",
        important_paths=[
            f'physical.years."{TARGET_YEAR}".per_beam_capacity_mbps',
            f'physical.years."{TARGET_YEAR}".naive_capacity_mbps',
        ],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="arpu_collectable_ceiling_2036",
        question_answered="What is the collectable per-customer revenue ceiling (ARPU x share)?",
        jq_expression=f'.business.years."{TARGET_YEAR}".arpu_collectable_revenue_usd.value',
        expected_shape="single number (USD/yr)",
        important_paths=[f'business.years."{TARGET_YEAR}".arpu_collectable_revenue_usd'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="validation_warnings",
        question_answered="Which validation results did not pass?",
        jq_expression='[.meta.validation_results[] | select(.severity != "pass")]',
        expected_shape="list of non-passing validation results",
        important_paths=["meta.validation_results"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="trajectory_launches",
        question_answered="What is the per-year launch trajectory?",
        jq_expression=(
            "[.business.years | to_entries[] | "
            "{fy: (.key|tonumber), launches: .value.launches.value}]"
        ),
        expected_shape="list of {fy, launches}",
        important_paths=["business.years"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="living_fleet_per_year",
        question_answered="What is the per-year living fleet by class?",
        jq_expression=(
            "[.business.years | to_entries[] | {fy: (.key|tonumber), "
            "d2c: .value.direct_to_cell_living_fleet.value, "
            "broadband: .value.broadband_living_fleet.value}]"
        ),
        expected_shape="list of {fy, d2c, broadband}",
        important_paths=["business.years"],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="trace_a_cell",
        question_answered="What is the full provenance of the steady-state mid per-customer cost?",
        jq_expression=f'.business.years."{TARGET_YEAR}".cost_annual_per_customer_usd.mid',
        expected_shape="one cell: value, unit, formula, formula_name, uses, sources, source_status",
        important_paths=[f'business.years."{TARGET_YEAR}".cost_annual_per_customer_usd.mid'],
        applies_to=QueryAppliesTo.SPACE,
    ),
    QueryExample(
        name="trace_satellite_cost_breakdown_2036",
        question_answered="What is the direct-to-cell four-area satellite cost breakdown?",
        jq_expression=f'.physical.years."{TARGET_YEAR}".direct_to_cell.cost_breakdown',
        expected_shape="object: the four areas plus minor, build, launch, and satellite total",
        important_paths=[f'physical.years."{TARGET_YEAR}".direct_to_cell.cost_breakdown'],
        applies_to=QueryAppliesTo.SPACE,
    ),
]
"""The comms cold-reader contract: worked jq queries against the promoted space JSON."""


# ---------------------------------------------------------------------------
# The enrichment entry point (the model-copy multi-pass).
# ---------------------------------------------------------------------------


def enrich_comms_output(output: CommsModelOutput) -> CommsModelOutput:
    """Enrich a lean comms output's meta block with the full cold-reader scaffold.

    Takes the in-memory :class:`communications.output.CommsModelOutput` the engine
    returned (with a LEAN ``meta`` block) and returns an enriched copy whose
    ``meta`` block additionally carries the introspection-driven
    ``data_dictionary``, the comms-scoped ``formula_definitions`` catalog, the
    executable ``validation`` rules (via
    :func:`communications.validation.compute_comms_validation`), the public
    ``validation_results``, and the ``query_examples`` cold-reader contract. The
    engine's ``source_status_summary`` and ``schema_version_notes`` are preserved
    unchanged (the comms engine already computed the summary in Phase 3; unlike the
    DC, this enrichment does not recompute it).

    Mirrors the DC :func:`data_center.json_output.build_output` enrichment, adapted
    to the comms lean-engine split: the comms engine assembles the five-key output,
    and THIS function adds the meta scaffold afterward via ``model_copy``. The
    function is a PURE function of the input output (no I/O, no new numbers); it
    only reads cells and assembles the meta scaffold. Emits NO verdict, NO
    conclusion label, NO market-capture, NO heavier-vehicle value.

    Args:
        output: The lean :class:`CommsModelOutput` from the engine.

    Returns:
        A frozen :class:`CommsModelOutput` with an enriched ``meta`` block.
    """
    data_dictionary = build_comms_data_dictionary(CommsModelOutput)
    formula_definitions = _build_formula_definitions()

    # First pass: copy the data dictionary, the formula catalog, and the query
    # examples into the meta, so the validation rules (especially
    # check_data_dictionary_populated) run against the populated dictionary.
    meta_with_scaffold = output.meta.model_copy(
        update={
            "data_dictionary": data_dictionary,
            "formula_definitions": formula_definitions,
            "query_examples": QUERY_EXAMPLES,
        }
    )
    output_with_scaffold = output.model_copy(update={"meta": meta_with_scaffold})

    # Run the executable rules against the data-dictionary-populated output.
    rules = compute_comms_validation(output_with_scaffold)
    meta_with_rules = meta_with_scaffold.model_copy(
        update={"validation": ValidationReport(rules=rules)}
    )
    output_with_rules = output_with_scaffold.model_copy(update={"meta": meta_with_rules})

    # Map the rules to public validation results.
    validation_results = _build_comms_validation_results(output_with_rules)
    final_meta = meta_with_rules.model_copy(update={"validation_results": validation_results})
    return output_with_rules.model_copy(update={"meta": final_meta})


__all__ = [
    "QUERY_EXAMPLES",
    "build_comms_data_dictionary",
    "enrich_comms_output",
]
