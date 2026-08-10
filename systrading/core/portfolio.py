from __future__ import annotations

from datetime import date
from typing import Iterable

import numpy as np

from systrading.core.diversification import div_multiplier
from systrading.core.models import PortfolioResult, SubsystemResult


def instrument_diversification_multiplier(
    weights: Iterable[float],
    corr: Iterable[Iterable[float]],
    cap: float = 2.5,
    floor_zero: bool = True,
    persona: str = "staunch",
    max_bets: float | None = None,
    avg_bets: float | None = None,
) -> float:
    if persona == "semi_auto":
        if not max_bets or not avg_bets or avg_bets <= 0:
            raise ValueError("semi_auto IDM requires max_bets and avg_bets")
        return min(float(max_bets) / float(avg_bets), cap)
    return div_multiplier(weights, corr, cap=cap, floor_zero=floor_zero)


def rounded_target_position(portfolio_position: float, min_block: float = 1.0) -> float:
    if min_block <= 0:
        raise ValueError("min_block must be positive")
    return round(float(portfolio_position) / min_block) * min_block


def trade_from_target(
    rounded_target: float,
    current_position: float,
    inertia_pct: float = 0.10,
) -> float:
    target = float(rounded_target)
    current = float(current_position)
    if target != 0.0 and abs(current - target) < float(inertia_pct) * abs(target):
        return 0.0
    return target - current


def portfolio_positions(
    asof: date,
    subsystem_results: dict[str, SubsystemResult],
    instrument_weights: dict[str, float],
    corr: Iterable[Iterable[float]],
    current_positions: dict[str, float] | None = None,
    min_blocks: dict[str, float] | None = None,
    idm: float | None = None,
    inertia_pct: float = 0.10,
    idm_cap: float = 2.5,
) -> PortfolioResult:
    current_positions = current_positions or {}
    min_blocks = min_blocks or {}
    symbols = list(subsystem_results)
    weights = np.asarray([instrument_weights[s] for s in symbols], dtype=float)
    if np.any(weights < 0) or not np.isclose(weights.sum(), 1.0):
        raise ValueError("instrument weights must be non-negative and sum to 1")
    resolved_idm = idm if idm is not None else instrument_diversification_multiplier(weights, corr, cap=idm_cap)
    per: dict[str, dict] = {}
    for symbol in symbols:
        result = subsystem_results[symbol]
        weight = float(instrument_weights[symbol])
        portfolio_position = result.subsystem_position * weight * float(resolved_idm)
        rounded = rounded_target_position(portfolio_position, min_blocks.get(symbol, 1.0))
        current = float(current_positions.get(symbol, 0.0))
        trade = trade_from_target(rounded, current, inertia_pct=inertia_pct)
        per[symbol] = {
            "subsystem_position": result.subsystem_position,
            "weight": weight,
            "idm": float(resolved_idm),
            "portfolio_position": portfolio_position,
            "rounded_target": rounded,
            "current_position": current,
            "trade": trade,
            "subsystem": result,
        }
    return PortfolioResult(date=asof, per_instrument=per)

