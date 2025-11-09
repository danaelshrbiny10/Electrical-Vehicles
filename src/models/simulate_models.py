from pydantic import BaseModel
from typing import List

class SimulateResponse(BaseModel):
    """Response of the route simulation endpoint."""
    distance_km: float
    energy_needed_kwh: float
    battery_remaining_kwh: float
    battery_remaining_percent: float
    needs_charge: bool
    message: str

class ChargingCurveResponse(BaseModel):
    """Response for charging curve estimation."""
    soc_from: float
    soc_to: float
    estimated_minutes: float
    curve_points: List[float]
    message: str
