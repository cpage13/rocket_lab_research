"""Tests for the comms fixed-width text report and the one-line headline."""

from __future__ import annotations

from communications.ground import GroundReferenceOutput
from communications.output import CommsModelOutput
from communications.text_report import render_comms_headline, render_comms_text

_EM_DASH = chr(0x2014)  # the long-dash character, built from its codepoint (founder rule)

_FORBIDDEN_VERDICT_TOKENS = (
    "conclusion_label",
    "verdict",
    "space_wins",
    "ground_wins",
    "recommended",
    "recommendation",
)


def test_render_text_is_total(default_comms_output: CommsModelOutput) -> None:
    """The space-only report renders every section with no exception."""
    text = render_comms_text(default_comms_output)
    assert text
    for header in (
        "COST-VS-GROUND MODEL",
        "PROVENANCE SUMMARY",
        "PER-YEAR PER-CLASS PHYSICAL",
        "PER-YEAR FLEET ROLLUP",
        "CUSTOMER + COST BAND",
        "VALIDATION CHECKS",
    ):
        assert header in text


def test_render_text_with_ground_renders_comparison(
    default_comms_output: CommsModelOutput,
    default_ground_output: GroundReferenceOutput,
) -> None:
    """With a ground reference, the comparison block renders numbers and flags, no verdict."""
    text = render_comms_text(default_comms_output, default_ground_output)
    assert "COST-TO-COST COMPARISON" in text
    assert "SPARSE" in text
    assert "DENSE" in text
    assert "REVENUE-CEILING RECONCILIATION" in text
    assert "STARLINK-FLOOR HONESTY" in text
    lowered = text.lower()
    for token in _FORBIDDEN_VERDICT_TOKENS:
        assert token not in lowered


def test_render_headline_is_one_line(default_comms_output: CommsModelOutput) -> None:
    """The headline is a single line naming the fleet, served, and cost mid band."""
    line = render_comms_headline(default_comms_output)
    assert "\n" not in line
    assert "FY2036" in line
    assert "living fleet" in line
    assert "subscribers" in line


def test_text_report_renders_enriched_validation(
    default_comms_output: CommsModelOutput,
    default_enriched_output: CommsModelOutput,
) -> None:
    """The enriched report lists rule names; the lean report shows the placeholder line."""
    enriched_text = render_comms_text(default_enriched_output)
    assert "provenance_formula_keys" in enriched_text
    assert "PASS" in enriched_text
    lean_text = render_comms_text(default_comms_output)
    assert "run via --json or --promote" in lean_text


def test_text_report_has_no_em_dash(
    default_comms_output: CommsModelOutput,
    default_ground_output: GroundReferenceOutput,
) -> None:
    """Generated report text carries no long-dash character (the standing rule)."""
    assert _EM_DASH not in render_comms_text(default_comms_output)
    assert _EM_DASH not in render_comms_text(default_comms_output, default_ground_output)
    assert _EM_DASH not in render_comms_headline(default_comms_output)
