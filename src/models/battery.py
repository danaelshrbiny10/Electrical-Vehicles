"""Models for battery status requests and responses."""

from pydantic import BaseModel


class BatteryStatusRequest(BaseModel):
    """Request model for battery status calculation."""

    battery_percentage: float
    distance_km: float


class BatteryStatusResponse(BaseModel):
    """Response model for battery status calculation."""

    remaining_battery_percentage: int
    energy_used_kwh: float
