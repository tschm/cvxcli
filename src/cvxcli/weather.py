#    Copyright 2023 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Module for retrieving weather data from the Open-Meteo API.

This module provides a command-line interface for fetching current weather data
for a specified location and metric using the Open-Meteo API.
"""

from typing import Any

import fire  # type: ignore
import requests  # type: ignore

# HTTP status code constants
HTTP_OK = 200


class MetricNotSupportedError(ValueError):
    """Raised when an unsupported metric is requested.

    >>> raise MetricNotSupportedError()
    Traceback (most recent call last):
        ...
    cvxcli.weather.MetricNotSupportedError: Metric not supported!
    """

    def __init__(self) -> None:
        """Initialize the exception with a default message."""
        super().__init__("Metric not supported!")


class ServiceUnavailableError(ConnectionError):
    """Raised when the Open-Meteo service is unavailable."""

    def __init__(self) -> None:
        """Initialize the exception with a default message."""
        super().__init__("Open-Meteo is down!")


def cli(metric: str, latitude: float = 37.4419, longitude: float = -122.143) -> Any:
    """Get the current weather for a given metric.

    Parameters
    ----------
    metric : str
        The metric to get the current weather for.
        Use time, temperature, windspeed, winddirection or weathercode
        For details: https://open-meteo.com/en/docs
    latitude : float, optional
        The latitude to get the current weather for, by default 37.4419
    longitude : float, optional
        The longitude to get the current weather for, by default -122.143
    """
    url = "https://api.open-meteo.com/v1/forecast"
    url = f"{url}?latitude={latitude!s}&longitude={longitude!s}&current_weather=true"
    r = requests.get(url, timeout=10)

    if r.status_code == HTTP_OK:
        if metric in r.json()["current_weather"]:
            x = r.json()["current_weather"][metric]
            return x
        else:
            raise MetricNotSupportedError()
    else:
        raise ServiceUnavailableError()


def main() -> None:  # pragma: no cover
    """Run the CLI using Fire."""
    fire.Fire(cli)
