"""Response Enums for the application."""

from enum import Enum


class ResponseSignal(Enum):
    """Enumeration for response signals."""
    SUCCESS = "Operation successful"
    FETCHING = "Fetching data from OpenChargeMap API..."
    API_ERROR = "API request failed"
    NO_DATA = "No data returned from API"
    SAVED_LOCAL = "Data saved locally"
    ENV_MISSING = "Missing or invalid API key in environment"
    UNKNOWN_ERROR = "Unknown error occurred"