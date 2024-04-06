import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from assignment2.assignment2 import fetch_weather_code


@pytest.fixture
def mock_successful_response():
    """Fixture to simulate a successful API response."""
    return MagicMock(status_code=200, json=lambda: {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": {
            "time": ["2024-03-01T00:00", "2024-03-01T01:00"],
            "weather_code": [0, 100]
        }
    })


@pytest.fixture
def mock_failure_response():
    """Fixture to simulate an API failure response."""
    return MagicMock(status_code=404)


@patch('assignment2.assignment2.requests.get')
def test_fetch_weather_code_success(mock_get, mock_successful_response):
    """Test successful fetching of weather code."""
    mock_get.return_value = mock_successful_response

    # Assuming your function expects a datetime object for incident_datetime
    incident_datetime = datetime.strptime("2024-03-01T00:30", "%Y-%m-%dT%H:%M")
    latitude, longitude = 52.52, 13.41

    # Attempt to fetch weather code
    weather_code = fetch_weather_code(latitude, longitude, incident_datetime)

    # Validate that the correct weather code was fetched
    assert weather_code == 0, "Expected weather code does not match."


@patch('assignment2.assignment2.requests.get')
def test_fetch_weather_code_failure(mock_get, mock_failure_response):
    """Test failure in fetching weather code."""
    mock_get.return_value = mock_failure_response

    incident_datetime = datetime.strptime("2024-03-01T00:30", "%Y-%m-%dT%H:%M")
    latitude, longitude = 52.52, 13.41

    # Attempt to fetch weather code expecting None due to failure
    weather_code = fetch_weather_code(latitude, longitude, incident_datetime)

    # Validate that the function handled the failure gracefully
    assert weather_code is None, "Expected None due to API call failure."
