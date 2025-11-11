from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from models.simulate import SimulateResponse
from models.car import Car
from models.enums.ResponseEnums import ResponseSignal

router = APIRouter()


class SimulateRequest(BaseModel):
    start: List[float] = Field(
        ..., description="Start coordinate [lat, lon]", example=[30.0444, 31.2357]
    )
    end: List[float] = Field(
        ..., description="End coordinate [lat, lon]", example=[30.0101, 31.2499]
    )
    car: Car = Field(..., description="Car parameters")
    start_soc: float = Field(80.0, ge=0, le=100, example=80)
    target_arrival_soc: float = Field(20.0, ge=0, le=100, example=20)
    avg_speed_kmh: Optional[float] = Field(
        None, description="Average speed (km/h)", example=90
    )


@router.post(
    "/simulate",
    response_model=SimulateResponse,
    summary="Simulate EV trip",
    description="Returns distance, energy needed, and remaining battery after a trip.",
    response_description="Simulation result with energy and battery info",
)
def simulate_route(req: SimulateRequest):
    try:
        # Placeholder logic, replace with AI model or calculations
        distance = 4.3
        energy_needed = req.car.efficiency_kwh_per_km * distance
        battery_remaining_kwh = req.car.battery_kwh - energy_needed
        battery_remaining_percent = (battery_remaining_kwh / req.car.battery_kwh) * 100
        needs_charge = battery_remaining_percent < req.target_arrival_soc

        return SimulateResponse(
            distance_km=distance,
            energy_needed_kwh=energy_needed,
            battery_remaining_kwh=battery_remaining_kwh,
            battery_remaining_percent=battery_remaining_percent,
            needs_charge=needs_charge,
            message=ResponseSignal.SUCCESS.value,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{ResponseSignal.ERROR.value}: {e}"
        )
