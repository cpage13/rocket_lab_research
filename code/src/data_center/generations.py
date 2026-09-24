"""Per-generation GPU package specification — the typed input layer.

This module defines :class:`GenerationSpec`, the typed Pydantic model for one
GPU package generation (NVIDIA's "as sold" unit at a point in time), the
:data:`KNOWN_GENS` list of five sourced generations (B200 → Feynman), the
:class:`GenerationSlopes` per-generation growth knobs, and helpers to extend
the list to a target year (:func:`extend_generations`) and to pick the
frontier generation at a given fiscal year (:func:`frontier_at`).

The package is the only modelling unit — the rack abstraction was removed
entirely in the cycle-1 GPU-first rework (D8 GPU = package; D13 kill rack
abstraction). Per-package values (``kw_per_pkg``, ``kg_per_pkg``,
``pf_per_pkg``) are **all-in** — the package's full share of system
electrical and mass including networking, cooling, sled, NVLink fabric.

Per-generation source values are grounded in the durable research corpus,
especially ``research/ai_hardware/gpu_generational_roadmap.md`` and the
claim-status ledger in ``research/SOURCE_INDEX.md``. The five known
generations are classed FACT (B200/GB200, B300/GB300), ESTIMATE (Rubin
VR200, Rubin Ultra), or EXTRAPOLATION (Feynman). Generations beyond Feynman
are extrapolated by applying :class:`GenerationSlopes` every ``cadence_yr``
years (default 18 months) until the target year is covered. The k-th
extrapolated generation lands at ``latest.year_available + k x cadence_yr``
(computed, not accumulated), and :func:`frontier_at` compares availability
with :data:`FRONTIER_YEAR_TOLERANCE` so a generation due exactly in a fiscal
year flies that year despite float rounding.

D-decisions this module rests on:
    D6: the selected Neutron SSO mass-envelope scenario is the sole binding
        constraint; power and volume are derived, not capped.
    D7: 18-month generation cadence (the frontier-gen rule).
    D8: the GPU package is the modelling unit (NVIDIA CES 2026 reversion).
    D12: post-Feynman FLOPS/kW slope = 25%/gen (the extrapolation rule).
    D13: the rack abstraction was killed in the cycle-1 rework.

Sources: brainstorm Part VIII (§42–49), Part X (§50–60). The extend /
frontier helpers' behaviour is pinned by ``tests/data_center/test_generations.py``.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Any, Final  # typing-acceptable: Any is the YAML deserialization boundary

import yaml
from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt

from common.file_io import ModelFileError, load_yaml_mapping
from data_center.constants import (
    GENERATION_SLOPE_MAX,
    GENERATION_SLOPE_MIN,
    KG_GROWTH_PER_GEN_DEFAULT,
    KW_GROWTH_PER_GEN_DEFAULT,
    MAX_FY,
    MIN_FY,
    PF_GROWTH_PER_GEN_DEFAULT,
    USD_GROWTH_PER_GEN_DEFAULT,
)

logger = logging.getLogger(__name__)

FRONTIER_YEAR_TOLERANCE: Final[float] = 1e-9
"""Slack, in years, when comparing a generation's ``year_available`` with a
fiscal year. Extrapolated availability years are float sums of the release
cadence, so a generation due exactly in a year can land a few ulps past it
(``2029.0 + 1.4 + 1.4 + 1.4 + 1.4 + 1.4`` is ``2036.0000000000005``). A
nanoyear is far below any calendar meaning and far above float error at
these magnitudes, so a due generation always flies in its year."""


class SourcingClass(StrEnum):
    """Source-confidence tier for a per-generation value.

    FACT: real-world, multi-source corroboration (e.g. shipping or
    publicly-disclosed NVIDIA generations).

    ESTIMATE: research-doc estimate based on partial disclosures or
    industry analyst consensus.

    EXTRAPOLATION: the research's own projection, typically for ~2030+ where
    no public roadmap exists.
    """

    FACT = "fact"
    ESTIMATE = "estimate"
    EXTRAPOLATION = "extrapolation"


class Source(BaseModel):
    """Structured reference for a sourced figure.

    Carries the path to the source wiki doc, an optional anchor/section,
    an optional quoted figure as it appears in the source, and the
    confidence tier. ``extra="forbid"``: a typo in a scenario's source
    block fails loudly.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    doc_path: str = Field(..., description="Path to the source wiki doc.")
    anchor: str | None = Field(None, description="Section / anchor in the doc.")
    quoted_figure: str | None = Field(None, description="The figure as quoted from the source.")
    sourcing: SourcingClass = Field(..., description="FACT / ESTIMATE / EXTRAPOLATION.")


