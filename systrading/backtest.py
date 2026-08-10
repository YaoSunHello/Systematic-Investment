from __future__ import annotations

from typing import Iterable

from systrading.core.models import PortfolioResult


def turnover_round_trips(results: Iterable[PortfolioResult]) -> dict[str, float]:
    totals: dict[str, float] = {}
    held: dict[str, list[float]] = {}
    for result in results:
        for symbol, row in result.per_instrument.items():
            totals[symbol] = totals.get(symbol, 0.0) + abs(float(row["trade"]))
            held.setdefault(symbol, []).append(abs(float(row["rounded_target"])))
    turnover: dict[str, float] = {}
    for symbol, traded in totals.items():
        avg_held = sum(held[symbol]) / max(len(held[symbol]), 1)
        turnover[symbol] = 0.0 if avg_held == 0.0 else traded / (2.0 * avg_held)
    return turnover

