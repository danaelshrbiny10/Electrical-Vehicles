"""AI Response Models."""

from pydantic import BaseModel


class ConsumptionInput(BaseModel):
    distance: float
    speed: float
    temp: float
    ac: int
    heater: int
    payload: float
    battery_kwh: float
    eff: float


class ConsumptionResult(BaseModel):
    prediction_kwh: float
    message: str
