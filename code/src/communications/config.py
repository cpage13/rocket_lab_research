"""The dial schema and YAML loader for the communications CELLULAR cost model.

This module defines the INPUT contract of the slim, roughly 6-variable
cost-to-serve model for a Rocket Lab Neutron-launched CELLULAR direct-to-cell
(satellite-to-phone) constellation. It mirrors the data-center model's config
shape: a top-level frozen :class:`CommsConfig` (``extra="forbid"``) whose nested
blocks are each their own frozen ``extra="forbid"`` BaseModel, every field with a
named-constant default so a no-argument construct is fully valid, plus the
``comms_config_from_dict`` / ``load_comms_config`` YAML loader pair. Nothing here
computes a cost, a coverage fraction, a subscriber count, or a comparison; it is
the contract the engine (Phase 2), the coverage->subscribers logic (Phase 3), the
ground comparison (Phase 4), and the light output (Phase 5) consume.

The product is CELLULAR (the subscriber unit is a PERSON, a phone subscriber, NOT
a household). It is NOT a market-share, demand, or revenue/DCF model. The blocks:

* ``metadata: CommsMetadataDials`` -- base year, horizon, scenario name.
* ``cadence: CadenceDials`` -- the shared whole-fleet logistic launch ramp
  (the DC shape, REUSED verbatim: ceiling 150, year-5 14, year-10 90, first 1).
  This prices the launch cost at the whole-fleet cadence (variable 2's ramp).
* ``comms_cadence: CommsCadenceDials`` -- the comms slice's SHARE of the fleet
  cadence (variable 2's share); how many launches comms flies.
* ``launch_cost: LaunchCostDials`` -- the cadence-indexed log-linear launch-cost
  curve (the DC shape, REUSED verbatim: 25.0 / 13.5 / 5.0 / 100.0) (variable 6).
* ``satellite: SatelliteDials`` -- the fixed CELLULAR-satellite spec: satellites
  per launch (variable 1), lifetime (variable 4, the cohort cliff), and the flat
  mass-manufactured hardware build cost (variable 5).
* ``coverage: CoverageDials`` -- the NEW constellation-size target the build-out
  fills toward (variable 3).
* ``subscribers: SubscriberDials`` -- the per-PERSON denominator basis (Phase 3
  consumes this): the served-PERSON count at full coverage plus an optional direct
  override.
* ``ground: GroundInterfaceDials | None`` -- the marked, TWO-REGIME ground
  INTERFACE (Phase 4), default ``None`` so the cost side never blocks on a ground
  number. The dense + sparse baselines are individually None-able caller inputs.

This model imports only from ``common.*`` and ``communications.*`` (never
``data_center``, per the cross-import guard) and uses none of the forbidden
demand-side tokens. YAML loading: scenario files are YAML mappings whose top-level
keys are the block names above, all optional (omitted = defaults). ``extra="forbid"``
means a typo in a scenario file fails loudly.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from communications.constants import (
    BASE_YEAR_DEFAULT,
    CADENCE_CEILING_DEFAULT,
    COMMS_SHARE_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    GROUND_BASIS_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    HORIZON_YEARS_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    MAX_FY,
    MAX_HORIZON_YEARS,
    MIN_FY,
    MIN_HORIZON_YEARS,
    SATELLITE_BUILD_COST_MUSD_DEFAULT,
    SATELLITE_LIFETIME_YEARS_DEFAULT,
    SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
    SATELLITES_PER_LAUNCH_DEFAULT,
    SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
)

logger = logging.getLogger(__name__)

# ===========================================================================
# 1. Dial blocks (each its own frozen, extra-forbid BaseModel)
# ===========================================================================


class CommsMetadataDials(BaseModel):
    """Run metadata: base year, analysis horizon, and the scenario label.

    Mirrors the DC ``MetadataConfig`` base-year / horizon pattern (both REQUIRED,
    no field default; the all-defaults construct supplies them via the
    :func:`_default_comms_metadata` factory). The DC-specific enums (workload,
    operator, radiator architecture) are DROPPED: the satellite is a fixed spec
    with no workload/operator/radiator taxonomy.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    base_year: int = Field(
        ge=MIN_FY,
        le=MAX_FY,
        description="Calendar year corresponding to model year 0 (Neutron first-flight year).",
    )
    horizon_years: int = Field(
        ge=MIN_HORIZON_YEARS,
        le=MAX_HORIZON_YEARS,
        description="Number of fiscal-year steps after year 0 (base_year + horizon = final year).",
    )
    scenario_name: str = Field(
        default="Comms cellular direct-to-cell (central case)",
        description="Human-readable scenario label, surfaced in the output metadata.",
    )