class GenerationSpec(BaseModel):
    """One GPU package generation — NVIDIA's 'as sold' unit at a point in time.

    All per-package physical values are **all-in / full-system** — the
    package's share of system electrical and mass including networking,
    cooling, sled, NVLink fabric (not bare die TDP). ``year_available`` is
    bounded by the same fiscal-year limits as the run window
    (:data:`data_center.constants.MIN_FY` to :data:`~data_center.constants.MAX_FY`),
    so every window the config accepts can be covered by extrapolation.
    ``extra="forbid"``: a typo in a scenario's generation entry fails loudly.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., description="Human label, e.g. 'B300/GB300'.")
    year_available: float = Field(
        ...,
        description="Approximate calendar year of availability.",
        ge=MIN_FY,
        le=MAX_FY,
    )
    usd_per_pkg: PositiveInt = Field(..., description="Real per-package price in $.")
    kw_per_pkg: PositiveFloat = Field(
        ...,
        description=("All-in package electrical kW (incl. networking + cooling). NOT bare TDP."),
    )
    kg_per_pkg: PositiveFloat = Field(
        ...,
        description=("All-in package mass kg (incl. NVLink fabric, sled, cold plates)."),
    )
    pf_per_pkg: PositiveFloat = Field(..., description="Dense FP4 PFLOPS per package.")
    die_count: PositiveInt = Field(..., description="Number of dies on the package.")
    source: Source = Field(..., description="Structured source reference.")


class GenerationSlopes(BaseModel):
    """Per-generation post-Feynman growth slopes (every ~18 months).

    Applied multiplicatively by :func:`extend_generations` when projecting
    beyond the last known generation. All slopes are gen-relative
    (e.g. ``0.30`` means +30% per generation; ``-0.10`` means -10% per
    generation). The field defaults are the single source of the default
    slopes (the named constants in :mod:`data_center.constants`), so
    ``GenerationSlopes()`` is the default slope set. ``extra="forbid"``: a
    typo in a scenario's ``slopes`` block fails loudly.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    usd_growth_per_gen: float = Field(
        default=USD_GROWTH_PER_GEN_DEFAULT,
        description="$/pkg growth per generation.",
        ge=GENERATION_SLOPE_MIN,
        le=GENERATION_SLOPE_MAX,
    )
    kw_growth_per_gen: float = Field(
        default=KW_GROWTH_PER_GEN_DEFAULT,
        description=(
            "kW/pkg growth per generation. 0.20, per-package power "
            "growth/gen; corrected from 0.30 (assembly-rate misapplied) "
            "per validation V-A, sourcing_audit_05_21.md. The 0.30 figure "
            "was the historical assembly-level package-power growth rate, "
            "which grew that fast only because more packages were added "
            "per assembly; applied per-package it double-counts."
        ),
        ge=GENERATION_SLOPE_MIN,
        le=GENERATION_SLOPE_MAX,
    )
    kg_growth_per_gen: float = Field(
        default=KG_GROWTH_PER_GEN_DEFAULT,
        description=("kg/pkg growth per generation (negative = denser packaging)."),
        ge=GENERATION_SLOPE_MIN,
        le=GENERATION_SLOPE_MAX,
    )
    pf_growth_per_gen: float = Field(
        default=PF_GROWTH_PER_GEN_DEFAULT,
        description=(
            "PF/pkg growth per generation. Default 0.625 → implied PF/kW slope ≈ 25%/gen."
        ),
        ge=GENERATION_SLOPE_MIN,
        le=GENERATION_SLOPE_MAX,
    )


