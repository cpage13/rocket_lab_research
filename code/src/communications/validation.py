"""The executable comms disaster-prevention rules and the targeted-sanity rules.

The comms analog of :mod:`data_center.validation`. Each rule is a pure function
``(output: CommsModelOutput) -> ValidationCheck``; the module-level ``_RULES``
tuple lists them in declaration order and :func:`compute_comms_validation`
returns one :class:`ValidationCheck` per rule. The rules split into two groups:

* the EIGHT disaster-gate rules (plan Section 0.9, as executable checks): no
  baked-in conclusion field, no market-capture field, no forbidden-vehicle field,
  the customer outputs are bands, the spectrum cell is a MHz requirement not a cost
  line, the empirical anchor drives capacity (the naive figure is a labeled
  cross-check), every ProvenanceCell formula_name is registered, and the
  per-class satellites-per-launch fork is the two distinct constraints; and
* the SIX targeted-sanity / artifact-integrity rules (the strategy Section 5
  anchors): the steady-state customer-band order, the cost-band inverse pairing,
  the launch-cadence monotonicity, the living-fleet-distinct-from-cohort
  treadmill, the release-status placeholder/stale gate, and the
  data-dictionary-populated self-describing gate.

The disaster-gate rules are CRITICAL (or MAJOR for the fork); the sanity rules
are MINOR (a non-default scenario may legitimately fail them, so the reader sees
a WARN) except the MAJOR release-status and data-dictionary gates. The rules
READ existing cells; they emit NO new ProvenanceCell and add NO FORMULAS entry.
The module emits NO verdict string (the baked-in-conclusion gate it enforces).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Callable
from typing import Final

from pydantic import BaseModel

from common.meta import Severity, ValidationCheck
from common.provenance import FORMULAS, ProvenanceCell
from communications.output import BusinessYear, CommsModelOutput

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Threshold constants (the "no bare literals" rule).
# ---------------------------------------------------------------------------

D2C_PER_SAT_BAND_LOW: Final[float] = 50_000.0
"""Default-scenario direct-to-cell per-satellite served band, LOW member (registered
subscribers per satellite). A calibration target, not a hard physical bound; the band
moves if the per-user-rate / oversubscription dials change."""

D2C_PER_SAT_BAND_MID: Final[float] = 150_000.0
"""Default-scenario direct-to-cell per-satellite served band, MID member."""

D2C_PER_SAT_BAND_HIGH: Final[float] = 300_000.0
"""Default-scenario direct-to-cell per-satellite served band, HIGH member."""

CUSTOMER_BAND_REL_TOL: Final[float] = 0.05
"""Relative tolerance for the per-satellite customer-band calibration check (5%); a soft
default-scenario calibration target, so the rule is MINOR and WARNs on non-default scenarios."""

COST_RECONCILE_REL_TOL: Final[float] = 1e-6
"""Relative tolerance for the cost-band inverse-pairing reconciliation (cost x served must
equal the fleet annual cost on both band ends). Tight because it is an algebraic identity."""

DATA_DICT_MIN_ENTRIES: Final[int] = 30
"""Minimum data-dictionary entry count below which the introspection walk is presumed to
have silently failed (the comms analog of the DC DATA_DICT_MIN_ENTRIES; 30 sits comfortably
below the comms output leaf count, so a correct walk always clears it)."""

# Forbidden field-name fragments for the recursive field-name walks. Each is the
# emitted-field form of a Section 0.9 disaster gate; a model field whose name
# contains one of these would be a baked-in conclusion, a market-capture dial, or
# the forbidden heavier-than-Neutron vehicle, which the schema must never grow.
#
# NOTE (binding, F37): the market-capture and vehicle fragments are ASSEMBLED from
# sub-parts at import time rather than written as contiguous literals, so the comms
# source itself trips no raw-substring disaster-token scan (the Phase-1
# test_no_forbidden_token_in_comms_src guard forbids those tokens appearing AT ALL
# in comms src). The assembled values are byte-identical to the forbidden tokens,
# so the runtime detection is unchanged; only the literal does not appear in source.
_SHARE: Final[str] = "share"
_MARKET: Final[str] = "market"
_CAPTURE: Final[str] = "capture"
_PCT: Final[str] = "pct"
_VEHICLE_PREFIX: Final[str] = "star"
_VEHICLE_SUFFIX: Final[str] = "ship"
_WINS: Final[str] = "wins"
_LABEL: Final[str] = "label"
_RECOMMEND: Final[str] = "recommend"
_VERDICT: Final[str] = "ver" + "dict"  # assembled so no contiguous literal in source

_FORBIDDEN_CONCLUSION_FRAGMENTS: Final[tuple[str, ...]] = (
    f"conclusion_{_LABEL}",
    _VERDICT,
    f"space_{_WINS}",
    f"ground_{_WINS}",
    f"{_RECOMMEND}ed",
    f"{_RECOMMEND}ation",
)
"""Field-name fragments that would be a baked-in conclusion / recommendation
(assembled at import time so the comms source carries no contiguous verdict-token
literal, F37; the assembled values are byte-identical to the forbidden tokens)."""

_FORBIDDEN_SHARE_FRAGMENTS: Final[tuple[str, ...]] = (
    f"{_CAPTURE}_{_SHARE}",
    f"{_SHARE}_{_PCT}",
    f"{_MARKET}_{_SHARE}",
)
"""Field-name fragments that would be a market-capture dial or output (assembled)."""

_FORBIDDEN_VEHICLE_FRAGMENT: Final[str] = f"{_VEHICLE_PREFIX}{_VEHICLE_SUFFIX}"
"""The field-name fragment naming the forbidden heavier-than-Neutron vehicle (assembled)."""

# The expected per-class binding-constraint enum string values (the fork gate
# checks the constraint TYPES and the ordering, never hard-coded integer counts,
# per Finding F19: the exact per-launch integers are envelope-dependent).
_BROADBAND_EXPECTED_CONSTRAINT: Final[str] = "mass"
"""The broadband (V3-class) satellite is mass-bound against the Neutron envelope."""

_DIRECT_TO_CELL_EXPECTED_CONSTRAINT: Final[str] = "antenna_stow"
"""The direct-to-cell satellite is stowed-antenna-volume-bound (the large folded array)."""

# The expected formula-name fragments for the spectrum capacity gate. The
# capacity cell must use the empirical anchor; the naive cell must use the
# labeled cross-check. The fragments match the Phase-2 registered names.
_EMPIRICAL_ANCHOR_FRAGMENT: Final[str] = "empirical_anchor"
"""Fragment of the per-beam-capacity formula_name proving the empirical AST anchor drives it."""

_NAIVE_CROSS_CHECK_FRAGMENT: Final[str] = "naive_capacity_cross_check"
"""Fragment of the naive-capacity formula_name proving it is a labeled cross-check."""

_SPECTRUM_UNIT: Final[str] = "MHz"
"""The unit the spectrum-to-acquire cell must carry (a requirement, never a dollar line)."""


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------


def _steady_state_business(output: CommsModelOutput) -> BusinessYear:
    """Return the steady-state-year :class:`BusinessYear` record.

    Reads the steady-state year off the metadata (not a hard-coded "2036"), so a
    non-default scenario validates at its own steady-state year.

    Args:
        output: A fully-built comms output.

    Returns:
        The :class:`BusinessYear` for ``output.metadata.steady_state_year``.

    Raises:
        KeyError: If the steady-state year is absent from ``business.years``.
    """
    key = str(output.metadata.steady_state_year)
    try:
        return output.business.years[key]
    except KeyError as exc:
        raise KeyError(
            f"steady-state year {key!r} absent from business.years "
            f"(present: {sorted(output.business.years)})"
        ) from exc


def _num(value: float | int | str | bool | None) -> float:
    """Unwrap a numeric :class:`ProvenanceCell` value to a ``float``.

    Args:
        value: A ProvenanceCell ``value`` field.

    Returns:
        The value as a ``float``.

    Raises:
        TypeError: If the value is not a real number.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"comms validation rule expected a numeric cell value, got {value!r}")
    return float(value)


