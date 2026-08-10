from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import pytest

from systrading.config import load_defaults
from systrading.core.combine import combine_forecasts
from systrading.core.costs import min_position_feasibility, standardised_cost
from systrading.core.diversification import div_multiplier, table18_approx_multiplier
from systrading.core.forecasts.carry import CarryRule
from systrading.core.forecasts.ewmac import DEFAULT_FORECAST_SCALARS
from systrading.core.handcraft import handcraft, three_asset_table8_weights
from systrading.core.models import Forecast, Instrument, MarketSnapshot
from systrading.core.position import subsystem_position
from systrading.core.volatility import ewma_lambda, price_volatility
from systrading.pipeline import InstrumentRunConfig, run


def assert_rel(actual: float, expected: float, tolerance: float = 0.005) -> None:
    assert actual == pytest.approx(expected, rel=tolerance)


def test_gt1_subsystem_position_sizing() -> None:
    result = subsystem_position(
        symbol="WTI",
        combined_forecast=-6.0,
        price_volatility_pct=1.33,
        block_value_instr_ccy=750.0,
        fx_rate_instr_per_base=0.67,
        daily_cash_vol_target=62_500.0,
    )
    assert_rel(result.instrument_ccy_vol, 997.50)
    assert_rel(result.instrument_value_vol, 668.325)
    assert_rel(result.volatility_scalar, 93.52)
    assert_rel(result.subsystem_position, -56.11)


def test_gt2_full_three_asset_portfolio() -> None:
    asof = date(2015, 1, 23)
    prices = pd.Series([100.0, 101.0])
    instruments = [
        InstrumentRunConfig(
            Instrument("US20Y", "bond", "USD", 1.0),
            MarketSnapshot(asof, 100.0, prices, 0.88),
            combined_forecast_override=10.0,
            price_volatility_override=0.52,
            block_value_override=1500.0,
        ),
        InstrumentRunConfig(
            Instrument("SP500", "equity", "USD", 1.0),
            MarketSnapshot(asof, 100.0, prices, 0.88),
            combined_forecast_override=-10.0,
            # SPEC-NOTE: The book displays 0.84% and $1145, but the stated ICV
            # is $956. Use the unrounded volatility implied by the worked row.
            price_volatility_override=956.0 / 1145.0,
            block_value_override=1145.0,
        ),
        InstrumentRunConfig(
            Instrument("NASDAQ", "equity", "USD", 1.0),
            MarketSnapshot(asof, 100.0, prices, 0.88),
            combined_forecast_override=-15.0,
            price_volatility_override=0.87,
            block_value_override=880.0,
        ),
    ]
    result = run(
        instruments,
        daily_cash_vol_target=6_250.0,
        instrument_weights={"US20Y": 0.50, "SP500": 0.25, "NASDAQ": 0.25},
        date_=asof,
        current_positions={"US20Y": 4, "SP500": -2, "NASDAQ": -5},
        corr=np.eye(3),
        idm=1.41,
    )
    bond = result.per_instrument["US20Y"]
    sp = result.per_instrument["SP500"]
    nasdaq = result.per_instrument["NASDAQ"]
    assert_rel(bond["subsystem"].instrument_ccy_vol, 780.0)
    assert_rel(bond["subsystem"].instrument_value_vol, 686.0)
    assert_rel(bond["subsystem"].volatility_scalar, 9.11)
    assert_rel(bond["subsystem_position"], 9.11)
    assert_rel(bond["portfolio_position"], 6.42)
    assert bond["rounded_target"] == 6
    assert bond["trade"] == 2
    assert_rel(sp["subsystem"].instrument_ccy_vol, 956.0)
    assert_rel(sp["subsystem"].instrument_value_vol, 841.0)
    assert_rel(sp["subsystem"].volatility_scalar, 7.43)
    assert_rel(sp["subsystem_position"], -7.43)
    assert_rel(sp["portfolio_position"], -2.62)
    assert sp["rounded_target"] == -3
    assert sp["trade"] == -1
    assert_rel(nasdaq["subsystem"].instrument_ccy_vol, 766.0)
    assert_rel(nasdaq["subsystem"].instrument_value_vol, 674.0)
    assert_rel(nasdaq["subsystem"].volatility_scalar, 9.28)
    assert_rel(nasdaq["subsystem_position"], -13.9)
    assert_rel(nasdaq["portfolio_position"], -4.91)
    assert nasdaq["rounded_target"] == -5
    assert nasdaq["trade"] == 0


