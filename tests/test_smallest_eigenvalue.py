import pytest

from src.cvx.cli import smallest_ev


def test_smallest_eigenvalue(resource_dir):
    file = resource_dir / "test.bson"

    data = smallest_ev(file)
    assert data["cov"] == pytest.approx(8.673386399472251e-05)
