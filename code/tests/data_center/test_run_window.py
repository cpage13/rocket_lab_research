"""End-to-end tests for run windows other than the default (the anchor year).

Every place that reads "the headline year" (the anchor-year validation
checks, the V6 band, the query examples, and the ground reference anchor)
reads one config-derived anchor year: :func:`data_center.config.anchor_year`,
the year-10 cadence anchor (``base_year + 10``) when the window reaches it,
else the final window year. The default window (2026, ten years) resolves to
FY2036, so the promoted default is unchanged.

These tests drive shifted and shortened windows through the real CLI and the
ground builder: before the fix a five-year horizon or a 2040 base year
crashed every CLI mode with ``KeyError: '2036'``, and a 2027 base year
checked the cadence target against the wrong model year.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from data_center import cli
from data_center.config import anchor_year, config_from_dict
from data_center.engine import run_valuation
from data_center.ground import (
    DEFAULT_GROUND_SCENARIO_PATH,
    build_ground_reference_output,
    load_ground_config,
)

_GROUND_SCENARIO = Path(__file__).resolve().parents[2] / "scenarios" / "ground_default.yaml"


@pytest.mark.parametrize(
    ("base_year", "horizon_years", "expected"),
    [(2026, 10, 2036), (2026, 14, 2036), (2026, 5, 2031), (2040, 10, 2050), (2027, 10, 2037)],
)
def test_anchor_year_is_the_year_10_anchor_or_the_window_end(
    base_year: int, horizon_years: int, expected: int
) -> None:
    """Objective: one rule picks the anchor year for every window.

    Expected: ``base_year + 10`` when the horizon reaches it, else the final
    window year; the default window gives 2036.
    """
    assert anchor_year(base_year, horizon_years) == expected


def _write_scenario(tmp_path: Path, base_year: int, horizon_years: int) -> Path:
    """Write a default-dial scenario with the given window; return its path."""
    path = tmp_path / f"window_{base_year}_{horizon_years}.yaml"
    path.write_text(
        yaml.safe_dump({"metadata": {"base_year": base_year, "horizon_years": horizon_years}}),
        encoding="utf-8",
    )
    return path


@pytest.mark.parametrize(
    ("base_year", "horizon_years", "anchor_fy"),
    [(2026, 5, "2031"), (2040, 10, "2050")],
    ids=["horizon_5", "base_year_2040"],
)
def test_shifted_windows_run_through_every_cli_mode(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    base_year: int,
    horizon_years: int,
    anchor_fy: str,
) -> None:
    """Objective: a five-year horizon and a 2040 base year run end to end.

    Expected: the text report, ``--brief``, and ``--json`` all exit 0; the
    JSON's anchor-year checks and query examples address the run's anchor
    year and never 2036; these non-default scenarios carry no default guard;
    the year-10 cadence invariant appears only when the window reaches model
    year 10 (the 2040 base year), where it reads the anchor year.
    """
    scenario = str(_write_scenario(tmp_path, base_year, horizon_years))
    assert cli.main([scenario]) == 0
    assert cli.main([scenario, "--brief"]) == 0
    capsys.readouterr()
    assert cli.main([scenario, "--json"]) == 0
    artifact = json.loads(capsys.readouterr().out)

    results = {r["validation_id"]: r for r in artifact["meta"]["validation_results"]}
    assert not [vid for vid in results if vid.startswith("default_")]
    cadence_id = "anchor_year_launches_match_year_10_dial"
    if horizon_years >= 10:
        assert results[cadence_id]["related_json_paths"][-1] == (
            f'business.years."{anchor_fy}".launches'
        )
    else:
        assert cadence_id not in results
    assert (
        f'business.years."{anchor_fy}".kw_living_fleet'
        in (results["living_fleet_distinct_from_deployed_year_cohort"]["related_json_paths"])
    )
    assert f"FY{anchor_fy} " in results["pf_per_kw_in_band"]["observed_result"]
    names = {q["name"] for q in artifact["meta"]["query_examples"]}
    assert f"headline_{anchor_fy}_revenue_central" in names
    assert "2036" not in json.dumps(artifact["meta"]["query_examples"])


@pytest.mark.parametrize(
    ("base_year", "horizon_years", "anchor_fy"),
    [(2026, 5, 2031), (2040, 10, 2050)],
    ids=["horizon_5", "base_year_2040"],
)
def test_ground_reference_anchors_to_the_runs_anchor_year(
    base_year: int, horizon_years: int, anchor_fy: int
) -> None:
    """Objective: the ground reference builds for shifted windows (ADR-003).

    Expected: the ground anchor is the anchor year's deployed-year cohort
    (nodes deployed that year, never the living fleet) and its source paths
    cite that year.
    """
    space = run_valuation(
        config_from_dict({"metadata": {"base_year": base_year, "horizon_years": horizon_years}})
    )
    ground = build_ground_reference_output(
        space,
        load_ground_config(_GROUND_SCENARIO),
        space_model_path="scratch/space.json",
        ground_scenario_path=DEFAULT_GROUND_SCENARIO_PATH,
    )
    key = str(anchor_fy)
    assert ground.anchor.year == anchor_fy
    assert ground.anchor.nodes == space.business.years[key].nodes_deployed_this_year.value
    assert ground.anchor.source_paths[0] == (
        f'space:business.years."{key}".nodes_deployed_this_year'
    )
    assert ground.meta.validation_results[0].validation_id == f"ground_anchor_{key}_deployed_year"
    assert ground.meta.validation_results[0].severity == "pass"


def test_base_year_2027_checks_the_cadence_target_at_its_own_year_10() -> None:
    """Objective: a shifted base year reads the cadence target at its anchor.

    With base year 2027 the year-10 anchor (90 launches) is FY2037; FY2036
    is model year 9. Expected: the config-derived invariant
    ``anchor_year_launches_match_year_10_dial`` passes against FY2037 (the
    old pinned "90 launches in 2036" check read FY2036 and failed).
    """
    out = run_valuation(config_from_dict({"metadata": {"base_year": 2027, "horizon_years": 10}}))
    results = {r.validation_id: r for r in out.meta.validation_results}
    assert out.business.years["2037"].launches.value == 90
    check = results["anchor_year_launches_match_year_10_dial"]
    assert check.severity == "pass"
    assert check.observed_result == "90 launches in FY2037"
