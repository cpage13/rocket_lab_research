"""The product case's scenario, its refusals, its cell specs and its formula catalog (box B0).

The code defaults and ``code/scenarios/product_case.yaml`` are one default (the file's own label
aside); every refusal the config makes names its field; no IoT count is a setting; every
scenario value and every named constant that is an input carries a cell spec with its status,
claim and basis; the formula catalog holds one entry per formula of the method.
"""

from __future__ import annotations

import ast
import itertools
import math
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

import product_case.constants as constants_module
from common.input_manifest import AssumptionRole, SourceStatus
from product_case.config import (
    CONSTANT_INPUTS,
    SCENARIO_SPECS,
    ProductCaseConfig,
    load_product_case_config,
)
from product_case.constants import (
    CLASS_KIND,
    DATA_IOT_ANCHOR_ARPU_USD_MONTH,
    DATA_IOT_ANCHOR_CUSTOMERS,
    FORMULA_CATALOG,
    IOT_ARPU_USD_MONTH,
    IOT_CUSTOMERS_TODAY,
    PATH_SEPARATOR,
    SCENARIO_NAME_DEFAULT,
    TERMINAL_CUSTOMERS_TODAY,
    ClassKind,
    ProductCaseFormula,
    ProductClass,
)

type Mutation = Callable[[dict[str, Any]], None]
"""A change made to the shipped scenario's mapping before it is written and loaded."""

PRODUCT_CASE_CLAIMS = frozenset({"COMM-722", "COMM-723", "COMM-724", "COMM-725", "COMM-726"})
"""The five source-ledger rows the product case's settings cite (its prices, the Monte Carlo's
settings, the usage paths, the usable floors and data IoT's anchor)."""

IDENTITY_FIELDS = frozenset({"scenario_name", "engineering_artifact_path"})
"""The scenario's two identity fields: the run's label and the engineering artifact's path,
published in the artifact's metadata, not as inputs."""

USAGE_PATHS = (
    ("usage", "small_terminal", "gb_per_month"),
    ("usage", "mounted_terminal", "gb_per_month"),
    ("usage", "minimal_packet_iot", "messages_per_day"),
    ("usage", "data_iot", "bursts_per_day"),
    ("usage", "data_iot", "bursts_outside_busy_hours"),
)
"""The five usage paths that hold one value per reported year."""


def _set(path: tuple[str, ...], value: object) -> Mutation:
    """A mutation that sets the value at ``path`` (creating the last key when it is new)."""

    def mutate(data: dict[str, Any]) -> None:
        node = data
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value

    return mutate


def _drop_last(path: tuple[str, ...]) -> Mutation:
    """A mutation that drops the last value of the list at ``path``."""

    def mutate(data: dict[str, Any]) -> None:
        node = data
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = list(node[path[-1]])[:-1]

    return mutate


def _leaf_paths(model: BaseModel, prefix: str = "") -> list[str]:
    """Every leaf field path of a config model (a nested model recursed, a list a leaf)."""
    paths: list[str] = []
    for name in type(model).model_fields:
        value = getattr(model, name)
        path = f"{prefix}{name}"
        if isinstance(value, BaseModel):
            paths.extend(_leaf_paths(value, f"{path}."))
        else:
            paths.append(path)
    return paths


def test_the_code_defaults_equal_the_shipped_scenario_file(product_case_yaml: Path) -> None:
    """Objective: the code defaults and ``code/scenarios/product_case.yaml`` are one default, so
    the shipped scenario holds exactly the named constants, its own label aside (the data
    center's ``test_code_defaults_equal_the_default_scenario_file`` is the model, popping the
    name); the code's label is neutral, so a side run that sets none claims nothing.

    Sample: the shipped scenario file, loaded through ``load_product_case_config``; the config
    built from the code alone, ``ProductCaseConfig()``.

    Expected outcome: the two configs are equal field for field once the names are popped; the
    file names itself "The product case at the investor's prices, held flat" and the code's
    label is ``SCENARIO_NAME_DEFAULT``, "A product-case scenario".
    """
    from_file = load_product_case_config(product_case_yaml).model_dump()
    from_code = ProductCaseConfig().model_dump()
    assert from_file.pop("scenario_name") == "The product case at the investor's prices, held flat"
    assert from_code.pop("scenario_name") == SCENARIO_NAME_DEFAULT == "A product-case scenario"
    assert from_file == from_code


