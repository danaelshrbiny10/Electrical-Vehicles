"""AI Models for Vehicle Energy Consumption Prediction."""

from pydantic import BaseModel


class AIConsumptionRequest(BaseModel):
    """Request model for AI energy consumption prediction."""

    distance: float
    speed: float
    temp: float
    ac: int
    heater: int
    payload: float
    battery_kwh: float


class AIConsumptionResponse(BaseModel):
    """Response model for AI energy consumption prediction."""

    predicted_consumption_kwh_100km: float
    total_energy_used_kwh: float
