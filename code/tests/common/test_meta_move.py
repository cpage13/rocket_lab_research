"""Tests that the cold-reader contract types moved cleanly to ``common`` (Phase 0, T0.14)."""

from __future__ import annotations

from common.meta import (
    DataDictEntry,
    QueryAppliesTo,
    QueryExample,
    Severity,
    SourceStatusSummary,
    ValidationCheck,
    ValidationSeverity,
)


def test_validation_severity_strings() -> None:
    assert ValidationSeverity.OK == "pass"
    assert ValidationSeverity.WARN == "warn"
    assert ValidationSeverity.FAIL == "fail"


def test_query_applies_to_has_space_ground_both() -> None:
    assert QueryAppliesTo.SPACE == "space"
    assert QueryAppliesTo.GROUND == "ground"
    assert QueryAppliesTo.BOTH == "both"


def test_query_example_jq_property() -> None:
    example = QueryExample(
        name="example",
        question_answered="what?",
        jq_expression=".x",
        expected_shape="a number",
        important_paths=["x"],
        applies_to=QueryAppliesTo.SPACE,
    )
    assert example.jq == ".x"


def test_validation_check_pass_flag() -> None:
    check = ValidationCheck(
        name="mass_util_in_range",
        what_it_tests="mass utilization is within range",
        expected="in [0.85, 1.0]",
        computed="0.92",
        pass_check=True,
        severity=Severity.MAJOR,
    )
    assert check.pass_check is True
    assert check.severity is Severity.MAJOR


def test_source_status_summary_eight_counts() -> None:
    summary = SourceStatusSummary(
        certified=1,
        sourced_estimate=2,
        derived_estimate=3,
        projection=4,
        extrapolation=5,
        scenario=6,
        placeholder=0,
        stale=0,
    )
    dumped = summary.model_dump()
    expected_keys = {
        "certified",
        "sourced_estimate",
        "derived_estimate",
        "projection",
        "extrapolation",
        "scenario",
        "placeholder",
        "stale",
    }
    assert set(dumped.keys()) == expected_keys
    assert all(isinstance(v, int) for v in dumped.values())


def test_data_dict_entry_uses_field_path() -> None:
    entry = DataDictEntry(
        path="a.b",
        description="a field",
        unit="MUSD",
        type="number",
        source_class="DERIVED",
    )
    assert entry.path == "a.b"
