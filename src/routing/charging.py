from typing import List
from models.car_model import CarInput

def estimate_charge_minutes_and_curve(vehicle: CarInput, station_power_kw: float, soc_from: float, soc_to: float) -> tuple[float, List[float]]:
    """
    Estimate charging time and generate charging curve points.
    """
    # Convert SOC to kWh
    battery_start = vehicle.battery_kwh * soc_from
    battery_end = vehicle.battery_kwh * soc_to

    # Effective charging power
    power_kw = min(station_power_kw, vehicle.max_charge_kw)
    energy_needed = battery_end - battery_start

    # Estimate minutes
    minutes = (energy_needed / power_kw) * 60 if power_kw > 0 else 0

    # Generate simple linear curve
    num_points = 10
    curve_points = [battery_start + i * (energy_needed/num_points) for i in range(1, num_points+1)]
    return minutes, curve_points