def test_an_empty_scenario_takes_every_default(tmp_path: Path) -> None:
    """Objective: a scenario file that sets nothing loads as the default config.

    Sample: an empty YAML file, loaded from a string path.

    Expected outcome: the loaded config equals ``ProductCaseConfig()``.
    """
    empty = tmp_path / "empty.yaml"
    empty.write_text("", encoding="utf-8")
    assert load_product_case_config(str(empty)) == ProductCaseConfig()


REFUSALS: list[tuple[str, Mutation, str, str]] = [
    (
        "end prices that do not open with the start price",
        _set(("prices", "small_terminal", "end_usd_month"), [9.0, 8.0]),
        "prices.small_terminal.end_usd_month",
        "must open with the start price",
    ),
    (
        "end prices that rise",
        _set(("prices", "mounted_terminal", "end_usd_month"), [50.0, 55.0]),
        "prices.mounted_terminal.end_usd_month",
        "fall strictly",
    ),
    (
        "end prices that repeat",
        _set(("prices", "mounted_terminal", "end_usd_month"), [50.0, 50.0]),
        "prices.mounted_terminal.end_usd_month",
        "fall strictly",
    ),
    (
        "a start price of zero",
        _set(("prices", "small_terminal", "start_usd_month"), 0.0),
        "prices.small_terminal.start_usd_month",
        "greater than 0",
    ),
    (
        "usage scales that do not open at 1",
        _set(("usage", "minimal_packet_iot", "scales"), [2.0, 4.0]),
        "usage.minimal_packet_iot.scales",
        "must open at 1",
    ),
    (
        "usage scales that do not rise",
        _set(("usage", "data_iot", "scales"), [1.0, 4.0, 2.0]),
        "usage.data_iot.scales",
        "must rise strictly",
    ),
    (
        "fewer than two reported years",
        _set(("reported_years",), [2031]),
        "reported_years",
        "at least 2 reported years",
    ),
    (
        "reported years out of order",
        _set(("reported_years",), [2031, 2035, 2033, 2036]),
        "reported_years",
        "must be in order",
    ),
    (
        "a reported year twice",
        _set(("reported_years",), [2031, 2033, 2033, 2036]),
        "reported_years",
        "must be in order",
    ),
    (
        "a network range whose low end is above its high end",
        _set(("market", "gamma"), {"low": 1.2, "high": 1.0}),
        "market.gamma",
        "is above the high end",
    ),
    (
        "a price range whose low end is above its high end",
        _set(("market", "epsilon"), {"low": 1.6, "high": 1.5}),
        "market.epsilon",
        "is above the high end",
    ),
    (
        "a service range whose low end is above its high end",
        _set(("market", "eta"), {"low": 0.6, "high": 0.5}),
        "market.eta",
        "is above the high end",
    ),
    (
        "draws below 9",
        _set(("market", "draws"), 8),
        "market.draws",
        "greater than or equal to 9",
    ),
    (
        "a fill floor of zero",
        _set(("floors", "fill"), 0.0),
        "floors.fill",
        "greater than 0",
    ),
    (
        "a fill floor above 1",
        _set(("floors", "fill"), 1.5),
        "floors.fill",
        "less than or equal to 1",
    ),
    (
        "a robust floor of zero",
        _set(("floors", "robust"), 0.0),
        "floors.robust",
        "greater than 0",
    ),
    (
        "a robust floor above 1",
        _set(("floors", "robust"), 1.01),
        "floors.robust",
        "less than or equal to 1",
    ),
    (
        "a margin floor of zero",
        _set(("floors", "margin_pct"), 0.0),
        "floors.margin_pct",
        "greater than 0",
    ),
    (
        "a margin floor of 100 percent",
        _set(("floors", "margin_pct"), 100.0),
        "floors.margin_pct",
        "less than 100",
    ),
    (
        "a monthly total of zero",
        _set(("usage", "small_terminal", "gb_per_month"), [0.0, 6.7, 8.1, 9.0]),
        "usage.small_terminal.gb_per_month",
        "above 0 GB",
    ),
    (
        "a year with no message",
        _set(("usage", "minimal_packet_iot", "messages_per_day"), [0, 72, 96, 96]),
        "usage.minimal_packet_iot.messages_per_day",
        "at least 1 message",
    ),
    (
        "negative bursts",
        _set(("usage", "data_iot", "bursts_per_day"), [8, -1, 12, 13]),
        "usage.data_iot.bursts_per_day",
        "cannot be negative",
    ),
    (
        "a boolean where a number goes",
        _set(("floors", "margin_pct"), True),
        "floors.margin_pct",
        "valid number",
    ),
    (
        "a boolean in a list of numbers",
        _set(("usage", "small_terminal", "gb_per_month"), [True, 6.7, 8.1, 9.0]),
        "usage.small_terminal.gb_per_month.0",
        "valid number",
    ),
    (
        "a quoted number",
        _set(("prices", "small_terminal", "start_usd_month"), "10"),
        "prices.small_terminal.start_usd_month",
        "valid number",
    ),
    (
        "a quoted whole number",
        _set(("market", "draws"), "2000"),
        "market.draws",
        "valid integer",
    ),
    (
        "an infinite number",
        _set(("market", "gamma", "high"), math.inf),
        "market.gamma.high",
        "finite number",
    ),
    (
        "a number that is not a number",
        _set(("prices", "minimal_packet_iot", "start_usd_month"), math.nan),
        "prices.minimal_packet_iot.start_usd_month",
        "finite number",
    ),
    (
        "data IoT's price as a setting",
        _set(("prices", "data_iot"), {"start_usd_month": 6.0, "end_usd_month": [6.0]}),
        "prices.data_iot",
        "Extra inputs are not permitted",
    ),
    (
        "an unknown key",
        _set(("market", "seeds"), 5),
        "market.seeds",
        "Extra inputs are not permitted",
    ),
    *(
        (
            f"{'.'.join(path)} one value short",
            _drop_last(path),
            ".".join(path),
            "it needs one per reported year",
        )
        for path in USAGE_PATHS
    ),
]
"""Each refusal: what it is, the change to the shipped scenario, the field the error must name
and a phrase of its reason."""


