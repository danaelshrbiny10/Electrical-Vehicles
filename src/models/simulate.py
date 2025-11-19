"""Data models for simulation requests and responses."""

from pydantic import BaseModel
from typing import List, Optional, Literal


class Coordinates(BaseModel):
    """Latitude / Longitude coordinates."""

    lat: float
    lon: float


class ChargerPreference(BaseModel):
    """User preference for how charging stops are selected."""

    mode: Literal["few_long", "quickest_arrival", "many_short"]


class CarModel(BaseModel):
    """Car and battery information for simulation."""

    model_name: str
    current_battery_percentage: float
    destination_arrival_soc: float
    charger_stops: ChargerPreference


class StationInfo(BaseModel):
    """Information about a charging station."""

    name: str
    lat: float
    lon: float


class SimulationRequest(BaseModel):
    """Request model for a trip simulation."""

    start: Coordinates
    end: Coordinates
    car: CarModel


class SimulationResponse(BaseModel):
    """Response model for a trip simulation."""

    trip_time_minutes: float
    avg_consumption_kwh_100km: float
    energy_used_kwh: float
    start: Coordinates
    end: Coordinates
    charges: bool
    number_of_charges: int
    stations: Optional[List[StationInfo]] = []
