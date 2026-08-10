from __future__ import annotations

from systrading.core.forecasts.base import TradingRule
from systrading.core.models import Forecast, Instrument, MarketSnapshot


VERBAL_SCALE = {
    "very-strong-sell": -20.0,
    "strong-sell": -15.0,
    "sell": -10.0,
    "weak-sell": -5.0,
    "neutral": 0.0,
    "weak-buy": 5.0,
    "buy": 10.0,
    "strong-buy": 15.0,
    "very-strong-buy": 20.0,
}


class DiscretionaryRule(TradingRule):
    rule_id = "discretionary"

    def __init__(self, forecast_value: float | str) -> None:
        if isinstance(forecast_value, str):
            key = forecast_value.strip().lower()
            if key not in VERBAL_SCALE:
                raise ValueError(f"unknown discretionary forecast: {forecast_value}")
            value = VERBAL_SCALE[key]
        else:
            value = float(forecast_value)
        if value < -20.0 or value > 20.0:
            raise ValueError("discretionary forecast must be in [-20, 20]")
        self.value = value

    def forecast(self, snapshot: MarketSnapshot, instrument: Instrument) -> Forecast:
        value = max(self.value, 0.0) if instrument.tradeable_long_only else self.value
        return Forecast(rule_id=self.rule_id, value=value)

