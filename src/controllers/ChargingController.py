"""compute charging curve function implementation."""

from models.charging import ChargingCurveRequest, ChargingCurveResponse, CurvePoint


def compute_charging_curve(data: ChargingCurveRequest) -> ChargingCurveResponse:
    """Compute the charging curve based on current and target state of charge and charger power."""
    battery_capacity = 60
    soc_diff = (data.target_soc - data.current_soc) / 100
    energy_needed = battery_capacity * soc_diff

    time_hours = energy_needed / data.charger_power_kw
    time_minutes = round(time_hours * 60, 2)

    # Generate SOC curve
    curve = []
    step = max(time_minutes // 5, 1)

    for m in range(0, int(time_minutes) + 1, int(step)):
        """Linear interpolation for SOC at each time step."""
        soc = data.current_soc + (
            (m / time_minutes) * (data.target_soc - data.current_soc)
        )
        curve.append(CurvePoint(minute=m, soc=round(soc, 1)))

    curve.append(CurvePoint(minute=time_minutes, soc=data.target_soc))

    return ChargingCurveResponse(
        charging_time_minutes=time_minutes,
        energy_added_kwh=round(energy_needed, 2),
        curve_points=curve,
    )
