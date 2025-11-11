from infer.manager import ModelManager
import math
from models.enums.ResponseEnums import ResponseSignal

mgr = ModelManager()


class SimulateController:
    def simulate(
        self,
        car: dict,
        start: list,
        end: list,
        start_soc: float,
        target_arrival_soc: float,
    ):
        # haversine distance
        lat1, lon1 = start
        lat2, lon2 = end
        R = 6371.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_km = R * c

        # Use ML model for prediction
        energy = mgr.predict_consumption(
            distance=float(distance_km),
            speed=80.0,
            temp=25.0,
            ac=0,
            heater=0,
            payload=100.0,
            battery_kwh=car["battery_kwh"],
            eff=car["efficiency_kwh_per_km"],
        )
        battery_remaining_kwh = max(
            car["battery_kwh"] * (start_soc / 100.0) - energy, 0.0
        )
        battery_remaining_pct = (battery_remaining_kwh / car["battery_kwh"]) * 100.0
        needs_charge = battery_remaining_pct < target_arrival_soc

        return {
            "distance_km": round(distance_km, 3),
            "energy_needed_kwh": round(energy, 3),
            "battery_remaining_kwh": round(battery_remaining_kwh, 3),
            "battery_remaining_percent": round(battery_remaining_pct, 2),
            "needs_charge": needs_charge,
            "message": ResponseSignal.SUCCESS.value,
        }
