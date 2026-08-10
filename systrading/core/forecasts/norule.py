from __future__ import annotations

from systrading.core.forecasts.base import TradingRule
from systrading.core.models import Forecast, Instrument, MarketSnapshot


class NoRule(TradingRule):
    rule_id = "norule"

    def forecast(self, snapshot: MarketSnapshot, instrument: Instrument) -> Forecast:
        return Forecast(rule_id=self.rule_id, value=10.0)

