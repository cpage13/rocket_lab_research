"""Engine-computed sanity checks for one v8 ``ValuationOutput``.

This module computes the ``meta.validation`` block. Each rule examines the
typed v8 :class:`ValuationOutput` and returns a :class:`ValidationCheck`
describing what it tested, what it expected, what it found, whether the
check passed, and how bad a failure would be.

Reader contract: a downstream consumer (or LLM walking the artifact) can
run::

    jq '.meta.validation.rules[] | select(.pass_check == false)' artifact.json

and see every flagged anomaly without re-deriving the model. The 17 wired
rules are V1..V17; they are listed in :data:`_RULES` in declaration order
and that order is the order they appear in the artifact.

**Cycle-2 v8 re-pathing (Phase 4A).** V1–V10 are the cycle-1 checks
re-pointed at the v8 output structure (``physical.years`` / ``business.years``
/ ``inputs.generations``); their intent is unchanged where the v8 schema
still carries the field. Two rules lost their cycle-1 subject when the v8
schema dropped the ``cost.compute_share`` and ``decisions`` blocks, so they
are re-targeted to a v8-meaningful invariant (see V5 / V10 docstrings).
Phase 5 adds V11–V17 and may further refine the re-targeted rules.

**Cycle-2 v8 new rules (Phase 5).** Seven new V-rules V11-V17 are fully
implemented: :func:`check_no_legacy_r_scalar` (V11),
:func:`check_operator_r_consistency` (V12),
:func:`check_provenance_formula_keys` (V13),
:func:`check_cadence_monotonicity` (V14),
:func:`check_volume_fits_horizon` (V15),
:func:`check_fleet_cliff_consistency` (V16), and
:func:`check_radiator_dial_arch_consistency` (V17). They are wired into
:data:`_RULES` after V1-V10.

Severity tiers (see :class:`output.Severity`):

* ``CRITICAL`` — model is invalid; do not quote.
* ``MAJOR`` — substantive defect that affects the headline.
* ``MINOR`` — soft check (range warning, secondary metric).

References:
    plan_05_20_cycle2.md § 5 — Phase 4A (v8 output re-pathing).
    strategy_05_20_cycle2.md § 5 — the validation strategy.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Final

from pydantic import BaseModel

from .config import BindingConstraint, OperatorModel, RadiatorArchitecture
from .output import Severity, ValidationCheck, ValuationOutput
from .provenance import FORMULAS, ProvenanceCell

# ---------------------------------------------------------------------------
# Numeric constants used by the rules.
#
# These thresholds and bands are the rule definitions themselves — they
# encode "what counts as a passing run". Surface them as named module-level
# constants (per CLAUDE.md, no bare numeric literals) so a reader can find
# every threshold in one place.
# ---------------------------------------------------------------------------

# V1 — mass utilisation must be tight (D2 says mass is the only constraint,
# so every year should pack close to the envelope). v8 carries mass
# utilisation as a PERCENT (0-100); cycle-1 carried a 0-1 fraction.
MASS_UTIL_MIN_PCT: Final[float] = 85.0
MASS_UTIL_MAX_PCT: Final[float] = 100.0

# V2 — sane $/pkg (NVIDIA's largest 'as sold' Blackwell rack is ~$3.5M;
# anything above $5M is fictional / a data-entry mistake).
USD_PER_PKG_MAX: Final[int] = 5_000_000

# V3 — active-fleet gross-margin floor. The default five-year operating plan
# should not decay from the 1.50 cost multiple into a low-margin tail; active
# years must stay at or above this floor. v8 carries margin as a PERCENT
# (0-100). No-fleet years are ignored because revenue is zero.
MARGIN_PCT_MIN: Final[float] = 25.0

# V4 — at least one package on the node (a zero-N year means the mass
# envelope is too small to carry even one frontier-generation GPU).
N_PACKAGES_MIN: Final[int] = 1

# V5 — re-targeted to PF/kW (the v8 schema dropped cost.compute_share).
# Compute density trends upward year-over-year as silicon outpaces power;
# a dip larger than this is a generation-trajectory glitch.
PF_PER_KW_MAX_DIP: Final[float] = 2.0

# V6 — last-year PF/kW sanity band (Part IX of the brainstorm: 20-80
# PFLOPS/kW spans pessimistic-to-optimistic post-Feynman slope).
PF_PER_KW_MIN: Final[float] = 20.0
PF_PER_KW_MAX: Final[float] = 80.0

# V9 — per-node ANNUAL $M sanity band. The v8 schema carries the annualized
# cost per node (total / service_life); the cycle-1 node-total band
# [50, 200] divided by a 5-year service life gives [10, 40].
COST_ANNUAL_MIN_MUSD: Final[float] = 5.0
COST_ANNUAL_MAX_MUSD: Final[float] = 60.0

# V10 — re-targeted to the data-dictionary block (the v8 schema dropped the
# `decisions` block). The artifact is self-describing only if the data
# dictionary is populated; this is the minimum entry count expected.
DATA_DICT_MIN_ENTRIES: Final[int] = 30

# V11 — the cycle-1 scalar R field name. The founder dropped the scalar
# `r_revenue_cost` gospel field in favour of the R-band (D18); V11 fails if a
# scenario YAML re-adds it. The check also rejects any other bare-`r` scalar
# leaking into the gospel block — the R-band is the only sanctioned R input.
LEGACY_R_SCALAR_FIELD: Final[str] = "r_revenue_cost"
LEGACY_R_SCALAR_NAMES: Final[frozenset[str]] = frozenset({"r_revenue_cost", "r"})

# V12 — the B2B-premium R floor. The B2B dedicated-optical/RF operator model
# (D15) carries a premium over neocloud pricing (~1.16-1.19); the central R
# trajectory must start at or above this floor at the base year. The floor is
# 1.40 (not R4's 1.50) — strategy § 5.1 relaxes it to leave ~0.10 headroom
# for conservative B2B sensitivity scenarios while keeping the premium
# meaningfully above neocloud.
B2B_R_CENTRAL_FLOOR: Final[float] = 1.40

# V14 — launches per year must be integer, non-decreasing, equal to deployed
# nodes, and never exceed the cadence ceiling. The ceiling is read per-run from
# `inputs.cadence.cadence_ceiling`; this is the numeric slack tolerated when
# comparing the launch count against it.
CADENCE_CEILING_EPSILON: Final[float] = 1e-6

# V16 — the cohort service-life cliff window. The living fleet at year Y is
# the sum of node counts from cohorts launched in [Y - 4, Y] under the
# 5-year hard cliff (D1). The window span is service_life - 1 = 4 years back.
FLEET_CLIFF_LOOKBACK_YEARS: Final[int] = 4

# V17 — the radiator t/kW lower bound for the single-face co-mounted
# architecture (D16). R1's sourced band is 0.010-0.014 t/kW; a post-Tjmax
# dial below 0.010 would mean a two-face dedicated-radiator value was used
# with a co-mounted architecture lock — the cycle-1 mistake.
RADIATOR_T_PER_KW_CO_MOUNTED_MIN: Final[float] = 0.010


# ---------------------------------------------------------------------------
# V1 — mass_utilization_in_band (critical)
# ---------------------------------------------------------------------------


def check_mass_utilization_in_band(output: ValuationOutput) -> ValidationCheck:
    """Every year's ``physical.years[].mass_utilization_pct`` in [85, 100] (D2).

    Mass is the only hard physical constraint; a correctly-sized node
    should pack the envelope tight. Below 85% means the engine is leaving
    a tonne+ of slack and N is being clamped by something other than mass;
    above 100% is impossible by construction.
    """
    years = output.physical.years
    failing = [
        fy
        for fy, py in years.items()
        if not (MASS_UTIL_MIN_PCT <= _num(py.mass_utilization_pct.value) <= MASS_UTIL_MAX_PCT)
    ]
    if failing:
        computed = f"failed years: {sorted(failing)}"
    else:
        vals = [_num(py.mass_utilization_pct.value) for py in years.values()]
        computed = f"all {len(years)} years in [{min(vals):.2f}%, {max(vals):.2f}%]"
    return ValidationCheck(
        name="mass_utilization_in_band",
        what_it_tests=(
            f"every year's physical.mass_utilization_pct in "
            f"[{MASS_UTIL_MIN_PCT}, {MASS_UTIL_MAX_PCT}] (D2: mass is the "
            f"only hard constraint, so node packs the envelope tight)"
        ),
        expected=f"all years in [{MASS_UTIL_MIN_PCT}, {MASS_UTIL_MAX_PCT}]",
        computed=computed,
        pass_check=not failing,
        severity=Severity.CRITICAL,
    )


# ---------------------------------------------------------------------------
# V2 — no_trillion_dollar_pkg (critical)
# ---------------------------------------------------------------------------


def check_no_trillion_dollar_pkg(output: ValuationOutput) -> ValidationCheck:
    """``inputs.generations[*].usd_per_pkg`` must stay below ``USD_PER_PKG_MAX``.

    NVIDIA's "as sold" unit prices are tracked in plan § 0; even Feynman
    is $225K. Anything north of $5M is a data-entry typo or a fictional
    generation list.
    """
    gens = output.inputs.generations
    failing = [
        (str(g["name"]), int(g["usd_per_pkg"]))
        for g in gens
        if int(g["usd_per_pkg"]) >= USD_PER_PKG_MAX
    ]
    if failing:
        computed = "failed generations: " + ", ".join(f"{name}=${usd:,}" for name, usd in failing)
    else:
        max_pkg = max(int(g["usd_per_pkg"]) for g in gens)
        computed = f"all {len(gens)} generations under ${USD_PER_PKG_MAX:,} (max ${max_pkg:,})"
    return ValidationCheck(
        name="no_trillion_dollar_pkg",
        what_it_tests=(
            f"every generation's usd_per_pkg < ${USD_PER_PKG_MAX:,} (sane $/pkg sanity check)"
        ),
        expected=f"all generations under ${USD_PER_PKG_MAX:,}",
        computed=computed,
        pass_check=not failing,
        severity=Severity.CRITICAL,
    )


# ---------------------------------------------------------------------------
# V3 — positive_margin_floor (critical)
# ---------------------------------------------------------------------------


def check_positive_margin_floor(output: ValuationOutput) -> ValidationCheck:
    """Every active year's central gross margin must be above the floor.

    Margin = (R - 1) / R x 100. A 25% floor corresponds to R = 4/3, so the
    default central R trajectory should never decay below that level in any
    year with deployed revenue. No-fleet years are excluded because their
    revenue and margin are mechanically zero.
    """
    years = output.business.years
    active_years = {
        fy: by for fy, by in years.items() if _num(by.revenue_annual_fleet_musd_central.value) > 0
    }
    failing = [
        fy for fy, by in active_years.items() if _num(by.margin_central_pct.value) < MARGIN_PCT_MIN
    ]
    if failing:
        computed = f"failed years: {sorted(failing)}"
    elif not active_years:
        computed = "no active revenue years"
    else:
        vals = [_num(by.margin_central_pct.value) for by in active_years.values()]
        computed = (
            f"all {len(active_years)} active years central margin in "
            f"[{min(vals):.2f}%, {max(vals):.2f}%]"
        )
    return ValidationCheck(
        name="positive_margin_floor",
        what_it_tests=(
            f"every active year's business.margin_central_pct >= {MARGIN_PCT_MIN} "
            "(25% floor means R >= 1.333...)"
        ),
        expected=f"all active revenue years >= {MARGIN_PCT_MIN}",
        computed=computed,
        pass_check=not failing,
        severity=Severity.CRITICAL,
    )


# ---------------------------------------------------------------------------
# V4 — gpu_count_positive (critical)
# ---------------------------------------------------------------------------


def check_gpu_count_positive(output: ValuationOutput) -> ValidationCheck:
    """Every year's ``physical.years[].gpus_per_node`` must be >= 1.

    A zero-N year means the chosen frontier generation does not fit on
    the mass envelope at all — either the envelope was misconfigured
    (too small) or the generation's per-package mass is absurd.
    """
    years = output.physical.years
    failing = [fy for fy, py in years.items() if _num(py.gpus_per_node.value) < N_PACKAGES_MIN]
    if failing:
        computed = f"failed years: {sorted(failing)}"
    else:
        vals = [int(_num(py.gpus_per_node.value)) for py in years.values()]
        computed = f"all {len(years)} years N in [{min(vals)}, {max(vals)}]"
    return ValidationCheck(
        name="gpu_count_positive",
        what_it_tests=(
            f"every year's physical.gpus_per_node >= {N_PACKAGES_MIN} "
            f"(at least one package fits on the mass envelope)"
        ),
        expected=f"all years >= {N_PACKAGES_MIN}",
        computed=computed,
        pass_check=not failing,
        severity=Severity.CRITICAL,
    )


# ---------------------------------------------------------------------------
# V5 — monotonic_pf_per_kw (major)
# ---------------------------------------------------------------------------


def check_monotonic_pf_per_kw(output: ValuationOutput) -> ValidationCheck:
    """PF/kW must be near-monotonic year-over-year.

    **Re-targeted (cycle-2 Phase 4A).** Cycle-1's V5 checked
    ``cost.compute_share`` monotonicity; the v8 schema dropped the
    compute-share field, so V5 is re-pointed at the next-best
    trajectory invariant — compute density. PF/kW trends up as silicon
    (PF/pkg) outpaces power (kW/pkg); for every consecutive pair:

        ``pf_per_kw[i+1] >= pf_per_kw[i] - PF_PER_KW_MAX_DIP``

    A drop larger than the tolerance usually means a frontier-generation
    mis-pick or an extrapolation-slope mis-step.
    """
    items = sorted(output.physical.years.items(), key=lambda kv: int(kv[0]))
    failing: list[tuple[str, str]] = []
    for (fy_a, py_a), (fy_b, py_b) in zip(items, items[1:], strict=False):
        prev = _num(py_a.pf_per_kw.value)
        nxt = _num(py_b.pf_per_kw.value)
        if nxt < prev - PF_PER_KW_MAX_DIP:
            failing.append((fy_a, fy_b))
    if failing:
        computed = "failed pairs: " + ", ".join(f"FY{a}->FY{b}" for a, b in failing)
    else:
        computed = f"all {max(len(items) - 1, 0)} consecutive pairs within tolerance"
    return ValidationCheck(
        name="monotonic_pf_per_kw",
        what_it_tests=(
            f"for every consecutive pair: pf_per_kw[i+1] >= pf_per_kw[i] - "
            f"{PF_PER_KW_MAX_DIP} (compute density trends up year-over-year)"
        ),
        expected="non-decreasing within tolerance",
        computed=computed,
        pass_check=not failing,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V6 — pf_per_kw_in_band (major)
# ---------------------------------------------------------------------------


def check_pf_per_kw_in_band(output: ValuationOutput) -> ValidationCheck:
    """Last year's ``physical.years[].pf_per_kw`` must lie in [20, 80].

    Brainstorm Part IX maps this band to the pessimistic-to-optimistic
    post-Feynman PF/kW slope. Below 20 means silicon stopped outpacing
    power; above 80 means the slope is unrealistically aggressive.
    """
    years = output.physical.years
    if not years:
        return ValidationCheck(
            name="pf_per_kw_in_band",
            what_it_tests=(
                f"last year's physical.pf_per_kw in [{PF_PER_KW_MIN}, "
                f"{PF_PER_KW_MAX}] (Part IX sensitivity band)"
            ),
            expected=f"last year in [{PF_PER_KW_MIN}, {PF_PER_KW_MAX}]",
            computed="no years emitted",
            pass_check=False,
            severity=Severity.MAJOR,
        )
    last_fy = max(years, key=int)
    pf_per_kw = _num(years[last_fy].pf_per_kw.value)
    in_band = PF_PER_KW_MIN <= pf_per_kw <= PF_PER_KW_MAX
    return ValidationCheck(
        name="pf_per_kw_in_band",
        what_it_tests=(
            f"last year's physical.pf_per_kw in [{PF_PER_KW_MIN}, "
            f"{PF_PER_KW_MAX}] (Part IX sensitivity band)"
        ),
        expected=f"last year in [{PF_PER_KW_MIN}, {PF_PER_KW_MAX}]",
        computed=f"FY{last_fy} pf_per_kw = {pf_per_kw:.2f}",
        pass_check=in_band,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V7 — launch_cost_non_increasing (minor)
# ---------------------------------------------------------------------------


def check_launch_cost_non_increasing(output: ValuationOutput) -> ValidationCheck:
    """``business.years[].launch_cost_this_year_musd`` non-increasing year-over-year.

    Per D12, launch cost falls as Neutron's cadence matures (the
    cadence-indexed log-linear curve is monotone non-increasing in the
    launch rate, and the launch rate is non-decreasing). An increase in
    any pair would mean a config typo or a sign-flipped interpolation.
    """
    items = sorted(output.business.years.items(), key=lambda kv: int(kv[0]))
    failing: list[tuple[str, str]] = []
    for (fy_a, by_a), (fy_b, by_b) in zip(items, items[1:], strict=False):
        prev = _num(by_a.launch_cost_this_year_musd.value)
        nxt = _num(by_b.launch_cost_this_year_musd.value)
        if nxt > prev:
            failing.append((fy_a, fy_b))
    if failing:
        computed = "failed pairs: " + ", ".join(f"FY{a}->FY{b}" for a, b in failing)
    elif items:
        first = _num(items[0][1].launch_cost_this_year_musd.value)
        last = _num(items[-1][1].launch_cost_this_year_musd.value)
        computed = f"launch cost ${first:.2f}M -> ${last:.2f}M (non-increasing)"
    else:
        computed = "no years emitted"
    return ValidationCheck(
        name="launch_cost_non_increasing",
        what_it_tests=(
            "business.launch_cost_this_year_musd non-increasing year-over-year "
            "(D12: Neutron cadence ramp drives launch cost down)"
        ),
        expected="non-increasing",
        computed=computed,
        pass_check=not failing,
        severity=Severity.MINOR,
    )


# ---------------------------------------------------------------------------
# V8 — revenue_above_cost_per_node (critical)
# ---------------------------------------------------------------------------


def check_revenue_above_cost_per_node(output: ValuationOutput) -> ValidationCheck:
    """Every year's per-node central revenue must exceed per-node annual cost.

    **Re-pathed (cycle-2 Phase 4A).** Cycle-1's V8 compared lifetime
    revenue / cost per package; the v8 schema carries annualized per-node
    economics, so V8 checks the same R > 1 floor on the v8 fields:
    ``revenue_annual_per_node_musd_central > cost_annual_per_node_musd``
    in every year. A violation means R <= 1 for that vintage.
    """
    years = output.physical.years
    failing = [
        fy
        for fy, py in years.items()
        if _num(py.revenue_annual_per_node_musd_central.value)
        <= _num(py.cost_annual_per_node_musd.value)
    ]
    if failing:
        computed = f"failed years: {sorted(failing)}"
    else:
        ratios = [
            _num(py.revenue_annual_per_node_musd_central.value)
            / _num(py.cost_annual_per_node_musd.value)
            for py in years.values()
            if _num(py.cost_annual_per_node_musd.value) > 0
        ]
        if ratios:
            computed = (
                f"all {len(years)} years rev/cost ratio in [{min(ratios):.3f}, {max(ratios):.3f}]"
            )
        else:
            computed = "no years with positive cost-per-node to compare"
    return ValidationCheck(
        name="revenue_above_cost_per_node",
        what_it_tests=(
            "every year's revenue_annual_per_node_musd_central > "
            "cost_annual_per_node_musd (D9 R > 1 floor on a per-node basis)"
        ),
        expected="all years rev/node > cost/node",
        computed=computed,
        pass_check=not failing,
        severity=Severity.CRITICAL,
    )


# ---------------------------------------------------------------------------
# V9 — cost_annual_per_node_in_band (major)
# ---------------------------------------------------------------------------


def check_cost_annual_per_node_in_band(output: ValuationOutput) -> ValidationCheck:
    """Every year's ``cost_annual_per_node_musd`` must lie in [5, 60].

    **Re-pathed (cycle-2 Phase 4A).** Cycle-1's V9 banded the per-node
    *total* cost [50, 200]; the v8 schema carries the *annualized* per-node
    cost (total / service life), so the band is the cycle-1 band over a
    5-year life — [10, 40] — widened to [5, 60] to tolerate the 3-year and
    7-year service-life scenarios.
    """
    years = output.physical.years
    failing = [
        (fy, _num(py.cost_annual_per_node_musd.value))
        for fy, py in years.items()
        if not (
            COST_ANNUAL_MIN_MUSD <= _num(py.cost_annual_per_node_musd.value) <= COST_ANNUAL_MAX_MUSD
        )
    ]
    if failing:
        computed = "failed years: " + ", ".join(f"FY{fy}: ${v:.1f}M" for fy, v in sorted(failing))
    else:
        vals = [_num(py.cost_annual_per_node_musd.value) for py in years.values()]
        computed = f"all {len(years)} years cost_annual in [${min(vals):.1f}M, ${max(vals):.1f}M]"
    return ValidationCheck(
        name="cost_annual_per_node_in_band",
        what_it_tests=(
            f"every year's cost_annual_per_node_musd in "
            f"[${COST_ANNUAL_MIN_MUSD:.0f}M, ${COST_ANNUAL_MAX_MUSD:.0f}M] "
            f"(sanity range for one annualized Neutron SSO scenario node)"
        ),
        expected=(f"all years in [${COST_ANNUAL_MIN_MUSD:.0f}M, ${COST_ANNUAL_MAX_MUSD:.0f}M]"),
        computed=computed,
        pass_check=not failing,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V10 — data_dictionary_populated (major)
# ---------------------------------------------------------------------------


def check_data_dictionary_populated(output: ValuationOutput) -> ValidationCheck:
    """The ``meta.data_dictionary`` block must be populated.

    **Re-targeted (cycle-2 Phase 4A).** Cycle-1's V10 asserted the
    ``decisions`` block held all 13 D-decisions; the v8 schema dropped the
    ``decisions`` block, so V10 is re-pointed at the v8 self-describing
    block — the data dictionary. The artifact is only self-describing if
    the introspected data dictionary covers every emitted leaf; an empty
    or near-empty dictionary means the build step silently failed.
    """
    count = len(output.meta.data_dictionary)
    ok = count >= DATA_DICT_MIN_ENTRIES
    return ValidationCheck(
        name="data_dictionary_populated",
        what_it_tests=(
            f"meta.data_dictionary has >= {DATA_DICT_MIN_ENTRIES} entries "
            f"(the artifact is self-describing)"
        ),
        expected=f">= {DATA_DICT_MIN_ENTRIES} entries",
        computed=f"{count} entries",
        pass_check=ok,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V11 — no_legacy_r_scalar (major)
# ---------------------------------------------------------------------------


def check_no_legacy_r_scalar(output: ValuationOutput) -> ValidationCheck:
    """The ``inputs.gospel`` block must carry no legacy scalar R field.

    The founder dropped the cycle-1 scalar ``r_revenue_cost`` gospel field
    in favour of the three-trajectory R-band (D18); R is now modelled only
    as :class:`data_center.config.RBand`. V11 fails fast if a scenario YAML
    accidentally re-adds ``r_revenue_cost`` (or any other bare-``r`` scalar)
    to the gospel block — a stale scalar would silently shadow the band and
    quietly mis-state revenue.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if a legacy scalar R name
        is present in ``inputs.gospel``.
    """
    indexed_leaf_names = {path.rsplit(".", 1)[-1] for path in output.inputs.assumption_index}
    gospel_keys = set(output.inputs.gospel) | indexed_leaf_names
    offenders = sorted(gospel_keys & LEGACY_R_SCALAR_NAMES)
    if offenders:
        computed = f"inputs.gospel carries legacy scalar R field(s): {offenders}"
    else:
        computed = (
            f"inputs.gospel has no legacy scalar R field "
            f"({len(gospel_keys)} gospel keys, R modelled as the R-band)"
        )
    return ValidationCheck(
        name="no_legacy_r_scalar",
        what_it_tests=(
            f"inputs.gospel carries no legacy scalar R field "
            f"({sorted(LEGACY_R_SCALAR_NAMES)}); R is modelled only as the "
            f"R-band (D18)"
        ),
        expected=f"no {LEGACY_R_SCALAR_FIELD} (or bare 'r') in inputs.gospel",
        computed=computed,
        pass_check=not offenders,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V12 — operator_r_consistency (major)
# ---------------------------------------------------------------------------


def _r_central_at(output: ValuationOutput, year: int) -> float:
    """Return the central-R-band value at ``year``.

    Evaluates the central R trajectory the same way the engine does
    (:func:`data_center.fleet.r_at_year`): clamped flat outside the anchor
    range, linearly interpolated between adjacent anchors otherwise. The
    R-band's anchors are guaranteed sorted by ``fy`` ascending and at least
    two entries long (:class:`data_center.config.RBand` validator).

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.
        year: The calendar year at which to evaluate central R.

    Returns:
        The interpolated central-R value at ``year``.
    """
    anchors = output.inputs.r_band.central
    if year <= anchors[0].fy:
        return anchors[0].r
    if year >= anchors[-1].fy:
        return anchors[-1].r
    for a, b in zip(anchors, anchors[1:], strict=False):
        if a.fy <= year <= b.fy:
            frac = (year - a.fy) / (b.fy - a.fy)
            return a.r + frac * (b.r - a.r)
    return anchors[-1].r  # unreachable — covered by the clamps above


def check_operator_r_consistency(output: ValuationOutput) -> ValidationCheck:
    """B2B operator model implies central R at base year >= the B2B floor.

    The B2B dedicated-optical/RF operator model (D15) carries a pricing
    premium over neocloud (~1.16-1.19); the central R trajectory must
    therefore start at or above ``B2B_R_CENTRAL_FLOOR`` (1.40) at the base
    year. A central-R below the floor means either the model is
    underselling the B2B premium or the operator-model lock is wrong.

    The floor is 1.40, not the R4-recommended 1.50 — strategy § 5.1
    relaxes it to leave headroom for conservative B2B sensitivity
    scenarios while keeping the premium meaningfully above neocloud.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if the operator model is
        B2B and central R at the base year is below the floor.
    """
    base_year = output.metadata.base_year
    operator = output.metadata.operator_model
    r_central_base = _r_central_at(output, base_year)
    is_b2b = operator == OperatorModel.B2B_DEDICATED_OPTICAL_RF
    # The rule only constrains B2B runs; a non-B2B operator model passes
    # vacuously (the floor is a B2B-premium check).
    failed = is_b2b and r_central_base < B2B_R_CENTRAL_FLOOR
    if failed:
        computed = (
            f"operator_model={operator.value}, central R at base year "
            f"{base_year} = {r_central_base:.3f} (< {B2B_R_CENTRAL_FLOOR} floor)"
        )
    elif is_b2b:
        computed = (
            f"operator_model={operator.value}, central R at base year "
            f"{base_year} = {r_central_base:.3f} (>= {B2B_R_CENTRAL_FLOOR} floor)"
        )
    else:
        computed = f"operator_model={operator.value}: B2B floor not applicable"
    return ValidationCheck(
        name="operator_r_consistency",
        what_it_tests=(
            f"operator_model == B2B_DEDICATED_OPTICAL_RF implies central R "
            f"at the base year >= {B2B_R_CENTRAL_FLOOR} (the B2B-premium "
            f"floor, D15)"
        ),
        expected=f"central R at base year >= {B2B_R_CENTRAL_FLOOR} when B2B",
        computed=computed,
        pass_check=not failed,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V13 — provenance_formula_keys (major)
# ---------------------------------------------------------------------------


def _cells_of(record: BaseModel) -> list[ProvenanceCell]:
    """Collect every :class:`ProvenanceCell` in one per-year record.

    A field is either a ProvenanceCell leaf or a nested :class:`BaseModel`
    sub-object (e.g. ``PhysicalYear.cost_breakdown``, a
    :class:`output.CostBreakdownBlock` of six cells); a nested model is
    walked one level deeper to reach the cells it holds.

    Args:
        record: One per-year record (a :class:`output.PhysicalYear` or
            :class:`output.BusinessYear`).

    Returns:
        Every ProvenanceCell the record carries, in field-declaration order.
    """
    cells: list[ProvenanceCell] = []
    for field_name in type(record).model_fields:
        value = getattr(record, field_name)
        if isinstance(value, ProvenanceCell):
            cells.append(value)
        elif isinstance(value, BaseModel):
            cells.extend(_cells_of(value))
    return cells


def _all_provenance_cells(output: ValuationOutput) -> list[ProvenanceCell]:
    """Collect every :class:`ProvenanceCell` leaf in the v8 output.

    ProvenanceCell leaves live only in the per-year ``physical.years`` and
    ``business.years`` maps — every field of :class:`output.PhysicalYear`
    and :class:`output.BusinessYear` is a ProvenanceCell or a nested
    sub-object of cells (``cost_breakdown``). The ``inputs`` block carries
    config models and flat dicts (no cells), so walking the two per-year
    maps reaches every cell in the artifact.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        Every ProvenanceCell in the artifact, physical years then business
        years, each year's cells in model-field declaration order.
    """
    cells: list[ProvenanceCell] = []
    for py in output.physical.years.values():
        cells.extend(_cells_of(py))
    for by in output.business.years.values():
        cells.extend(_cells_of(by))
    return cells


def check_provenance_formula_keys(output: ValuationOutput) -> ValidationCheck:
    """Every ProvenanceCell's ``formula_name`` must exist in :data:`FORMULAS`.

    Every leaf numeric value in the v8 output is a
    :class:`data_center.provenance.ProvenanceCell` carrying a
    ``formula_name`` — a stable key into the :data:`FORMULAS` lookup table.
    V13 walks every cell and fails if any ``formula_name`` is absent from
    :data:`FORMULAS`. This catches a silent typo in a formula-name string
    (which would otherwise ship an un-resolvable provenance reference) and
    enforces the plan § 0.8 rule that a new formula name must be registered
    in :data:`FORMULAS` before use.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if any cell references a
        ``formula_name`` not present in :data:`FORMULAS`.
    """
    cells = _all_provenance_cells(output)
    used = {c.formula_name for c in cells}
    missing = sorted(name for name in used if name not in FORMULAS)
    if missing:
        computed = f"{len(cells)} cells; formula_name(s) absent from FORMULAS: {missing}"
    else:
        computed = (
            f"all {len(cells)} cells reference one of {len(used)} formula "
            f"names, every one present in FORMULAS"
        )
    return ValidationCheck(
        name="provenance_formula_keys",
        what_it_tests=(
            "every ProvenanceCell formula_name exists in the FORMULAS "
            "lookup table (no silent formula-name typos)"
        ),
        expected="all formula_name values present in FORMULAS",
        computed=computed,
        pass_check=not missing,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V14 — cadence_monotonicity (major)
# ---------------------------------------------------------------------------


def check_cadence_monotonicity(output: ValuationOutput) -> ValidationCheck:
    """Launches per year are integer, monotonic, and within the ceiling.

    The launch cadence is a logistic ramp (D7): launches per year must be
    whole-number mission counts, monotonically non-decreasing across the
    horizon, and no year may exceed the configured
    ``inputs.cadence.cadence_ceiling`` hard cap. The emitted
    ``nodes_deployed_this_year`` count must also equal launches because the
    default node contract is one node per Neutron flight. A fractional value
    would mean a raw launch rate leaked into the public model; a decrease
    would mean a sign-flipped logistic; a value above the ceiling would mean
    the clamp failed. ``business.years[].launches`` carries the per-year
    cadence.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if launch/node counts are
        fractional, launches dip year-over-year, nodes differ from launches,
        or launches exceed the cadence ceiling.
    """
    ceiling = output.inputs.cadence.cadence_ceiling
    items = sorted(output.business.years.items(), key=lambda kv: int(kv[0]))
    launches = [(fy, _num(by.launches.value)) for fy, by in items]
    nodes = [(fy, _num(by.nodes_deployed_this_year.value)) for fy, by in items]
    fractional = [(fy, val) for fy, val in launches if not val.is_integer()]
    fractional_nodes = [(fy, val) for fy, val in nodes if not val.is_integer()]
    node_mismatches = [
        (fy_l, launch_val, node_val)
        for (fy_l, launch_val), (fy_n, node_val) in zip(launches, nodes, strict=True)
        if fy_l != fy_n or int(launch_val) != int(node_val)
    ]

    decreasing: list[tuple[str, str]] = [
        (fy_a, fy_b)
        for (fy_a, val_a), (fy_b, val_b) in zip(launches, launches[1:], strict=False)
        if val_b < val_a
    ]
    over_ceiling = [(fy, val) for fy, val in launches if val > ceiling + CADENCE_CEILING_EPSILON]

    if fractional or fractional_nodes or node_mismatches or decreasing or over_ceiling:
        problems: list[str] = []
        if fractional:
            problems.append(
                "fractional launches at " + ", ".join(f"FY{fy}={val:.2f}" for fy, val in fractional)
            )
        if fractional_nodes:
            problems.append(
                "fractional nodes at "
                + ", ".join(f"FY{fy}={val:.2f}" for fy, val in fractional_nodes)
            )
        if node_mismatches:
            problems.append(
                "launch/node mismatches at "
                + ", ".join(
                    f"FY{fy}: launches={launch_val:.0f}, nodes={node_val:.0f}"
                    for fy, launch_val, node_val in node_mismatches
                )
            )
        if decreasing:
            problems.append("dips at " + ", ".join(f"FY{a}->FY{b}" for a, b in decreasing))
        if over_ceiling:
            problems.append(
                "over ceiling at " + ", ".join(f"FY{fy}={val:.2f}" for fy, val in over_ceiling)
            )
        computed = "; ".join(problems)
    elif launches:
        computed = (
            f"integer launches {launches[0][1]:.0f} -> {launches[-1][1]:.0f} over "
            f"{len(launches)} years, non-decreasing and <= ceiling {ceiling}"
        )
    else:
        computed = "no years emitted"
    passed = (
        not fractional
        and not fractional_nodes
        and not node_mismatches
        and not decreasing
        and not over_ceiling
    )
    return ValidationCheck(
        name="cadence_monotonicity",
        what_it_tests=(
            "business.launches integer-valued, non-decreasing year-over-year, "
            "equal to nodes_deployed_this_year, and every year <= "
            "inputs.cadence.cadence_ceiling (D7 logistic ramp)"
        ),
        expected="integer, nodes == launches, non-decreasing, and <= cadence_ceiling",
        computed=computed,
        pass_check=passed,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V15 — volume_fits_horizon (major)
# ---------------------------------------------------------------------------


def check_volume_fits_horizon(output: ValuationOutput) -> ValidationCheck:
    """No year may be volume-only-bound — mass binds first (D6).

    D6 makes mass the only hard physical constraint; the stowed-volume
    check is for transparency and must never gate the package count. For
    every year, ``physical.years[].binding_constraint`` must be one of
    ``MASS`` / ``BOTH`` / ``NEITHER`` — a sole ``VOLUME`` value means the
    radiator/solar dials are pushing the node to bust the fairing volume
    before the mass envelope, contradicting D6. V15 fails if any year is
    volume-only-bound.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if any year's
        ``binding_constraint`` is sole ``VOLUME``.
    """
    volume_only = BindingConstraint.VOLUME.value
    years = output.physical.years
    failing = [fy for fy, py in years.items() if str(py.binding_constraint.value) == volume_only]
    if failing:
        computed = f"volume-only-bound years: {sorted(failing)}"
    else:
        seen = sorted({str(py.binding_constraint.value) for py in years.values()})
        computed = f"all {len(years)} years bound by {seen} (no sole VOLUME)"
    return ValidationCheck(
        name="volume_fits_horizon",
        what_it_tests=(
            "every year's physical.binding_constraint is one of "
            "{mass, both, neither}; sole 'volume' is forbidden (D6: "
            "mass-only binding)"
        ),
        expected="no year is volume-only-bound",
        computed=computed,
        pass_check=not failing,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V16 — fleet_cliff_consistency (major)
# ---------------------------------------------------------------------------


def check_fleet_cliff_consistency(output: ValuationOutput) -> ValidationCheck:
    """``living_fleet[Y]`` equals the cohort-cliff sum of node counts.

    Under the 5-year hard cliff (D1) the living fleet at year Y is the sum
    of node counts from cohorts launched in ``[Y - 4, Y]``. The engine
    deploys the integer ``launches`` count directly, so V16 re-derives each
    year's living fleet as ``sum(launches[c] for c in [Y - 4, Y])`` over
    the trajectory years and fails on any mismatch with the emitted
    ``business.years[].living_fleet``.

    The cohort-year window is intersected with the emitted trajectory —
    cohorts before the first model year do not exist, exactly as the
    engine's fleet rollup treats them.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if any year's emitted
        living fleet differs from the re-derived cohort-cliff sum.
    """
    years = output.business.years
    nodes_by_year: dict[int, int] = {
        int(fy): int(_num(by.launches.value)) for fy, by in years.items()
    }
    mismatches: list[tuple[str, int, int]] = []
    for fy, by in years.items():
        y = int(fy)
        derived = sum(
            nodes_by_year[c]
            for c in range(y - FLEET_CLIFF_LOOKBACK_YEARS, y + 1)
            if c in nodes_by_year
        )
        emitted = round(_num(by.living_fleet.value))
        if derived != emitted:
            mismatches.append((fy, emitted, derived))
    if mismatches:
        computed = "mismatches: " + ", ".join(
            f"FY{fy}: emitted {emitted} vs cliff-sum {derived}"
            for fy, emitted, derived in sorted(mismatches)
        )
    else:
        computed = (
            f"all {len(years)} years: living_fleet == "
            f"sum(launches[Y-{FLEET_CLIFF_LOOKBACK_YEARS}..Y])"
        )
    return ValidationCheck(
        name="fleet_cliff_consistency",
        what_it_tests=(
            "every year's business.living_fleet == sum of integer launches "
            f"over the cohort window [Y-{FLEET_CLIFF_LOOKBACK_YEARS}, Y] "
            f"(D1 5-year hard cliff)"
        ),
        expected="living_fleet matches the cohort-cliff sum every year",
        computed=computed,
        pass_check=not mismatches,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# V17 — radiator_dial_matches_architecture (major)
# ---------------------------------------------------------------------------


def check_radiator_dial_arch_consistency(output: ValuationOutput) -> ValidationCheck:
    """Single-face co-mounted architecture implies the radiator dial >= 0.010.

    The single-face co-mounted radiator architecture (D16) has an R1-sourced
    post-Tjmax t/kW band of 0.010-0.014. V17 fails if
    ``metadata.radiator_architecture`` is ``SINGLE_FACE_CO_MOUNTED`` while
    ``inputs.gospel.radiator_t_per_kw_post`` is below the 0.010 lower bound
    — that would mean a leaner two-face dedicated-radiator dial was paired
    with the co-mounted architecture lock, the exact cycle-1 mistake D17
    corrects.

    Args:
        output: A fully-built v8 :class:`ValuationOutput`.

    Returns:
        A :class:`ValidationCheck`; fails (MAJOR) if the architecture is
        single-face co-mounted and the post-Tjmax radiator dial is below
        the floor.
    """
    architecture = output.metadata.radiator_architecture
    radiator_post = float(output.inputs.gospel["radiator_t_per_kw_post"])
    is_co_mounted = architecture == RadiatorArchitecture.SINGLE_FACE_CO_MOUNTED
    failed = is_co_mounted and radiator_post < RADIATOR_T_PER_KW_CO_MOUNTED_MIN
    if failed:
        computed = (
            f"radiator_architecture={architecture.value}, "
            f"radiator_t_per_kw_post={radiator_post} "
            f"(< {RADIATOR_T_PER_KW_CO_MOUNTED_MIN} floor)"
        )
    elif is_co_mounted:
        computed = (
            f"radiator_architecture={architecture.value}, "
            f"radiator_t_per_kw_post={radiator_post} "
            f"(>= {RADIATOR_T_PER_KW_CO_MOUNTED_MIN} floor)"
        )
    else:
        computed = f"radiator_architecture={architecture.value}: co-mounted floor not applicable"
    return ValidationCheck(
        name="radiator_dial_matches_architecture",
        what_it_tests=(
            f"radiator_architecture == SINGLE_FACE_CO_MOUNTED implies "
            f"inputs.gospel.radiator_t_per_kw_post >= "
            f"{RADIATOR_T_PER_KW_CO_MOUNTED_MIN} (R1 0.010-0.014 band, D16/D17)"
        ),
        expected=(f"radiator_t_per_kw_post >= {RADIATOR_T_PER_KW_CO_MOUNTED_MIN} when co-mounted"),
        computed=computed,
        pass_check=not failed,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# Cell-value unwrap helper
# ---------------------------------------------------------------------------


def _num(value: float | int | str | bool | None) -> float:
    """Unwrap a :class:`ProvenanceCell` value to a numeric ``float``.

    The v8 output's leaf values are ProvenanceCell values — a union over
    numeric / str / bool / None. The validation rules only ever read
    numeric cells; this helper narrows the union for mypy and raises if a
    rule is pointed at a non-numeric cell by mistake.

    Args:
        value: A ProvenanceCell's ``value`` field.

    Returns:
        The value as a ``float``.

    Raises:
        TypeError: If the value is not a real number.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"validation rule expected a numeric cell value, got {value!r}")
    return float(value)


