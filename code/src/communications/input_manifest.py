"""The comms input manifest: every config dial as a source-linked InputCell.

This is the comms analog of the data-center ``input_manifest.py`` TREE side (the
venture-specific part; the cell VOCABULARY moved to ``common.input_manifest`` in
Phase 0). It turns each :class:`communications.config.CommsConfig` dial into a
source-linked :class:`common.input_manifest.InputCell` for the output JSON's
``inputs`` block, assembles the per-block trees, then collects every cell into a
flat ``assumption_index`` keyed by each cell's stable public ``path`` (the
meta-block source-status summary tallies over that flat index).

Per plan Section 0.0 Amendment A1, there is no demand block: the price /
collectability references live in the ``price_reference`` block (the renamed
former demand block). No market-size, growth, capture-share, or take-rate dial
exists to surface.

The trees mirror the config blocks one-for-one. Band-triple dials (the
per-user-rate band, the oversubscription band) are surfaced as THREE sibling
cells (``...low`` / ``...mid`` / ``...high``) mirroring the band-leaf
convention; the per-class four-area cost dials are surfaced under a
``broadband`` and a ``direct_to_cell`` sub-tree. The ground dials are surfaced
even though the engine's compute path ignores them, so the promoted JSON records
every dial the run carried.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, ConfigDict, Field

from common.input_manifest import (
    AssumptionRole,
    CellSpec,
    InputCell,
    InputValue,
    SourceRef,
    SourceRefType,
    SourceStatus,
)
from communications.config import (
    BandTriple,
    CommsConfig,
    ConstellationDials,
    CostDownDials,
    GroundDials,
    LaunchDials,
    MetadataDials,
    PriceReferenceDials,
    SatelliteClassDials,
    ScopeWeights,
    SpectrumDials,
)

logger = logging.getLogger(__name__)

# The research doc that backs the comms dials at the design level (used as the
# default research reference for scenario / placeholder dials that have no
# single SOURCE_INDEX claim ID).
_DESIGN_DOC = "research/comms_model_design/DESIGN.md"


# ===========================================================================
# 1. The per-block input trees (one frozen BaseModel per config block)
# ===========================================================================


class MetadataInputTree(BaseModel):
    """Typed metadata input cells (base year, horizon, steady-state year)."""

    model_config = ConfigDict(frozen=True)

    base_year: InputCell = Field(..., description="Base-year input.")
    horizon_years: InputCell = Field(..., description="Horizon-length input.")
    steady_state_year: InputCell = Field(..., description="Steady-state-year input.")


class SatelliteClassInputTree(BaseModel):
    """Typed four-area cost and packing input cells for one satellite class."""

    model_config = ConfigDict(frozen=True)

    antenna_cost_musd: InputCell = Field(..., description="Antenna build-cost input.")
    comms_electronics_cost_musd: InputCell = Field(..., description="Comms-electronics cost input.")
    solar_cost_usd_per_kw: InputCell = Field(..., description="Solar cost-per-kW input.")
    payload_power_kw: InputCell = Field(..., description="Payload-power input.")
    radiator_bus_cost_musd: InputCell = Field(..., description="Radiator/bus cost input.")
    satellite_mass_t: InputCell = Field(..., description="Satellite mass input.")
    stowed_volume_m3: InputCell = Field(..., description="Stowed-volume input.")
    minor_component_pct: InputCell = Field(..., description="Minor-component fraction input.")


class ConstellationInputTree(BaseModel):
    """Typed constellation input cells: two class sub-trees plus lifetime/V4/flags."""

    model_config = ConfigDict(frozen=True)

    broadband: SatelliteClassInputTree = Field(..., description="Broadband class inputs.")
    direct_to_cell: SatelliteClassInputTree = Field(..., description="Direct-to-cell class inputs.")
    satellite_lifetime_years: InputCell = Field(..., description="Service-life cliff input.")
    v4_capability_multiplier: InputCell = Field(..., description="V4 capability-step input.")
    upgraded_neutron: InputCell = Field(..., description="Upgraded-Neutron flag input.")
    low_inclination_leo: InputCell = Field(..., description="Low-inclination-LEO flag input.")


class LaunchInputTree(BaseModel):
    """Typed launch input cells: the cadence/launch-cost dials and the envelopes."""

    model_config = ConfigDict(frozen=True)

    cadence_ceiling: InputCell = Field(..., description="Cadence-ceiling input.")
    launches_at_year_5: InputCell = Field(..., description="Year-5 launch anchor input.")
    launches_at_year_10: InputCell = Field(..., description="Year-10 launch anchor input.")
    first_launch_year: InputCell = Field(..., description="First-launch-year input.")
    low_cadence_cost_musd: InputCell = Field(..., description="Low-cadence launch-cost input.")
    high_cadence_cost_musd: InputCell = Field(..., description="High-cadence launch-cost input.")
    low_cadence_launches: InputCell = Field(..., description="Low-cadence launch-count input.")
    high_cadence_launches: InputCell = Field(..., description="High-cadence launch-count input.")
    neutron_mass_envelope_t: InputCell = Field(..., description="Baseline Neutron mass envelope.")
    neutron_fairing_volume_m3: InputCell = Field(
        ..., description="Baseline Neutron fairing volume."
    )
    upgraded_neutron_mass_envelope_t: InputCell = Field(
        ..., description="Upgraded Neutron mass envelope."
    )
    upgraded_neutron_fairing_volume_m3: InputCell = Field(
        ..., description="Upgraded Neutron fairing volume."
    )


class CostDownInputTree(BaseModel):
    """Typed cost-down (learning-curve) input cells."""

    model_config = ConfigDict(frozen=True)

    learning_rate_per_doubling: InputCell = Field(
        ..., description="Learning-rate-per-doubling input."
    )
    cost_down_reference_units: InputCell = Field(
        ..., description="Cost-down reference-units input."
    )


class SpectrumInputTree(BaseModel):
    """Typed spectrum input cells (the band triples surfaced as low/mid/high cells)."""

    model_config = ConfigDict(frozen=True)

    leased_bandwidth_mhz: InputCell = Field(..., description="Leased-bandwidth input.")
    spectral_efficiency_bps_per_hz: InputCell = Field(
        ..., description="Spectral-efficiency cross-check input."
    )
    beams_per_sat: InputCell = Field(..., description="Beams-per-satellite input.")
    target_per_user_rate_mbps_low: InputCell = Field(
        ..., description="Per-user-rate band-low input."
    )
    target_per_user_rate_mbps_mid: InputCell = Field(
        ..., description="Per-user-rate band-mid input."
    )
    target_per_user_rate_mbps_high: InputCell = Field(
        ..., description="Per-user-rate band-high input."
    )
    oversubscription_factor_low: InputCell = Field(
        ..., description="Oversubscription band-low input."
    )
    oversubscription_factor_mid: InputCell = Field(
        ..., description="Oversubscription band-mid input."
    )
    oversubscription_factor_high: InputCell = Field(
        ..., description="Oversubscription band-high input."
    )


class ScopeWeightsInputTree(BaseModel):
    """Typed geographic-scope weight input cells (context only, not a verdict driver)."""

    model_config = ConfigDict(frozen=True)

    us: InputCell = Field(..., description="US scope-weight input.")
    europe: InputCell = Field(..., description="Europe scope-weight input.")
    asia_ex_china: InputCell = Field(..., description="Asia-ex-China scope-weight input.")


class PriceReferenceInputTree(BaseModel):
    """Typed price/collectability reference input cells plus the scope sub-tree.

    The renamed former demand block (plan Amendment A1): price/collectability
    references and geographic scope context only, NOT a demand lever.
    """

    model_config = ConfigDict(frozen=True)

    retail_reference_usd_per_month: InputCell = Field(..., description="Retail-reference input.")
    arpu_usd_per_month: InputCell = Field(..., description="ARPU input.")
    operator_revenue_share: InputCell = Field(..., description="Operator-revenue-share input.")
    scope: ScopeWeightsInputTree = Field(..., description="Geographic-scope context inputs.")


class GroundInputTree(BaseModel):
    """Typed bottom-up ground (cellular) cost input cells (consumed in Phase 4)."""

    model_config = ConfigDict(frozen=True)

    tower_cost_musd_per_site: InputCell = Field(..., description="Tower/site build-cost input.")
    sites_per_million_subs: InputCell = Field(..., description="Sites-per-million-subs input.")
    backhaul_cost_musd_per_site_year: InputCell = Field(..., description="Backhaul-cost input.")
    ground_opex_musd_per_site_year: InputCell = Field(..., description="Ground-opex input.")
    ground_amortization_years: InputCell = Field(
        ..., description="Ground-amortization-years input."
    )
    spectrum_cost_musd: InputCell = Field(..., description="Ground spectrum-cost wash input.")
    incumbent_marginal_fraction_of_arpu: InputCell = Field(
        ..., description="Dense-regime incumbent marginal defend-floor fraction-of-ARPU input."
    )
    starlink_disclosed_all_in_cost_usd_per_sub_year: InputCell = Field(
        ..., description="Disclosed all-in Starlink floor reference input."
    )


class ScenarioInputTree(BaseModel):
    """Typed scenario-identity input cell (the scenario name)."""

    model_config = ConfigDict(frozen=True)

    scenario_name: InputCell = Field(..., description="Scenario-name input.")


class ScenarioMeta(BaseModel):
    """Source-scenario identity metadata (the comms analog of the DC ScenarioIdentity)."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Human-readable scenario name.")
    description: str = Field(..., description="What the scenario represents.")
    path: str = Field(..., description="Repository-relative source scenario path.")
    is_default: bool = Field(..., description="Whether this is the canonical default scenario.")


