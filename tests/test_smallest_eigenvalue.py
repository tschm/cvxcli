"""Tests for the smallest_eigenvalue module functionality.

This module contains tests to verify that the smallest eigenvalue calculation
works correctly with the provided test data.
"""

import pytest

from cvxcli import smallest_ev


def test_smallest_eigenvalue(resource_dir):
    """Test that the smallest eigenvalue calculation works correctly.

    This test verifies that the smallest_ev function correctly calculates
    the smallest eigenvalue from a test BSON file and returns the expected value.

    Args:
        resource_dir: Fixture providing the path to the test resources directory.
    """
    file = resource_dir / "test.bson"

    data = smallest_ev(file)
    assert data["cov"] == pytest.approx(8.673386399472251e-05)
