"""Environment and terrain change functions for SEEOS."""

import math


def update_rut_depth(
    current_depth_m: float,
    illustrative_increment_m: float,
) -> float:
    """Apply a supplied illustrative rut increment; does not predict soil mechanics."""
    if current_depth_m < 0 or illustrative_increment_m < 0:
        raise ValueError("rut depths and increments must not be negative")

    return current_depth_m + illustrative_increment_m


def lumped_temperature_step(
    current_c: float,
    ambient_c: float,
    time_step_s: float,
    time_constant_s: float,
) -> float:
    """First-order lumped temperature relaxation, not a spatial heat-transfer model."""
    if time_step_s < 0:
        raise ValueError("time_step_s must not be negative")

    if time_constant_s <= 0:
        raise ValueError("time_constant_s must be positive")

    fraction = 1.0 - math.exp(-time_step_s / time_constant_s)
    return current_c + (ambient_c - current_c) * fraction
