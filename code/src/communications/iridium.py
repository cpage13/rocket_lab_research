"""The Iridium family: the narrowing function and the Iridium entry.

A communications config of the Iridium family carries a top-level ``iridium:`` block; one of
the High-Bandwidth Cellular Pure Play family does not. Every Iridium path starts by narrowing
its config with :func:`iridium_dials_of`, which returns the Iridium dials or refuses a config
of the other family with :class:`NotAnIridiumConfigError`, so one condition and one error
guard every path: the saturation command (``python -m communications.saturation``) calls it
before it reads the dials the curve depends on, the Iridium promotion command
(``python -m communications.json_output``) before it loads the curve, and the Iridium entry
before anything else. The message is the one the Iridium promotion command gives today.

The Iridium entry, :func:`run_iridium_model`, takes the config and its saturation curve, both
required, so the curve's presence is a type fact: no call runs the Iridium family without
one. On every run it narrows the config, then
checks that the curve was computed for the config's own inputs (the identity check,
:func:`communications.saturation_curve.check_curve_matches`), and only then runs. Until the
shared fleet-and-cost loop lands, the run itself is the interim shared path the cellular entry
also calls (:func:`communications.engine.run_comms_trajectory`), where the fleet is still sized
by today's density path; the curve does not yet size or price anything.

numpy-free, like every communications module but the saturation module (ADR 010).
"""

from __future__ import annotations

import logging
from typing import Final

from communications.config import CommsConfig, IridiumDials
from communications.engine import CommsTrajectory, run_comms_trajectory
from communications.saturation_curve import (
    SaturationCurve,
    check_curve_matches,
    saturation_inputs_for,
)

logger = logging.getLogger(__name__)

_NOT_AN_IRIDIUM_CONFIG: Final[str] = (
    "the scenario does not select the Iridium model: it needs a top-level "
    "'iridium:' block (see scenarios/iridium.yaml)"
)
"""The refusal of a config without an ``iridium:`` block, word for word the Iridium promotion
command's (``communications.json_output``)."""


class NotAnIridiumConfigError(ValueError):
    """A config of the cellular family where an Iridium path needs the Iridium dials."""


def iridium_dials_of(config: CommsConfig) -> IridiumDials:
    """Return a config's Iridium dials, refusing a config that does not select the Iridium model.

    Args:
        config: A communications config.

    Returns:
        Its ``iridium`` block.

    Raises:
        NotAnIridiumConfigError: If the config has no ``iridium:`` block (it is the cellular
            family's).
    """
    if config.iridium is None:
        raise NotAnIridiumConfigError(_NOT_AN_IRIDIUM_CONFIG)
    return config.iridium


def run_iridium_model(config: CommsConfig, curve: SaturationCurve) -> CommsTrajectory:
    """Run an Iridium config on its saturation curve: the Iridium entry.

    On every run, in this order: the config is narrowed to its Iridium dials
    (:func:`iridium_dials_of`); the curve is checked against the inputs those dials imply
    (``check_curve_matches(saturation_inputs_for(dials), curve)``), so a curve computed for
    other inputs (another held spectrum, say) is never read; then the run, on the interim
    shared path (:func:`communications.engine.run_comms_trajectory`).

    Args:
        config: A communications config with an ``iridium:`` block.
        curve: The saturation curve computed for the config's inputs (the one its
            ``iridium.saturation.curve_path`` names, loaded with
            :func:`communications.saturation_curve.load_saturation_curve`).

    Returns:
        The run's :class:`~communications.engine.CommsTrajectory`.

    Raises:
        NotAnIridiumConfigError: If the config has no ``iridium:`` block.
        SaturationCurveMismatchError: If the curve was computed for other inputs, naming the
            first field that differs.
        ValueError: If the run itself fails (the Iridium dials derive fewer than one subscriber
            per satellite).
    """
    dials = iridium_dials_of(config)
    check_curve_matches(saturation_inputs_for(dials), curve)
    logger.debug("the saturation curve %s matches the run's inputs", curve.input_hash)
    return run_comms_trajectory(config)


__all__ = ["NotAnIridiumConfigError", "iridium_dials_of", "run_iridium_model"]
