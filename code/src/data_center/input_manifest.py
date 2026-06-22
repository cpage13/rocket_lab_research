"""Typed input manifest for the public space-model JSON artifact.

This module owns the ``inputs`` contract for the promoted space model. It turns
the validated scenario config and generated hardware roadmap into source-linked
``InputCell`` objects, then exposes both a nested typed tree and a flat path
index so agents can traverse assumptions without reading Python source.
"""

from __future__ import annotations

import logging
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import (
    AssumptionRole,
    CellSpec,
    InputCell,
    InputPath,
    InputScalar,
    InputValue,
    SourceRef,
    SourceRefType,
    SourceStatus,
    _cell,
    _field_description,
    _first_research_ref,
    _float_value,
    _int_value,
    _number_value,
    _research_ref,
    _source_index_ref,
    _str_value,
    _with_scenario_ref,
)
from data_center.config import (
    CadenceDials,
    FleetDials,
    LaunchCostDials,
    RBand,
    ValuationConfig,
    VolumeDials,
    YearRValue,
)
from data_center.generations import GenerationSpec, SourcingClass

logger = logging.getLogger(__name__)

ASSUMPTION_INDEX_PREFIX: Final[str] = "inputs.assumption_index"
DEFAULT_SCENARIO_PATH: Final[str] = "code/scenarios/default.yaml"
MARKET_REFERENCE_CAPACITY_GW: Final[float] = 100.0
PATH_SUFFIX_SPLITS: Final[int] = 1


