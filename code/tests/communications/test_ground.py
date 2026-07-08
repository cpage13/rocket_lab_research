"""Tests for the slim two-regime comms ground comparison (clean rewrite, Phase 4).

Exercises :func:`communications.ground.build_comms_ground_comparison`: the
``ground=None`` skip (the cost side never blocks), the per-regime ground/space
ratio orientation and the 0.5 / 2.0 materiality-band verdict labels, the
canonical opposite-direction case (space wins the sparse fringe, loses the dense
served market), the same-order band, one regime absent not blocking the other,
the headline boolean's True / False / None states, and the basis-mismatch
exception. The space side is a plain ``float`` (the model's own computed cellular
annual cost per subscriber); no ProvenanceCells, no price/ARPU machinery.
"""

from __future__ import annotations

import pytest

from communications.config import GroundInterfaceDials
from communications.constants import GROUND_BASIS_DEFAULT, DensityRegime
from communications.ground import (
    GROUND_MATERIALLY_CHEAPER_RATIO,
    SPACE_MATERIALLY_CHEAPER_RATIO,
    CommsGroundComparison,
    GroundBasisMismatchError,
    GroundConclusionLabel,
    build_comms_ground_comparison,
)

# A representative model-computed cellular space cost per subscriber, USD/sub/yr.
# All ground baselines below are chosen RELATIVE to this so the band crossings are
# explicit (the value itself is illustrative, not load-bearing).
_SPACE_COST_USD: float = 500.0

# A sparse fresh-build ground cost ABOVE 2x the space cost: ratio 2.4 > 2.0, so
# space is materially cheaper in the sparse fringe (the niche).
_SPARSE_ABOVE_2X_USD: float = 1_200.0

# A dense incumbent-marginal ground cost BELOW 0.5x the space cost: ratio 0.4 <
# 0.5, so ground is materially cheaper in the dense served market.
_DENSE_BELOW_HALF_USD: float = 200.0

# A ground cost inside the [0.5x, 2.0x] band: ratio 1.0, same order of magnitude.
_SAME_ORDER_USD: float = 500.0


def test_ground_none_returns_none() -> None:
    """With no ground interface supplied, the comparison is absent (cost side does not block)."""
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=None,
    )
    assert result is None


def test_opposite_direction_case() -> None:
    """The canonical case: space wins the sparse fringe, loses the dense served market."""
    ground = GroundInterfaceDials(
        dense_ground_cost_per_subscriber_usd=_DENSE_BELOW_HALF_USD,
        sparse_ground_cost_per_subscriber_usd=_SPARSE_ABOVE_2X_USD,
    )
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert isinstance(result, CommsGroundComparison)
    # Sparse: ground 1200 / space 500 = 2.4 > 2.0 -> space materially cheaper.
    assert result.sparse.conclusion_label == GroundConclusionLabel.SPACE_CHEAPER.value
    assert result.sparse.space_is_cheaper is True
    # Dense: ground 200 / space 500 = 0.4 < 0.5 -> ground materially cheaper.
    assert result.dense.conclusion_label == GroundConclusionLabel.GROUND_CHEAPER.value
    assert result.dense.space_is_cheaper is False
    # The headline: space below the sparse fresh-build cost is the niche.
    assert result.headline_space_below_sparse_fresh_build is True


def test_ratio_orientation_is_ground_over_space() -> None:
    """The per-regime ratio is ground / space (the DC ground/orbital convention)."""
    ground = GroundInterfaceDials(
        dense_ground_cost_per_subscriber_usd=_DENSE_BELOW_HALF_USD,
        sparse_ground_cost_per_subscriber_usd=_SPARSE_ABOVE_2X_USD,
    )
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    assert result.sparse.ground_to_space_ratio == pytest.approx(
        _SPARSE_ABOVE_2X_USD / _SPACE_COST_USD
    )
    assert result.sparse.space_to_ground_ratio == pytest.approx(
        _SPACE_COST_USD / _SPARSE_ABOVE_2X_USD
    )
    assert result.sparse.absolute_delta_usd == pytest.approx(_SPARSE_ABOVE_2X_USD - _SPACE_COST_USD)
    assert result.dense.ground_to_space_ratio == pytest.approx(
        _DENSE_BELOW_HALF_USD / _SPACE_COST_USD
    )


