"""Car model specifications used in requests."""

from pydantic import BaseModel, Field


class Car(BaseModel):
    """Car specification used in requests."""

    model_name: str = Field("UserEV", description="Model name")
    battery_kwh: float = Field(..., gt=0, description="Usable battery capacity (kWh)")
    efficiency_kwh_per_km: float = Field(..., gt=0, description="Consumption (kWh/km)")
    max_charge_kw: float = Field(
        ..., gt=0, description="Vehicle charge acceptance (kW)"
    )
