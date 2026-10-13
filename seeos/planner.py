"""Planning score helpers for SEEOS."""


def route_score(time_s: float, energy_wh: float, risk_score: float, uncertainty_score: float) -> float:
    """Return a simple additive route score, lower is preferred."""
    return float(time_s + energy_wh + risk_score + uncertainty_score)
