from fastapi import HTTPException
from models.battery import BatteryInput, BatteryResult


class BatteryController:

    def compute_remaining_battery(self, req: BatteryInput) -> BatteryResult:
        try:
            # extract car dict
            car = req.car

            battery_kwh = float(car.get("battery_kwh", 0))
            eff_kwh_per_km = float(car.get("efficiency_kwh_per_km", 0))

            if battery_kwh <= 0 or eff_kwh_per_km <= 0:
                raise ValueError("Invalid car specifications")

            # energy usage
            energy_used = req.distance_km * eff_kwh_per_km

            # starting battery
            start_kwh = (req.start_soc_pct / 100.0) * battery_kwh

            # remaining
            remaining_kwh = start_kwh - energy_used
            remaining_pct = (
                (remaining_kwh / battery_kwh) * 100 if battery_kwh > 0 else 0
            )

            if remaining_kwh < 0:
                remaining_kwh = 0
                remaining_pct = 0

            return BatteryResult(
                battery_remaining_kwh=round(remaining_kwh, 2),
                battery_remaining_percent=round(remaining_pct, 2),
                energy_used_kwh=round(energy_used, 2),
                message="Battery calculation successful",
            )

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Battery calculation error: {e}"
            )