def test_gt3_combine_forecasts() -> None:
    combined, diag = combine_forecasts(
        [Forecast("ewmac", 15), Forecast("carry", -10)],
        weights=[0.5, 0.5],
        corr=[[1.0, 1.0], [1.0, 1.0]],
    )
    assert combined == pytest.approx(2.5)
    assert diag["raw_combined"] == pytest.approx(2.5)
    capped, _ = combine_forecasts(
        [Forecast("a", 16), Forecast("b", 16)],
        weights=[0.5, 0.5],
        corr=[[1.0, -0.5555555556], [-0.5555555556, 1.0]],
        fdm_cap=1.5,
    )
    assert capped == 20.0
    corr = np.full((4, 4), 0.5)
    np.fill_diagonal(corr, 1.0)
    precise = div_multiplier([0.25, 0.25, 0.25, 0.25], corr)
    approx = table18_approx_multiplier(4, 0.5)
    assert precise == pytest.approx(1.2649, rel=0.01)
    assert approx == pytest.approx(1.2649, rel=0.01)


def test_gt4_diversification_multiplier_two_assets() -> None:
    weights = [0.5, 0.5]
    assert div_multiplier(weights, [[1, 1], [1, 1]]) == pytest.approx(1.00)
    assert div_multiplier(weights, [[1, 0.5], [0.5, 1]]) == pytest.approx(1.1547, rel=0.005)
    assert table18_approx_multiplier(2, 0.0) == pytest.approx(1.4142, rel=0.005)


def test_gt5_standardised_costs() -> None:
    assert standardised_cost(8, 506) == pytest.approx(0.0020, abs=0.00005)
    assert standardised_cost(4, 49.50) == pytest.approx(0.0101, rel=0.01)
    assert standardised_cost(40, 62) == pytest.approx(0.0806, rel=0.01)


def test_gt6_min_position_feasibility() -> None:
    result = min_position_feasibility(1.49, 0.25, 1.41)
    assert result.max_feasible_position == pytest.approx(1.05, rel=0.005)
    assert result.level == "warn"
    concentrated = min_position_feasibility(1.49, 1.00, 1.00)
    assert concentrated.max_feasible_position == pytest.approx(2.98, rel=0.005)
    assert concentrated.level == "warn"


def test_gt7_handcrafting() -> None:
    grouped = handcraft({"bond": ["US20Y"], "equities": ["SP500", "NASDAQ"]})
    assert grouped == {"US20Y": 0.50, "SP500": 0.25, "NASDAQ": 0.25}
    assert three_asset_table8_weights(0.0, 0.9, 0.0) == pytest.approx((0.27, 0.46, 0.27))


def test_gt8_ewmac_scalars_and_volatility_defaults() -> None:
    assert ewma_lambda(36) == pytest.approx(2 / 37)
    assert DEFAULT_FORECAST_SCALARS[(2, 8)] == 10.6
    assert DEFAULT_FORECAST_SCALARS[(4, 16)] == 7.5
    assert DEFAULT_FORECAST_SCALARS[(8, 32)] == 5.3
    assert DEFAULT_FORECAST_SCALARS[(16, 64)] == 3.75
    assert DEFAULT_FORECAST_SCALARS[(32, 128)] == 2.65
    assert DEFAULT_FORECAST_SCALARS[(64, 256)] == 1.87
    assert CarryRule().forecast_scalar == 30
    defaults = load_defaults()
    assert defaults["volatility"]["ewma_lookback_days"] == 36


def test_no_lookahead_volatility_truncation() -> None:
    history = pd.Series([100, 101, 99, 102, 103, 102, 104], dtype=float)
    full_at_t = price_volatility(history.iloc[:5], method="ewma", lookback=36)
    truncated_at_t = price_volatility(history.iloc[:5], method="ewma", lookback=36)
    future_sensitive = price_volatility(history, method="ewma", lookback=36)
    assert full_at_t == truncated_at_t
    assert full_at_t != future_sensitive