class ScenarioIdentity(BaseModel):
    """Scenario identity for the input manifest."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Human-readable scenario name.")
    description: str = Field(..., description="What the scenario represents.")
    path: str = Field(..., description="Repository-relative source scenario path.")
    is_default: bool = Field(..., description="Whether this is the canonical default scenario.")
    owner_note: str | None = Field(default=None, description="Maintainer note for this scenario.")


class CadenceInputTree(BaseModel):
    """Typed cadence-input cells."""

    model_config = ConfigDict(frozen=True)

    cadence_ceiling: InputCell = Field(..., description="Launch cadence ceiling input.")
    launches_at_year_5: InputCell = Field(..., description="Year-5 launch-count anchor input.")
    launches_at_year_10: InputCell = Field(..., description="Year-10 launch-count anchor input.")
    first_launch_year: InputCell = Field(..., description="First launch model-year input.")


class FleetInputTree(BaseModel):
    """Typed fleet-service-life input cells."""

    model_config = ConfigDict(frozen=True)

    service_life_years: InputCell = Field(..., description="Node service-life input.")


class VolumeInputTree(BaseModel):
    """Typed stowed-volume-envelope input cells."""

    model_config = ConfigDict(frozen=True)

    si_areal_density_kg_m2: InputCell = Field(..., description="Solar-array areal density input.")
    si_bol_efficiency: InputCell = Field(..., description="Solar-array BOL efficiency input.")
    fold_ratio: InputCell = Field(..., description="Solar-array folded-volume ratio input.")
    stowed_pitch_mm: InputCell = Field(..., description="Panel stowed-pitch input.")
    radiator_solar_area_ratio: InputCell = Field(..., description="Radiator-to-solar area ratio.")
    mounting_overhead_pct: InputCell = Field(..., description="Array mounting overhead input.")
    neutron_fairing_usable_volume_m3: InputCell = Field(..., description="Fairing volume input.")


class LaunchInputTree(BaseModel):
    """Typed cadence-indexed launch-cost input cells."""

    model_config = ConfigDict(frozen=True)

    low_cadence_cost_musd: InputCell = Field(..., description="Low-cadence launch cost input.")
    high_cadence_cost_musd: InputCell = Field(..., description="High-cadence launch cost input.")
    low_cadence_launches: InputCell = Field(..., description="Low-cadence launch-count input.")
    high_cadence_launches: InputCell = Field(..., description="High-cadence launch-count input.")


class PhysicalInputTree(BaseModel):
    """Typed physical-envelope and per-node cost input cells."""

    model_config = ConfigDict(frozen=True)

    mass_envelope_t: InputCell = Field(..., description="Payload mass-envelope input.")
    node_mass_fixed_t: InputCell = Field(..., description="Fixed node mass input.")
    node_volume_fixed_m3: InputCell = Field(..., description="Fixed node stowed-volume input.")
    tjmax_lift_year: InputCell = Field(..., description="Radiator hot-loop arrival input.")
    radiator_t_per_kw_pre: InputCell = Field(..., description="Pre-hot-loop radiator mass input.")
    radiator_t_per_kw_post: InputCell = Field(..., description="Post-hot-loop radiator mass input.")
    solar_mass_t_per_kw: InputCell = Field(..., description="Solar mass per kW input.")
    bus_base_musd: InputCell = Field(..., description="Year-zero bus cost input.")
    bus_flatten_after_yr: InputCell = Field(..., description="Bus-cost flattening year input.")
    bus_growth_pre: InputCell = Field(..., description="Pre-flattening bus-cost trend input.")
    solar_cost_musd_per_kw: InputCell = Field(..., description="Solar cost per kW input.")
    radiator_cost_musd_per_kw: InputCell = Field(..., description="Radiator cost per kW input.")
    release_cadence_yr: InputCell = Field(..., description="GPU generation cadence input.")


class RevenueInputTree(BaseModel):
    """Typed revenue-multiple input cells."""

    model_config = ConfigDict(frozen=True)

    central: list[InputCell] = Field(..., description="Central R-band anchor cells.")
    low: list[InputCell] = Field(..., description="Low sensitivity R-band anchor cells.")
    high: list[InputCell] = Field(..., description="High sensitivity R-band anchor cells.")


class GenerationSlopesInputTree(BaseModel):
    """Typed post-Feynman generation-slope input cells."""

    model_config = ConfigDict(frozen=True)

    usd_growth_per_gen: InputCell = Field(..., description="Cost growth per generation input.")
    kw_growth_per_gen: InputCell = Field(..., description="Power growth per generation input.")
    kg_growth_per_gen: InputCell = Field(..., description="Mass growth per generation input.")
    pf_growth_per_gen: InputCell = Field(..., description="Compute growth per generation input.")


class GenerationInputTree(BaseModel):
    """Typed input cells for one GPU package generation."""

    model_config = ConfigDict(frozen=True)

    name: InputCell = Field(..., description="Generation name input.")
    year_available: InputCell = Field(..., description="Generation availability-year input.")
    usd_per_pkg: InputCell = Field(..., description="Generation package-cost input.")
    kw_per_pkg: InputCell = Field(..., description="Generation package-power input.")
    kg_per_pkg: InputCell = Field(..., description="Generation package-mass input.")
    pf_per_pkg: InputCell = Field(..., description="Generation package-compute input.")
    die_count: InputCell = Field(..., description="Generation die-count input.")


class MarketSanityInputTree(BaseModel):
    """Validation-only market-reference inputs."""

    model_config = ConfigDict(frozen=True)

    reference_capacity_gw: InputCell = Field(
        ...,
        description="Mid-2030s AI data-center capacity sanity-check input.",
    )


class TypedInputTree(BaseModel):
    """Nested typed mirror of all known scenario input blocks."""

    model_config = ConfigDict(frozen=True)

    cadence: CadenceInputTree = Field(..., description="Launch cadence inputs.")
    fleet: FleetInputTree = Field(..., description="Fleet/service-life inputs.")
    volume: VolumeInputTree = Field(..., description="Stowed volume-envelope inputs.")
    launch: LaunchInputTree = Field(..., description="Launch-cost inputs.")
    physical: PhysicalInputTree = Field(..., description="Physical-envelope and cost inputs.")
    revenue: RevenueInputTree = Field(..., description="Revenue-multiple inputs.")
    generation_slopes: GenerationSlopesInputTree = Field(
        ...,
        description="Post-Feynman generation-slope inputs.",
    )
    generations: list[GenerationInputTree] = Field(
        ..., description="GPU package generation inputs."
    )
    market_sanity_check: MarketSanityInputTree = Field(
        ...,
        description="Validation-only market sanity-check inputs.",
    )


class InputManifest(BaseModel):
    """Complete typed input object for the space-model JSON."""

    model_config = ConfigDict(frozen=True)

    scenario: ScenarioIdentity = Field(..., description="Scenario identity metadata.")
    config: TypedInputTree = Field(..., description="Nested typed input tree.")
    assumption_index: dict[InputPath, InputCell] = Field(
        ...,
        description="Flat path-indexed lookup for all input cells.",
    )

    @property
    def gospel(self) -> dict[str, float | int]:
        """Return legacy physical-input values for internal validation helpers."""
        physical = self.config.physical
        return {
            "mass_envelope_t": _number_value(physical.mass_envelope_t),
            "node_mass_fixed_t": _number_value(physical.node_mass_fixed_t),
            "node_volume_fixed_m3": _number_value(physical.node_volume_fixed_m3),
            "tjmax_lift_year": _number_value(physical.tjmax_lift_year),
            "radiator_t_per_kw_pre": _number_value(physical.radiator_t_per_kw_pre),
            "radiator_t_per_kw_post": _number_value(physical.radiator_t_per_kw_post),
            "solar_mass_t_per_kw": _number_value(physical.solar_mass_t_per_kw),
            "bus_base_musd": _number_value(physical.bus_base_musd),
            "bus_flatten_after_yr": _number_value(physical.bus_flatten_after_yr),
            "bus_growth_pre": _number_value(physical.bus_growth_pre),
            "solar_cost_musd_per_kw": _number_value(physical.solar_cost_musd_per_kw),
            "radiator_cost_musd_per_kw": _number_value(physical.radiator_cost_musd_per_kw),
            "release_cadence_yr": _number_value(physical.release_cadence_yr),
        }

    @property
    def slopes(self) -> dict[str, float | int]:
        """Return legacy generation-slope values for internal renderers."""
        slopes = self.config.generation_slopes
        return {
            "usd_growth_per_gen": _number_value(slopes.usd_growth_per_gen),
            "kw_growth_per_gen": _number_value(slopes.kw_growth_per_gen),
            "kg_growth_per_gen": _number_value(slopes.kg_growth_per_gen),
            "pf_growth_per_gen": _number_value(slopes.pf_growth_per_gen),
        }

    @property
    def cadence(self) -> CadenceDials:
        """Return the cadence config model represented by the manifest."""
        cadence = self.config.cadence
        return CadenceDials(
            cadence_ceiling=_int_value(cadence.cadence_ceiling),
            launches_at_year_5=_int_value(cadence.launches_at_year_5),
            launches_at_year_10=_int_value(cadence.launches_at_year_10),
            first_launch_year=_int_value(cadence.first_launch_year),
        )

    @property
    def fleet(self) -> FleetDials:
        """Return the fleet config model represented by the manifest."""
        return FleetDials(service_life_years=_int_value(self.config.fleet.service_life_years))

    @property
    def volume(self) -> VolumeDials:
        """Return the volume config model represented by the manifest."""
        volume = self.config.volume
        return VolumeDials(
            si_areal_density_kg_m2=_float_value(volume.si_areal_density_kg_m2),
            si_bol_efficiency=_float_value(volume.si_bol_efficiency),
            fold_ratio=_float_value(volume.fold_ratio),
            stowed_pitch_mm=_float_value(volume.stowed_pitch_mm),
            radiator_solar_area_ratio=_float_value(volume.radiator_solar_area_ratio),
            mounting_overhead_pct=_float_value(volume.mounting_overhead_pct),
            neutron_fairing_usable_volume_m3=_float_value(volume.neutron_fairing_usable_volume_m3),
        )

    @property
    def launch_cost(self) -> LaunchCostDials:
        """Return the launch-cost config model represented by the manifest."""
        launch = self.config.launch
        return LaunchCostDials(
            low_cadence_cost_musd=_float_value(launch.low_cadence_cost_musd),
            high_cadence_cost_musd=_float_value(launch.high_cadence_cost_musd),
            low_cadence_launches=_float_value(launch.low_cadence_launches),
            high_cadence_launches=_float_value(launch.high_cadence_launches),
        )

    @property
    def r_band(self) -> RBand:
        """Return the R-band config model represented by the manifest."""
        revenue = self.config.revenue
        return RBand(
            central=_anchor_values(revenue.central),
            low=_anchor_values(revenue.low),
            high=_anchor_values(revenue.high),
        )

    @property
    def generations(self) -> list[dict[str, str | float | int]]:
        """Return flattened generation values for existing text/report helpers."""
        rows: list[dict[str, str | float | int]] = []
        for generation in self.config.generations:
            rows.append(
                {
                    "name": _str_value(generation.name),
                    "year_available": _number_value(generation.year_available),
                    "usd_per_pkg": _number_value(generation.usd_per_pkg),
                    "kw_per_pkg": _number_value(generation.kw_per_pkg),
                    "kg_per_pkg": _number_value(generation.kg_per_pkg),
                    "pf_per_pkg": _number_value(generation.pf_per_pkg),
                    "die_count": _number_value(generation.die_count),
                    "source_class": generation.name.source_status.value,
                    "source_doc_path": _first_research_ref(generation.name),
                }
            )
        return rows


def _anchor_values(cells: list[InputCell]) -> list[YearRValue]:
    """Convert revenue input cells back into R-band anchor models."""
    anchors: list[YearRValue] = []
    for cell in cells:
        fy = int(cell.path.rsplit(".", PATH_SUFFIX_SPLITS)[-1])
        anchors.append(YearRValue(fy=fy, r=_float_value(cell)))
    return anchors


def _generation_status(sourcing: SourcingClass) -> SourceStatus:
    """Map generation-source tiers into the public source-status taxonomy."""
    if sourcing is SourcingClass.FACT:
        return SourceStatus.CERTIFIED
    if sourcing is SourcingClass.ESTIMATE:
        return SourceStatus.SOURCED_ESTIMATE
    return SourceStatus.EXTRAPOLATION


def _source_refs_for_generation(generation: GenerationSpec) -> list[SourceRef]:
    """Build source refs for a generation input cell."""
    if generation.source.sourcing is SourcingClass.FACT:
        claim_id = "GPU-001"
    elif generation.source.sourcing is SourcingClass.ESTIMATE:
        claim_id = "GPU-012"
    else:
        claim_id = "GPU-010"
    return [
        _source_index_ref(claim_id, "Source-status support for this hardware generation."),
        _research_ref(
            generation.source.doc_path,
            "Durable research note for generation values.",
            claim_id=claim_id,
        ),
    ]


def _generation_cell(
    *,
    path: str,
    label: str,
    value: InputValue,
    unit: str | None,
    description: str,
    generation: GenerationSpec,
) -> InputCell:
    """Construct one generation input cell."""
    return InputCell(
        path=path,
        label=label,
        value=value,
        unit=unit,
        description=description,
        assumption_role=AssumptionRole.DEFAULT,
        source_status=_generation_status(generation.source.sourcing),
        source_refs=_source_refs_for_generation(generation),
        rationale="Generation values come from the hardware roadmap used by the default model.",
        notes=generation.source.quoted_figure,
    )


CADENCE_SPECS: Final[dict[str, CellSpec]] = {
    "cadence_ceiling": CellSpec(
        label="Cadence ceiling",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-010",
        source_note="Supports the high-cadence model scenario.",
        rationale="The ceiling bounds the logistic launch ramp above the 2036 target.",
    ),
    "launches_at_year_5": CellSpec(
        label="Year-5 launches",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-010",
        source_note="Supports the launch-ramp scenario shape.",
        rationale="This anchor shapes the midpoint of the venture-model cadence ramp.",
    ),
    "launches_at_year_10": CellSpec(
        label="2036 launches",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-CADENCE-90",
        source_note="Public claim for the default 2036 target cadence.",
        rationale="This is the default 2036 deployed-year cohort target.",
    ),
    "first_launch_year": CellSpec(
        label="First launch year index",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-011",
        source_note="Public schedule context for the first-flight model year.",
        rationale="The first launch clamp prevents year-zero deployment before Neutron service.",
    ),
}

FLEET_SPECS: Final[dict[str, CellSpec]] = {
    "service_life_years": CellSpec(
        label="Service life",
        unit="years",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SERVICE-LIFE-5Y",
        source_note="Public claim for the default five-year service life.",
        rationale="The default models a hard five-year cohort cliff.",
    )
}

LAUNCH_SPECS: Final[dict[str, CellSpec]] = {
    "low_cadence_cost_musd": CellSpec(
        label="Low-cadence launch cost",
        unit="MUSD/launch",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports cadence-indexed Neutron cost assumptions.",
        rationale="The launch-cost curve starts at a higher low-cadence cost.",
    ),
    "high_cadence_cost_musd": CellSpec(
        label="High-cadence launch cost",
        unit="MUSD/launch",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-LAUNCH-COST-2036",
        source_note="Public claim for high-cadence launch cost.",
        rationale="The default uses a lower internal cost once cadence is high.",
    ),
    "low_cadence_launches": CellSpec(
        label="Low-cadence anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports the low-cadence cost anchor.",
        rationale="This anchor identifies where the high-cost end of the curve applies.",
    ),
    "high_cadence_launches": CellSpec(
        label="High-cadence anchor",
        unit="launches/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="NTR-009",
        source_note="Supports the high-cadence cost anchor.",
        rationale="This anchor identifies where the lower steady-state cost applies.",
    ),
}

PHYSICAL_SPECS: Final[dict[str, CellSpec]] = {
    "mass_envelope_t": CellSpec(
        label="Reusable SSO mass envelope",
        unit="t",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-PAYLOAD-SSO-UPGRADE",
        source_note="Public claim for the block-upgrade SSO payload scenario.",
        rationale="The node packing model is mass-bound to this reusable SSO scenario.",
    ),
    "node_mass_fixed_t": CellSpec(
        label="Fixed node mass",
        unit="t",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-011",
        source_note="Supports flyable node power and mass-envelope assumptions.",
        rationale="Fixed mass accounts for bus, structure, propulsion, and integration overhead.",
    ),
    "node_volume_fixed_m3": CellSpec(
        label="Fixed node volume",
        unit="m3",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-011",
        source_note="Supports node envelope assumptions.",
        rationale="Fixed volume accounts for bus and structure before packed arrays.",
    ),
    "tjmax_lift_year": CellSpec(
        label="Hot-loop year",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="THR-003",
        source_note="Supports the hot-loop radiator-improvement assumption.",
        rationale="The model steps radiator mass down when hot-loop cooling arrives.",
    ),
    "radiator_t_per_kw_pre": CellSpec(
        label="Radiator mass before hot loop",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-003",
        source_note="Supports radiator mass scaling.",
        rationale="Pre-hot-loop radiator mass keeps the near-term model conservative.",
    ),
    "radiator_t_per_kw_post": CellSpec(
        label="Radiator mass after hot loop",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-003",
        source_note="Supports radiator mass scaling after higher-temperature operation.",
        rationale="The cycle-2 default uses the central single-face co-mounted radiator dial.",
    ),
    "solar_mass_t_per_kw": CellSpec(
        label="Solar mass per kW",
        unit="t/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable solar-array mass assumptions.",
        rationale="Solar mass is apportioned per package through node power.",
    ),
    "bus_base_musd": CellSpec(
        label="Base bus cost",
        unit="MUSD",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-011",
        source_note="Supports bus/platform scale assumptions.",
        rationale="The bus cost dial gives every node a platform-cost base.",
    ),
    "bus_flatten_after_yr": CellSpec(
        label="Bus cost flattening year",
        unit="model year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="THR-011",
        source_note="Supports platform-cost modeling assumptions.",
        rationale="The model stops compounding bus-cost decline after the flattening year.",
    ),
    "bus_growth_pre": CellSpec(
        label="Bus cost trend before flattening",
        unit="fraction/year",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="THR-011",
        source_note="Supports platform-cost modeling assumptions.",
        rationale="This dial applies modest real cost decline before the flattening year.",
    ),
    "solar_cost_musd_per_kw": CellSpec(
        label="Solar cost per kW",
        unit="MUSD/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-COST",
        source_note="Public claim for solar/radiator cost dials.",
        rationale="The default keeps the solar cost dial explicit pending better sourcing.",
    ),
    "radiator_cost_musd_per_kw": CellSpec(
        label="Radiator cost per kW",
        unit="MUSD/kW",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="RLDC-SOLAR-RADIATOR-COST",
        source_note="Public claim for solar/radiator cost dials.",
        rationale="The default keeps the radiator cost dial explicit pending better sourcing.",
    ),
    "release_cadence_yr": CellSpec(
        label="GPU generation cadence",
        unit="years/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SCENARIO,
        claim_id="GPU-010",
        source_note="Supports the long-run generation cadence projection.",
        rationale="The model extrapolates post-Feynman generations on this cadence.",
    ),
}

VOLUME_SPECS: Final[dict[str, CellSpec]] = {
    "si_areal_density_kg_m2": CellSpec(
        label="Solar-array areal density",
        unit="kg/m2",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable solar-array mass assumptions.",
        rationale="The volume model uses this density to derive array scale.",
    ),
    "si_bol_efficiency": CellSpec(
        label="Solar-array BOL efficiency",
        unit="fraction",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.CERTIFIED,
        claim_id="THR-007",
        source_note="Supports solar-array technology relevance.",
        rationale="This efficiency connects node power to required collector area.",
    ),
    "fold_ratio": CellSpec(
        label="Solar-array fold ratio",
        unit="ratio",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable array packaging assumptions.",
        rationale="The volume check needs a stowed-to-deployed packaging ratio.",
    ),
    "stowed_pitch_mm": CellSpec(
        label="Stowed panel pitch",
        unit="mm",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable array packaging assumptions.",
        rationale="Panel pitch turns deployed area into stowed volume.",
    ),
    "radiator_solar_area_ratio": CellSpec(
        label="Radiator-to-solar area ratio",
        unit="ratio",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.DERIVED_ESTIMATE,
        claim_id="THR-003",
        source_note="Supports single-face radiator area modeling.",
        rationale="The single-face co-mounted architecture links radiator and solar area.",
    ),
    "mounting_overhead_pct": CellSpec(
        label="Mounting overhead",
        unit="fraction",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="THR-006",
        source_note="Supports deployable-array packaging overhead.",
        rationale="The volume model reserves margin for yokes, hinges, and deployment hardware.",
    ),
    "neutron_fairing_usable_volume_m3": CellSpec(
        label="Neutron usable fairing volume",
        unit="m3",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.SOURCED_ESTIMATE,
        claim_id="NTR-004",
        source_note="Supports Neutron payload-envelope context.",
        rationale="The volume check compares stowed node volume with usable fairing volume.",
    ),
}

SLOPE_SPECS: Final[dict[str, CellSpec]] = {
    "usd_growth_per_gen": CellSpec(
        label="Package cost growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-012",
        source_note="Supports GPU cost trajectory estimates.",
        rationale="Post-Feynman package cost is extrapolated from the hardware roadmap.",
    ),
    "kw_growth_per_gen": CellSpec(
        label="Package power growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run package-power projection.",
        rationale="This corrected per-package growth avoids double-counting assembly growth.",
    ),
    "kg_growth_per_gen": CellSpec(
        label="Package mass growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run hardware roadmap projection.",
        rationale="The model assumes packaging density improves after Feynman.",
    ),
    "pf_growth_per_gen": CellSpec(
        label="Package compute growth per generation",
        unit="fraction/generation",
        role=AssumptionRole.DEFAULT,
        source_status=SourceStatus.EXTRAPOLATION,
        claim_id="GPU-010",
        source_note="Supports long-run hardware roadmap projection.",
        rationale="Compute growth drives the post-Feynman performance trajectory.",
    ),
}


def _cadence_tree(config: ValuationConfig, scenario_path: str) -> CadenceInputTree:
    """Build typed cadence input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.cadence.{key}",
                getattr(config.cadence, key),
                _field_description(CadenceDials, key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in CADENCE_SPECS.items()
    }
    return CadenceInputTree(**cells)


