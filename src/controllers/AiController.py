"""AI Controller for predicting energy consumption of electric vehicles."""

from models.ai_responses import AIConsumptionRequest, AIConsumptionResponse


def predict_energy_consumption(data: AIConsumptionRequest) -> AIConsumptionResponse:
    """Predict energy consumption based on various parameters."""
    base = 14.5

    speed_factor = (data.speed - 70) * 0.05
    payload_factor = (data.payload / 100) * 0.3
    temp_factor = abs(data.temp - 20) * 0.1

    ac_factor = 1.0 if data.ac == 1 else 0
    heater_factor = 1.5 if data.heater == 1 else 0

    predicted = (
        base + speed_factor + payload_factor + temp_factor + ac_factor + heater_factor
    )

    energy_used = (predicted / 100) * data.distance

    return AIConsumptionResponse(
        predicted_consumption_kwh_100km=round(predicted, 2),
        total_energy_used_kwh=round(energy_used, 2),
    )
