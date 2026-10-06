"""The Iridium family: the narrowing function and the Iridium entry.

A communications config of the Iridium family carries a top-level ``iridium:`` block; one of
the High-Bandwidth Cellular Pure Play family does not. Each way into the Iridium family (the
two commands and the Iridium entry) starts by narrowing its config with
:func:`iridium_dials_of`, which returns the Iridium dials or refuses a config of the other
family with :class:`NotAnIridiumConfigError`, so one condition and one error guard each of
them: the saturation command (``python -m communications.saturation``) calls it before it
reads the dials the curve depends on, the Iridium promotion command
(``python -m communications.json_output``) before it loads the curve, and the Iridium entry
before anything else. The message is the one the Iridium promotion command gives today.

The Iridium entry, :func:`run_iridium_model`, takes the config and its saturation curve, both
required, so the curve's presence is a type fact: no call through the entry (the promotion
command's among them) runs the Iridium family without one. On every run it narrows the
config, then checks that the curve was computed for the config's own inputs (the identity
check, :func:`communications.saturation_curve.check_curve_matches`), and only then runs. Until
the Iridium family's own rule and record are built here, the run is interim: the fleet is
sized by today's density path in :mod:`communications.engine` (the derived density, the
aperture-coupled satellites per launch, the fleet target), deployed on the shared
fleet-and-cost loop (:func:`communications.engine.run_fleet_loop`) under the cellular
family's target-and-hold rule, and recorded by the cellular family's record with the v5
physics block; the curve does not yet size or price anything. The loop is not an entry: it
checks neither the family nor a curve, so the guarantees here hold through the two entries.

numpy-free, like every communications module but the saturation module (ADR 010).
"""

from __future__ import annotations

import logging
from typing import Final

from communications.config import CommsConfig, IridiumDials
from communications.engine import (
    CellularRun,
    CellularSizing,
    build_cellular_record,
    build_iridium_result,
    cellular_rule,
    compute_fleet_target,
    derive_iridium_satellites_per_launch,
    derive_iridium_subscribers_per_satellite,
    derive_per_satellite_capacity_gbps,
    resolve_device_spectral_efficiency,
    run_fleet_loop,
)
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


def run_iridium_model(config: CommsConfig, curve: SaturationCurve) -> CellularRun:
    """Run an Iridium config on its saturation curve: the Iridium entry.

    On every run, in this order: the config is narrowed to its Iridium dials
    (:func:`iridium_dials_of`); the curve is checked against the inputs those dials imply
    (``check_curve_matches(saturation_inputs_for(dials), curve)``), so a curve computed for
    other inputs (another held spectrum, say) is never read; then the run, interim until the
    Iridium family's own rule and record are built: today's density path sizes the fleet (the
    device class's spectral efficiency, the per-satellite capacity at the panel, the derived
    people per satellite, the aperture-coupled satellites per launch, and the fleet target
    with its regime, :func:`communications.engine.compute_fleet_target`), the v5 physics block
    is assembled (:func:`communications.engine.build_iridium_result`), the shared
    fleet-and-cost loop deploys the fleet under the cellular rule for that target
    (:func:`communications.engine.run_fleet_loop`,
    :func:`communications.engine.cellular_rule`), and the cellular record carries the v5 block
    (:func:`communications.engine.build_cellular_record`).

    Args:
        config: A communications config with an ``iridium:`` block.
        curve: The saturation curve computed for the config's inputs (the one its
            ``iridium.saturation.curve_path`` names, loaded with
            :func:`communications.saturation_curve.load_saturation_curve`).

    Returns:
        The run's :class:`~communications.engine.CellularRun`: the shared fleet-and-cost
        record and the cellular record with the v5 physics block.

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
    spectral_efficiency = resolve_device_spectral_efficiency(dials)
    per_satellite_capacity_gbps = derive_per_satellite_capacity_gbps(
        dials.spectrum_mhz, spectral_efficiency, dials.aperture_m2
    )
    subscribers_per_satellite = derive_iridium_subscribers_per_satellite(
        per_satellite_capacity_gbps=per_satellite_capacity_gbps,
        active_user_rate_mbps=dials.active_user_rate_mbps,
        concurrency_peak=dials.concurrency_peak,
    )
    satellites_per_launch = derive_iridium_satellites_per_launch(
        configured_satellites_per_launch=config.satellite.satellites_per_launch,
        aperture_m2=dials.aperture_m2,
    )
    fleet_target, binding_regime = compute_fleet_target(
        subscriber_target=config.subscribers.subscribers_at_full_coverage,
        subscribers_per_satellite=subscribers_per_satellite,
        coverage_floor=config.coverage.satellites_for_full_coverage,
        max_fleet_satellites=config.coverage.max_fleet_satellites,
    )
    sizing = CellularSizing(
        fleet_target=fleet_target,
        binding_regime=binding_regime,
        subscribers_per_satellite=subscribers_per_satellite,
        satellites_per_launch=satellites_per_launch,
    )
    physics = build_iridium_result(
        dials,
        fleet_target=fleet_target,
        subscribers_per_satellite=subscribers_per_satellite,
        effective_satellites_per_launch=satellites_per_launch,
    )
    fleet = run_fleet_loop(
        config, cellular_rule(fleet_target), satellites_per_launch=satellites_per_launch
    )
    return CellularRun(
        fleet=fleet, cellular=build_cellular_record(config, fleet, sizing, iridium=physics)
    )


__all__ = ["NotAnIridiumConfigError", "iridium_dials_of", "run_iridium_model"]