def _fleet_tree(config: ValuationConfig, scenario_path: str) -> FleetInputTree:
    """Build typed fleet input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.fleet.{key}",
                getattr(config.fleet, key),
                _field_description(FleetDials, key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in FLEET_SPECS.items()
    }
    return FleetInputTree(**cells)


def _volume_tree(config: ValuationConfig, scenario_path: str) -> VolumeInputTree:
    """Build typed volume input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.volume.{key}",
                getattr(config.volume, key),
                _field_description(VolumeDials, key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in VOLUME_SPECS.items()
    }
    return VolumeInputTree(**cells)


def _launch_tree(config: ValuationConfig, scenario_path: str) -> LaunchInputTree:
    """Build typed launch-cost input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.launch.{key}",
                getattr(config.launch_cost, key),
                _field_description(LaunchCostDials, key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in LAUNCH_SPECS.items()
    }
    return LaunchInputTree(**cells)


def _physical_tree(config: ValuationConfig, scenario_path: str) -> PhysicalInputTree:
    """Build typed physical-envelope input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.physical.{key}",
                getattr(config.gospel, key),
                _field_description(type(config.gospel), key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in PHYSICAL_SPECS.items()
    }
    return PhysicalInputTree(**cells)


def _revenue_cells(
    *,
    scenario_path: str,
    band_name: str,
    anchors: list[YearRValue],
    role: AssumptionRole,
) -> list[InputCell]:
    """Build typed R-band anchor cells for one trajectory."""
    cells: list[InputCell] = []
    for anchor in anchors:
        source_status = (
            SourceStatus.SCENARIO if role is AssumptionRole.DEFAULT else SourceStatus.SCENARIO
        )
        spec = CellSpec(
            label=f"{band_name} R anchor {anchor.fy}",
            unit="ratio",
            role=role,
            source_status=source_status,
            claim_id="RLDC-REVENUE-MULTIPLE-1_5X" if band_name == "central" else "REV-008",
            source_note="Supports the revenue-to-cost multiple trajectory.",
            rationale=(
                "The central R band is the public default; low/high bands are sensitivities."
            ),
            notes="R is revenue divided by annualized cost.",
        )
        cells.append(
            _with_scenario_ref(
                _cell(
                    f"inputs.config.revenue.{band_name}.{anchor.fy}",
                    anchor.r,
                    "Revenue-to-cost multiple anchor for one fiscal year.",
                    spec,
                ),
                scenario_path,
            )
        )
    return cells


