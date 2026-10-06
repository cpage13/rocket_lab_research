"""Tests for the shared cadence spine, :mod:`common.cadence`.

The one home of the whole-fleet launch cadence both ventures use: the eight
cadence and launch-cost defaults, the two validated dial blocks, and the two
cell-producing functions. The data-center and communications configs hold
these very classes (asserted below), so there is no second copy to drift.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import get_args

import pytest
import yaml
from pydantic import ValidationError

from common.cadence import (
    CADENCE_CEILING_DEFAULT,
    FIRST_LAUNCH_YEAR_DEFAULT,
    HIGH_CADENCE_COST_MUSD_DEFAULT,
    HIGH_CADENCE_LAUNCHES_DEFAULT,
    LAUNCHES_AT_YEAR_5_DEFAULT,
    LAUNCHES_AT_YEAR_10_DEFAULT,
    LOW_CADENCE_COST_MUSD_DEFAULT,
    LOW_CADENCE_LAUNCHES_DEFAULT,
    CadenceDials,
    LaunchCostDials,
    compute_launch_cost_musd,
    compute_launches_per_year,
)
from communications.config import CommsConfig, load_comms_config
from data_center.config import ValuationConfig, load_config


def test_both_configs_hold_the_shared_dial_blocks() -> None:
    """Objective: one cadence spine, not two copies kept equal by a drift test.

    Expected: the data-center and communications configs declare their
    ``cadence`` and ``launch_cost`` fields as the :mod:`common.cadence`
    classes, and their defaults are equal.
    """
    for config in (ValuationConfig, CommsConfig):
        assert config.model_fields["cadence"].annotation is CadenceDials
        assert config.model_fields["launch_cost"].annotation is LaunchCostDials
    assert ValuationConfig().cadence == CommsConfig().cadence
    assert ValuationConfig().launch_cost == CommsConfig().launch_cost


def test_the_dial_blocks_default_to_the_known_anchors() -> None:
    """Objective: the defaults are the named constants and the venture-scenario values.

    Expected: ceiling 150, year-5 14, year-10 90, first launch 1; launch cost
    $25.0M at 5 launches a year and $13.5M at 100.
    """
    cadence = CadenceDials()
    assert (
        (
            cadence.cadence_ceiling,
            cadence.launches_at_year_5,
            cadence.launches_at_year_10,
            cadence.first_launch_year,
        )
        == (
            CADENCE_CEILING_DEFAULT,
            LAUNCHES_AT_YEAR_5_DEFAULT,
            LAUNCHES_AT_YEAR_10_DEFAULT,
            FIRST_LAUNCH_YEAR_DEFAULT,
        )
        == (150, 14, 90, 1)
    )
    launch = LaunchCostDials()
    assert (
        (
            launch.low_cadence_cost_musd,
            launch.high_cadence_cost_musd,
            launch.low_cadence_launches,
            launch.high_cadence_launches,
        )
        == (
            LOW_CADENCE_COST_MUSD_DEFAULT,
            HIGH_CADENCE_COST_MUSD_DEFAULT,
            LOW_CADENCE_LAUNCHES_DEFAULT,
            HIGH_CADENCE_LAUNCHES_DEFAULT,
        )
        == (25.0, 13.5, 5.0, 100.0)
    )


@pytest.mark.parametrize("dials", [CadenceDials, LaunchCostDials])
def test_the_dial_blocks_are_frozen_and_reject_unknown_fields(
    dials: type[CadenceDials] | type[LaunchCostDials],
) -> None:
    """Objective: a scenario typo fails loudly and a loaded block cannot change.

    Expected: an unknown key (including the retired v7 ``launch_y0_musd``)
    raises ``ValidationError``, and so does assigning to a loaded field.
    """
    for bogus in ({"bogus": 1}, {"launch_y0_musd": 25.0}):
        with pytest.raises(ValidationError):
            dials.model_validate(bogus)
    block = dials()
    field = next(iter(dials.model_fields))
    with pytest.raises(ValidationError):
        setattr(block, field, getattr(block, field))


def test_a_nonpositive_cadence_ceiling_is_rejected() -> None:
    """Objective: the carrying capacity is a positive launch count. Expected: 0 raises."""
    with pytest.raises(ValidationError):
        CadenceDials(cadence_ceiling=0)


def test_the_launch_cost_dials_refuse_a_number_that_is_not_finite_naming_the_field(
    tmp_path: Path,
) -> None:
    """Objective: no run of either model starts from a NaN or an infinity in the shared
    launch-cost block: each float dial of :class:`LaunchCostDials` is refused at load when it
    is not finite, naming the field (before the fix an infinite launch cost loaded for both
    models, which the communications model's artifact then refused and the data-center path
    did not check, and an infinite ``low_cadence_launches`` was refused only by the anchors'
    order, naming no field).

    Sample: every float field of the block, walked from the model's own fields (so a field
    added later is walked too), each written in a scenario YAML's ``launch_cost`` block as
    ``.inf``, ``-.inf`` and ``.nan`` in turn and loaded by both models' scenario loaders
    (``communications.config.load_comms_config`` and ``data_center.config.load_config``).

    Expected outcome: the walk finds the block's four dials; each scenario fails at load, for
    both models, with one ValidationError located at that field
    (``launch_cost.high_cadence_cost_musd``, say), of pydantic's type for a number that is not
    finite.
    """
    fields = [
        name
        for name, field in LaunchCostDials.model_fields.items()
        if float in (get_args(field.annotation) or (field.annotation,))
    ]
    assert {
        "low_cadence_cost_musd",
        "high_cadence_cost_musd",
        "low_cadence_launches",
        "high_cadence_launches",
    } <= set(fields)
    scenario = tmp_path / "not_finite.yaml"
    for field in fields:
        for value in (math.inf, -math.inf, math.nan):
            scenario.write_text(yaml.safe_dump({"launch_cost": {field: value}}), encoding="utf-8")
            for load in (load_comms_config, load_config):
                with pytest.raises(ValidationError) as refused:
                    load(scenario)
                located = [
                    (".".join(map(str, error["loc"])), error["type"])
                    for error in refused.value.errors()
                ]
                assert located == [(f"launch_cost.{field}", "finite_number")], (
                    load.__module__,
                    field,
                    value,
                )


def test_launches_per_year_year_zero_is_zero() -> None:
    """Objective: no launch before the first launch year. Expected: year 0 flies 0."""
    assert compute_launches_per_year(0).value == 0


def test_launches_per_year_is_integer() -> None:
    """Objective: launches are whole missions. Expected: an int count cell."""
    result = compute_launches_per_year(8)
    assert isinstance(result.value, int)
    assert result.unit == "count"


def test_launch_cost_is_provenance_cell() -> None:
    """Objective: the launch cost is a traced cell. Expected: a $M float cell."""
    result = compute_launch_cost_musd(50)
    assert isinstance(result.value, float)
    assert result.unit == "MUSD"
    assert result.formula_name == "launch_cost_musd_from_cadence_log_linear"
