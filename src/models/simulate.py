"""Data models for simulation requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Literal


class Coordinates(BaseModel):
    """Geographical coordinates with latitude and longitude."""

    lat: float
    lon: float


class ChargerPreference(BaseModel):
    """User preference for charger stops during the trip."""

    mode: Literal["few_long", "quickest_arrival", "many_short"]


class CarModel(BaseModel):
    """Details about the car model for the simulation."""

    model_name: str
    current_battery_percentage: float = Field(..., ge=0, le=100)
    destination_arrival_soc: float = Field(..., ge=0, le=100)
    charger_stops: ChargerPreference


class SimulationRequest(BaseModel):
    """Request model for trip simulation."""

    start: Coordinates
    end: Coordinates
    car: CarModel


class SimulationResponse(BaseModel):
    """Response model for trip simulation results."""

    trip_time_minutes: float
    avg_consumption_kwh_100km: float
    energy_used_kwh: float
    start: Coordinates
    end: Coordinates
    charges: bool
    number_of_charges: int