def _revenue_tree(config: ValuationConfig, scenario_path: str) -> RevenueInputTree:
    """Build typed revenue input cells."""
    return RevenueInputTree(
        central=_revenue_cells(
            scenario_path=scenario_path,
            band_name="central",
            anchors=config.r_band.central,
            role=AssumptionRole.DEFAULT,
        ),
        low=_revenue_cells(
            scenario_path=scenario_path,
            band_name="low",
            anchors=config.r_band.low,
            role=AssumptionRole.SENSITIVITY,
        ),
        high=_revenue_cells(
            scenario_path=scenario_path,
            band_name="high",
            anchors=config.r_band.high,
            role=AssumptionRole.SENSITIVITY,
        ),
    )


def _slopes_tree(config: ValuationConfig, scenario_path: str) -> GenerationSlopesInputTree:
    """Build typed generation-slope input cells."""
    cells = {
        key: _with_scenario_ref(
            _cell(
                f"inputs.config.generation_slopes.{key}",
                getattr(config.slopes, key),
                _field_description(type(config.slopes), key),
                spec,
            ),
            scenario_path,
        )
        for key, spec in SLOPE_SPECS.items()
    }
    return GenerationSlopesInputTree(**cells)


def _generation_tree(generation: GenerationSpec, index: int) -> GenerationInputTree:
    """Build typed input cells for one generation row."""
    prefix = f"inputs.config.generations[{index}]"
    return GenerationInputTree(
        name=_generation_cell(
            path=f"{prefix}.name",
            label=f"{generation.name} name",
            value=generation.name,
            unit=None,
            description=_field_description(GenerationSpec, "name"),
            generation=generation,
        ),
        year_available=_generation_cell(
            path=f"{prefix}.year_available",
            label=f"{generation.name} availability year",
            value=generation.year_available,
            unit="year",
            description=_field_description(GenerationSpec, "year_available"),
            generation=generation,
        ),
        usd_per_pkg=_generation_cell(
            path=f"{prefix}.usd_per_pkg",
            label=f"{generation.name} package cost",
            value=generation.usd_per_pkg,
            unit="USD/package",
            description=_field_description(GenerationSpec, "usd_per_pkg"),
            generation=generation,
        ),
        kw_per_pkg=_generation_cell(
            path=f"{prefix}.kw_per_pkg",
            label=f"{generation.name} package power",
            value=generation.kw_per_pkg,
            unit="kW/package",
            description=_field_description(GenerationSpec, "kw_per_pkg"),
            generation=generation,
        ),
        kg_per_pkg=_generation_cell(
            path=f"{prefix}.kg_per_pkg",
            label=f"{generation.name} package mass",
            value=generation.kg_per_pkg,
            unit="kg/package",
            description=_field_description(GenerationSpec, "kg_per_pkg"),
            generation=generation,
        ),
        pf_per_pkg=_generation_cell(
            path=f"{prefix}.pf_per_pkg",
            label=f"{generation.name} package compute",
            value=generation.pf_per_pkg,
            unit="PFLOPS/package",
            description=_field_description(GenerationSpec, "pf_per_pkg"),
            generation=generation,
        ),
        die_count=_generation_cell(
            path=f"{prefix}.die_count",
            label=f"{generation.name} die count",
            value=generation.die_count,
            unit="dies/package",
            description=_field_description(GenerationSpec, "die_count"),
            generation=generation,
        ),
    )


