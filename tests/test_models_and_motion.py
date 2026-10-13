import pytest

from seeos.environment_change import lumped_temperature_step, update_rut_depth
from seeos.mobility import estimate_motion
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
