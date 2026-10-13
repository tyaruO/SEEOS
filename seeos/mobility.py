"""Mobility calculations for the SEEOS prototype."""

import math


def estimate_motion(
    mass_kg: float,
    slope_deg: float,
    distance_km: float,
    rolling_resistance_coefficient: float = 0.05,
    drivetrain_efficiency: float = 0.75,
):
    """Estimate power demand for a simple terrain traversal.

    The implementation intentionally uses a simplified physics model and is meant
    as an educational prototype, not a validated rover model.
    """
    if mass_kg <= 0:
        raise ValueError("mass_kg must be positive")
    if distance_km < 0:
        raise ValueError("distance_km must not be negative")
    if rolling_resistance_coefficient < 0:
        raise ValueError("rolling resistance coefficient must not be negative")
    if not 0 < drivetrain_efficiency <= 1:
        raise ValueError("drivetrain efficiency must be in (0, 1]")

    slope_rad = math.radians(slope_deg)
    gravity = 9.81

    slope_force_n = mass_kg * gravity * math.sin(slope_rad)
    rolling_force_n = (
        mass_kg * gravity * rolling_resistance_coefficient * math.cos(slope_rad)
    )
    total_force_n = slope_force_n + rolling_force_n

    # Assume a nominal 1-hour traversal over the supplied distance.
    speed_m_s = (distance_km * 1000.0) / 3600.0
    estimated_electrical_power_w = (total_force_n * speed_m_s) / drivetrain_efficiency

    return {
        "slope_force_n": slope_force_n,
        "rolling_force_n": rolling_force_n,
        "total_force_n": total_force_n,
        "estimated_electrical_power_w": max(estimated_electrical_power_w, 0.0),
    }
