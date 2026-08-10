from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np

from systrading.core.models import Forecast, Instrument, MarketSnapshot


def apply_scalar_and_cap(
    raw: float,
    scalar: float,
    cap: float = 20.0,
    long_only: bool = False,
) -> float:
    lower = 0.0 if long_only else -cap
    return float(np.clip(raw * scalar, lower, cap))


def calibrate_forecast_scalar(raw_forecasts: Iterable[float], target_abs_value: float = 10.0) -> float:
    values = np.asarray(list(raw_forecasts), dtype=float)
    if values.size == 0:
        raise ValueError("raw_forecasts cannot be empty")
    mean_abs = float(np.nanmean(np.abs(values)))
    if mean_abs <= 0:
        raise ValueError("mean absolute raw forecast must be positive")
    return target_abs_value / mean_abs


class TradingRule(ABC):
    rule_id: str

    @abstractmethod
    def forecast(self, snapshot: MarketSnapshot, instrument: Instrument) -> Forecast:
        raise NotImplementedError

