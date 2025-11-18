import math
import pickle
import os


class ModelManager:

    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "models", "Saved", "battery.pkl"
        )

        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.model = None  # no dataset - use mathematical models

    # ------------------------------
    # Consumption prediction model
    # ------------------------------
    def predict_consumption(
        self, distance, speed, temp, ac, heater, payload, battery_kwh, eff
    ):
        """
        Mathematical EV consumption simulation:
        base consumption = distance * eff
        speed_factor increases linearly
        climate_factor based on AC/heater usage
        payload_factor increases consumption
        """
        base = distance * eff

        speed_factor = base * (0.015 * (speed - 70))  # extra per km/h above 70
        climate_factor = base * (0.05 * ac + 0.04 * heater)
        payload_factor = base * (payload / 1000)

        predicted = base + speed_factor + climate_factor + payload_factor
        predicted_kwh = round(predicted, 2)

        return {
            "predicted_kwh": predicted_kwh,
            "remaining_after_trip": round(battery_kwh - predicted_kwh, 2),
            "energy_per_km": predicted_kwh / distance,
        }

    # ------------------------------
    # Charging curve simulation
    # ------------------------------
    def predict_charging_minutes(
        self, battery_kwh, max_charge_kw, station_power_kw, soc_from, soc_to
    ):
        """
        Mathematical curve: 0–80% full power, 80–100% slow rate.
        """
        usable_power = min(max_charge_kw, station_power_kw)

        energy_needed_kwh = battery_kwh * (soc_to - soc_from) / 100
        slow_zone = max(0, soc_to - 80)

        fast_zone_kwh = energy_needed_kwh - (battery_kwh * slow_zone / 100)
        slow_zone_kwh = battery_kwh * slow_zone / 100

        fast_time = (fast_zone_kwh / usable_power) * 60
        slow_time = (slow_zone_kwh / (usable_power * 0.5)) * 60

        return {
            "minutes_total": round(fast_time + slow_time, 2),
            "fast_minutes": round(fast_time, 2),
            "slow_minutes": round(slow_time, 2),
            "kwh_added": round(energy_needed_kwh, 2),
        }