def test_same_order_band() -> None:
    """A ground cost inside [0.5x, 2.0x] the space cost is same order of magnitude."""
    ground = GroundInterfaceDials(
        dense_ground_cost_per_subscriber_usd=_SAME_ORDER_USD,
        sparse_ground_cost_per_subscriber_usd=_SAME_ORDER_USD,
    )
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    assert result.sparse.conclusion_label == GroundConclusionLabel.SAME_ORDER.value
    assert result.dense.conclusion_label == GroundConclusionLabel.SAME_ORDER.value
    # At ratio 1.0 exactly, space is not cheaper (the boundary is > 1.0).
    assert result.sparse.space_is_cheaper is False


def test_band_boundaries_are_strict() -> None:
    """A ratio exactly at 0.5 or 2.0 stays same-order (the bands are strict < / >)."""
    # Ground exactly 0.5x the space cost: ratio == 0.5, not < 0.5 -> same order.
    at_half = GroundInterfaceDials(
        dense_ground_cost_per_subscriber_usd=_SPACE_COST_USD * GROUND_MATERIALLY_CHEAPER_RATIO,
        sparse_ground_cost_per_subscriber_usd=_SPACE_COST_USD * SPACE_MATERIALLY_CHEAPER_RATIO,
    )
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=at_half,
    )
    assert result is not None
    assert result.dense.conclusion_label == GroundConclusionLabel.SAME_ORDER.value
    assert result.sparse.conclusion_label == GroundConclusionLabel.SAME_ORDER.value


def test_sparse_supplied_dense_absent() -> None:
    """One regime absent (dense=None) does not block the other regime or the headline."""
    ground = GroundInterfaceDials(
        dense_ground_cost_per_subscriber_usd=None,
        sparse_ground_cost_per_subscriber_usd=_SPARSE_ABOVE_2X_USD,
    )
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    # Dense face is absent: every derived field is None.
    assert result.dense.regime is DensityRegime.DENSE
    assert result.dense.ground_cost_per_subscriber_usd is None
    assert result.dense.ground_to_space_ratio is None
    assert result.dense.space_to_ground_ratio is None
    assert result.dense.absolute_delta_usd is None
    assert result.dense.conclusion_label is None
    assert result.dense.space_is_cheaper is None
    # Sparse face and the headline still compute.
    assert result.sparse.conclusion_label == GroundConclusionLabel.SPACE_CHEAPER.value
    assert result.headline_space_below_sparse_fresh_build is True


def test_headline_true_when_space_below_sparse() -> None:
    """Headline is True when the space cost lands below the sparse fresh-build cost."""
    ground = GroundInterfaceDials(sparse_ground_cost_per_subscriber_usd=_SPACE_COST_USD * 3.0)
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    assert result.headline_space_below_sparse_fresh_build is True


def test_headline_false_when_space_above_sparse() -> None:
    """Headline is False when the space cost is at or above the sparse fresh-build cost."""
    # Sparse ground BELOW the space cost: space is more expensive than even the
    # fresh-build ground, so the niche test fails.
    ground = GroundInterfaceDials(sparse_ground_cost_per_subscriber_usd=_SPACE_COST_USD * 0.5)
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    assert result.headline_space_below_sparse_fresh_build is False


def test_headline_none_when_sparse_absent() -> None:
    """Headline is None when the sparse baseline was not supplied."""
    ground = GroundInterfaceDials(dense_ground_cost_per_subscriber_usd=_DENSE_BELOW_HALF_USD)
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=ground,
    )
    assert result is not None
    assert result.sparse.ground_cost_per_subscriber_usd is None
    assert result.headline_space_below_sparse_fresh_build is None


def test_basis_mismatch_raises() -> None:
    """A basis mismatch between the space figure and the ground block raises."""
    ground = GroundInterfaceDials(
        sparse_ground_cost_per_subscriber_usd=_SPARSE_ABOVE_2X_USD,
        basis="cost_per_gb",
    )
    with pytest.raises(GroundBasisMismatchError):
        build_comms_ground_comparison(
            space_cost_per_subscriber_usd=_SPACE_COST_USD,
            space_basis=GROUND_BASIS_DEFAULT,
            ground=ground,
        )


def test_both_regimes_absent_runs_with_default_block() -> None:
    """A default (all-None) ground block yields both faces absent and a None headline."""
    result = build_comms_ground_comparison(
        space_cost_per_subscriber_usd=_SPACE_COST_USD,
        space_basis=GROUND_BASIS_DEFAULT,
        ground=GroundInterfaceDials(),
    )
    assert result is not None
    assert result.dense.ground_cost_per_subscriber_usd is None
    assert result.sparse.ground_cost_per_subscriber_usd is None
    assert result.headline_space_below_sparse_fresh_build is None
    assert result.basis == GROUND_BASIS_DEFAULT
