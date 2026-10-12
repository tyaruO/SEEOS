# SEEOS
宇宙予想

SEEOS/
├── README.md
├── requirements.txt
├── main.py
├── seeos/
│   ├── __init__.py
│   ├── models.py
│   ├── mobility.py
│   ├── environment_change.py
│   └── planner.py
└── tests/
    └── test_models_and_motion.py


# SEEOS — Subsurface Extreme Environment OS (prototype scaffold)

An educational prototype for integrating terrain, vehicle, material, and changing-environment variables into a simple planning score.

This is **not** a validated rover simulator, engineering design tool, or safety assessment. Models are intentionally simplified and require calibration against real measurements before serious use.

## Run
Requires Python 3.10+ and NumPy.

```bash
python -m pip install -r requirements.txt
python main.py

Current simplifications:
Mobility uses slope and a constant rolling-resistance coefficient.
Rut change is a caller-supplied illustrative increment, not a soil-mechanics prediction.
Temperature is a lumped first-order approximation, not a spatial heat-transfer solver.
Route scores depend on transparent, user-selected weights.



## 2. `requirements.txt`

```text
numpy>=1.24


from seeos.models import Material, Vehicle, CellState
from seeos.mobility import estimate_motion
from seeos.environment_change import (
    update_rut_depth,
    lumped_temperature_step
)
from seeos.planner import route_score


def main():
    soil = Material(
        "illustrative regolith",
        1600,
        0.25,
        800,
        35
    )

    rover = Vehicle(
        "demo rover",
        180,
        500,
        0.06,
        0.75
    )

    cell = CellState(
        "cell-001",
        12.0,
        0.25,
        -20.0,
        0.0,
        dust_index=0.2,
        rut_depth_m=0.01
    )

    soil.validate()
    rover.validate()
    cell.validate()

    motion = estimate_motion(
        rover.mass_kg,
        cell.slope_deg,
        0.5,
        rover.rolling_resistance_coefficient,
        rover.drivetrain_efficiency
    )

    new_rut = update_rut_depth(
        cell.rut_depth_m,
        illustrative_increment_m=0.002
    )

    next_temp = lumped_temperature_step(
        cell.temperature_c,
        ambient_c=-25,
        time_step_s=60,
        time_constant_s=600
    )

    score = route_score(
        time_s=120,
        energy_wh=motion["estimated_electrical_power_w"] / 30,
        risk_score=0.2,
        uncertainty_score=0.3
    )

    print("Material:", soil)
    print("Cell:", cell)
    print("Motion estimate:", motion)
    print("Illustrative next rut depth (m):", new_rut)
    print("Lumped next temperature (C):", next_temp)
    print("Illustrative route score (lower is preferred):", score)


if __name__ == "__main__":
    main()


"""SEEOS environment and mobility prototype."""

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
            "bearing_capacity_kpa"
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
            raise ValueError(
                "rolling resistance coefficient must not be negative"
            )

        if not 0 < self.drivetrain_efficiency <= 1:
            raise ValueError(
                "drivetrain efficiency must be in (0, 1]"
            )


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
            raise ValueError(
                "slope_deg must be between -90 and 90"
            )

        for field in (
            "roughness_index",
            "radiation_msv_h",
            "dust_index",
            "rut_depth_m"
        ):
            if getattr(self, field) < 0:
                raise ValueError(f"{field} must not be negative")


def update_rut_depth(
    current_depth_m: float,
    illustrative_increment_m: float
) -> float:
    """Apply a supplied illustrative rut increment; does not predict soil mechanics."""

    if current_depth_m < 0 or illustrative_increment_m < 0:
        raise ValueError(
            "rut depths and increments must not be negative"
        )

    return current_depth_m + illustrative_increment_m


def lumped_temperature_step(
    current_c: float,
    ambient_c: float,
    time_step_s: float,
    time_constant_s: float
) -> float:
    """First-order lumped temperature relaxation, not a spatial heat-transfer model."""

    if time_step_s < 0:
        raise ValueError("time_step_s must not be negative")

    if time_constant_s <= 0:
        raise ValueError("time_constant_s must be positive")

    fraction = 1.0 - __import__("math").exp(
        -time_step_s / time_constant_s
    )

    return current_c + (ambient_c - current_c) * fraction



import pytest
from seeos.mobility import estimate_motion
from seeos.environment_change import (
    update_rut_depth,
    lumped_temperature_step
)
from seeos.planner import route_score


def test_motion_positive_power_on_uphill():
    result = estimate_motion(100, 10, 1.0)
    assert result["estimated_electrical_power_w"] > 0


def test_rut_increment():
    assert update_rut_depth(0.01, 0.002) == pytest.approx(0.012)


def test_temperature_relaxes_toward_ambient():
    result = lumped_temperature_step(20, 0, 60, 600)
    assert 0 < result < 20


def test_route_score():
    assert route_score(1, 2, 3, 4) == 10





ACP-Lab / SEEOS ソースコード一式

このフォルダには、独立した2つのPythonプロジェクトが入っています。

1. ACP-Lab：音響信号のサンプル解析・実験データ記録
2. SEEOS：地形・移動・環境変化の簡易モデル

iPhoneでの扱い方：
- 下のZIPを「ファイル」アプリに保存し、タップして解凍できます。
- 個々の .py / .md / .txt ファイルはソースコードです。タップして読むことはできますが、iPhone標準機能だけでは通常Pythonプログラムとして実行できません。
- 実行するにはPython実行環境が必要です（PC、または対応するオンライン開発環境など）。

注意：
これは研究開発用の初期プロトタイプです。医療機器・医療効果・音響安全性を検証したものではありません。SEEOSの計算も簡略化されており、実環境で検証済みの工学シミュレーターではありません。