class InputManifest(BaseModel):
    """The complete typed input object for the comms space-model JSON.

    Carries the per-block trees, the source-scenario descriptor, and a flat
    ``assumption_index`` keyed by each cell's stable public ``path``. The flat
    index holds the SAME cells the trees hold (kept in lockstep by construction:
    every tree cell is collected into the index), and is the collection the
    meta-block source-status summary tallies over.
    """

    model_config = ConfigDict(frozen=True)

    metadata: MetadataInputTree = Field(..., description="Metadata inputs.")
    constellation: ConstellationInputTree = Field(..., description="Constellation inputs.")
    launch: LaunchInputTree = Field(..., description="Launch / cadence / envelope inputs.")
    cost_down: CostDownInputTree = Field(..., description="Cost-down (learning-curve) inputs.")
    spectrum: SpectrumInputTree = Field(..., description="Spectrum inputs.")
    price_reference: PriceReferenceInputTree = Field(
        ..., description="Price/collectability inputs."
    )
    ground: GroundInputTree = Field(..., description="Bottom-up ground-cost inputs.")
    scenario: ScenarioInputTree = Field(..., description="Scenario-identity inputs.")
    scenario_meta: ScenarioMeta = Field(..., description="Source-scenario descriptor.")
    assumption_index: dict[str, InputCell] = Field(
        ..., description="Flat path-indexed lookup for every input cell."
    )


