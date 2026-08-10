from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class VolatilityConfig:
    method: str = "ewma"
    sma_lookback_days: int = 25
    ewma_lookback_days: int = 36
    suspicious_low_vol_pct: float = 0.05


def ewma_lambda(span: int) -> float:
    if span <= 0:
        raise ValueError("span must be positive")
    return 2.0 / (1.0 + span)


def percentage_returns(price_history: pd.Series) -> pd.Series:
    prices = pd.Series(price_history, dtype="float64").dropna()
    if len(prices) < 2:
        raise ValueError("price_history must contain at least two observations")
    return prices.pct_change().dropna()


def price_volatility(
    price_history: pd.Series,
    method: str = "ewma",
    lookback: int | None = None,
    suspicious_low_vol_pct: float | None = None,
) -> float:
    """Daily volatility of percent returns, returned as number-of-percent.

    Example: a 1.33% daily sigma is returned as 1.33, not 0.0133.
    """
    returns = percentage_returns(price_history)
    method = method.lower()
    if method == "sma":
        window = lookback or 25
        if len(returns) < window:
            sigma = returns.std(ddof=1)
        else:
            sigma = returns.rolling(window).std(ddof=1).iloc[-1]
    elif method == "ewma":
        span = lookback or 36
        lam = ewma_lambda(span)
        variance = float(returns.iloc[0] ** 2)
        for value in returns.iloc[1:]:
            variance = lam * float(value * value) + (1.0 - lam) * variance
        sigma = math.sqrt(variance)
    else:
        raise ValueError(f"unsupported volatility method: {method}")
    pct = float(sigma) * 100.0
    if suspicious_low_vol_pct is not None and pct < suspicious_low_vol_pct:
        raise ValueError(f"suspiciously low volatility: {pct:.4f}%")
    return pct

