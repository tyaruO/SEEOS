"""Demonstration entry point for SEEOS."""

from seeos.environment_change import lumped_temperature_step, update_rut_depth
from seeos.models import CellState, Material, Vehicle
from seeos.mobility import estimate_motion
from seeos.planner import route_score


def main():
    soil = Material(
        "illustrative regolith",
        1600,
        0.25,
        800,
        35,
    )

    rover = Vehicle(
        "demo rover",
        180,
        500,
        0.06,
        0.75,
    )

    cell = CellState(
        "cell-001",
        12.0,
        0.25,
        -20.0,
        0.0,
        dust_index=0.2,
        rut_depth_m=0.01,
    )

    soil.validate()
    rover.validate()
    cell.validate()

    motion = estimate_motion(
        rover.mass_kg,
        cell.slope_deg,
        0.5,
        rover.rolling_resistance_coefficient,
        rover.drivetrain_efficiency,
    )

    new_rut = update_rut_depth(
        cell.rut_depth_m,
        illustrative_increment_m=0.002,
    )

    next_temp = lumped_temperature_step(
        cell.temperature_c,
        ambient_c=-25,
        time_step_s=60,
        time_constant_s=600,
    )

    score = route_score(
        time_s=120,
        energy_wh=motion["estimated_electrical_power_w"] / 30,
        risk_score=0.2,
        uncertainty_score=0.3,
    )

    print("Material:", soil)
    print("Cell:", cell)
    print("Motion estimate:", motion)
    print("Illustrative next rut depth (m):", new_rut)
    print("Lumped next temperature (C):", next_temp)
    print("Illustrative route score (lower is preferred):", score)


if __name__ == "__main__":
    main()