DEFAULT_GENERATIONS_DOC: Final[str] = "research/ai_hardware/gpu_generational_roadmap.md"
"""Default durable research source doc for bundled :data:`KNOWN_GENS` entries."""


KNOWN_GENS: Final[list[GenerationSpec]] = [
    GenerationSpec(
        name="B200/GB200",
        year_available=2024.5,
        usd_per_pkg=50_000,
        kw_per_pkg=1.75,
        kg_per_pkg=18.9,
        pf_per_pkg=9.0,
        die_count=2,
        source=Source(
            doc_path=DEFAULT_GENERATIONS_DOC,
            anchor=None,
            quoted_figure=None,
            sourcing=SourcingClass.FACT,
        ),
    ),
    GenerationSpec(
        name="B300/GB300",
        year_available=2025.5,
        usd_per_pkg=70_000,
        kw_per_pkg=2.05,
        kg_per_pkg=18.9,
        pf_per_pkg=15.0,
        die_count=2,
        source=Source(
            doc_path=DEFAULT_GENERATIONS_DOC,
            anchor=None,
            quoted_figure=None,
            sourcing=SourcingClass.FACT,
        ),
    ),
    GenerationSpec(
        name="Rubin VR200",
        year_available=2026.5,
        usd_per_pkg=70_000,
        kw_per_pkg=2.60,
        kg_per_pkg=23.0,
        pf_per_pkg=34.0,
        die_count=2,
        source=Source(
            doc_path=DEFAULT_GENERATIONS_DOC,
            anchor=None,
            quoted_figure=None,
            sourcing=SourcingClass.ESTIMATE,
        ),
    ),
    GenerationSpec(
        name="Rubin Ultra",
        year_available=2027.5,
        usd_per_pkg=180_000,
        kw_per_pkg=4.17,
        kg_per_pkg=22.0,
        pf_per_pkg=52.0,
        die_count=4,
        source=Source(
            doc_path=DEFAULT_GENERATIONS_DOC,
            anchor=None,
            quoted_figure=None,
            sourcing=SourcingClass.ESTIMATE,
        ),
    ),
    GenerationSpec(
        name="Feynman",
        year_available=2029.0,
        usd_per_pkg=225_000,
        kw_per_pkg=5.50,
        kg_per_pkg=10.0,
        pf_per_pkg=100.0,
        die_count=8,
        source=Source(
            doc_path=DEFAULT_GENERATIONS_DOC,
            anchor=None,
            quoted_figure=None,
            sourcing=SourcingClass.EXTRAPOLATION,
        ),
    ),
]
"""The five sourced GPU generations covering FY2024.5–FY2029.

Origin: ``research/ai_hardware/gpu_generational_roadmap.md`` (numerical
values), with claim-status cross-checks in ``research/SOURCE_INDEX.md``.

The exact values **must** match the sourced generation table in this module and
the source ledger; this is tested by the parity test in
``tests/test_generations.py``.
"""


class NoFrontierAvailableError(ValueError):
    """No GPU generation is available at the requested year.

    Raised by :func:`frontier_at` when no entry in the supplied
    ``gens`` list has ``year_available <= year``. Common causes are an
    empty list, or a year earlier than the earliest known generation.
    """


