"""Example test module demonstrating testing best practices."""

from typing import Tuple

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Create sample data for testing."""
    np.random.seed(42)
    n_samples = 100
    X = pd.DataFrame({
        "feature1": np.random.normal(0, 1, n_samples),
        "feature2": np.random.uniform(-1, 1, n_samples),
    })
    y = pd.Series(np.random.binomial(1, 0.5, n_samples), name="target")
    return X, y


def test_data_shape(sample_data: Tuple[pd.DataFrame, pd.Series]) -> None:
    """Features and target must align."""
    X, y = sample_data
    assert X.shape[0] == y.shape[0]
    assert X.shape[1] == 2


def test_no_missing_values(sample_data: Tuple[pd.DataFrame, pd.Series]) -> None:
    """Dataset must be complete."""
    X, y = sample_data
    assert not X.isna().any().any()
    assert not y.isna().any()


@pytest.mark.parametrize("threshold", [-0.5, 0.0, 0.5])
def test_feature_threshold(sample_data: Tuple[pd.DataFrame, pd.Series], threshold: float) -> None:
    """Threshold filter returns a boolean Series."""
    X, _ = sample_data
    result = X["feature1"] > threshold
    assert isinstance(result, pd.Series)
    assert result.dtype == bool
