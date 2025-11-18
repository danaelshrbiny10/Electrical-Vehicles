"""AI Routing Module
This module defines the routing for AI-related endpoints, specifically for predicting energy consumption.
It uses FastAPI to create an API router and defines a POST endpoint for consumption prediction.
"""

from fastapi import APIRouter
from models.ai_responses import AIConsumptionRequest, AIConsumptionResponse
from controllers.AiController import predict_energy_consumption

router = APIRouter()


@router.post("/predict/consumption", response_model=AIConsumptionResponse)
async def predict_consumption(payload: AIConsumptionRequest):
    """Endpoint to predict energy consumption using AI models."""
    return predict_energy_consumption(payload)
