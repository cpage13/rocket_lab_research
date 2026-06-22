"""Tests locking the communications YAML loader behavior (T1.8).

These pin the round-trip of the default scenario against the schema defaults
and the loader's error paths (missing file, empty file, non-mapping root,
malformed YAML, partial fill-out).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from communications.config import CommsConfig, load_config

# The repo-anchored path to the default scenario, computed from this file's
# location so the test is CWD-independent: tests/communications/<this> ->
# repo-root code/scenarios/comms_default.yaml is parents[2]/scenarios/...
_DEFAULT_YAML = Path(__file__).resolve().parents[2] / "scenarios" / "comms_default.yaml"


def test_load_default_scenario_round_trips() -> None:
    """load_config(comms_default.yaml) equals CommsConfig() field-for-field.

    Passes ONLY if the YAML sets every value to the schema default, including
    scenario_levers.scenario_name == "Communications default (central case)".
    """
    assert load_config(_DEFAULT_YAML) == CommsConfig()


def test_missing_file_raises() -> None:
    """A non-existent path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_config(_DEFAULT_YAML.parent / "does_not_exist.yaml")


def test_empty_file_is_all_defaults(tmp_path: Path) -> None:
    """An empty file loads to all defaults (the data is None branch)."""
    empty = tmp_path / "empty.yaml"
    empty.write_text("")
    assert load_config(empty) == CommsConfig()


def test_non_mapping_root_rejected(tmp_path: Path) -> None:
    """A YAML file whose root is a list raises ValueError (the non-mapping guard)."""
    listy = tmp_path / "list_root.yaml"
    listy.write_text("- 1\n- 2\n")
    with pytest.raises(ValueError, match="must contain a YAML mapping"):
        load_config(listy)


def test_malformed_yaml_raises_valueerror(tmp_path: Path) -> None:
    """A file with invalid YAML raises ValueError (the yaml.YAMLError wrap)."""
    bad = tmp_path / "bad.yaml"
    bad.write_text("a: : :\n")
    with pytest.raises(ValueError, match="could not parse YAML"):
        load_config(bad)


def test_partial_yaml_fills_defaults(tmp_path: Path) -> None:
    """A mapping setting only one value loads it overridden, every other block at default."""
    partial = tmp_path / "partial.yaml"
    partial.write_text("spectrum:\n  leased_bandwidth_mhz: 80.0\n")
    cfg = load_config(partial)
    assert cfg.spectrum.leased_bandwidth_mhz == 80.0
    # Every other block fell to its default_factory.
    default = CommsConfig()
    assert cfg.metadata == default.metadata
    assert cfg.constellation == default.constellation
    assert cfg.price_reference == default.price_reference
    assert cfg.ground == default.ground
    # The untouched spectrum fields stay at their defaults.
    assert cfg.spectrum.beams_per_sat == default.spectrum.beams_per_sat
