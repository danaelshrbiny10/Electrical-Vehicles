"""Models for simulation requests and responses."""

from typing import List
from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    start: List[float] = Field(..., description="[lat, lon]")
    end: List[float] = Field(..., description="[lat, lon]")
    car: dict
    start_soc: float = Field(80.0, ge=0, le=100)
    target_arrival_soc: float = Field(20.0, ge=0, le=100)


class SimulateResponse(BaseModel):
    distance_km: float
    energy_needed_kwh: float
    battery_remaining_kwh: float
    battery_remaining_percent: float
    needs_charge: bool
    message: str