class CadenceDials(BaseModel):
    """Whole-fleet launch-cadence dials feeding the shared logistic ramp.

    REUSED VERBATIM from the DC ``CadenceDials`` shape (same field names, same
    bounds, same named-constant defaults sourced from the shared
    ``common.cadence`` spine). This is the WHOLE-FLEET Neutron cadence (the 90/year
    FY2036 ramp) that prices the launch cost; the comms slice flies a SHARE of it
    (see :class:`CommsCadenceDials`). Consumed by
    ``common.cadence.compute_launches_per_year``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    cadence_ceiling: int = Field(
        default=CADENCE_CEILING_DEFAULT,
        gt=0,
        description="Hard cap on whole-number launches per year.",
    )
    launches_at_year_5: int = Field(
        default=LAUNCHES_AT_YEAR_5_DEFAULT,
        ge=0,
        description="Integer logistic anchor: launches per year at model year 5.",
    )
    launches_at_year_10: int = Field(
        default=LAUNCHES_AT_YEAR_10_DEFAULT,
        ge=0,
        description="Integer logistic anchor: launches per year at model year 10.",
    )
    first_launch_year: int = Field(
        default=FIRST_LAUNCH_YEAR_DEFAULT,
        ge=0,
        description="Model-year index before which launch count is clamped to zero.",
    )


class CommsCadenceDials(BaseModel):
    """The comms slice's SHARE of the whole-fleet cadence (variable 2's share).

    The whole-fleet cadence (:class:`CadenceDials`) ramps to 90 launches/year by
    FY2036; the comms constellation flies a SHARE of those launches. Phase 2
    multiplies the shared per-year integer launch count by ``share_of_fleet`` and
    re-rounds to an integer (with the shared half-up offset) to get the comms
    launches flown per year. The launch COST is still priced at the whole-fleet
    cadence (the cost-down is a Neutron-production-scale effect, shared), not at
    the comms slice's own cadence.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    share_of_fleet: float = Field(
        default=COMMS_SHARE_DEFAULT,
        gt=0,
        le=1.0,
        description=(
            "Comms fraction of the whole-fleet per-year launch count. FOUNDER_SET "
            "to 0.18 (~16 of the 90 FY2036 launches/year); the founder's ~15 to 20 "
            "band maps to ~0.167 to ~0.222. Configurable."
        ),
    )


