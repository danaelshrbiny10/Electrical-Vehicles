from pydantic import BaseModel, Field
from typing import Optional
from .car_model import CarInput

class BatteryInput(BaseModel):
    """Battery status request input."""
    car: CarInput
    distance_km: float = Field(..., gt=0, description="Distance to drive in km")
    start_soc_pct: float = Field(..., ge=0, le=100, description="Start SOC (%)")

class BatteryResult(BaseModel):
    """Battery status response."""
    battery_remaining_kwh: float
    battery_remaining_percent: float
    energy_used_kwh: float
    message: str

class ChargingCurveRequest(BaseModel):
    """Request for charging curve calculation."""
    car: CarInput
    station_power_kw: float = Field(..., gt=0, description="Station power in kW")
    soc_from_percent: float = Field(..., ge=0, le=100)
    soc_to_percent: float = Field(..., ge=0, le=100)
