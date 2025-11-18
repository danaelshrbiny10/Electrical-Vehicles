"""Routing module for charging curve computations."""

from fastapi import APIRouter
from models.charging import ChargingCurveRequest, ChargingCurveResponse
from controllers.ChargingController import compute_charging_curve

router = APIRouter()


@router.post("/charging_curve", response_model=ChargingCurveResponse)
async def charging_curve(payload: ChargingCurveRequest):
    """Endpoint to compute the charging curve based on the given parameters."""
    return compute_charging_curve(payload)