class LaunchCostDials(BaseModel):
    """Cadence-indexed launch-cost dials feeding the log-linear cost curve.

    REUSED VERBATIM from the DC ``LaunchCostDials`` shape (same field names, same
    bounds, same named-constant defaults from the shared ``common.cadence`` spine).
    The cost is priced at the WHOLE-FLEET cadence. Consumed by
    ``common.cadence.compute_launch_cost_musd``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    low_cadence_cost_musd: float = Field(
        default=LOW_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the low-cadence anchor, $M.",
    )
    high_cadence_cost_musd: float = Field(
        default=HIGH_CADENCE_COST_MUSD_DEFAULT,
        gt=0,
        description="Launch cost at the high-cadence anchor, $M.",
    )
    low_cadence_launches: float = Field(
        default=LOW_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the low-cost anchor.",
    )
    high_cadence_launches: float = Field(
        default=HIGH_CADENCE_LAUNCHES_DEFAULT,
        gt=0,
        description="Cadence (launches/yr) at the high-cost anchor.",
    )


class SatelliteDials(BaseModel):
    """The fixed CELLULAR direct-to-cell satellite spec (variables 1, 4, 5).

    The satellite is a flat mass-manufactured satellite-to-phone bird (a fixed
    spec, NOT a re-spec'd frontier generation, so the DC ``generations`` /
    ``slopes`` engine is dropped). Three dials: satellites per launch (a direct
    input), the operating life (the cohort cliff), and the one flat hardware
    build-cost scalar.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    satellites_per_launch: int = Field(
        default=SATELLITES_PER_LAUNCH_DEFAULT,
        ge=1,
        le=16,
        description=(
            "Satellites per Neutron launch, a DIRECT input scalar (12 default, up "
            "to 16). Mass-bound count for a Flatellite-class bird: ~12 (SSO), ~16 "
            "(LEO). Source COMM-258 / COMM-260."
        ),
    )
    satellite_lifetime_years: int = Field(
        default=SATELLITE_LIFETIME_YEARS_DEFAULT,
        ge=1,
        le=20,
        description=(
            "Satellite operating life in years, the cohort cliff: after this a "
            "cohort retires and contributes zero coverage. ~5-year Starlink "
            "replacement anchor (COMM-091), a design assumption not a certified "
            "field life."
        ),
    )
    satellite_build_cost_musd: float = Field(
        default=SATELLITE_BUILD_COST_MUSD_DEFAULT,
        gt=0,
        description=(
            "The flat MASS-MANUFACTURED CELLULAR-SATELLITE HARDWARE cost, ONE "
            "scalar, ~$1.0 to 1.1M (FOUNDER_SET 1.05). A V3-class hardware analogy "
            "(Starlink V3 ~$1.2M, the upper anchor, COMM-080) for a direct-to-cell "
            "payload (bigger antenna and more power than a broadband panel, far "
            "smaller than AST's giant array, so AST ~$19 to 21M is the WRONG "
            "anchor). A hardware build-cost analogy, NOT a broadband-product claim. "
            "Configurable."
        ),
    )


class CoverageDials(BaseModel):
    """The NEW constellation-size coverage target (variable 3).

    The build-out fills toward ``satellites_for_full_coverage`` satellites on
    orbit; the coverage fraction reached each year (Phase 2) drives the
    coverage-driven subscriber count (Phase 3). This dial exists in NO current
    model. The ELEVATION MASK is the underlying physical dial (this default is the
    25-degree quality-link, populated-band, 95%-coverage figure).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    satellites_for_full_coverage: int = Field(
        default=SATELLITES_FOR_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "Constellation-size target the build-out fills toward. FOUNDER_SET to "
            "340: the quality-link case (25 degree elevation mask, populated "
            "mid-latitude band +/-55 deg at 95%, ~450 km, ~53 deg). Coverage sim "
            "(.agent/other/coverage_sim/FINDINGS.md: 341, rounded to 340) plus "
            "COMM-209 / COMM-216 / COMM-217 and COMM-386..COMM-405. Configurable."
        ),
    )


class SubscriberDials(BaseModel):
    """The per-PERSON denominator basis for the cellular cost per subscriber.

    The unit is a PERSON (a phone subscriber), NOT a household (cellular is
    per-person). Subscribers are COVERAGE-DRIVEN (Phase 3 scales the full-coverage
    base by the coverage fraction reached), NOT capacity-derived: the spectrum ->
    capacity -> demand chain the old model used is CUT. None of the field names use
    a forbidden demand-side token.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    subscribers_at_full_coverage: int = Field(
        default=SUBSCRIBERS_AT_FULL_COVERAGE_DEFAULT,
        ge=1,
        description=(
            "The served-PERSON count (phone subscribers) when coverage reaches 1.0, "
            "a coverage-driven capacity-of-coverage figure, NOT a demand estimate, "
            "NOT a household count. FOUNDER_SET to a starting 50,000,000 people and "
            "flagged as the SWING DIAL that most moves cost-per-subscriber. Niche "
            "basis: the ~300M global coverage-gap people (COMM-021 / COMM-390) plus "
            "the developed-world remote/unserved layer (household tiers, e.g. "
            "COMM-065, converted at ~2.5 people/household). The base grows over "
            "time. Configurable."
        ),
    )
    subscribers_served_override: int | None = Field(
        default=None,
        ge=1,
        description=(
            "OPTIONAL direct assumed-subscribers scalar. If set, it overrides the "
            "coverage-driven full-coverage base (the model uses this absolute count "
            "at coverage 1.0; below full coverage it still scales by coverage "
            "fraction). Default None means use the coverage-driven mapping."
        ),
    )


