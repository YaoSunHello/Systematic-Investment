from __future__ import annotations

from pathlib import Path

from systrading.cli import main


def test_cli_run_smoke(tmp_path: Path, capsys) -> None:
    portfolio = tmp_path / "portfolio.yaml"
    portfolio.write_text(
        """
date: 2015-01-23
idm: 1.0
instruments:
  - symbol: TEST
    asset_class: equity
    currency: USD
    block_multiplier: 1
    price: 100
    fx_rate_instr_per_base: 1
    weight: 1.0
    combined_forecast: 10
    price_volatility: 1
    block_value: 1
""",
        encoding="utf-8",
    )
    main(["run", "--portfolio", str(portfolio), "--daily-cash-vol-target", "100"])
    out = capsys.readouterr().out
    assert "TEST: target=100" in out
    assert "trade=100" in out

