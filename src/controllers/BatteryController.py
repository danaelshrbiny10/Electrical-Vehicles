from fastapi import APIRouter, HTTPException
from models.car_model import CarInput
from models.battery_status import BatteryInput, BatteryResult
from models.enums.ResponseEnums import ResponseSignal
from routing.battery import compute_battery_after_distance

router = APIRouter()

@router.post("/battery_status", response_model=BatteryResult)
def battery_status(req: BatteryInput):
    try:
        return compute_battery_after_distance(
            car=req.car,
            distance_km=req.distance_km,
            start_soc_pct=req.start_soc_pct
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{ResponseSignal.ERROR.value} {e}")
