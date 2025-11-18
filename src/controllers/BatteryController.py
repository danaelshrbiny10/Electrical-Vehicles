"""calculate battery status based on distance traveled and initial battery percentage."""

from models.battery import BatteryStatusRequest, BatteryStatusResponse


def calculate_battery_status(data: BatteryStatusRequest) -> BatteryStatusResponse:
    """Calculate remaining battery percentage and energy used."""
    consumption = 16.0  # kWh/100km
    used_energy = (data.distance_km / 100) * consumption

    raw_remaining = data.battery_percentage - (used_energy / 0.7)
    remaining_int = max(int(raw_remaining), 0)

    return BatteryStatusResponse(
        remaining_battery_percentage=remaining_int,
        energy_used_kwh=round(used_energy, 2),
    )
