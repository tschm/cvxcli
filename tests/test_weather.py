"""Tests for the weather module functionality.

This module contains tests to verify that the weather API client works correctly,
handles errors appropriately, and validates input parameters.
"""

from unittest import mock

import pytest

from cvxcli.weather import cli, MetricNotSupportedError, ServiceUnavailableError


def test_weather():
    """Test that the weather API client returns valid temperature data.

    This test verifies that the cli function correctly retrieves temperature data
    from the Open-Meteo API and that the returned value is a float within a
    reasonable temperature range (-50°C to 50°C).
    """
    temperature = cli(metric="temperature")
    print(temperature)
    assert isinstance(temperature, float)
    assert temperature > -50
    assert temperature < 50


def test_missing_metric():
    """Test that the weather API client properly handles invalid metrics.

    This test verifies that the cli function raises a MetricNotSupportedError when
    an unsupported metric name is provided.
    """
    with pytest.raises(MetricNotSupportedError, match="Metric not supported!"):
        cli(metric="maffay")


def test_server_down():
    """Test that the weather API client properly handles server errors.

    This test mocks a 500 server response and verifies that the cli function
    raises a ServiceUnavailableError when the API server returns an error status code.
    """
    with mock.patch("requests.get", return_value=mock.Mock(status_code=500)):
        with pytest.raises(ServiceUnavailableError):
            cli("temperature")


def test_timeout_parameter():
    """Test that the weather API client includes a timeout parameter.

    This test verifies that the cli function passes a timeout parameter
    to requests.get to prevent hanging requests.
    """
    with mock.patch("requests.get") as mock_get:
        mock_get.return_value = mock.Mock(
            status_code=200,
            json=lambda: {"current_weather": {"temperature": 20.0}},
        )
        cli("temperature")
        mock_get.assert_called_once()
        # Verify timeout parameter is present in the call
        args, kwargs = mock_get.call_args
        assert "timeout" in kwargs
        assert kwargs["timeout"] == 10
