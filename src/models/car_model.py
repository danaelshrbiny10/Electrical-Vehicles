from pydantic import BaseModel, Field

class CarInput(BaseModel):
    """
    Car parameters expected from the user.

    - battery_kwh: usable battery capacity in kWh
    - efficiency_kwh_per_km: energy consumption (kWh per km)
    - max_charge_kw: maximum vehicle charging power (kW)
    - model_name: optional vehicle name
    """
    model_name: str = Field("UserEV", description="Vehicle model name")
    battery_kwh: float = Field(..., gt=0, description="Usable battery capacity (kWh)")
    efficiency_kwh_per_km: float = Field(..., gt=0, description="Energy consumption per km (kWh/km)")
    max_charge_kw: float = Field(..., gt=0, description="Max vehicle charging power (kW)")
