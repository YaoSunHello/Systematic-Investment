from systrading.core.forecasts.base import TradingRule, apply_scalar_and_cap, calibrate_forecast_scalar
from systrading.core.forecasts.carry import CarryRule
from systrading.core.forecasts.discretionary import DiscretionaryRule
from systrading.core.forecasts.ewmac import DEFAULT_FORECAST_SCALARS, EWMACRule
from systrading.core.forecasts.norule import NoRule

__all__ = [
    "TradingRule",
    "apply_scalar_and_cap",
    "calibrate_forecast_scalar",
    "CarryRule",
    "DiscretionaryRule",
    "DEFAULT_FORECAST_SCALARS",
    "EWMACRule",
    "NoRule",
]

