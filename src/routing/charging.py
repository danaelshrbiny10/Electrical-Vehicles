from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from models.battery import BatteryInput, BatteryResult
from models.enums.ResponseEnums import ResponseSignal

router = APIRouter()


class ChargingCurveResult(BaseModel):
    soc_from: float
    soc_to: float
    estimated_minutes: float
    curve_points: List[float]
    message: str


def estimate_charge_minutes_and_curve(
    car: dict, station_power_kw: float, soc_from: float, soc_to: float
):
    max_power = min(car.get("max_charge_kw", 50), station_power_kw)
    battery_capacity = car["battery_kwh"]
    soc_from_kwh = soc_from * battery_capacity
    soc_to_kwh = soc_to * battery_capacity
    energy_needed = soc_to_kwh - soc_from_kwh
    time_hours = energy_needed / max_power
    time_minutes = time_hours * 60
    steps = 10
    curve_points = [
        round(soc_from + (soc_to - soc_from) * i / steps, 3) * 100
        for i in range(steps + 1)
    ]
    return time_minutes, curve_points


@router.post(
    "/charging_curve",
    response_model=ChargingCurveResult,
    summary="EV Charging Curve",
    description="Estimate EV charging time and SOC curve points.",
)
def charging_curve(req: BatteryInput, BatteryResult):
    try:
        soc_from = req.soc_from_percent / 100.0
        soc_to = req.soc_to_percent / 100.0
        minutes, curve = estimate_charge_minutes_and_curve(
            car=req.car,
            station_power_kw=req.station_power_kw,
            soc_from=soc_from,
            soc_to=soc_to,
        )
        return ChargingCurveResult(
            soc_from=req.soc_from_percent,
            soc_to=req.soc_to_percent,
            estimated_minutes=round(minutes, 2),
            curve_points=[round(p, 2) for p in curve],
            message=ResponseSignal.SUCCESS.value,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{ResponseSignal.ERROR.value}: {e}"
        )