def _market_tree() -> MarketSanityInputTree:
    """Build validation-only market sanity-check inputs."""
    spec = CellSpec(
        label="Mid-2030s AI data-center market reference",
        unit="GW",
        role=AssumptionRole.VALIDATION_ONLY,
        source_status=SourceStatus.PROJECTION,
        claim_id="RLDC-MARKET-100GW-2036",
        source_note="Public market-scale sanity check, not a market-share thesis.",
        rationale="The default deployment is compared against broad external market scale.",
        notes="Used only for scale sanity checking.",
    )
    return MarketSanityInputTree(
        reference_capacity_gw=_cell(
            "inputs.config.market_sanity_check.reference_capacity_gw",
            MARKET_REFERENCE_CAPACITY_GW,
            "Order-of-magnitude AI data-center capacity reference for sanity checking.",
            spec,
        )
    )


def _collect_cells(node: BaseModel | list[BaseModel]) -> list[InputCell]:
    """Collect all ``InputCell`` leaves from a typed input tree."""
    cells: list[InputCell] = []
    if isinstance(node, list):
        for item in node:
            cells.extend(_collect_cells(item))
        return cells
    for value in node.__dict__.values():
        if isinstance(value, InputCell):
            cells.append(value)
        elif isinstance(value, (BaseModel, list)):
            cells.extend(_collect_cells(value))
    return cells