@pytest.mark.parametrize(
    ("mutation", "field", "reason"),
    [pytest.param(m, f, r, id=name) for name, m, f, r in REFUSALS],
)
def test_every_refusal_names_its_field(
    shipped_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    mutation: Mutation,
    field: str,
    reason: str,
) -> None:
    """Objective: every scenario the config refuses is refused at load, naming the field, for
    each refusal the part file lists (an end-price list that does not open with its start price
    or fall strictly; usage scales that do not open at 1 or rise; a usage path whose length is
    not the reported years'; fewer than two reported years or years out of order; a range whose
    low end is above its high end; draws below 9; a fill or robust floor outside (0, 1]; a
    margin floor outside (0, 100) percent; an unknown key; a boolean or a quoted number where a
    number goes; a number that is not finite) and for the positivity each path needs.

    Sample: the shipped scenario with one change, written to a temporary YAML file and loaded
    through ``load_product_case_config`` (so YAML's own booleans, quotes and ``.inf`` reach the
    config).

    Expected outcome: a ``ValidationError`` whose message holds the field's dotted path and the
    reason's phrase.
    """
    mutation(shipped_scenario)
    with pytest.raises(ValidationError) as caught:
        load_product_case_config(write_scenario(shipped_scenario))
    message = str(caught.value)
    assert field in message, message
    assert reason in message, message


def test_the_reported_years_compare_as_integers(
    shipped_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
) -> None:
    """Objective: the reported years are compared as the integers they are, so a year beyond the
    range of a double loads (the engineering view then refuses it as a year it does not hold)
    and two years a double cannot tell apart keep their order (the numerics lens's m3: a year
    of 10^400 escaped the loader as a bare ``OverflowError``).

    Sample: the shipped scenario with its last reported year 10^400, written to YAML and loaded;
    then with its last two years 10^400 + 1 and 10^400.

    Expected outcome: the first loads, its last year 10^400 exactly; the second is refused,
    naming ``reported_years`` and its order.
    """
    shipped_scenario["reported_years"] = [2031, 2033, 2035, 10**400]
    config = load_product_case_config(write_scenario(shipped_scenario))
    assert config.reported_years[-1] == 10**400
    shipped_scenario["reported_years"] = [2031, 2033, 10**400 + 1, 10**400]
    with pytest.raises(ValidationError) as caught:
        load_product_case_config(write_scenario(shipped_scenario))
    message = str(caught.value)
    assert "reported_years" in message, message
    assert "must be in order" in message, message


