from fastapi import APIRouter, HTTPException
from models.battery import BatteryInput, BatteryResult
from models.enums.ResponseEnums import ResponseSignal

router = APIRouter()


@router.post(
    "/battery_status",
    response_model=BatteryResult,
    summary="Compute battery status",
    description="Returns remaining battery after a trip segment.",
)
def battery_status(req: BatteryInput):
    try:
        energy_used = req.car["efficiency_kwh_per_km"] * req.distance_km
        battery_remaining = req.car["battery_kwh"] - energy_used
        battery_remaining_pct = (battery_remaining / req.car["battery_kwh"]) * 100

        return BatteryResult(
            battery_remaining_kwh=battery_remaining,
            battery_remaining_percent=battery_remaining_pct,
            energy_used_kwh=energy_used,
            message=ResponseSignal.SUCCESS.value,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{ResponseSignal.ERROR.value}: {e}"
        )
