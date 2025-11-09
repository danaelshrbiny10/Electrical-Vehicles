from models.car_model import CarInput
from models.simulate_models import SimulateResponse

def simulate_trip(start: tuple, end: tuple, car: CarInput, start_soc_pct: float, min_arrival_soc_pct: float, avg_speed_kmh: float = 90.0) -> dict:
    """
    Simulate route energy consumption and battery usage.
    """
    # Example simple distance calculation (replace with real routing later)
    distance_km = ((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5 * 111  # rough approx
    energy_needed_kwh = distance_km * car.efficiency_kwh_per_km
    battery_remaining_kwh = car.battery_kwh * (start_soc_pct/100) - energy_needed_kwh
    battery_remaining_pct = max(0.0, (battery_remaining_kwh / car.battery_kwh) * 100)
    needs_charge = battery_remaining_pct < min_arrival_soc_pct

    return {
        "distance_km": distance_km,
        "energy_needed_kwh": energy_needed_kwh,
        "battery_remaining_kwh": battery_remaining_kwh,
        "battery_remaining_percent": battery_remaining_pct,
        "needs_charge": needs_charge
    }
