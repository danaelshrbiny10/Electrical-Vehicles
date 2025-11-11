from fastapi import HTTPException
from models.charging import ChargingCurveRequest, ChargingCurveResult
from models.enums.ResponseEnums import ResponseSignal


class ChargingController:

    def compute_charging_curve(self, req: ChargingCurveRequest) -> ChargingCurveResult:
        try:
            car = req.car
            battery_kwh = float(car.get("battery_kwh", 0))
            max_charge_kw = float(car.get("max_charge_kw", 0))

            if battery_kwh <= 0 or max_charge_kw <= 0:
                raise ValueError("Invalid car specifications")

            station_power = req.station_power_kw
            soc_from = req.soc_from_percent / 100.0
            soc_to = req.soc_to_percent / 100.0

            # linear approximation
            max_power = min(max_charge_kw, station_power)
            energy_needed = (soc_to - soc_from) * battery_kwh
            time_hours = energy_needed / max_power
            time_minutes = time_hours * 60

            # sample curve points
            steps = 10
            curve_points = [
                round((soc_from + (soc_to - soc_from) * i / steps) * 100, 2)
                for i in range(steps + 1)
            ]

            return ChargingCurveResult(
                soc_from=req.soc_from_percent,
                soc_to=req.soc_to_percent,
                estimated_minutes=round(time_minutes, 2),
                curve_points=curve_points,
                message=ResponseSignal.SUCCESS.value,
            )

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"{ResponseSignal.ERROR.value}: {e}"
            )
