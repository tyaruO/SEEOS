"""Data models for the SEEOS prototype."""

from dataclasses import dataclass


@dataclass
class Material:
    name: str
    density_kg_m3: float
    thermal_conductivity_w_mk: float
    specific_heat_j_kgk: float
    bearing_capacity_kpa: float

    def validate(self):
        if not self.name.strip():
            raise ValueError("material name must not be empty")

        for field in (
            "density_kg_m3",
            "thermal_conductivity_w_mk",
            "specific_heat_j_kgk",
            "bearing_capacity_kpa",
        ):
            if getattr(self, field) <= 0:
                raise ValueError(f"{field} must be positive")


@dataclass
class Vehicle:
    name: str
    mass_kg: float
    max_power_w: float
    rolling_resistance_coefficient: float = 0.05
    drivetrain_efficiency: float = 0.75

    def validate(self):
        if not self.name.strip():
            raise ValueError("vehicle name must not be empty")

        if self.mass_kg <= 0 or self.max_power_w <= 0:
            raise ValueError("mass and max_power must be positive")

        if self.rolling_resistance_coefficient < 0:
            raise ValueError("rolling resistance coefficient must not be negative")

        if not 0 < self.drivetrain_efficiency <= 1:
            raise ValueError("drivetrain efficiency must be in (0, 1]")


@dataclass
class CellState:
    cell_id: str
    slope_deg: float
    roughness_index: float
    temperature_c: float
    radiation_msv_h: float
    dust_index: float = 0.0
    rut_depth_m: float = 0.0

    def validate(self):
        if not self.cell_id.strip():
            raise ValueError("cell_id must not be empty")

        if not -90 <= self.slope_deg <= 90:
            raise ValueError("slope_deg must be between -90 and 90")

        for field in (
            "roughness_index",
            "radiation_msv_h",
            "dust_index",
            "rut_depth_m",
        ):
            if getattr(self, field) < 0:
                raise ValueError(f"{field} must not be negative")
