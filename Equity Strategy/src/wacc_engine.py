from src.models import HistoricalYear, MarketInputs, WaccResult


def calculate_wacc(market: MarketInputs, latest: HistoricalYear) -> WaccResult:
    equity_value = market.market_cap or market.current_share_price * latest.diluted_shares
    debt_value = latest.debt
    invested_capital = equity_value + debt_value
    if invested_capital <= 0:
        raise ValueError("Equity plus debt must be positive for WACC.")

    cost_of_equity = market.risk_free_rate + market.beta * market.equity_risk_premium
    after_tax_cost_of_debt = market.pre_tax_cost_of_debt * (1 - market.marginal_tax_rate)
    equity_weight = equity_value / invested_capital
    debt_weight = debt_value / invested_capital
    wacc = equity_weight * cost_of_equity + debt_weight * after_tax_cost_of_debt
    return WaccResult(
        cost_of_equity=cost_of_equity,
        after_tax_cost_of_debt=after_tax_cost_of_debt,
        equity_weight=equity_weight,
        debt_weight=debt_weight,
        wacc=wacc,
    )