# ===========================================================================
# 2. Cell-building helpers (mirroring the DC tree side)
# ===========================================================================


def _scenario_ref(path: str) -> SourceRef:
    """Build the source-scenario reference attached to every cell."""
    return SourceRef(
        ref_type=SourceRefType.RESEARCH_DOC,
        ref=path,
        claim_id=None,
        note="Scenario YAML value used for this model run.",
    )


def _build_cell(
    *,
    path: str,
    value: InputValue,
    description: str,
    spec: CellSpec,
    scenario_path: str,
) -> InputCell:
    """Construct one source-linked comms input cell, with the scenario ref attached.

    Builds the InputCell to the FULL field list (plan Section 0.4): a
    SOURCE_INDEX claim-ledger reference plus the source-scenario research
    reference, so every cell carries a non-empty ``source_refs``.

    Args:
        path: Stable public JSON path for this input.
        value: The config dial value.
        description: Plain-language meaning (the config field description).
        spec: The cell metadata (label, unit, role, status, claim, rationale).
        scenario_path: Repository-relative scenario YAML path.

    Returns:
        A frozen :class:`InputCell`.
    """
    return InputCell(
        path=path,
        label=spec.label,
        value=value,
        unit=spec.unit,
        description=description,
        assumption_role=spec.role,
        source_status=spec.source_status,
        source_refs=[
            SourceRef(
                ref_type=SourceRefType.SOURCE_INDEX,
                ref=f"research/SOURCE_INDEX.md#{spec.claim_id}",
                claim_id=spec.claim_id,
                note=spec.source_note,
            ),
            _scenario_ref(scenario_path),
        ],
        rationale=spec.rationale,
        notes=spec.notes,
    )


def _scenario_spec(
    *,
    label: str,
    unit: str | None,
    rationale: str,
    status: SourceStatus = SourceStatus.SCENARIO,
    claim_id: str = "COMM-082",
    role: AssumptionRole = AssumptionRole.DEFAULT,
    notes: str | None = None,
) -> CellSpec:
    """Build a CellSpec for a comms dial, defaulting to the scenario status / design doc.

    Most comms dials are INTERIM anchors set as YAML dials, which map to the
    ``scenario`` source status (plan Section 0.5). A small claim ID set backs
    the cost / cadence lines; absent a specific claim ID, the design doc backs
    the dial as a scenario anchor.
    """
    return CellSpec(
        label=label,
        unit=unit,
        role=role,
        source_status=status,
        claim_id=claim_id,
        source_note=f"Comms model dial backed by {_DESIGN_DOC}.",
        rationale=rationale,
        notes=notes,
    )


# ===========================================================================
# 3. The per-block tree builders
# ===========================================================================


