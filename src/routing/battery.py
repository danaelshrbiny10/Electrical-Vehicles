from models.car_model import CarInput
from models.battery_status import BatteryResult

def compute_battery_after_distance(car: CarInput, distance_km: float, start_soc_pct: float) -> BatteryResult:
    """
    Compute battery remaining after traveling a given distance.
    """
    energy_used = distance_km * car.efficiency_kwh_per_km
    battery_remaining_kwh = car.battery_kwh * (start_soc_pct/100) - energy_used
    battery_remaining_pct = max(0.0, (battery_remaining_kwh / car.battery_kwh) * 100)
    return BatteryResult(
        battery_remaining_kwh=battery_remaining_kwh,
        battery_remaining_percent=battery_remaining_pct,
        energy_used_kwh=energy_used,
        message="Success"
    )
