from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from models.car_model import CarInput
from models.simulate_models import SimulateResponse
from models.enums.ResponseEnums import ResponseSignal
from routing.simulate import simulate_trip

router = APIRouter()


class SimulateRequest(BaseModel):
    start: List[float] = Field(..., description="Start [lat, lon]")
    end: List[float] = Field(..., description="End [lat, lon]")
    car: CarInput
    start_soc: float = Field(80.0, ge=0, le=100)
    target_arrival_soc: float = Field(20.0, ge=0, le=100)
    avg_speed_kmh: Optional[float] = Field(None)


@router.post("/simulate", response_model=SimulateResponse)
def simulate_route(req: SimulateRequest):
    try:
        result = simulate_trip(
            start=tuple(req.start),
            end=tuple(req.end),
            car=req.car,
            start_soc_pct=req.start_soc,
            min_arrival_soc_pct=req.target_arrival_soc,
            avg_speed_kmh=req.avg_speed_kmh or 90.0,
        )
        return SimulateResponse(**result, message=ResponseSignal.SUCCESS.value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{ResponseSignal.ERROR.value} {e}")
