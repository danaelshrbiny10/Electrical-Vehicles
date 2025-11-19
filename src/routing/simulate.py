"""Simulate routing endpoint."""

from fastapi import APIRouter
from models.simulate import SimulationRequest, SimulationResponse
from controllers.SimulateController import simulate_trip

router = APIRouter()


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_endpoint(payload: SimulationRequest):
    """Endpoint to simulate a trip based on the given parameters."""
    return await simulate_trip(payload)