@pytest.mark.parametrize("iot_class", ["minimal_packet_iot", "data_iot"])
def test_an_iot_count_in_the_scenario_is_refused_naming_the_field(
    shipped_scenario: dict[str, Any],
    write_scenario: Callable[[dict[str, Any]], Path],
    iot_class: str,
) -> None:
    """Objective: no IoT count is ever a setting (the investor, 2026-10-06): a scenario that
    sets a count of devices for an IoT class is refused at load as an unknown key, naming it.

    Sample: the shipped scenario with ``usage.<iot class>.devices`` set to a million.

    Expected outcome: a ``ValidationError`` naming ``usage.<iot class>.devices`` as an extra
    input; nothing loads.
    """
    shipped_scenario["usage"][iot_class]["devices"] = 1_000_000
    with pytest.raises(ValidationError) as caught:
        load_product_case_config(write_scenario(shipped_scenario))
    message = str(caught.value)
    assert f"usage.{iot_class}.devices" in message, message
    assert "Extra inputs are not permitted" in message, message


def test_the_config_has_no_field_that_counts_customers_or_devices() -> None:
    """Objective: the config's shape holds no customer or device count anywhere, so no setting
    can set one; every customer the product case publishes comes from the demand curve.

    Sample: every leaf field path of the default config.

    Expected outcome: no path ends in a count of customers or devices.
    """
    counts = ("customers", "devices", "count")
    paths = _leaf_paths(ProductCaseConfig())
    assert paths, "the config has no fields"
    assert [path for path in paths if path.rsplit(".", 1)[-1].endswith(counts)] == []


def test_every_scenario_value_has_one_cell_spec() -> None:
    """Objective: every value the scenario sets has exactly one cell spec (D20), so every input
    the artifact publishes carries a status, a claim and a basis.

    Sample: the leaf paths of the default config, but the scenario's two identity fields; the
    keys of ``SCENARIO_SPECS``.

    Expected outcome: the two sets are equal.
    """
    paths = {path for path in _leaf_paths(ProductCaseConfig()) if path not in IDENTITY_FIELDS}
    assert set(SCENARIO_SPECS) == paths


def test_each_scenario_spec_states_its_status_claim_and_basis() -> None:
    """Objective: each scenario value's spec is a default of status ``scenario`` that cites one
    of the product case's five ledger rows and opens its rationale with its source class.

    Sample: every entry of ``SCENARIO_SPECS``.

    Expected outcome: role ``default``, status ``scenario``, a claim among COMM-722 to COMM-726,
    a rationale opening ``INVESTOR_SET`` or ``SCENARIO``; the terminals' end prices cite the
    prices row first and the Monte Carlo's settings row beside it.
    """
    for path, spec in SCENARIO_SPECS.items():
        assert spec.role is AssumptionRole.DEFAULT, path
        assert spec.source_status is SourceStatus.SCENARIO, path
        assert spec.claim_id in PRODUCT_CASE_CLAIMS, path
        assert spec.rationale.startswith(("INVESTOR_SET", "SCENARIO")), path
    for terminal in ("small_terminal", "mounted_terminal"):
        spec = SCENARIO_SPECS[f"prices.{terminal}.end_usd_month"]
        assert spec.claim_id == "COMM-722"
        assert [claim.claim_id for claim in spec.supporting_claims] == ["COMM-723"]


def test_each_constant_input_carries_its_value_status_and_claim() -> None:
    """Objective: the named constants that are model inputs carry their values, statuses and
    claims: Iridium's customers and ARPU today certified (COMM-617, COMM-618), data IoT's anchor
    the investor's proportion (COMM-726), stating that the two IoT classes start from twice
    Iridium's IoT revenue today (montecarlo M1).

    Sample: every entry of ``CONSTANT_INPUTS``; the anchors' constants.

    Expected outcome: certified entries cite COMM-617 or COMM-618 and open SOURCED_FACT; the
    others are ``scenario`` and cite the product case's rows; data IoT's anchor is 999,000
    devices at $15.56, half the IoT customers at double the ARPU; the terminal base 418,100.
    """
    for path, entry in CONSTANT_INPUTS.items():
        spec = entry.spec
        assert spec.role is AssumptionRole.DEFAULT, path
        if spec.source_status is SourceStatus.CERTIFIED:
            assert spec.claim_id in {"COMM-617", "COMM-618"}, path
            assert spec.rationale.startswith("SOURCED_FACT"), path
        else:
            assert spec.source_status is SourceStatus.SCENARIO, path
            assert spec.claim_id in PRODUCT_CASE_CLAIMS, path
            assert spec.rationale.startswith(("INVESTOR_SET", "SCENARIO")), path
    customers = CONSTANT_INPUTS["anchors.data_iot.customers"]
    arpu = CONSTANT_INPUTS["anchors.data_iot.arpu_usd_month"]
    assert customers.value == DATA_IOT_ANCHOR_CUSTOMERS == IOT_CUSTOMERS_TODAY / 2 == 999_000
    assert arpu.value == DATA_IOT_ANCHOR_ARPU_USD_MONTH == 2 * IOT_ARPU_USD_MONTH
    assert math.isclose(DATA_IOT_ANCHOR_ARPU_USD_MONTH, 15.56, rel_tol=1e-12)
    assert "twice Iridium's IoT revenue today" in customers.spec.rationale
    assert CONSTANT_INPUTS["terminal_customers_today"].value == TERMINAL_CUSTOMERS_TODAY == 418_100