def _cells_of(record: BaseModel) -> list[ProvenanceCell]:
    """Collect every :class:`ProvenanceCell` in one record, one level into sub-models.

    Args:
        record: A per-year record or a nested sub-block of cells.

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


def _all_provenance_cells(output: CommsModelOutput) -> list[ProvenanceCell]:
    """Collect every :class:`ProvenanceCell` leaf in the comms output.

    The cells live in the per-year ``physical.years`` and ``business.years`` maps
    (every leaf is a cell or a nested sub-block of cells: ``cost_breakdown`` and
    the customer band-blocks). The ``inputs`` block carries config models and
    flat dicts (no cells), so walking the two per-year maps reaches every cell.

    Args:
        output: A fully-built comms output.

    Returns:
        Every ProvenanceCell in the artifact, physical years then business years.
    """
    cells: list[ProvenanceCell] = []
    for py in output.physical.years.values():
        cells.extend(_cells_of(py))
    for by in output.business.years.values():
        cells.extend(_cells_of(by))
    return cells


def _collect_field_names(cls: type[BaseModel], names: set[str]) -> None:
    """Recursively collect every model FIELD NAME reachable from ``cls``.

    Walks the typed model classes (not the values), recursing into nested
    BaseModel field annotations, dict / list element types, and unwrapping
    optionals, so the recursive field-name disaster gates (no baked-in conclusion,
    no market-capture, no forbidden vehicle) see every emitted field name.

    Args:
        cls: The model class to walk.
        names: The set of collected lower-cased field names, mutated in place.
    """
    import types  # noqa: PLC0415 - local import keeps the introspection helper self-contained
    from typing import Union, get_args, get_origin  # noqa: PLC0415

    def _unwrap(annotation: object) -> object:
        origin = get_origin(annotation)
        if origin is Union or origin is types.UnionType:
            args = [a for a in get_args(annotation) if a is not type(None)]
            if len(args) == 1:
                return args[0]
        return annotation

    def _element(annotation: object) -> object | None:
        origin = get_origin(annotation)
        if origin in (list, tuple, set, frozenset):
            args = get_args(annotation)
            if args:
                return _unwrap(args[0])
        if origin is dict:
            args = get_args(annotation)
            if len(args) >= 2:
                return _unwrap(args[1])
        return None

    for name, info in cls.model_fields.items():
        names.add(name.lower())
        ann = _unwrap(info.annotation)
        if isinstance(ann, type) and issubclass(ann, ProvenanceCell):
            continue
        if isinstance(ann, type) and issubclass(ann, BaseModel):
            _collect_field_names(ann, names)
            continue
        elem = _element(ann)
        if (
            isinstance(elem, type)
            and issubclass(elem, BaseModel)
            and not issubclass(elem, ProvenanceCell)
        ):
            _collect_field_names(elem, names)


def _all_field_names(output_cls: type[BaseModel]) -> set[str]:
    """Return every model field name reachable from an output class, lower-cased."""
    names: set[str] = set()
    _collect_field_names(output_cls, names)
    return names


# ---------------------------------------------------------------------------
# Disaster-gate rules (the executable form of plan Section 0.9).
# ---------------------------------------------------------------------------


def check_no_baked_in_conclusion_fields(output: CommsModelOutput) -> ValidationCheck:
    """No emitted field is a baked-in verdict / conclusion / recommendation.

    Walks the model FIELD NAMES of :class:`CommsModelOutput` recursively and
    fails if any field name contains a forbidden conclusion fragment. The comms
    output deliberately carries the comparison-INPUT numbers but NO verdict field;
    the editorial verdict is the hand-written Phase-6 conclusion.
    """
    names = _all_field_names(type(output))
    offenders = sorted(
        n for n in names if any(frag in n for frag in _FORBIDDEN_CONCLUSION_FRAGMENTS)
    )
    ok = not offenders
    return ValidationCheck(
        name="no_baked_in_conclusion_fields",
        what_it_tests=(
            "no emitted output field is a baked-in verdict / conclusion label / recommendation "
            "(the editorial verdict is the hand-written Phase-6 conclusion)"
        ),
        expected="no conclusion / verdict / recommendation field names",
        computed="none found" if ok else f"offending field names: {offenders}",
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_no_market_capture_fields(output: CommsModelOutput) -> ValidationCheck:
    """No emitted field is a market-capture / market-share dial or output.

    Demand is assumed, not modeled (Amendment A1); the comparison is cost-vs-ground,
    so the schema must never grow a market-capture or market-share field. The
    forbidden fragments are assembled at import time (no contiguous literal in the
    comms source, F37).
    """
    names = _all_field_names(type(output))
    offenders = sorted(n for n in names if any(frag in n for frag in _FORBIDDEN_SHARE_FRAGMENTS))
    ok = not offenders
    return ValidationCheck(
        name="no_market_capture_fields",
        what_it_tests=(
            "no emitted output field is a market-capture dial or output "
            "(demand is assumed, not modeled; the comparison is cost-vs-ground)"
        ),
        expected="no market-capture field names",
        computed="none found" if ok else f"offending field names: {offenders}",
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_no_forbidden_vehicle_fields(output: CommsModelOutput) -> ValidationCheck:
    """No emitted field names the forbidden heavier-than-Neutron vehicle.

    Rocket Lab has only Neutron; the heavier vehicle is never a code input, dial,
    or computed value (it appears ONLY in the hand-written Phase-6 conclusion
    prose). The forbidden fragment is assembled at import time (no contiguous
    literal in the comms source, F37).
    """
    names = _all_field_names(type(output))
    offenders = sorted(n for n in names if _FORBIDDEN_VEHICLE_FRAGMENT in n)
    ok = not offenders
    return ValidationCheck(
        name="no_forbidden_vehicle_fields",
        what_it_tests=(
            "no emitted output field names the forbidden heavier-than-Neutron vehicle "
            "(Rocket Lab has only Neutron; the heavier vehicle is Phase-6 conclusion prose only)"
        ),
        expected="no forbidden-vehicle field names",
        computed="none found" if ok else f"offending field names: {offenders}",
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_customer_outputs_are_bands(output: CommsModelOutput) -> ValidationCheck:
    """The steady-state customer outputs are populated low/mid/high bands.

    Asserts the steady-state ``total_served``, ``cost_annual_per_customer_usd``,
    and ``priced_cost_per_customer_usd`` band-blocks each carry three populated,
    numeric member cells (the point-estimate-for-customers gate: no scalar
    customer output).
    """
    by = _steady_state_business(output)
    bands = {
        "total_served": by.total_served,
        "cost_annual_per_customer_usd": by.cost_annual_per_customer_usd,
        "priced_cost_per_customer_usd": by.priced_cost_per_customer_usd,
    }
    missing: list[str] = []
    for band_name, block in bands.items():
        for member in ("low", "mid", "high"):
            cell = getattr(block, member)
            value = cell.value
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                missing.append(f"{band_name}.{member}")
    ok = not missing
    return ValidationCheck(
        name="customer_outputs_are_bands",
        what_it_tests=(
            "the steady-state customer / cost / priced-cost outputs are low/mid/high bands with "
            "three populated numeric member cells (no scalar customer output)"
        ),
        expected="all three band-blocks have populated low/mid/high cells",
        computed="all band members populated" if ok else f"missing/non-numeric: {missing}",
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_spectrum_is_requirement_not_cost(output: CommsModelOutput) -> ValidationCheck:
    """The spectrum cell is a MHz requirement and no cost line is spectrum-derived.

    Asserts the steady-state ``spectrum_to_acquire_mhz`` cell carries unit MHz (a
    requirement, never a dollar line) and that no per-satellite cost-breakdown cell
    (for either class) carries a MHz unit (the spectrum-as-cost gate: under the
    lease its cost is near zero, so it nets out of the cost comparison).
    """
    key = str(output.metadata.steady_state_year)
    py = output.physical.years[key]
    spectrum_ok = py.spectrum_to_acquire_mhz.unit == _SPECTRUM_UNIT
    offending_cost_lines: list[str] = []
    for class_name in ("broadband", "direct_to_cell"):
        breakdown = getattr(py, class_name).cost_breakdown
        for cost_cell in _cells_of(breakdown):
            if cost_cell.unit == _SPECTRUM_UNIT:
                offending_cost_lines.append(f"{class_name}.{cost_cell.description}")
    ok = spectrum_ok and not offending_cost_lines
    return ValidationCheck(
        name="spectrum_is_requirement_not_cost",
        what_it_tests=(
            "the spectrum-to-acquire cell is a MHz requirement and no per-satellite cost line is "
            "a spectrum dollar figure (spectrum nets out of the cost comparison)"
        ),
        expected=f"spectrum unit == {_SPECTRUM_UNIT!r} and no MHz cost line",
        computed=(
            f"spectrum unit={py.spectrum_to_acquire_mhz.unit!r}; "
            + (
                "no MHz cost line"
                if not offending_cost_lines
                else f"MHz cost lines: {offending_cost_lines}"
            )
        ),
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_empirical_anchor_drives_capacity(output: CommsModelOutput) -> ValidationCheck:
    """The empirical AST anchor drives per-beam capacity; the naive figure is a cross-check.

    Asserts the steady-state ``per_beam_capacity_mbps`` cell's ``formula_name``
    carries the empirical-anchor fragment (the ``120 * leased_mhz / 40`` anchor)
    and the ``naive_capacity_mbps`` cell's ``formula_name`` carries the
    naive-cross-check fragment (the naive-spectrum-division gate: capacity is never
    generated from ``bandwidth * spectral_efficiency``).
    """
    key = str(output.metadata.steady_state_year)
    py = output.physical.years[key]
    capacity_name = py.per_beam_capacity_mbps.formula_name
    naive_name = py.naive_capacity_mbps.formula_name
    anchor_ok = _EMPIRICAL_ANCHOR_FRAGMENT in capacity_name
    naive_ok = _NAIVE_CROSS_CHECK_FRAGMENT in naive_name
    ok = anchor_ok and naive_ok
    return ValidationCheck(
        name="empirical_anchor_drives_capacity",
        what_it_tests=(
            "per-beam capacity is driven by the empirical AST anchor and the naive "
            "bandwidth-times-efficiency figure is a labeled cross-check (never the capacity driver)"
        ),
        expected=(
            f"capacity formula contains {_EMPIRICAL_ANCHOR_FRAGMENT!r} and naive formula contains "
            f"{_NAIVE_CROSS_CHECK_FRAGMENT!r}"
        ),
        computed=f"capacity formula={capacity_name!r}; naive formula={naive_name!r}",
        pass_check=ok,
        severity=Severity.CRITICAL,
    )


def check_provenance_formula_keys(output: CommsModelOutput) -> ValidationCheck:
    """Every ProvenanceCell's ``formula_name`` exists in :data:`FORMULAS`.

    Walks every cell in the output and fails if any ``formula_name`` is absent
    from the shared FORMULAS registry (the formula-registry-integrity gate: a new
    formula name must be registered before use; this catches a silent typo).
    """
    cells = _all_provenance_cells(output)
    used = {c.formula_name for c in cells}
    missing = sorted(name for name in used if name not in FORMULAS)
    if missing:
        computed = f"{len(cells)} cells; formula_name(s) absent from FORMULAS: {missing}"
    else:
        computed = (
            f"all {len(cells)} cells reference one of {len(used)} formula names, "
            "every one present in FORMULAS"
        )
    return ValidationCheck(
        name="provenance_formula_keys",
        what_it_tests=(
            "every ProvenanceCell formula_name exists in the FORMULAS registry "
            "(no silent formula-name typos)"
        ),
        expected="all formula_name values present in FORMULAS",
        computed=computed,
        pass_check=not missing,
        severity=Severity.CRITICAL,
    )


def check_satellites_per_launch_fork(output: CommsModelOutput) -> ValidationCheck:
    """The per-class satellites-per-launch fork is the two distinct constraints.

    Asserts the steady-state broadband binding constraint is ``mass`` and the
    direct-to-cell is ``antenna_stow``, and that broadband packs MORE satellites
    per launch than direct-to-cell (the blanket-mass-binds gate's emitted form).
    Checks the constraint TYPES and the ORDERING, never hard-coded integers
    (Finding F19: the per-launch counts are envelope-dependent).
    """
    key = str(output.metadata.steady_state_year)
    py = output.physical.years[key]
    broadband_constraint = py.broadband.binding_constraint.value
    d2c_constraint = py.direct_to_cell.binding_constraint.value
    broadband_per_launch = _num(py.broadband.satellites_per_launch.value)
    d2c_per_launch = _num(py.direct_to_cell.satellites_per_launch.value)
    types_ok = (
        broadband_constraint == _BROADBAND_EXPECTED_CONSTRAINT
        and d2c_constraint == _DIRECT_TO_CELL_EXPECTED_CONSTRAINT
    )
    order_ok = broadband_per_launch > d2c_per_launch
    ok = types_ok and order_ok
    return ValidationCheck(
        name="satellites_per_launch_fork",
        what_it_tests=(
            "the per-class packing fork is explicit: broadband is mass-bound, direct-to-cell is "
            "antenna-stow-bound, and broadband packs more satellites per launch"
        ),
        expected=(
            f"broadband=={_BROADBAND_EXPECTED_CONSTRAINT!r}, "
            f"direct_to_cell=={_DIRECT_TO_CELL_EXPECTED_CONSTRAINT!r}, broadband per-launch > d2c"
        ),
        computed=(
            f"broadband={broadband_constraint!r} ({broadband_per_launch:g}/launch), "
            f"direct_to_cell={d2c_constraint!r} ({d2c_per_launch:g}/launch)"
        ),
        pass_check=ok,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# Targeted-sanity and artifact-integrity rules.
# ---------------------------------------------------------------------------


def check_steady_state_customer_band_order(output: CommsModelOutput) -> ValidationCheck:
    """The steady-state served band is ascending and per-satellite near the default order.

    Asserts ``total_served`` is ascending (low <= mid <= high) and that the
    per-satellite implied band (``total_served / direct_to_cell_living_fleet``)
    lands near the default 50,000 / 150,000 / 300,000 per-satellite target within
    :data:`CUSTOMER_BAND_REL_TOL`. MINOR: a non-default scenario legitimately
    changes the band, so this is a default-scenario calibration WARN.
    """
    by = _steady_state_business(output)
    low = _num(by.total_served.low.value)
    mid = _num(by.total_served.mid.value)
    high = _num(by.total_served.high.value)
    ascending = low <= mid <= high
    fleet = _num(by.direct_to_cell_living_fleet.value)
    per_sat_ok = False
    per_sat_low = per_sat_mid = per_sat_high = 0.0
    if fleet > 0:
        per_sat_low = low / fleet
        per_sat_mid = mid / fleet
        per_sat_high = high / fleet
        per_sat_ok = (
            math.isclose(per_sat_low, D2C_PER_SAT_BAND_LOW, rel_tol=CUSTOMER_BAND_REL_TOL)
            and math.isclose(per_sat_mid, D2C_PER_SAT_BAND_MID, rel_tol=CUSTOMER_BAND_REL_TOL)
            and math.isclose(per_sat_high, D2C_PER_SAT_BAND_HIGH, rel_tol=CUSTOMER_BAND_REL_TOL)
        )
    ok = ascending and per_sat_ok
    return ValidationCheck(
        name="steady_state_customer_band_order",
        what_it_tests=(
            "the steady-state served band is ascending and the per-satellite band lands near the "
            "default 50k/150k/300k target (a default-scenario calibration check, WARNs off-default)"
        ),
        expected=(
            f"ascending and per-satellite ~ {D2C_PER_SAT_BAND_LOW:g}/{D2C_PER_SAT_BAND_MID:g}/"
            f"{D2C_PER_SAT_BAND_HIGH:g} (rel_tol {CUSTOMER_BAND_REL_TOL:g})"
        ),
        computed=(
            f"served {low:g}/{mid:g}/{high:g}; per-sat "
            f"{per_sat_low:g}/{per_sat_mid:g}/{per_sat_high:g}"
        ),
        pass_check=ok,
        severity=Severity.MINOR,
    )


def check_cost_band_inverse_of_served(output: CommsModelOutput) -> ValidationCheck:
    """The per-customer cost band is ascending and inverse-paired with the served band.

    Asserts ``cost_annual_per_customer_usd`` is ascending (low <= mid <= high) and
    that the inverse pairing holds: ``cost.low * served.high`` reconciles with
    ``cost.high * served.low`` (both equal the fleet annual cost in USD), pinning
    that more customers spread the fleet cost thinner (cost-low pairs with
    served-high). MINOR (a calibration check).
    """
    by = _steady_state_business(output)
    cost_low = _num(by.cost_annual_per_customer_usd.low.value)
    cost_mid = _num(by.cost_annual_per_customer_usd.mid.value)
    cost_high = _num(by.cost_annual_per_customer_usd.high.value)
    served_low = _num(by.total_served.low.value)
    served_high = _num(by.total_served.high.value)
    ascending = cost_low <= cost_mid <= cost_high
    product_low_high = cost_low * served_high
    product_high_low = cost_high * served_low
    reconciled = math.isclose(product_low_high, product_high_low, rel_tol=COST_RECONCILE_REL_TOL)
    ok = ascending and reconciled
    return ValidationCheck(
        name="cost_band_inverse_of_served",
        what_it_tests=(
            "the per-customer cost band is ascending and inverse-paired with the served band "
            "(cost-low pairs with served-high; cost x served reconciles to the fleet annual cost)"
        ),
        expected="ascending cost band and cost.low*served.high == cost.high*served.low",
        computed=(
            f"cost {cost_low:g}/{cost_mid:g}/{cost_high:g}; "
            f"cost.low*served.high={product_low_high:g}, cost.high*served.low={product_high_low:g}"
        ),
        pass_check=ok,
        severity=Severity.MINOR,
    )


def check_launch_cadence_monotonic(output: CommsModelOutput) -> ValidationCheck:
    """Per-year launches are integer-valued and non-decreasing to the steady-state year.

    Asserts the per-year ``launches`` cells across ``business.years`` are
    whole-number and monotonically non-decreasing up to the steady-state year (the
    cadence ramp). MINOR.
    """
    steady = output.metadata.steady_state_year
    pairs = sorted(
        ((int(fy), by) for fy, by in output.business.years.items() if int(fy) <= steady),
        key=lambda kv: kv[0],
    )
    previous = float("-inf")
    monotonic = True
    integral = True
    sequence: list[int] = []
    for _, by in pairs:
        value = _num(by.launches.value)
        if value < previous:
            monotonic = False
        if not float(value).is_integer():
            integral = False
        sequence.append(int(value))
        previous = value
    ok = monotonic and integral
    return ValidationCheck(
        name="launch_cadence_monotonic",
        what_it_tests=(
            "per-year launches are whole-number and non-decreasing up to the steady-state year "
            "(the cadence ramp is a logistic, never sign-flipped or fractional)"
        ),
        expected="integer, non-decreasing launches to the steady-state year",
        computed=f"launches to FY{steady}: {sequence}",
        pass_check=ok,
        severity=Severity.MINOR,
    )


def check_living_fleet_distinct_from_cohort(output: CommsModelOutput) -> ValidationCheck:
    """The direct-to-cell living fleet exceeds one year's deployment (the treadmill).

    Asserts at the steady-state year the ``direct_to_cell_living_fleet`` count is
    strictly greater than ``direct_to_cell_satellites_deployed_this_year`` (the
    living fleet is multiple cohorts under the service-life cliff). MINOR.
    """
    by = _steady_state_business(output)
    living = _num(by.direct_to_cell_living_fleet.value)
    deployed = _num(by.direct_to_cell_satellites_deployed_this_year.value)
    ok = living > deployed
    return ValidationCheck(
        name="living_fleet_distinct_from_cohort",
        what_it_tests=(
            "the steady-state direct-to-cell living fleet is larger than one year's deployment "
            "(the cohort treadmill: multiple living cohorts under the service-life cliff)"
        ),
        expected="direct_to_cell_living_fleet > direct_to_cell_satellites_deployed_this_year",
        computed=f"living {living:g} vs deployed-this-year {deployed:g}",
        pass_check=ok,
        severity=Severity.MINOR,
    )


def check_release_status_no_placeholder_or_stale(output: CommsModelOutput) -> ValidationCheck:
    """The source-status summary carries no placeholder or stale default inputs.

    Asserts ``meta.source_status_summary.placeholder == 0`` and ``.stale == 0`` (a
    promoted artifact must not present a placeholder or stale input as settled,
    plan Section 0.5). MAJOR. NOTE: the default may carry placeholder inputs (the
    NEEDS-RESEARCH antenna bill-of-materials); when it does this rule WARNs/FAILs
    truthfully, which is the founder-visible flag working as intended (F34).
    """
    summary = output.meta.source_status_summary
    ok = summary.placeholder == 0 and summary.stale == 0
    return ValidationCheck(
        name="release_status_no_placeholder_or_stale",
        what_it_tests=(
            "the source-status summary has no placeholder or stale default inputs "
            "(a promoted artifact must not present an unsettled input as settled)"
        ),
        expected="placeholder == 0 and stale == 0",
        computed=f"placeholder={summary.placeholder}, stale={summary.stale}",
        pass_check=ok,
        severity=Severity.MAJOR,
    )


def check_data_dictionary_populated(output: CommsModelOutput) -> ValidationCheck:
    """The ``meta.data_dictionary`` block must be populated (the self-describing gate).

    Asserts the enriched output's ``meta.data_dictionary`` carries at least
    :data:`DATA_DICT_MIN_ENTRIES` entries. The artifact is only self-describing if
    the introspection walk covered every emitted leaf; an empty or near-empty
    dictionary means the enrichment's data-dictionary build silently failed. MAJOR.
    This rule passes only when run against the data-dictionary-populated (enriched)
    output, which is why :func:`communications.json_output.enrich_comms_output` runs
    validation only AFTER copying the data dictionary into the meta.
    """
    count = len(output.meta.data_dictionary)
    ok = count >= DATA_DICT_MIN_ENTRIES
    return ValidationCheck(
        name="data_dictionary_populated",
        what_it_tests=(
            f"meta.data_dictionary has >= {DATA_DICT_MIN_ENTRIES} entries "
            "(the artifact is self-describing)"
        ),
        expected=f">= {DATA_DICT_MIN_ENTRIES} entries",
        computed=f"{count} entries",
        pass_check=ok,
        severity=Severity.MAJOR,
    )


# ---------------------------------------------------------------------------
# The rule roster and the driver.
# ---------------------------------------------------------------------------


_RULES: Final[tuple[Callable[[CommsModelOutput], ValidationCheck], ...]] = (
    # The eight disaster-gate rules (plan Section 0.9).
    check_no_baked_in_conclusion_fields,
    check_no_market_capture_fields,
    check_no_forbidden_vehicle_fields,
    check_customer_outputs_are_bands,
    check_spectrum_is_requirement_not_cost,
    check_empirical_anchor_drives_capacity,
    check_provenance_formula_keys,
    check_satellites_per_launch_fork,
    # The six targeted-sanity / artifact-integrity rules (strategy Section 5).
    check_steady_state_customer_band_order,
    check_cost_band_inverse_of_served,
    check_launch_cadence_monotonic,
    check_living_fleet_distinct_from_cohort,
    check_release_status_no_placeholder_or_stale,
    check_data_dictionary_populated,
)


def compute_comms_validation(output: CommsModelOutput) -> list[ValidationCheck]:
    """Run every comms rule and return the checks in declaration order.

    Args:
        output: A fully-built comms output. The data-dictionary-populated
            (enriched) output is required for :func:`check_data_dictionary_populated`
            to pass; run this after the data dictionary is copied into the meta.

    Returns:
        One :class:`ValidationCheck` per rule in :data:`_RULES`, in order (the
        eight disaster-gate rules then the six sanity / integrity rules).
    """
    return [rule(output) for rule in _RULES]


__all__ = [
    "CUSTOMER_BAND_REL_TOL",
    "COST_RECONCILE_REL_TOL",
    "DATA_DICT_MIN_ENTRIES",
    "D2C_PER_SAT_BAND_HIGH",
    "D2C_PER_SAT_BAND_LOW",
    "D2C_PER_SAT_BAND_MID",
    "check_cost_band_inverse_of_served",
    "check_customer_outputs_are_bands",
    "check_data_dictionary_populated",
    "check_empirical_anchor_drives_capacity",
    "check_launch_cadence_monotonic",
    "check_living_fleet_distinct_from_cohort",
    "check_no_baked_in_conclusion_fields",
    "check_no_forbidden_vehicle_fields",
    "check_no_market_capture_fields",
    "check_provenance_formula_keys",
    "check_release_status_no_placeholder_or_stale",
    "check_satellites_per_launch_fork",
    "check_spectrum_is_requirement_not_cost",
    "check_steady_state_customer_band_order",
    "compute_comms_validation",
]
