"""Battery routing module."""

from fastapi import APIRouter
from models.battery import BatteryStatusRequest, BatteryStatusResponse
from controllers.BatteryController import calculate_battery_status

router = APIRouter()


@router.post("/battery_status", response_model=BatteryStatusResponse)
async def battery_status(payload: BatteryStatusRequest):
    """Endpoint to calculate battery status."""
    return calculate_battery_status(payload)
