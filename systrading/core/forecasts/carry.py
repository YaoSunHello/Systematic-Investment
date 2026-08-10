from __future__ import annotations

from systrading.core.forecasts.base import TradingRule, apply_scalar_and_cap
from systrading.core.models import Forecast, Instrument, MarketSnapshot
from systrading.core.volatility import price_volatility


class CarryRule(TradingRule):
    rule_id = "carry"

    def __init__(
        self,
        forecast_scalar: float = 30.0,
        cap: float = 20.0,
        annualisation_factor: float = 16.0,
        vol_method: str = "ewma",
        vol_lookback: int = 36,
    ) -> None:
        self.forecast_scalar = forecast_scalar
        self.cap = cap
        self.annualisation_factor = annualisation_factor
        self.vol_method = vol_method
        self.vol_lookback = vol_lookback

    def net_expected_return_price_units(self, snapshot: MarketSnapshot, instrument: Instrument) -> float:
        extra = snapshot.extra
        price = float(snapshot.price)
        if "net_expected_return_price_units" in extra:
            return float(extra["net_expected_return_price_units"])
        if instrument.instrument_type == "future":
            years = float(extra["years_between_contracts"])
            if "nearer_price" in extra:
                return (price - float(extra["nearer_price"])) / years
            return (float(extra["next_price"]) - price) / years
        if instrument.instrument_type in {"equity", "equity_cfd"}:
            funding_key = "avg_funding_cost" if instrument.instrument_type == "equity_cfd" else "funding_cost"
            return (float(extra["dividend_yield"]) - float(extra[funding_key])) * price
        if instrument.instrument_type == "fx":
            return (float(extra["foreign_interest"]) - float(extra["domestic_funding"])) * price
        if instrument.instrument_type == "spread_bet":
            return (float(extra["spot_level"]) - float(extra["bet_level"])) / float(extra["time_to_maturity_years"])
        raise ValueError(f"carry not configured for instrument_type={instrument.instrument_type}")

    def forecast(self, snapshot: MarketSnapshot, instrument: Instrument) -> Forecast:
        sigma_points_daily = price_volatility(
            snapshot.price_history,
            method=self.vol_method,
            lookback=self.vol_lookback,
        ) / 100.0 * float(snapshot.price)
        sigma_points_annual = sigma_points_daily * self.annualisation_factor
        if sigma_points_annual <= 0:
            raise ValueError("annualized volatility in points must be positive")
        raw = self.net_expected_return_price_units(snapshot, instrument) / sigma_points_annual
        value = apply_scalar_and_cap(
            raw,
            self.forecast_scalar,
            cap=self.cap,
            long_only=instrument.tradeable_long_only,
        )
        return Forecast(rule_id=self.rule_id, value=value)

