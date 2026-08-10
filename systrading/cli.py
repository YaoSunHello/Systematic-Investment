from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from systrading.config import load_yaml
from systrading.core.forecasts.discretionary import DiscretionaryRule
from systrading.core.forecasts.norule import NoRule
from systrading.core.models import Instrument, MarketSnapshot
from systrading.core.costs import max_turnover, min_position_feasibility, standardised_cost
from systrading.pipeline import InstrumentRunConfig, run


def _read_positions(path: str | None) -> dict[str, float]:
    if not path:
        return {}
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        return {row["symbol"]: float(row["position"]) for row in csv.DictReader(f)}


def _portfolio_from_yaml(path: str) -> tuple[list[InstrumentRunConfig], dict[str, float], list[list[float]], float | None]:
    data = load_yaml(path)
    configs: list[InstrumentRunConfig] = []
    weights: dict[str, float] = {}
    for item in data["instruments"]:
        inst = Instrument(
            symbol=item["symbol"],
            asset_class=item.get("asset_class", "unknown"),
            currency=item.get("currency", "USD"),
            block_multiplier=float(item.get("block_multiplier", 1.0)),
            min_block=float(item.get("min_block", 1.0)),
            tradeable_long_only=bool(item.get("tradeable_long_only", False)),
            instrument_type=item.get("instrument_type", "equity"),
        )
        history = pd.Series(item.get("price_history", [item["price"] * 0.99, item["price"]]))
        snapshot = MarketSnapshot(
            date=date.fromisoformat(str(data["date"])),
            price=float(item["price"]),
            price_history=history,
            fx_rate_instr_per_base=float(item.get("fx_rate_instr_per_base", 1.0)),
            extra=item.get("extra", {}),
        )
        rule_cfg = item.get("rule", {"type": "norule"})
        if rule_cfg["type"] == "discretionary":
            rules = (DiscretionaryRule(rule_cfg["forecast"]),)
        elif rule_cfg["type"] == "norule":
            rules = (NoRule(),)
        else:
            raise ValueError(f"CLI portfolio loader does not support rule type {rule_cfg['type']}")
        configs.append(
            InstrumentRunConfig(
                instrument=inst,
                snapshot=snapshot,
                rules=rules,
                combined_forecast_override=item.get("combined_forecast"),
                price_volatility_override=item.get("price_volatility"),
                block_value_override=item.get("block_value"),
            )
        )
        weights[inst.symbol] = float(item["weight"])
    corr = data.get("corr", np.eye(len(configs)).tolist())
    return configs, weights, corr, data.get("idm")


def run_command(args: argparse.Namespace) -> None:
    configs, weights, corr, idm = _portfolio_from_yaml(args.portfolio)
    current = _read_positions(args.positions)
    result = run(
        portfolio=configs,
        daily_cash_vol_target=float(args.daily_cash_vol_target),
        instrument_weights=weights,
        date_=configs[0].snapshot.date,
        current_positions=current,
        corr=corr,
        idm=idm,
    )
    for symbol, row in result.per_instrument.items():
        print(
            f"{symbol}: target={row['rounded_target']:.0f} current={row['current_position']:.0f} "
            f"trade={row['trade']:.0f} unrounded={row['portfolio_position']:.4f}"
        )


def costs_command(args: argparse.Namespace) -> None:
    data = load_yaml(args.portfolio)
    speed_limit = float(data.get("speed_limit_sr", 0.13))
    for item in data["instruments"]:
        icv = float(item["instrument_ccy_vol"])
        cost = standardised_cost(float(item["cost_per_block"]), icv)
        headroom = max_turnover(speed_limit, cost)
        feas = min_position_feasibility(
            float(item["volatility_scalar"]),
            float(item["weight"]),
            float(data.get("idm", 1.0)),
            persona=data.get("persona", "staunch"),
        )
        print(f"{item['symbol']}: cost={cost:.4f} max_turnover={headroom:.1f} feasibility={feas.level} {feas.max_feasible_position:.2f}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="systrading", description="Carver-style systematic trading decision engine")
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--portfolio", required=True)
    run_parser.add_argument("--date")
    run_parser.add_argument("--positions")
    run_parser.add_argument("--daily-cash-vol-target", type=float, required=True)
    run_parser.set_defaults(func=run_command)
    costs_parser = sub.add_parser("costs")
    costs_parser.add_argument("--portfolio", required=True)
    costs_parser.set_defaults(func=costs_command)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