def validate_generation_order(gens: Sequence[GenerationSpec]) -> None:
    """Fail loudly unless ``gens`` is non-empty and strictly ascending by year.

    The frontier rule and the extrapolation both read the list as a roadmap:
    the last entry is the latest generation, the one extrapolation extends
    from. A newest-first or shuffled list would silently extrapolate from an
    older generation, and two entries with the same ``year_available`` would
    make the frontier choice ambiguous. Used by the config validator (load
    time) and by :func:`extend_generations` (API callers).

    Args:
        gens: The generation list to check.

    Raises:
        ValueError: If ``gens`` is empty, or any entry's ``year_available`` is
            not strictly greater than the previous entry's.
    """
    if not gens:
        raise ValueError("the generations list needs at least one generation")
    for prev, nxt in zip(gens, gens[1:], strict=False):
        if nxt.year_available <= prev.year_available:
            raise ValueError(
                "generations must be listed oldest first with strictly increasing "
                f"year_available: {nxt.name!r} ({nxt.year_available}) follows "
                f"{prev.name!r} ({prev.year_available})"
            )


def extend_generations(
    known: list[GenerationSpec],
    slopes: GenerationSlopes,
    cadence_yr: float,
    target_yr: float,
) -> list[GenerationSpec]:
    """Extend the list with extrapolated generations until ``target_yr`` is covered.

    Starting from the latest entry in ``known`` (its last entry: the list must
    be ordered, see :func:`validate_generation_order`), append extrapolated
    generations while the next one is due by ``target_yr``. The k-th
    extrapolated generation is available at
    ``latest.year_available + k x cadence_yr``, computed from the latest known
    year rather than accumulated step by step, so float error does not grow
    with k; the due test uses :data:`FRONTIER_YEAR_TOLERANCE`. Each step
    applies the multiplicative :class:`GenerationSlopes` to the previous
    generation's values: kW, kg, and PF compound to
    ``latest x (1 + slope) ** k`` up to float rounding, while the USD price
    is truncated to a whole dollar at every step, so the k-th price can sit a
    few dollars below ``latest x (1 + slope) ** k``.

    A very short release cadence needs many extrapolated generations to reach
    ``target_yr``, and compounding the slopes that many times can exceed the
    largest representable float (``release_cadence_yr`` 0.001 needs thousands
    of generations to cover the default window). The extension stops at the
    first value that is no longer finite and raises a ``ValueError`` saying
    so, instead of carrying an infinite value into the model or crashing on
    it.

    The extrapolated generations inherit the last known generation's
    ``die_count`` (held constant — die-stacking projections beyond Feynman
    are not part of the research and would over-extrapolate). Their
    ``source.sourcing`` is :class:`SourcingClass.EXTRAPOLATION`.

    Args:
        known: The known generations (typically :data:`KNOWN_GENS`), ordered
            oldest first with strictly increasing ``year_available``.
        slopes: The per-generation growth slopes.
        cadence_yr: Years between successive generations (default 1.5 →
            18 months, the D7 generation cadence).
        target_yr: Latest fiscal year that needs coverage.

    Returns:
        A new list — the known generations followed by zero or more
        extrapolated generations. The input ``known`` list is not mutated.

    Raises:
        ValueError: If ``known`` is empty (no anchor to extend from), is not
            strictly ascending by ``year_available``, or the extension
            compounds a per-package value past the largest representable
            float.
    """
    if not known:
        raise ValueError("extend_generations requires at least one known generation")
    validate_generation_order(known)

    out: list[GenerationSpec] = list(known)
    latest_year = known[-1].year_available
    i = 1
    while latest_year + i * cadence_yr <= target_yr + FRONTIER_YEAR_TOLERANCE:
        last = out[-1]
        usd = last.usd_per_pkg * (1 + slopes.usd_growth_per_gen)
        kw = last.kw_per_pkg * (1 + slopes.kw_growth_per_gen)
        kg = last.kg_per_pkg * (1 + slopes.kg_growth_per_gen)
        pf = last.pf_per_pkg * (1 + slopes.pf_growth_per_gen)
        if not all(math.isfinite(value) for value in (usd, kw, kg, pf)):
            needed = math.floor((target_yr + FRONTIER_YEAR_TOLERANCE - latest_year) / cadence_yr)
            raise ValueError(
                f"the generation extension overflows: a release cadence of {cadence_yr:g} "
                f"years needs about {needed} extrapolated generations to reach FY"
                f"{target_yr:g}, and compounding the growth slopes {i} times already "
                "exceeds the largest representable number; lengthen "
                "gospel.release_cadence_yr or reduce the generation slopes"
            )
        out.append(
            GenerationSpec(
                name=f"Gen+{i}(extrap)",
                year_available=latest_year + i * cadence_yr,
                usd_per_pkg=int(usd),
                kw_per_pkg=kw,
                kg_per_pkg=kg,
                pf_per_pkg=pf,
                die_count=last.die_count,
                source=Source(
                    doc_path=DEFAULT_GENERATIONS_DOC,
                    anchor=None,
                    quoted_figure=None,
                    sourcing=SourcingClass.EXTRAPOLATION,
                ),
            )
        )
        i += 1
    return out


