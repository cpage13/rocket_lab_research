"""Output assembly for :class:`SpaceModelOutput`: the space artifact and its data dictionary.

One responsibility, the assembly (the artifact is serialized by the shared
:func:`common.file_io.render_artifact_json`):

* :func:`build_output`: assemble the complete space artifact, a
  :class:`SpaceModelOutput`, from a :class:`data_center.config.ValuationConfig`,
  the extended generation list, and the per-year ``physical`` / ``business``
  maps the engine computes. The engine's :func:`data_center.engine.run_valuation`
  delegates the assembly to this function (plan § 5 T51/T52).
* The space artifact's data dictionary is built by the shared walker,
  :func:`common.meta.build_data_dictionary`, which :func:`build_output` runs on
  the assembled artifact. The dictionary is *generated*, not hand-maintained: a
  cell's unit is read from the cell itself, a non-cell field's unit from its
  declaration.

The ``meta.query_examples`` block (the cold-reader contract) is the
fixed 12-entry list :func:`data_center.query_examples.build_query_examples`
builds for the run's anchor year; :func:`build_output` places it at
``meta.query_examples`` in every emitted :class:`SpaceModelOutput`.

``meta.validation_results`` is built by
:func:`data_center.validation.build_validation_results` (every V-rule, the
model invariants, and, for the canonical default only, the default guards);
its anchor-year checks read the run's anchor year
(:func:`data_center.config.anchor_year`), never a hardcoded calendar year.
"""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version
from typing import Final

from common.meta import (
    FormulaDefinition,
    ValidationReport,
    build_data_dictionary,
    summarize_source_statuses,
)
from common.provenance import FORMULAS, YearString
from data_center.config import ValuationConfig, anchor_year
from data_center.constants import USD_PER_MUSD
from data_center.generations import GenerationSpec
from data_center.input_manifest import build_input_manifest, generation_source_status
from data_center.output import (
    SCHEMA_VERSION,
    ArtifactRole,
    BusinessBlock,
    BusinessYear,
    GenerationSummary,
    MetaBlock,
    PhysicalBlock,
    PhysicalYear,
    RunMetadata,
    SpaceModelOutput,
)
from data_center.query_examples import build_query_examples
from data_center.validation import build_validation_results, compute_validation

logger = logging.getLogger(__name__)

MODEL_PACKAGE_NAME: Final[str] = "rklb-value"

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


def _build_formula_definitions() -> list[FormulaDefinition]:
    """Build public formula metadata from the authoritative formula table.

    One entry per :data:`common.provenance.FORMULAS` entry, sorted by formula
    id: the space-model formulas and the ground-reference formulas the ground
    artifact's cells cite.
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
    ]


# ---------------------------------------------------------------------------
# Space artifact assembly
# ---------------------------------------------------------------------------


def build_output(
    *,
    config: ValuationConfig,
    extended_gens: list[GenerationSpec],
    physical_by_year: dict[YearString, PhysicalYear],
    business_by_year: dict[YearString, BusinessYear],
    generated_at: str,
    source_scenario_path: str,
    artifact_role: ArtifactRole = ArtifactRole.DRAFT,
) -> SpaceModelOutput:
    """Assemble the complete space artifact, a :class:`SpaceModelOutput`.

    The engine computes the per-year ``physical`` / ``business`` maps and
    calls this function to wrap them in the five-block artifact, building
    the ``metadata`` / ``inputs`` / ``meta`` blocks and running the
    validation rules against the assembled output.

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
        The frozen space artifact, with the validation report computed
        against the assembled artifact.
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
            f"{SCHEMA_VERSION} space output: the typed input manifest, source-status "
            "summary, formula definitions, validation_results, and query examples. "
            "Since v8 the duplicate business.years[].kw_on_orbit and pf_on_orbit are "
            "gone (read kw_living_fleet and pf_living_fleet) and the data dictionary's "
            "source_class is lowercase."
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


__all__ = ["build_output"]
