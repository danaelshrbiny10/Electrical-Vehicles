"""simulate trip controller."""

from models.simulate import SimulationRequest, SimulationResponse


def simulate_trip(data: SimulationRequest) -> SimulationResponse:
    """Simulate a trip based on the provided data."""
    distance_km = 120.0  # mock distance
    avg_consumption = 15.8
    energy_used = (distance_km / 100) * avg_consumption

    # simple fake logic for charging
    needs_charging = data.car.current_battery_percentage < 50
    charges = 2 if needs_charging else 0

    return SimulationResponse(
        trip_time_minutes=95,
        avg_consumption_kwh_100km=avg_consumption,
        energy_used_kwh=energy_used,
        start=data.start,
        end=data.end,
        charges=needs_charging,
        number_of_charges=charges,
    )
