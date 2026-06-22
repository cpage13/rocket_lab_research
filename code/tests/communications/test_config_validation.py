"""Tests locking the communications config validation behavior (T1.7).

These pin the rejection paths: extra keys, out-of-bounds values, the
BandTriple ordering validator, the ScopeWeights sum validator, the metadata
steady-state-window validator, and frozen/validate-assignment behavior.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from communications.config import (
    BandTriple,
    CommsConfig,
    MetadataDials,
    ScopeWeights,
    config_from_dict,
)


def test_extra_key_rejected() -> None:
    """An unknown top-level block raises ValidationError (CommsConfig extra='forbid')."""
    with pytest.raises(ValidationError):
        config_from_dict(
            {
                "metadata": {"base_year": 2026, "horizon_years": 10, "steady_state_year": 2036},
                "not_a_block": {},
            }
        )


def test_extra_key_in_block_rejected() -> None:
    """An unknown key inside a block raises ValidationError (every block extra='forbid')."""
    with pytest.raises(ValidationError):
        config_from_dict({"spectrum": {"not_a_spectrum_field": 1}})


def test_negative_bandwidth_rejected() -> None:
    """A non-positive leased bandwidth raises ValidationError (gt=0)."""
    with pytest.raises(ValidationError):
        config_from_dict({"spectrum": {"leased_bandwidth_mhz": -1.0}})


def test_lifetime_out_of_range_rejected() -> None:
    """A satellite lifetime of 0 or 21 raises ValidationError (ge=1, le=20)."""
    with pytest.raises(ValidationError):
        config_from_dict({"constellation": {"satellite_lifetime_years": 0}})
    with pytest.raises(ValidationError):
        config_from_dict({"constellation": {"satellite_lifetime_years": 21}})


def test_band_triple_unordered_rejected() -> None:
    """A descending BandTriple raises ValidationError (the low <= mid <= high validator)."""
    with pytest.raises(ValidationError):
        BandTriple(low=2.0, mid=1.0, high=3.0)


def test_band_triple_ordered_accepted() -> None:
    """An ascending BandTriple constructs."""
    triple = BandTriple(low=1.5, mid=2.0, high=3.0)
    assert (triple.low, triple.mid, triple.high) == (1.5, 2.0, 3.0)


def test_scope_weights_must_sum_to_one() -> None:
    """ScopeWeights summing to 1.1 raises; summing to 1.0 constructs."""
    with pytest.raises(ValidationError):
        ScopeWeights(us=0.5, europe=0.3, asia_ex_china=0.3)
    weights = ScopeWeights(us=0.5, europe=0.3, asia_ex_china=0.2)
    assert weights.us + weights.europe + weights.asia_ex_china == 1.0


def test_metadata_steady_state_within_window() -> None:
    """A steady-state year past base_year + horizon_years raises; one inside constructs."""
    with pytest.raises(ValidationError):
        MetadataDials(base_year=2026, horizon_years=10, steady_state_year=2040)
    meta = MetadataDials(base_year=2026, horizon_years=10, steady_state_year=2030)
    assert meta.steady_state_year == 2030


def test_frozen_config() -> None:
    """Assigning to a frozen block field raises; assigning an invalid top-level value raises."""
    cfg = CommsConfig()
    # A nested block is frozen: assignment raises.
    with pytest.raises(ValidationError):
        cfg.spectrum.leased_bandwidth_mhz = 50.0
    # The top-level config is frozen with validate_assignment=True: assignment raises.
    with pytest.raises(ValidationError):
        cfg.scenario_levers = cfg.scenario_levers