class GroundInterfaceDials(BaseModel):
    """The marked, TWO-REGIME CELLULAR-ground cost INTERFACE (Phase 4).

    INTERFACE INPUTS. These two ground baselines (dense-served incumbent-marginal
    and sparse fresh-build) come from the ground research wave; the founder owns the
    final ground call and is still unsure about the comparison. Do not hardcode
    settled values in the comms src; supply them per-scenario. Either or both may be
    None, in which case that regime's ratio is skipped and the model still reports
    the space cost per subscriber.

    The space side of the comparison is the model's OWN COMPUTED cellular annual
    cost-per-subscriber (Phase 3), NEVER Starlink's disclosed broadband per-sub
    number. This block is declared in Phase 1 (the ``ground`` field defaults to
    None on :class:`CommsConfig`); Phase 4 consumes it in ``ground.py``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    dense_ground_cost_per_subscriber_usd: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Dense-served incumbent-marginal CELLULAR ground cost per subscriber "
            "(the mobile-network all-in cost per human subscriber), grounded ~$140 "
            "to 310/sub/yr. MARKED INTERFACE INPUT; optional (None-able) so the cost "
            "side never blocks. Sources COMM-096 / COMM-098 and "
            "research/economics/ground_cellular_cost_per_subscriber.md Section 2.4."
        ),
    )
    sparse_ground_cost_per_subscriber_usd: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Sparse fresh-build ground cost per subscriber, grounded ~$875 to "
            "1,540/sub/yr rural (up to the ~$44,500 extreme tail). MARKED INTERFACE "
            "INPUT; optional. This is the regime the HEADLINE verdict reads: space "
            "below this number is the niche. Source COMM-100."
        ),
    )
    basis: str = Field(
        default=GROUND_BASIS_DEFAULT,
        description=(
            "Label stating which basis the ground numbers are on (default "
            "'annual_cost_per_subscriber'), so the Phase 4 comparison matches "
            "like-for-like with the space side (it asserts the bases match)."
        ),
    )
    scenario_name: str = Field(
        default="ground interface (research-grounded, founder owns the call)",
        description="Human-readable label for the supplied ground-interface scenario.",
    )
    source_note: str = Field(
        default="",
        description="Free-text record of the research provenance once firm (empty by default).",
    )


# ===========================================================================
# 2. The top-level CommsConfig
# ===========================================================================


class CommsConfig(BaseModel):
    """The complete configuration for one communications cellular cost run.

    Construct one (the defaults reproduce the central case), or load one from YAML
    with :func:`load_comms_config`. Hand it to ``run_comms_model`` (Phase 2) /
    ``build_comms_output`` (Phase 5).

    Every block defaults via ``default_factory`` (or, for ``ground``, a plain None)
    so a config constructed with no arguments, or a YAML omitting a block, gets a
    fully valid all-default block. The ``ground`` field is ``None`` by default,
    which is what makes the cost side run with no ground number.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, validate_assignment=True)

    metadata: CommsMetadataDials = Field(
        default_factory=lambda: _default_comms_metadata(),
        description="Run metadata: base year, horizon, scenario name.",
    )
    cadence: CadenceDials = Field(
        default_factory=CadenceDials,
        description="Whole-fleet launch-cadence dials (shared logistic ramp; prices launch cost).",
    )
    comms_cadence: CommsCadenceDials = Field(
        default_factory=CommsCadenceDials,
        description="The comms slice's share of the fleet cadence (how many launches comms flies).",
    )
    launch_cost: LaunchCostDials = Field(
        default_factory=LaunchCostDials,
        description="Cadence-indexed launch-cost dials (log-linear, priced at fleet cadence).",
    )
    satellite: SatelliteDials = Field(
        default_factory=SatelliteDials,
        description="The fixed cellular-satellite spec: per-launch count, lifetime, build cost.",
    )
    coverage: CoverageDials = Field(
        default_factory=CoverageDials,
        description="The NEW constellation-size coverage target the build-out fills toward.",
    )
    subscribers: SubscriberDials = Field(
        default_factory=SubscriberDials,
        description="The per-PERSON denominator basis (full-coverage count + optional override).",
    )
    ground: GroundInterfaceDials | None = Field(
        default=None,
        description=(
            "The marked, TWO-REGIME ground interface (Phase 4). None by default so "
            "the cost side runs with no ground number; supply it per-scenario."
        ),
    )


