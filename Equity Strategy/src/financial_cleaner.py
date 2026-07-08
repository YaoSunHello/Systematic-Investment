from src.models import CleanedFinancials, HistoricalYear


def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def clean_historical_financials(history: list[HistoricalYear]) -> CleanedFinancials:
    if len(history) < 2:
        raise ValueError("At least two historical years are required.")

    sorted_history = sorted(history, key=lambda item: item.year)
    ratios: dict[str, list[float | None]] = {
        "revenue_growth": [],
        "ebit_margin": [],
        "effective_tax_rate": [],
        "capex_to_sales": [],
        "da_to_sales": [],
        "nwc_to_sales": [],
        "fcff": [],
    }

    previous_revenue: float | None = None
    previous_nwc: float | None = None
    for row in sorted_history:
        ratios["revenue_growth"].append(
            None if previous_revenue is None else safe_divide(row.revenue, previous_revenue) - 1
        )
        ratios["ebit_margin"].append(safe_divide(row.ebit, row.revenue))
        ratios["effective_tax_rate"].append(safe_divide(row.tax_expense, row.pretax_income))
        ratios["capex_to_sales"].append(safe_divide(row.capex, row.revenue))
        ratios["da_to_sales"].append(safe_divide(row.depreciation_amortisation, row.revenue))
        ratios["nwc_to_sales"].append(safe_divide(row.net_working_capital, row.revenue))

        tax_rate = safe_divide(row.tax_expense, row.pretax_income) or 0.0
        change_in_nwc = 0.0 if previous_nwc is None else row.net_working_capital - previous_nwc
        fcff = row.ebit * (1 - tax_rate) + row.depreciation_amortisation - row.capex - change_in_nwc
        ratios["fcff"].append(fcff)

        previous_revenue = row.revenue
        previous_nwc = row.net_working_capital

    return CleanedFinancials(history=sorted_history, ratios=ratios, latest=sorted_history[-1])


def data_quality_flags(cleaned: CleanedFinancials) -> list[str]:
    flags: list[str] = []
    history = cleaned.history
    if len(history) < 5:
        flags.append("Historical financial data covers fewer than 5 years.")
    for row in history:
        if row.revenue <= 0:
            flags.append(f"Revenue is not positive in {row.year}.")
        if row.cash < 0:
            flags.append(f"Cash is negative in {row.year}.")
        if row.debt < 0:
            flags.append(f"Debt is negative in {row.year}.")
        if row.depreciation_amortisation < 0:
            flags.append(f"D&A is negative in {row.year}.")
        if row.diluted_shares <= 0:
            flags.append(f"Diluted shares are not positive in {row.year}.")

    growth = cleaned.ratios["revenue_growth"]
    for row, rate in zip(history, growth, strict=True):
        if rate is not None and (rate > 0.50 or rate < -0.30):
            flags.append(f"Revenue growth in {row.year} is outside the normal validation range.")

    margins = cleaned.ratios["ebit_margin"]
    for previous, current, row in zip(margins, margins[1:], history[1:], strict=False):
        if previous is not None and current is not None and abs(current - previous) > 0.10:
            flags.append(f"EBIT margin changed by more than 10 percentage points in {row.year}.")

    for previous, current in zip(history, history[1:], strict=False):
        if previous.diluted_shares > 0:
            change = current.diluted_shares / previous.diluted_shares - 1
            if abs(change) > 0.20:
                flags.append(f"Diluted shares changed by more than 20% in {current.year}.")
    return flags

