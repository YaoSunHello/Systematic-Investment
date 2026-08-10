from __future__ import annotations

import pandas as pd

from systrading.core.forecasts.base import TradingRule, apply_scalar_and_cap
from systrading.core.models import Forecast, Instrument, MarketSnapshot
from systrading.core.volatility import price_volatility


DEFAULT_FORECAST_SCALARS = {
    (2, 8): 10.6,
    (4, 16): 7.5,
    (8, 32): 5.3,
    (16, 64): 3.75,
    (32, 128): 2.65,
    (64, 256): 1.87,
}


class EWMACRule(TradingRule):
    def __init__(
        self,
        fast: int,
        slow: int,
        forecast_scalar: float | None = None,
        cap: float = 20.0,
        vol_method: str = "ewma",
        vol_lookback: int = 36,
    ) -> None:
        if slow != fast * 4:
            raise ValueError("EWMAC slow span must equal 4 * fast span")
        self.fast = fast
        self.slow = slow
        self.forecast_scalar = forecast_scalar or DEFAULT_FORECAST_SCALARS[(fast, slow)]
        self.cap = cap
        self.vol_method = vol_method
        self.vol_lookback = vol_lookback
        self.rule_id = f"ewmac_{fast}_{slow}"

    def forecast(self, snapshot: MarketSnapshot, instrument: Instrument) -> Forecast:
        prices = pd.Series(snapshot.price_history, dtype="float64").dropna()
        if len(prices) < self.slow:
            raise ValueError(f"{self.rule_id} requires at least {self.slow} prices")
        fast_ewma = prices.ewm(span=self.fast, adjust=False).mean().iloc[-1]
        slow_ewma = prices.ewm(span=self.slow, adjust=False).mean().iloc[-1]
        raw_crossover = float(fast_ewma - slow_ewma)
        vol_pct = price_volatility(prices, method=self.vol_method, lookback=self.vol_lookback)
        price_vol_points = (vol_pct / 100.0) * float(snapshot.price)
        if price_vol_points <= 0:
            raise ValueError("price volatility in points must be positive")
        vol_adjusted = raw_crossover / price_vol_points
        value = apply_scalar_and_cap(
            vol_adjusted,
            self.forecast_scalar,
            cap=self.cap,
            long_only=instrument.tradeable_long_only,
        )
        return Forecast(rule_id=self.rule_id, value=value)