# ---------------------------------------------------------------------------
# Top-level: run all rules in V1..V17 order
# ---------------------------------------------------------------------------


_RULES: Final[tuple[Callable[[ValuationOutput], ValidationCheck], ...]] = (
    # V1-V10 — cycle-1 rules, re-pathed to the v8 output structure.
    check_mass_utilization_in_band,
    check_no_trillion_dollar_pkg,
    check_positive_margin_floor,
    check_gpu_count_positive,
    check_monotonic_pf_per_kw,
    check_pf_per_kw_in_band,
    check_launch_cost_non_increasing,
    check_revenue_above_cost_per_node,
    check_cost_annual_per_node_in_band,
    check_data_dictionary_populated,
    # V11-V17 — cycle-2 rules (strategy § 5.1).
    check_no_legacy_r_scalar,
    check_operator_r_consistency,
    check_provenance_formula_keys,
    check_cadence_monotonicity,
    check_volume_fits_horizon,
    check_fleet_cliff_consistency,
    check_radiator_dial_arch_consistency,
)


def compute_validation(output: ValuationOutput) -> list[ValidationCheck]:
    """Run all 17 V1..V17 rules and return the resulting checks in order.

    Args:
        output: A fully-built v8 :class:`ValuationOutput` (post-engine).

    Returns:
        A 17-element list of :class:`ValidationCheck` instances in V1..V17
        declaration order (V1-V10 cycle-1 re-pathed, V11-V17 cycle-2 new).
        The engine wires the result into
        :attr:`ValuationOutput.meta.validation`.
    """
    return [rule(output) for rule in _RULES]


