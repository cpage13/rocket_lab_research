"""Shared fixtures for the communications test suite.

Provides the default ``CommsConfig`` and the default in-memory ``CommsModelOutput``
(the engine run) once per session so the ground / comparison tests do not each
re-run the engine, plus a default ground config and source catalog.
"""

from __future__ import annotations

import pytest

from communications.config import CommsConfig
from communications.engine import run_comms_model
from communications.ground import (
    GroundReferenceConfig,
    GroundReferenceOutput,
    SourceCatalog,
    build_ground_reference_output,
    default_ground_source_catalog,
    ground_config_from_comms_config,
)
from communications.json_output import enrich_comms_output
from communications.output import CommsModelOutput


@pytest.fixture
def default_comms_config() -> CommsConfig:
    """Return the default (central-case) comms config."""
    return CommsConfig()


@pytest.fixture
def default_comms_output(default_comms_config: CommsConfig) -> CommsModelOutput:
    """Return the default in-memory comms space-model output (one engine run)."""
    return run_comms_model(default_comms_config)


@pytest.fixture
def default_ground_config(default_comms_config: CommsConfig) -> GroundReferenceConfig:
    """Return the default comms ground-reference config built from the comms config."""
    return ground_config_from_comms_config(default_comms_config)


@pytest.fixture
def ground_source_catalog() -> SourceCatalog:
    """Return the default comms ground source catalog."""
    return default_ground_source_catalog()


@pytest.fixture
def default_enriched_output(default_comms_output: CommsModelOutput) -> CommsModelOutput:
    """Return the default comms output with the Phase-5-enriched meta block."""
    return enrich_comms_output(default_comms_output)


@pytest.fixture
def default_ground_output(
    default_comms_output: CommsModelOutput,
    default_ground_config: GroundReferenceConfig,
    default_comms_config: CommsConfig,
    ground_source_catalog: SourceCatalog,
) -> GroundReferenceOutput:
    """Return the default in-memory comms ground reference (one build)."""
    return build_ground_reference_output(
        default_comms_output,
        default_ground_config,
        default_comms_config.price_reference,
        ground_source_catalog,
    )