def _metadata_tree(dials: MetadataDials, scenario_path: str) -> MetadataInputTree:
    """Build the metadata input tree."""
    return MetadataInputTree(
        base_year=_build_cell(
            path="inputs.config.metadata.base_year",
            value=dials.base_year,
            description=_desc(MetadataDials, "base_year"),
            spec=_scenario_spec(
                label="Base year",
                unit="year",
                rationale="The calendar year of model year 0 (the run's anchor year).",
            ),
            scenario_path=scenario_path,
        ),
        horizon_years=_build_cell(
            path="inputs.config.metadata.horizon_years",
            value=dials.horizon_years,
            description=_desc(MetadataDials, "horizon_years"),
            spec=_scenario_spec(
                label="Horizon years",
                unit="years",
                rationale="The number of fiscal-year steps the trajectory runs.",
            ),
            scenario_path=scenario_path,
        ),
        steady_state_year=_build_cell(
            path="inputs.config.metadata.steady_state_year",
            value=dials.steady_state_year,
            description=_desc(MetadataDials, "steady_state_year"),
            spec=_scenario_spec(
                label="Steady-state year",
                unit="year",
                rationale="The mature year the headline figure is read at.",
            ),
            scenario_path=scenario_path,
        ),
    )


def _satellite_class_tree(
    dials: SatelliteClassDials, class_name: str, scenario_path: str
) -> SatelliteClassInputTree:
    """Build one satellite class's four-area cost and packing input sub-tree."""
    base = f"inputs.config.constellation.{class_name}"
    return SatelliteClassInputTree(
        antenna_cost_musd=_build_cell(
            path=f"{base}.antenna_cost_musd",
            value=dials.antenna_cost_musd,
            description=_desc(SatelliteClassDials, "antenna_cost_musd"),
            spec=_scenario_spec(
                label=f"{class_name} antenna cost",
                unit="MUSD",
                rationale="The dominant high-value line; bill-of-materials-derived, INTERIM.",
                claim_id="COMM-082",
            ),
            scenario_path=scenario_path,
        ),
        comms_electronics_cost_musd=_build_cell(
            path=f"{base}.comms_electronics_cost_musd",
            value=dials.comms_electronics_cost_musd,
            description=_desc(SatelliteClassDials, "comms_electronics_cost_musd"),
            spec=_scenario_spec(
                label=f"{class_name} comms electronics cost",
                unit="MUSD",
                rationale="The comms electronics line, broken out; bill-of-materials, INTERIM.",
            ),
            scenario_path=scenario_path,
        ),
        solar_cost_usd_per_kw=_build_cell(
            path=f"{base}.solar_cost_usd_per_kw",
            value=dials.solar_cost_usd_per_kw,
            description=_desc(SatelliteClassDials, "solar_cost_usd_per_kw"),
            spec=_scenario_spec(
                label=f"{class_name} solar cost per kW",
                unit="USD/kW",
                rationale="The power-array cost per kW (about $20k/kW, not the DC $40k/kW).",
            ),
            scenario_path=scenario_path,
        ),
        payload_power_kw=_build_cell(
            path=f"{base}.payload_power_kw",
            value=dials.payload_power_kw,
            description=_desc(SatelliteClassDials, "payload_power_kw"),
            spec=_scenario_spec(
                label=f"{class_name} payload power",
                unit="kW",
                rationale="The comms-payload power draw; sizes the solar line. NEEDS-RESEARCH.",
                status=SourceStatus.PLACEHOLDER,
                claim_id="COMM-082",
            ),
            scenario_path=scenario_path,
        ),
        radiator_bus_cost_musd=_build_cell(
            path=f"{base}.radiator_bus_cost_musd",
            value=dials.radiator_bus_cost_musd,
            description=_desc(SatelliteClassDials, "radiator_bus_cost_musd"),
            spec=_scenario_spec(
                label=f"{class_name} radiator/bus cost",
                unit="MUSD",
                rationale="The bus plus thermal line; anchored light and AI-1-class.",
            ),
            scenario_path=scenario_path,
        ),
        satellite_mass_t=_build_cell(
            path=f"{base}.satellite_mass_t",
            value=dials.satellite_mass_t,
            description=_desc(SatelliteClassDials, "satellite_mass_t"),
            spec=_scenario_spec(
                label=f"{class_name} satellite mass",
                unit="t",
                rationale="The per-satellite wet mass; the mass bound divides the envelope by it.",
            ),
            scenario_path=scenario_path,
        ),
        stowed_volume_m3=_build_cell(
            path=f"{base}.stowed_volume_m3",
            value=dials.stowed_volume_m3,
            description=_desc(SatelliteClassDials, "stowed_volume_m3"),
            spec=_scenario_spec(
                label=f"{class_name} stowed volume",
                unit="m3",
                rationale="The folded stowed volume; the volume bound divides the fairing by it.",
            ),
            scenario_path=scenario_path,
        ),
        minor_component_pct=_build_cell(
            path=f"{base}.minor_component_pct",
            value=dials.minor_component_pct,
            description=_desc(SatelliteClassDials, "minor_component_pct"),
            spec=_scenario_spec(
                label=f"{class_name} minor-component fraction",
                unit="fraction",
                rationale="A small fraction of the four-area sum carried for a minor component.",
            ),
            scenario_path=scenario_path,
        ),
    )


