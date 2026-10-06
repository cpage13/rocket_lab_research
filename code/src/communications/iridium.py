"""The Iridium family: the one function that narrows a config to its Iridium dials.

A communications config of the Iridium family carries a top-level ``iridium:`` block; one of
the High-Bandwidth Cellular Pure Play family does not. Every Iridium path starts by narrowing
its config with :func:`iridium_dials_of`, which returns the Iridium dials or refuses a config
of the other family with :class:`NotAnIridiumConfigError`, so one condition and one error
guard every path: the saturation command (``python -m communications.saturation``) calls it
before it reads the dials the curve depends on. The message is the one the Iridium promotion
command gives today.

numpy-free, like every communications module but the saturation module (ADR 010).
"""

from __future__ import annotations

import logging
from typing import Final

from communications.config import CommsConfig, IridiumDials

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


__all__ = ["NotAnIridiumConfigError", "iridium_dials_of"]