def build_input_manifest(
    *,
    config: ValuationConfig,
    extended_gens: list[GenerationSpec],
    source_scenario_path: str,
) -> InputManifest:
    """Build the complete typed input manifest for a space-model run.

    Args:
        config: Validated scenario config used by the model run.
        extended_gens: Hardware generation list after extrapolation to horizon.
        source_scenario_path: Repository-relative source scenario path.

    Returns:
        A frozen :class:`InputManifest` with nested config cells and a flat
        assumption index keyed by stable public paths.
    """
    is_default = source_scenario_path == DEFAULT_SCENARIO_PATH
    config_tree = TypedInputTree(
        cadence=_cadence_tree(config, source_scenario_path),
        fleet=_fleet_tree(config, source_scenario_path),
        volume=_volume_tree(config, source_scenario_path),
        launch=_launch_tree(config, source_scenario_path),
        physical=_physical_tree(config, source_scenario_path),
        revenue=_revenue_tree(config, source_scenario_path),
        generation_slopes=_slopes_tree(config, source_scenario_path),
        generations=[
            _generation_tree(generation, index) for index, generation in enumerate(extended_gens)
        ],
        market_sanity_check=_market_tree(),
    )
    cells = _collect_cells(config_tree)
    assumption_index = {InputPath(cell.path): cell for cell in cells}
    scenario = ScenarioIdentity(
        name=config.scenario_name,
        description=(
            "Canonical default orbital AI-inference data-center scenario."
            if is_default
            else "User-supplied orbital AI-inference data-center scenario."
        ),
        path=source_scenario_path,
        is_default=is_default,
        owner_note="Creator-selected default assumption set." if is_default else None,
    )
    return InputManifest(scenario=scenario, config=config_tree, assumption_index=assumption_index)


__all__ = [
    "ASSUMPTION_INDEX_PREFIX",
    "DEFAULT_SCENARIO_PATH",
    "AssumptionRole",
    "InputCell",
    "InputManifest",
    "InputPath",
    "InputScalar",
    "InputValue",
    "ScenarioIdentity",
    "SourceRef",
    "SourceRefType",
    "SourceStatus",
    "TypedInputTree",
    "build_input_manifest",
]
