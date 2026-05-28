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
years (default 18 months) until the target year is covered.

D-decisions this module rests on:
    D6: the selected Neutron SSO mass-envelope scenario is the sole binding
        constraint; power and volume are derived, not capped.
    D7: 18-month generation cadence (the frontier-gen rule).
    D8: the GPU package is the modelling unit (NVIDIA CES 2026 reversion).
    D12: post-Feynman FLOPS/kW slope = 25%/gen (the extrapolation rule).
    D13: the rack abstraction was killed in the cycle-1 rework.

Sources: brainstorm Part VIII (§42–49), Part X (§50–60). The extend /
frontier helpers' behaviour is pinned by ``tests/test_generations.py``.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Final  # typing-acceptable: Any is the YAML deserialization boundary

import yaml
from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt


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
    confidence tier.
    """

    model_config = ConfigDict(frozen=True)

    doc_path: str = Field(..., description="Path to the source wiki doc.")
    anchor: str | None = Field(None, description="Section / anchor in the doc.")
    quoted_figure: str | None = Field(None, description="The figure as quoted from the source.")
    sourcing: SourcingClass = Field(..., description="FACT / ESTIMATE / EXTRAPOLATION.")


class GenerationSpec(BaseModel):
    """One GPU package generation — NVIDIA's 'as sold' unit at a point in time.

    All per-package physical values are **all-in / full-system** — the
    package's share of system electrical and mass including networking,
    cooling, sled, NVLink fabric (not bare die TDP).
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Human label, e.g. 'B300/GB300'.")
    year_available: float = Field(
        ...,
        description="Approximate calendar year of availability.",
        ge=2020.0,
        le=2050.0,
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
    generation).
    """

    model_config = ConfigDict(frozen=True)

    usd_growth_per_gen: float = Field(
        0.30,
        description="$/pkg growth per generation.",
        ge=-0.5,
        le=2.0,
    )
    kw_growth_per_gen: float = Field(
        0.20,
        description=(
            "kW/pkg growth per generation. 0.20 — per-package power "
            "growth/gen; corrected from 0.30 (assembly-rate misapplied) "
            "per validation V-A, sourcing_audit_05_21.md. The 0.30 figure "
            "was the historical assembly-level package-power growth rate, "
            "which grew that fast only because more packages were added "
            "per assembly; applied per-package it double-counts."
        ),
        ge=-0.5,
        le=2.0,
    )
    kg_growth_per_gen: float = Field(
        -0.10,
        description=("kg/pkg growth per generation (negative = denser packaging)."),
        ge=-0.5,
        le=2.0,
    )
    pf_growth_per_gen: float = Field(
        0.625,
        description=(
            "PF/pkg growth per generation. Default 0.625 → implied PF/kW slope ≈ 25%/gen."
        ),
        ge=-0.5,
        le=2.0,
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


def extend_generations(
    known: list[GenerationSpec],
    slopes: GenerationSlopes,
    cadence_yr: float,
    target_yr: float,
) -> list[GenerationSpec]:
    """Extend the list with extrapolated generations until ``target_yr`` is covered.

    Starting from the last entry in ``known``, repeatedly append a new
    extrapolated generation spaced ``cadence_yr`` years apart, applying the
    multiplicative :class:`GenerationSlopes`, until the next generation
    would fall past ``target_yr``.

    The extrapolated generations inherit the last known generation's
    ``die_count`` (held constant — die-stacking projections beyond Feynman
    are not part of the research and would over-extrapolate). Their
    ``source.sourcing`` is :class:`SourcingClass.EXTRAPOLATION`.

    Args:
        known: The known generations (typically :data:`KNOWN_GENS`).
        slopes: The per-generation growth slopes.
        cadence_yr: Years between successive generations (default 1.5 →
            18 months, the D7 generation cadence).
        target_yr: Latest fiscal year that needs coverage.

    Returns:
        A new list — the known generations followed by zero or more
        extrapolated generations. The input ``known`` list is not mutated.

    Raises:
        ValueError: If ``known`` is empty (no anchor to extend from).
    """
    if not known:
        raise ValueError("extend_generations requires at least one known generation")

    out: list[GenerationSpec] = list(known)
    i = 1
    while out[-1].year_available + cadence_yr <= target_yr:
        last = out[-1]
        out.append(
            GenerationSpec(
                name=f"Gen+{i}(extrap)",
                year_available=last.year_available + cadence_yr,
                usd_per_pkg=int(last.usd_per_pkg * (1 + slopes.usd_growth_per_gen)),
                kw_per_pkg=last.kw_per_pkg * (1 + slopes.kw_growth_per_gen),
                kg_per_pkg=last.kg_per_pkg * (1 + slopes.kg_growth_per_gen),
                pf_per_pkg=last.pf_per_pkg * (1 + slopes.pf_growth_per_gen),
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
    list of generation-spec dicts. Each entry is validated via Pydantic;
    validation errors surface as :class:`pydantic.ValidationError`.

    Args:
        path: Input file path.

    Returns:
        The list of validated :class:`GenerationSpec` instances.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ValueError: If the YAML root is not a mapping, or the top-level
            key is missing, or the value is not a list.
    """
    with path.open("r", encoding="utf-8") as fh:
        loaded: Any = yaml.safe_load(fh)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping, got {type(loaded).__name__}")
    if GENERATIONS_YAML_KEY not in loaded:
        raise ValueError(f"{path}: missing top-level key '{GENERATIONS_YAML_KEY}'")
    entries: Any = loaded[GENERATIONS_YAML_KEY]
    if not isinstance(entries, list):
        raise ValueError(
            f"{path}: '{GENERATIONS_YAML_KEY}' must be a list, got {type(entries).__name__}"
        )
    return [GenerationSpec.model_validate(entry) for entry in entries]


def frontier_at(year: float, gens: list[GenerationSpec]) -> GenerationSpec:
    """Return the latest generation available at ``year``.

    Picks the maximum-``year_available`` entry in ``gens`` whose
    ``year_available <= year``.

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
    available = [g for g in gens if g.year_available <= year]
    if not available:
        raise NoFrontierAvailableError(
            f"no generation available at year {year} (candidates: {[g.name for g in gens]})"
        )
    return max(available, key=lambda g: g.year_available)
