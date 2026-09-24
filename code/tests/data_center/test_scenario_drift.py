"""Drift guard: a scenario that claims the default dials carries them.

``scenarios/with_premium.yaml`` and ``scenarios/upside_7yr.yaml`` each describe
themselves as the default dial set plus stated changes. Before their 2026-09-23
rebase they still carried the dials ``scenarios/default.yaml`` had dropped on
2026-07-14 (the co-mounted radiator at 0.013 and 0.012 t/kW, solar and radiator
cost at 0.04 $M/kW), so every comparison against the default was confounded.
This module loads each scenario and the default through the real loader,
:func:`data_center.config.load_config`, and compares every dial, so a change to
``default.yaml`` that is not mirrored into these files fails here, naming the
dial.

The stated changes come from each file's own header:

* ``with_premium.yaml``: the premium-uplifted central R band
  (``r_band.central``); its low and high bands fall to the model defaults.
* ``upside_7yr.yaml``: the 7-year service life (``fleet.service_life_years``)
  and its flat 1.47 central R (``r_band.central``).

Each file may also carry its own label, ``scenario_name``. The ``metadata``
block is NOT exempt: it holds the radiator-architecture dial, one of the dials
the rebase restored.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from data_center.config import load_config

type DialPath = str
"""A dotted path to one leaf of a dumped config, list items indexed (``r_band.central[0].r``)."""

_SCENARIO_LABEL: DialPath = "scenario_name"
"""The scenario's own label, which any scenario file may set."""

_STATED_CHANGES: dict[str, tuple[DialPath, ...]] = {
    "with_premium": ("r_band.central",),
    "upside_7yr": ("fleet.service_life_years", "r_band.central"),
}
"""Each rebased scenario's stated changes from the default, keyed by file stem, per its header."""

_ABSENT = "<absent>"
"""Stands in for a leaf only one config has (a band with fewer anchors); no dial holds it."""


def _leaves(node: object, path: DialPath = "") -> dict[DialPath, object]:
    """Flatten a dumped config into one entry per leaf value, keyed by its dotted path."""
    leaves: dict[DialPath, object] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            leaves.update(_leaves(value, f"{path}.{key}" if path else str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            leaves.update(_leaves(value, f"{path}[{index}]"))
    else:
        leaves[path] = node
    return leaves


def _within(path: DialPath, prefix: DialPath) -> bool:
    """Return whether ``path`` is ``prefix`` itself or a leaf beneath it."""
    return path == prefix or path.startswith((f"{prefix}.", f"{prefix}["))


@pytest.mark.parametrize("stem", sorted(_STATED_CHANGES))
def test_rebased_scenario_differs_from_default_only_in_its_stated_changes(
    stem: str, scenarios_dir: Path
) -> None:
    """Objective: ``<stem>.yaml`` is the default dial set plus its stated changes, nothing else.

    Both files load through the real loader and are dumped whole, so every dial
    is compared: the ``metadata`` block's radiator architecture, and the dials
    a file omits, which fall to the model defaults. Expected outcome: every
    leaf outside the stated changes and the scenario's own label equals the
    default's (on failure the message names each drifted dial by path, with
    both values), and each stated change still differs from the default, so the
    scenario keeps the sensitivity it exists to test.
    """
    default = _leaves(load_config(scenarios_dir / "default.yaml").model_dump(mode="json"))
    scenario = _leaves(load_config(scenarios_dir / f"{stem}.yaml").model_dump(mode="json"))
    stated = _STATED_CHANGES[stem]
    allowed = (_SCENARIO_LABEL, *stated)

    differing = sorted(
        path
        for path in default.keys() | scenario.keys()
        if default.get(path, _ABSENT) != scenario.get(path, _ABSENT)
    )
    drifted = [path for path in differing if not any(_within(path, p) for p in allowed)]
    assert not drifted, (
        f"{stem}.yaml differs from default.yaml outside its stated changes {allowed}:\n"
        + "\n".join(
            f"  {path}: default {default.get(path, _ABSENT)!r}, "
            f"{stem} {scenario.get(path, _ABSENT)!r}"
            for path in drifted
        )
    )

    missing = [p for p in stated if not any(_within(path, p) for path in differing)]
    assert not missing, f"{stem}.yaml no longer makes its stated change(s): {missing}"