__all__ = [
    "B2B_R_CENTRAL_FLOOR",
    "CADENCE_CEILING_EPSILON",
    "COST_ANNUAL_MAX_MUSD",
    "COST_ANNUAL_MIN_MUSD",
    "DATA_DICT_MIN_ENTRIES",
    "FLEET_CLIFF_LOOKBACK_YEARS",
    "LEGACY_R_SCALAR_FIELD",
    "LEGACY_R_SCALAR_NAMES",
    "MARGIN_PCT_MIN",
    "MASS_UTIL_MAX_PCT",
    "MASS_UTIL_MIN_PCT",
    "N_PACKAGES_MIN",
    "PF_PER_KW_MAX",
    "PF_PER_KW_MAX_DIP",
    "PF_PER_KW_MIN",
    "RADIATOR_T_PER_KW_CO_MOUNTED_MIN",
    "USD_PER_PKG_MAX",
    "check_cadence_monotonicity",
    "check_cost_annual_per_node_in_band",
    "check_data_dictionary_populated",
    "check_fleet_cliff_consistency",
    "check_gpu_count_positive",
    "check_launch_cost_non_increasing",
    "check_mass_utilization_in_band",
    "check_monotonic_pf_per_kw",
    "check_no_legacy_r_scalar",
    "check_no_trillion_dollar_pkg",
    "check_operator_r_consistency",
    "check_pf_per_kw_in_band",
    "check_positive_margin_floor",
    "check_provenance_formula_keys",
    "check_radiator_dial_arch_consistency",
    "check_revenue_above_cost_per_node",
    "check_volume_fits_horizon",
    "compute_validation",
]
