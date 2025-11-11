from fastapi import APIRouter, HTTPException
from models.ai_responses import ConsumptionInput, ConsumptionResult
from models.enums.ResponseEnums import ResponseSignal

router = APIRouter()


@router.post(
    "/predict/consumption",
    response_model=ConsumptionResult,
    summary="AI EV consumption prediction",
    description="Predict energy consumption using AI/ML.",
)
def predict_consumption(req: ConsumptionInput):
    try:
        # Simple ML calculation placeholder
        base_energy = req.distance * req.eff
        ac_penalty = 0.01 * req.distance if req.ac else 0
        heater_penalty = 0.02 * req.distance if req.heater else 0
        payload_penalty = 0.0001 * req.payload * req.distance
        temp_penalty = 0.0005 * abs(req.temp - 25) * req.distance

        prediction = (
            base_energy + ac_penalty + heater_penalty + payload_penalty + temp_penalty
        )

        return ConsumptionResult(
            prediction_kwh=round(prediction, 2), message=ResponseSignal.SUCCESS.value
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{ResponseSignal.ERROR.value}: {e}"
        )