def _constellation_tree(dials: ConstellationDials, scenario_path: str) -> ConstellationInputTree:
    """Build the constellation input tree (two class sub-trees plus lifetime/V4/flags)."""
    base = "inputs.config.constellation"
    return ConstellationInputTree(
        broadband=_satellite_class_tree(dials.broadband, "broadband", scenario_path),
        direct_to_cell=_satellite_class_tree(dials.direct_to_cell, "direct_to_cell", scenario_path),
        satellite_lifetime_years=_build_cell(
            path=f"{base}.satellite_lifetime_years",
            value=dials.satellite_lifetime_years,
            description=_desc(ConstellationDials, "satellite_lifetime_years"),
            spec=_scenario_spec(
                label="Satellite service life",
                unit="years",
                rationale="The service-life cliff (5 default, test 7).",
            ),
            scenario_path=scenario_path,
        ),
        v4_capability_multiplier=_build_cell(
            path=f"{base}.v4_capability_multiplier",
            value=dials.v4_capability_multiplier,
            description=_desc(ConstellationDials, "v4_capability_multiplier"),
            spec=_scenario_spec(
                label="V4 capability multiplier",
                unit="multiplier",
                rationale="The V4 capability step from the V1/V2/V3 trend; 1.0 = no step.",
            ),
            scenario_path=scenario_path,
        ),
        upgraded_neutron=_build_cell(
            path=f"{base}.upgraded_neutron",
            value=dials.upgraded_neutron,
            description=_desc(ConstellationDials, "upgraded_neutron"),
            spec=_scenario_spec(
                label="Upgraded-Neutron flag",
                unit=None,
                rationale="Whether the engine uses the upgraded-Neutron envelope.",
            ),
            scenario_path=scenario_path,
        ),
        low_inclination_leo=_build_cell(
            path=f"{base}.low_inclination_leo",
            value=dials.low_inclination_leo,
            description=_desc(ConstellationDials, "low_inclination_leo"),
            spec=_scenario_spec(
                label="Low-inclination-LEO flag",
                unit=None,
                rationale="Comms uses low-inclination LEO (more mass than SSO); informational.",
            ),
            scenario_path=scenario_path,
        ),
    )


def _launch_tree(dials: LaunchDials, scenario_path: str) -> LaunchInputTree:
    """Build the launch / cadence / envelope input tree."""
    base = "inputs.config.launch"

    def _c(name: str, unit: str | None, rationale: str, claim_id: str = "COMM-082") -> InputCell:
        return _build_cell(
            path=f"{base}.{name}",
            value=getattr(dials, name),
            description=_desc(LaunchDials, name),
            spec=_scenario_spec(
                label=name.replace("_", " "), unit=unit, rationale=rationale, claim_id=claim_id
            ),
            scenario_path=scenario_path,
        )

    return LaunchInputTree(
        cadence_ceiling=_c("cadence_ceiling", "count", "The hard cap on launches per year."),
        launches_at_year_5=_c("launches_at_year_5", "count", "The year-5 cadence logistic anchor."),
        launches_at_year_10=_c(
            "launches_at_year_10", "count", "The year-10 cadence anchor (90 by 2036)."
        ),
        first_launch_year=_c(
            "first_launch_year", "index", "The model-year index before which launches are zero."
        ),
        low_cadence_cost_musd=_c(
            "low_cadence_cost_musd", "MUSD", "Launch cost at the low-cadence anchor."
        ),
        high_cadence_cost_musd=_c(
            "high_cadence_cost_musd", "MUSD", "Launch cost at the high-cadence anchor (~$13.5M)."
        ),
        low_cadence_launches=_c("low_cadence_launches", "count", "Cadence at the low-cost anchor."),
        high_cadence_launches=_c(
            "high_cadence_launches", "count", "Cadence at the high-cost anchor."
        ),
        neutron_mass_envelope_t=_c(
            "neutron_mass_envelope_t", "t", "The baseline Neutron mass envelope to low-incl LEO."
        ),
        neutron_fairing_volume_m3=_c(
            "neutron_fairing_volume_m3", "m3", "The baseline Neutron fairing usable volume."
        ),
        upgraded_neutron_mass_envelope_t=_c(
            "upgraded_neutron_mass_envelope_t", "t", "The upgraded-Neutron mass envelope."
        ),
        upgraded_neutron_fairing_volume_m3=_c(
            "upgraded_neutron_fairing_volume_m3", "m3", "The upgraded-Neutron fairing volume."
        ),
    )


