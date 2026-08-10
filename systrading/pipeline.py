from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Mapping

import numpy as np

from systrading.core.combine import combine_forecasts
from systrading.core.forecasts.base import TradingRule
from systrading.core.models import Instrument, MarketSnapshot, PortfolioResult, SubsystemResult
from systrading.core.portfolio import portfolio_positions
from systrading.core.position import block_value, subsystem_position
from systrading.core.volatility import price_volatility


@dataclass(frozen=True)
class InstrumentRunConfig:
    instrument: Instrument
    snapshot: MarketSnapshot
    rules: tuple[TradingRule, ...] = field(default_factory=tuple)
    forecast_weights: tuple[float, ...] | None = None
    forecast_corr: tuple[tuple[float, ...], ...] | None = None
    combined_forecast_override: float | None = None
    price_volatility_override: float | None = None
    block_value_override: float | None = None


def run_subsystem(
    instrument_config: InstrumentRunConfig,
    daily_cash_vol_target: float,
    forecast_cap: float = 20.0,
    fdm_cap: float = 2.5,
) -> SubsystemResult:
    instrument = instrument_config.instrument
    snapshot = instrument_config.snapshot
    forecast_diagnostics: dict[str, object] = {}
    if instrument_config.combined_forecast_override is not None:
        combined = float(instrument_config.combined_forecast_override)
        forecast_diagnostics = {"combined_forecast_override": combined}
    else:
        forecasts = [rule.forecast(snapshot, instrument) for rule in instrument_config.rules]
        if not forecasts:
            raise ValueError(f"{instrument.symbol} has no rules and no forecast override")
        combined, forecast_diagnostics = combine_forecasts(
            forecasts,
            weights=instrument_config.forecast_weights,
            corr=instrument_config.forecast_corr,
            cap=forecast_cap,
            fdm_cap=fdm_cap,
        )
        forecast_diagnostics["forecasts"] = {forecast.rule_id: forecast.value for forecast in forecasts}

    vol_pct = (
        float(instrument_config.price_volatility_override)
        if instrument_config.price_volatility_override is not None
        else float(snapshot.extra.get("price_volatility", price_volatility(snapshot.price_history)))
    )
    block_val = (
        float(instrument_config.block_value_override)
        if instrument_config.block_value_override is not None
        else float(snapshot.extra.get("block_value", block_value(instrument, snapshot.price, snapshot.extra)))
    )
    result = subsystem_position(
        symbol=instrument.symbol,
        combined_forecast=combined,
        price_volatility_pct=vol_pct,
        block_value_instr_ccy=block_val,
        fx_rate_instr_per_base=snapshot.fx_rate_instr_per_base,
        daily_cash_vol_target=daily_cash_vol_target,
    )
    diagnostics = dict(result.diagnostics)
    diagnostics.update(forecast_diagnostics)
    return SubsystemResult(
        symbol=result.symbol,
        combined_forecast=result.combined_forecast,
        price_volatility=result.price_volatility,
        block_value=result.block_value,
        instrument_ccy_vol=result.instrument_ccy_vol,
        instrument_value_vol=result.instrument_value_vol,
        volatility_scalar=result.volatility_scalar,
        subsystem_position=result.subsystem_position,
        diagnostics=diagnostics,
    )


def run(
    portfolio: Iterable[InstrumentRunConfig],
    daily_cash_vol_target: float,
    instrument_weights: Mapping[str, float],
    date_: date,
    current_positions: Mapping[str, float] | None = None,
    corr: Iterable[Iterable[float]] | None = None,
    idm: float | None = None,
    inertia_pct: float = 0.10,
) -> PortfolioResult:
    configs = list(portfolio)
    subsystem_results = {
        config.instrument.symbol: run_subsystem(config, daily_cash_vol_target)
        for config in configs
    }
    symbols = list(subsystem_results)
    if corr is None:
        corr = np.eye(len(symbols))
    min_blocks = {config.instrument.symbol: config.instrument.min_block for config in configs}
    return portfolio_positions(
        asof=date_,
        subsystem_results=subsystem_results,
        instrument_weights=dict(instrument_weights),
        corr=corr,
        current_positions=dict(current_positions or {}),
        min_blocks=min_blocks,
        idm=idm,
        inertia_pct=inertia_pct,
    )

