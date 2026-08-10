from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeasibilityResult:
    max_feasible_position: float
    level: str
    message: str


def standardised_cost(cost_per_block: float, instrument_ccy_vol: float, annualisation_factor: float = 16.0) -> float:
    if instrument_ccy_vol <= 0:
        raise ValueError("instrument_ccy_vol must be positive")
    return (2.0 * float(cost_per_block)) / (float(annualisation_factor) * float(instrument_ccy_vol))


def max_turnover(speed_limit_sr: float, standardised_cost_sr: float) -> float:
    if standardised_cost_sr <= 0:
        raise ValueError("standardised_cost_sr must be positive")
    return float(speed_limit_sr) / float(standardised_cost_sr)


def cost_in_sr_per_year(standardised_cost_sr: float, turnover_round_trips_per_year: float) -> float:
    return float(standardised_cost_sr) * float(turnover_round_trips_per_year)


def min_position_feasibility(
    volatility_scalar: float,
    instrument_weight: float,
    idm: float,
    persona: str = "staunch",
    min_max_position_blocks: float = 4.0,
) -> FeasibilityResult:
    k = 1.0 if persona == "asset_allocator" else 2.0
    max_pos = k * float(volatility_scalar) * float(instrument_weight) * float(idm)
    if max_pos < 1.0:
        level = "error"
    elif max_pos < float(min_max_position_blocks):
        level = "warn"
    else:
        level = "ok"
    return FeasibilityResult(
        max_feasible_position=max_pos,
        level=level,
        message=f"max feasible position {max_pos:.2f} blocks is {level}",
    )

