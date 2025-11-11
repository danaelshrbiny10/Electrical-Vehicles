"""Battery model specifications used in requests."""

from pydantic import BaseModel, Field


class BatteryInput(BaseModel):
    car: dict
    distance_km: float = Field(..., gt=0)
    start_soc_pct: float = Field(..., ge=0, le=100)


class BatteryResult(BaseModel):
    battery_remaining_kwh: float
    battery_remaining_percent: float
    energy_used_kwh: float
    message: str
