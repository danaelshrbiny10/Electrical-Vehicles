"""Models for EV charging calculations."""

from pydantic import BaseModel, Field
from typing import List

class ChargingCurveRequest(BaseModel):
    """Request for charging curve calculation."""
    car: dict
    station_power_kw: float = Field(..., gt=0, description="Station power in kW")
    soc_from_percent: float = Field(..., ge=0, le=100)
    soc_to_percent: float = Field(..., ge=0, le=100)


class ChargingCurveResult(BaseModel):
    """Response for charging curve estimation."""
    soc_from: float
    soc_to: float
    estimated_minutes: float
    curve_points: List[float]
    message: str
