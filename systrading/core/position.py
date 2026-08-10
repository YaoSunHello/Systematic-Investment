from __future__ import annotations

from systrading.core.models import Instrument, SubsystemResult


def block_value(instrument: Instrument, price: float, extra: dict | None = None) -> float:
    extra = extra or {}
    if instrument.instrument_type == "eurodollar_future":
        notional = float(extra.get("notional", 1_000_000.0))
        tenor = float(extra.get("tenor_years", 0.25))
        return notional * 0.01 * tenor
    return float(instrument.block_multiplier) * float(price) * 0.01


def subsystem_position(
    symbol: str,
    combined_forecast: float,
    price_volatility_pct: float,
    block_value_instr_ccy: float,
    fx_rate_instr_per_base: float,
    daily_cash_vol_target: float,
) -> SubsystemResult:
    if price_volatility_pct <= 0:
        raise ValueError("price_volatility_pct must be positive")
    if block_value_instr_ccy <= 0:
        raise ValueError("block_value_instr_ccy must be positive")
    if fx_rate_instr_per_base <= 0:
        raise ValueError("fx_rate_instr_per_base must be positive")
    instrument_ccy_vol = float(block_value_instr_ccy) * float(price_volatility_pct)
    instrument_value_vol = instrument_ccy_vol * float(fx_rate_instr_per_base)
    volatility_scalar = float(daily_cash_vol_target) / instrument_value_vol
    position = (float(combined_forecast) * volatility_scalar) / 10.0
    return SubsystemResult(
        symbol=symbol,
        combined_forecast=float(combined_forecast),
        price_volatility=float(price_volatility_pct),
        block_value=float(block_value_instr_ccy),
        instrument_ccy_vol=instrument_ccy_vol,
        instrument_value_vol=instrument_value_vol,
        volatility_scalar=volatility_scalar,
        subsystem_position=position,
        diagnostics={
            "percent_convention": "price_volatility is number-of-percent",
            "fx_direction": "instrument currency per base currency multiplier",
        },
    )