def test_the_classes_run_small_mounted_minimal_packet_data() -> None:
    """Objective: every product-case list runs small terminal, mounted terminal, minimal-packet
    IoT, data IoT, never phone-first, the two terminals sold up to their seats and the two IoT
    classes uncapped.

    Sample: ``ProductClass`` and ``CLASS_KIND``.

    Expected outcome: the four classes in that order, two terminals then two IoT classes.
    """
    order = [
        ProductClass.SMALL_TERMINAL,
        ProductClass.MOUNTED_TERMINAL,
        ProductClass.MINIMAL_PACKET_IOT,
        ProductClass.DATA_IOT,
    ]
    assert list(ProductClass) == order
    assert list(CLASS_KIND) == order
    assert [CLASS_KIND[c] for c in order] == [ClassKind.TERMINAL] * 2 + [ClassKind.IOT] * 2


SOURCE_CLASSES = ("SOURCED_FACT", "INVESTOR_SET", "SCENARIO", "DERIVED")
"""The source classes a named constant's docstring opens with (the constants module's rule)."""

DEFINITIONS = frozenset(
    {
        "BITS_PER_BYTE",
        "BITS_PER_MEGABIT",
        "SECONDS_PER_HOUR",
        "HOURS_PER_DAY",
        "SECONDS_PER_DAY",
        "MONTHS_PER_YEAR",
        "DOLLARS_PER_MILLION",
        "PERCENT",
        "PRODUCT_CASE_SCHEMA_VERSION",
        "ENGINEERING_SCHEMA_VERSION",
        "MIN_REPORTED_YEARS",
        "MIN_DRAWS",
        "USAGE_SCALE_START",
        "CLASS_KIND",
        "TERMINAL_DEVICE_CLASS",
        "DEMAND_ANCHORS",
        "FORMULA_CATALOG",
        "SCENARIO_NAME_DEFAULT",
        "ENGINEERING_ARTIFACT_PATH_DEFAULT",
        "PATH_SEPARATOR",
        "PHONE_DEVICE_CLASS",
    }
)
"""The constants whose docstrings say what they are instead of a source class: the unit
conversions, the schema versions, the structural bounds, the mappings and the four definitions
the constants module's docstring names."""

RANGE_ENDS = frozenset(
    {
        "GAMMA_LOW_DEFAULT",
        "GAMMA_HIGH_DEFAULT",
        "EPSILON_LOW_DEFAULT",
        "EPSILON_HIGH_DEFAULT",
        "ETA_LOW_DEFAULT",
        "ETA_HIGH_DEFAULT",
    }
)
"""The six ends of the market responses' ranges."""


def _constant_docstrings() -> dict[str, str]:
    """Each module-level constant of ``product_case.constants`` with its docstring, from source."""
    tree = ast.parse(Path(constants_module.__file__).read_text(encoding="utf-8"))
    found: dict[str, str] = {}
    for node, following in itertools.pairwise(tree.body):
        if not (isinstance(following, ast.Expr) and isinstance(following.value, ast.Constant)):
            continue
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            found[node.target.id] = str(following.value.value)
    return found