def _cost_down_tree(dials: CostDownDials, scenario_path: str) -> CostDownInputTree:
    """Build the cost-down (learning-curve) input tree."""
    base = "inputs.config.cost_down"
    return CostDownInputTree(
        learning_rate_per_doubling=_build_cell(
            path=f"{base}.learning_rate_per_doubling",
            value=dials.learning_rate_per_doubling,
            description=_desc(CostDownDials, "learning_rate_per_doubling"),
            spec=_scenario_spec(
                label="Learning rate per doubling",
                unit="fraction",
                rationale="The fractional cost reduction per doubling of cumulative units.",
            ),
            scenario_path=scenario_path,
        ),
        cost_down_reference_units=_build_cell(
            path=f"{base}.cost_down_reference_units",
            value=dials.cost_down_reference_units,
            description=_desc(CostDownDials, "cost_down_reference_units"),
            spec=_scenario_spec(
                label="Cost-down reference units",
                unit="count",
                rationale="The cumulative-units anchor where the cost is un-discounted.",
            ),
            scenario_path=scenario_path,
        ),
    )


def _band_cells(
    *,
    base: str,
    field: str,
    band: BandTriple,
    unit: str,
    rationale: str,
    scenario_path: str,
) -> dict[str, InputCell]:
    """Build the three low/mid/high cells for one band-triple dial.

    Returns a dict keyed ``<field>_low`` / ``_mid`` / ``_high`` so the caller
    can splat it into the tree constructor.
    """
    out: dict[str, InputCell] = {}
    for member in ("low", "mid", "high"):
        out[f"{field}_{member}"] = _build_cell(
            path=f"{base}.{field}.{member}",
            value=getattr(band, member),
            description=f"{rationale} (band-{member}).",
            spec=_scenario_spec(
                label=f"{field.replace('_', ' ')} band-{member}",
                unit=unit,
                rationale=rationale,
                notes="A planning-band member; stored ascending by magnitude.",
            ),
            scenario_path=scenario_path,
        )
    return out


def _spectrum_tree(dials: SpectrumDials, scenario_path: str) -> SpectrumInputTree:
    """Build the spectrum input tree (band triples surfaced as low/mid/high cells)."""
    base = "inputs.config.spectrum"
    rate_cells = _band_cells(
        base=base,
        field="target_per_user_rate_mbps",
        band=dials.target_per_user_rate_mbps,
        unit="Mbps",
        rationale="The per-user service level the beam is provisioned against",
        scenario_path=scenario_path,
    )
    oversub_cells = _band_cells(
        base=base,
        field="oversubscription_factor",
        band=dials.oversubscription_factor,
        unit="ratio",
        rationale="Registered subscribers per simultaneously active user",
        scenario_path=scenario_path,
    )
    return SpectrumInputTree(
        leased_bandwidth_mhz=_build_cell(
            path=f"{base}.leased_bandwidth_mhz",
            value=dials.leased_bandwidth_mhz,
            description=_desc(SpectrumDials, "leased_bandwidth_mhz"),
            spec=_scenario_spec(
                label="Leased bandwidth",
                unit="MHz",
                rationale="The per-beam channel width leased under the SCS framework.",
            ),
            scenario_path=scenario_path,
        ),
        spectral_efficiency_bps_per_hz=_build_cell(
            path=f"{base}.spectral_efficiency_bps_per_hz",
            value=dials.spectral_efficiency_bps_per_hz,
            description=_desc(SpectrumDials, "spectral_efficiency_bps_per_hz"),
            spec=_scenario_spec(
                label="Spectral efficiency (cross-check)",
                unit="bps/Hz",
                rationale="The D2C spectral efficiency; used only as a capacity cross-check.",
            ),
            scenario_path=scenario_path,
        ),
        beams_per_sat=_build_cell(
            path=f"{base}.beams_per_sat",
            value=dials.beams_per_sat,
            description=_desc(SpectrumDials, "beams_per_sat"),
            spec=_scenario_spec(
                label="Beams per satellite",
                unit="count",
                rationale="The beams per satellite (AST Block 2 ~2,500 adjustable beams).",
            ),
            scenario_path=scenario_path,
        ),
        **rate_cells,
        **oversub_cells,
    )


def _scope_tree(scope: ScopeWeights, scenario_path: str) -> ScopeWeightsInputTree:
    """Build the geographic-scope weights input sub-tree (context only)."""
    base = "inputs.config.price_reference.scope"

    def _c(name: str) -> InputCell:
        return _build_cell(
            path=f"{base}.{name}",
            value=getattr(scope, name),
            description=_desc(ScopeWeights, name),
            spec=_scenario_spec(
                label=f"Scope weight {name}",
                unit="fraction",
                rationale="The geographic context split of the served base (context only).",
            ),
            scenario_path=scenario_path,
        )

    return ScopeWeightsInputTree(
        us=_c("us"), europe=_c("europe"), asia_ex_china=_c("asia_ex_china")
    )