# ===========================================================================
# 3. Default-builder helpers
# ===========================================================================


def _default_comms_metadata() -> CommsMetadataDials:
    """Build the default :class:`CommsMetadataDials` for the central case.

    A named builder is required because :class:`CommsMetadataDials` has two
    required fields (``base_year``, ``horizon_years``) with no field defaults, so
    ``default_factory=CommsMetadataDials`` would fail. Mirrors the DC
    ``_default_metadata`` pattern; supplies base year 2026 and horizon 10.
    """
    return CommsMetadataDials(base_year=BASE_YEAR_DEFAULT, horizon_years=HORIZON_YEARS_DEFAULT)


# ===========================================================================
# 4. YAML loaders
# ===========================================================================


def comms_config_from_dict(data: dict[str, object]) -> CommsConfig:
    """Build a :class:`CommsConfig` from an already-parsed YAML mapping.

    Top-level keys are the block names (``metadata``, ``cadence``,
    ``comms_cadence``, ``launch_cost``, ``satellite``, ``coverage``,
    ``subscribers``, ``ground``), all optional (omitted = defaults). An empty dict
    yields an all-defaults config.

    Validation is Pydantic's: an unknown key, a wrong type, an out-of-bounds value,
    or a missing required field raises :class:`pydantic.ValidationError` with a
    precise location.
    """
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping (a YAML object)")
    return CommsConfig.model_validate(data)


def load_comms_config(path: str | Path) -> CommsConfig:
    """Load and validate a :class:`CommsConfig` from a YAML file.

    Raises :class:`FileNotFoundError` if the path does not exist and
    :class:`ValueError` (a :class:`pydantic.ValidationError` for schema problems)
    on any malformed or invalid content. An empty file yields an all-defaults
    :class:`CommsConfig`.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"comms config file not found: {p}")
    try:
        data = yaml.safe_load(p.read_text())
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse YAML comms config {p}: {exc}") from exc
    if data is None:
        # An empty scenario file = all defaults.
        return CommsConfig()
    if not isinstance(data, dict):
        raise ValueError(
            f"comms config file {p} must contain a YAML mapping (got {type(data).__name__})"
        )
    return comms_config_from_dict(data)


# Re-export the public config surface so external callers (engine, ground, output,
# tests) import from one place.
__all__ = [
    "CadenceDials",
    "CommsCadenceDials",
    "CommsConfig",
    "CommsMetadataDials",
    "CoverageDials",
    "GroundInterfaceDials",
    "LaunchCostDials",
    "SatelliteDials",
    "SubscriberDials",
    "comms_config_from_dict",
    "load_comms_config",
]
