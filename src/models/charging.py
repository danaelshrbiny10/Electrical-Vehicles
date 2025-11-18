"""Data models for charging curve requests and responses."""

from pydantic import BaseModel
from typing import List


class CurvePoint(BaseModel):
    """Represents a point on the charging curve with time and state of charge."""

    minute: float
    soc: float


class ChargingCurveRequest(BaseModel):
    """Request model for charging curve calculation."""

    current_soc: float
    target_soc: float
    charger_power_kw: float


class ChargingCurveResponse(BaseModel):
    """Response model for charging curve calculation."""

    charging_time_minutes: float
    energy_added_kwh: float
    curve_points: List[CurvePoint]