def _price_reference_tree(
    dials: PriceReferenceDials, scenario_path: str
) -> PriceReferenceInputTree:
    """Build the price/collectability reference input tree plus the scope sub-tree."""
    base = "inputs.config.price_reference"
    return PriceReferenceInputTree(
        retail_reference_usd_per_month=_build_cell(
            path=f"{base}.retail_reference_usd_per_month",
            value=dials.retail_reference_usd_per_month,
            description=_desc(PriceReferenceDials, "retail_reference_usd_per_month"),
            spec=_scenario_spec(
                label="Retail reference (price to beat)",
                unit="USD/month",
                rationale="FOUNDER-SET: about $100/month of full cell service, a chosen reference.",
                notes="Founder-set config, not a sourced figure.",
            ),
            scenario_path=scenario_path,
        ),
        arpu_usd_per_month=_build_cell(
            path=f"{base}.arpu_usd_per_month",
            value=dials.arpu_usd_per_month,
            description=_desc(PriceReferenceDials, "arpu_usd_per_month"),
            spec=_scenario_spec(
                label="ARPU reference",
                unit="USD/month",
                rationale="The individual-phone ARPU used in the revenue-ceiling reconciliation.",
            ),
            scenario_path=scenario_path,
        ),
        operator_revenue_share=_build_cell(
            path=f"{base}.operator_revenue_share",
            value=dials.operator_revenue_share,
            description=_desc(PriceReferenceDials, "operator_revenue_share"),
            spec=_scenario_spec(
                label="Operator revenue share",
                unit="fraction",
                rationale="The fraction of ARPU the space operator collects under an SCS lease.",
            ),
            scenario_path=scenario_path,
        ),
        scope=_scope_tree(dials.scope, scenario_path),
    )


def _ground_tree(dials: GroundDials, scenario_path: str) -> GroundInputTree:
    """Build the bottom-up ground (cellular) cost input tree.

    Surfaced here even though the engine's compute path ignores the ground
    block, so the promoted JSON records every dial the run carried. The
    ``spectrum_cost_musd`` line is the explicit zero wash.
    """
    base = "inputs.config.ground"

    def _c(name: str, unit: str | None, rationale: str) -> InputCell:
        return _build_cell(
            path=f"{base}.{name}",
            value=getattr(dials, name),
            description=_desc(GroundDials, name),
            spec=_scenario_spec(label=name.replace("_", " "), unit=unit, rationale=rationale),
            scenario_path=scenario_path,
        )

    return GroundInputTree(
        tower_cost_musd_per_site=_c(
            "tower_cost_musd_per_site", "MUSD", "The amortized cellular tower/site build cost."
        ),
        sites_per_million_subs=_c(
            "sites_per_million_subs", "count", "The cell sites needed per million subscribers."
        ),
        backhaul_cost_musd_per_site_year=_c(
            "backhaul_cost_musd_per_site_year", "MUSD", "The annual backhaul cost per site."
        ),
        ground_opex_musd_per_site_year=_c(
            "ground_opex_musd_per_site_year", "MUSD", "The annual operations cost per site."
        ),
        ground_amortization_years=_c(
            "ground_amortization_years", "years", "The years over which ground capex is amortized."
        ),
        spectrum_cost_musd=_build_cell(
            path=f"{base}.spectrum_cost_musd",
            value=dials.spectrum_cost_musd,
            description=_desc(GroundDials, "spectrum_cost_musd"),
            spec=_scenario_spec(
                label="Ground spectrum-cost wash",
                unit="MUSD",
                rationale="Spectrum nets out of the cost comparison; an explicit zero wash.",
                status=SourceStatus.DERIVED_ESTIMATE,
            ),
            scenario_path=scenario_path,
        ),
        incumbent_marginal_fraction_of_arpu=_build_cell(
            path=f"{base}.incumbent_marginal_fraction_of_arpu",
            value=dials.incumbent_marginal_fraction_of_arpu,
            description=_desc(GroundDials, "incumbent_marginal_fraction_of_arpu"),
            spec=_scenario_spec(
                label="Incumbent marginal defend-floor fraction of ARPU",
                unit="fraction",
                rationale="The dense-regime incumbent marginal defend floor (COMM-096 midpoint).",
                status=SourceStatus.SOURCED_ESTIMATE,
                claim_id="COMM-096",
            ),
            scenario_path=scenario_path,
        ),
        starlink_disclosed_all_in_cost_usd_per_sub_year=_build_cell(
            path=f"{base}.starlink_disclosed_all_in_cost_usd_per_sub_year",
            value=dials.starlink_disclosed_all_in_cost_usd_per_sub_year,
            description=_desc(GroundDials, "starlink_disclosed_all_in_cost_usd_per_sub_year"),
            spec=_scenario_spec(
                label="Disclosed all-in Starlink floor",
                unit="USD/yr",
                rationale="The disclosed all-in Starlink floor (COMM-090/COMM-103); not RKLB.",
                status=SourceStatus.SOURCED_ESTIMATE,
                claim_id="COMM-090",
            ),
            scenario_path=scenario_path,
        ),
    )