GENERATIONS_YAML_KEY: Final[str] = "generations"
"""Top-level YAML key wrapping the list of generation specs."""


def dump_generations_yaml(gens: list[GenerationSpec], path: Path) -> None:
    """Serialise a generation list to YAML on disk.

    Writes a single top-level mapping ``{GENERATIONS_YAML_KEY: [...]}`` so
    the file can carry future top-level metadata without breaking the
    schema.

    Args:
        gens: The generations to serialise.
        path: Output file path.
    """
    payload: dict[str, list[dict[str, Any]]] = {
        GENERATIONS_YAML_KEY: [g.model_dump(mode="json") for g in gens]
    }
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, sort_keys=False, indent=2)


def load_generations_yaml(path: Path) -> list[GenerationSpec]:
    """Load a list of :class:`GenerationSpec` from a YAML file on disk.

    Expects the file to contain a top-level mapping with key
    ``GENERATIONS_YAML_KEY`` (``"generations"``) and a value that is a
    list of generation-spec mappings, read through the shared
    :func:`common.file_io.load_yaml_mapping`. Each entry is validated via
    Pydantic.

    Args:
        path: Input file path.

    Returns:
        The list of validated :class:`GenerationSpec` instances.

    Raises:
        common.file_io.ModelFileError: If the file is missing, unreadable,
            or malformed, its root is not a mapping, the top-level key is
            missing, or its value is not a list.
        pydantic.ValidationError: If an entry is not a valid generation spec.
    """
    loaded = load_yaml_mapping(path)
    if GENERATIONS_YAML_KEY not in loaded:
        raise ModelFileError(path, f"missing top-level key '{GENERATIONS_YAML_KEY}'")
    entries: Any = loaded[GENERATIONS_YAML_KEY]
    if not isinstance(entries, list):
        raise ModelFileError(
            path, f"'{GENERATIONS_YAML_KEY}' must be a list, got {type(entries).__name__}"
        )
    logger.debug("loaded %d generation entries from %s", len(entries), path)
    return [GenerationSpec.model_validate(entry) for entry in entries]


def frontier_at(year: float, gens: list[GenerationSpec]) -> GenerationSpec:
    """Return the latest generation available at ``year``.

    Picks the maximum-``year_available`` entry in ``gens`` whose
    ``year_available <= year`` (within :data:`FRONTIER_YEAR_TOLERANCE`, so a
    generation whose float availability year lands a few ulps past ``year``
    still counts as available that year).

    Args:
        year: The fiscal year of interest.
        gens: Candidate generations (typically the output of
            :func:`extend_generations`).

    Returns:
        The frontier generation at ``year``.

    Raises:
        NoFrontierAvailableError: If ``gens`` is empty or no entry has
            ``year_available <= year``.
    """
    available = [g for g in gens if g.year_available <= year + FRONTIER_YEAR_TOLERANCE]
    if not available:
        raise NoFrontierAvailableError(
            f"no generation available at year {year} (candidates: {[g.name for g in gens]})"
        )
    return max(available, key=lambda g: g.year_available)
