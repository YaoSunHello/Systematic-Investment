from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class Instrument:
    symbol: str
    asset_class: str
    currency: str
    block_multiplier: float
    min_block: float = 1.0
    tradeable_long_only: bool = False
    instrument_type: str = "equity"


@dataclass(frozen=True)
class MarketSnapshot:
    date: date
    price: float
    price_history: pd.Series
    fx_rate_instr_per_base: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Forecast:
    rule_id: str
    value: float


@dataclass(frozen=True)
class VolTarget:
    trading_capital: float
    percentage_vol_target: float
    annualised_cash_vol_target: float
    daily_cash_vol_target: float


@dataclass(frozen=True)
class SubsystemResult:
    symbol: str
    combined_forecast: float
    price_volatility: float
    block_value: float
    instrument_ccy_vol: float
    instrument_value_vol: float
    volatility_scalar: float
    subsystem_position: float
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PortfolioResult:
    date: date
    per_instrument: dict[str, dict[str, Any]]

