from infer.manager import ModelManager
from models.ai_responses import ConsumptionInput, ConsumptionResult


class AiController:

    def __init__(self):
        self.model = ModelManager()

    def predict_consumption(self, req: ConsumptionInput) -> ConsumptionResult:
        """
        Wrapper that calls ModelManager mathematical prediction,
        then formats output in the response Pydantic model.
        """
        result = self.model.predict_consumption(
            distance=req.distance,
            speed=req.speed,
            temp=req.temp,
            ac=req.ac,
            heater=req.heater,
            payload=req.payload,
            battery_kwh=req.battery_kwh,
            eff=req.eff,
        )

        # result is a dict returned by ModelManager
        predicted_kwh = result["predicted_kwh"]

        return ConsumptionResult(
            prediction_kwh=predicted_kwh,
            message=f"Estimated consumption for {req.distance} km is {predicted_kwh} kWh.",
        )