def test_every_named_constant_states_its_basis() -> None:
    """Objective: the constants module's documentation rule holds for every public constant
    (the investor's condition, 2026-10-06: the Monte Carlo documented by the repository's
    rules): a docstring opens with its source class, or the constant is a definition the
    module's docstring names; an INVESTOR_SET value quotes the investor's words with their
    date; each end of a market response's range says that no market research grounds it.

    Sample: every name in ``product_case.constants.__all__`` that is a constant (upper case),
    with its docstring read from the module's source.

    Expected outcome: each has a docstring; every non-definition opens with SOURCED_FACT,
    INVESTOR_SET, SCENARIO or DERIVED; every docstring that opens INVESTOR_SET holds a quoted
    span and a 2026 date; every range end's docstring says "no market research".
    """
    docstrings = _constant_docstrings()
    names = [name for name in constants_module.__all__ if name.isupper()]
    assert names, "the constants module exports no constants"
    for name in names:
        assert name in docstrings, f"{name} has no docstring"
        text = docstrings[name]
        if name in DEFINITIONS:
            continue
        assert text.startswith(SOURCE_CLASSES), f"{name}: {text[:60]!r}"
        if text.startswith("INVESTOR_SET"):
            assert '"' in text and "2026-" in text, f"{name} quotes no dated words"
        if name in RANGE_ENDS:
            words = " ".join(text.split()).lower()
            assert "no market research" in words, f"{name} does not say what grounds it"


def test_the_formula_catalog_holds_one_entry_per_formula() -> None:
    """Objective: the formula catalog holds one entry per formula of the method, each keyed by
    its own id, with the paths it reads and computes, the price and usage lines written in
    fiscal years (montecarlo m3) and the pick's entry stating what stops the usage.

    Sample: ``FORMULA_CATALOG`` and ``ProductCaseFormula``.

    Expected outcome: one entry per member, its ``formula_id`` the member's value, every text
    field filled; the price line divides by ``(t1 - t0)`` in fiscal years and the usage line
    rounds half up with the worked FY2033 line at x8; the pick's description says what stops
    the usage.
    """
    assert list(FORMULA_CATALOG) == list(ProductCaseFormula)
    for formula, entry in FORMULA_CATALOG.items():
        assert entry.formula_id == formula.value
        for text in (
            entry.formula_text,
            entry.description,
            entry.input_path_pattern,
            entry.output_path_pattern,
            entry.unit_behavior,
        ):
            assert text.strip(), formula
    price_line = FORMULA_CATALOG[ProductCaseFormula.PRICE_LINE].formula_text
    assert "(t - t0) / (t1 - t0)" in price_line
    assert "fiscal year" in price_line
    usage_line = FORMULA_CATALOG[ProductCaseFormula.USAGE_LINE].formula_text
    assert "round_half_up" in usage_line
    assert "72 x 3.8 = 273.6, so 274" in usage_line
    assert "What stops the usage" in FORMULA_CATALOG[ProductCaseFormula.PICK].description


def test_the_catalog_paths_are_in_the_walkers_form() -> None:
    """Objective: every catalog path is written as the data-dictionary walker writes the
    artifact's leaves (``PATH_SEPARATOR``'s rule: ``[]`` for a list's or map's records, a list or
    map of plain values one leaf, never ``*``), and the reported years and the source-status
    summary, which every numeric leaf check reaches, each have an entry (the spec lens's m5).

    Sample: every entry of ``FORMULA_CATALOG``, its input and output patterns split at
    ``PATH_SEPARATOR``.

    Expected outcome: no path holds ``*``; ``[]`` only ends a name; the years entry outputs each
    reported year's ``year`` under ``network``, ``headline`` and ``spreads``; the summary entry
    outputs ``meta.source_status_summary``; the draws' failures are one leaf,
    ``choices[].draws_failing``.
    """
    for formula, entry in FORMULA_CATALOG.items():
        for pattern in (entry.input_path_pattern, entry.output_path_pattern):
            for path in pattern.split(PATH_SEPARATOR):
                assert "*" not in path, (formula, path)
                assert all(part.count("[]") <= 1 for part in path.split(".")), (formula, path)
                assert all(part.endswith("[]") or "[]" not in part for part in path.split(".")), (
                    formula,
                    path,
                )
    years = FORMULA_CATALOG[ProductCaseFormula.REPORTED_YEARS].output_path_pattern
    assert years.split(PATH_SEPARATOR) == [
        "network.years[].year",
        "headline.years[].year",
        "spreads.years[].year",
    ]
    summary = FORMULA_CATALOG[ProductCaseFormula.SOURCE_STATUS_SUMMARY].output_path_pattern
    assert summary == "meta.source_status_summary"
    draws = FORMULA_CATALOG[ProductCaseFormula.DRAWS_FAILING].output_path_pattern
    assert draws == "choices[].draws_failing"