def _scenario_tree(scenario_name: str, scenario_path: str) -> ScenarioInputTree:
    """Build the scenario-identity input tree (the scenario name as a cell)."""
    return ScenarioInputTree(
        scenario_name=_build_cell(
            path="inputs.config.scenario_levers.scenario_name",
            value=scenario_name,
            description="Human-readable scenario label from the YAML config.",
            spec=_scenario_spec(
                label="Scenario name",
                unit=None,
                rationale="The scenario identity surfaced in the report and the JSON manifest.",
            ),
            scenario_path=scenario_path,
        )
    )


# ===========================================================================
# 4. The recursive cell walk and the builder
# ===========================================================================


def _collect_cells(node: BaseModel | list[BaseModel]) -> list[InputCell]:
    """Collect every ``InputCell`` leaf from a typed input tree (or list of trees).

    Mirrors the DC ``_collect_cells`` exactly: returns ``[]`` for an empty node,
    recurses into each element of a ``list``, and for a ``BaseModel`` iterates
    ``node.__dict__.values()`` appending any ``InputCell`` and recursing into any
    ``BaseModel`` or ``list``.

    Args:
        node: A tree model or a list of tree models.

    Returns:
        A flat list of every ``InputCell`` reachable from ``node``.
    """
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


def build_comms_input_manifest(
    *,
    config: CommsConfig,
    source_scenario_path: str,
) -> InputManifest:
    """Build the comms input manifest: every config dial as a source-linked InputCell.

    Walks the validated :class:`CommsConfig` and emits one :class:`InputCell`
    per dial, each carrying the full field list (path, label, value, unit,
    description, assumption_role, source_status, source_refs, rationale, notes).
    The source_status follows the design tag mapping (plan Section 0.5). The
    ground dials are surfaced even though the engine's compute path ignores
    them, so the promoted JSON records every dial the run carried. Assembles the
    per-block trees, then collects every cell with :func:`_collect_cells` into
    the flat ``assumption_index`` keyed by ``cell.path`` (mirroring the DC
    builder), so the meta block's source-status summary has a flat collection to
    tally over.

    Args:
        config: The validated comms config.
        source_scenario_path: Repository-relative path to the scenario YAML.

    Returns:
        A frozen :class:`InputManifest` of source-linked input cells, carrying
        both the per-block trees and the flat ``assumption_index``.
    """
    metadata_tree = _metadata_tree(config.metadata, source_scenario_path)
    constellation_tree = _constellation_tree(config.constellation, source_scenario_path)
    launch_tree = _launch_tree(config.launch, source_scenario_path)
    cost_down_tree = _cost_down_tree(config.cost_down, source_scenario_path)
    spectrum_tree = _spectrum_tree(config.spectrum, source_scenario_path)
    price_reference_tree = _price_reference_tree(config.price_reference, source_scenario_path)
    ground_tree = _ground_tree(config.ground, source_scenario_path)
    scenario_tree = _scenario_tree(config.scenario_levers.scenario_name, source_scenario_path)

    cells = _collect_cells(
        [
            metadata_tree,
            constellation_tree,
            launch_tree,
            cost_down_tree,
            spectrum_tree,
            price_reference_tree,
            ground_tree,
            scenario_tree,
        ]
    )
    assumption_index = {cell.path: cell for cell in cells}

    scenario_meta = ScenarioMeta(
        name=config.scenario_levers.scenario_name,
        description=(
            "Canonical default communications scenario."
            if source_scenario_path.endswith("comms_default.yaml")
            else "User-supplied communications scenario."
        ),
        path=source_scenario_path,
        is_default=source_scenario_path.endswith("comms_default.yaml"),
    )

    return InputManifest(
        metadata=metadata_tree,
        constellation=constellation_tree,
        launch=launch_tree,
        cost_down=cost_down_tree,
        spectrum=spectrum_tree,
        price_reference=price_reference_tree,
        ground=ground_tree,
        scenario=scenario_tree,
        scenario_meta=scenario_meta,
        assumption_index=assumption_index,
    )


def _desc(model_cls: type[BaseModel], field_name: str) -> str:
    """Return the Pydantic field description for a config field (a non-empty string)."""
    description = model_cls.model_fields[field_name].description
    if description is None:
        return f"Scenario field {field_name}."
    return description


__all__ = [
    "ConstellationInputTree",
    "CostDownInputTree",
    "GroundInputTree",
    "InputManifest",
    "LaunchInputTree",
    "MetadataInputTree",
    "PriceReferenceInputTree",
    "SatelliteClassInputTree",
    "ScenarioInputTree",
    "ScopeWeightsInputTree",
    "SpectrumInputTree",
    "build_comms_input_manifest",
]
