"""Car model definition for electric vehicles."""

from pydantic import BaseModel, Field


class Car(BaseModel):
    """Electric vehicle model representation."""

    model_name: str = "UserEV"
    battery_kwh: float = Field(..., gt=0, description="Usable battery capacity (kWh)")
    efficiency_kwh_per_km: float = 0  # default 0 if not needed
    max_charge_kw: float = Field(
        ..., gt=0, description="Vehicle charge acceptance (kW)"
    )
