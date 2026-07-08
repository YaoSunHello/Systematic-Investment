from src.financial_cleaner import clean_historical_financials, data_quality_flags
from src.forecast_engine import build_forecast
from src.models import ForecastAssumptions, ForecastYear, ValuationInput, ValuationResult
from src.recommendation import confidence_adjusted_recommendation, confidence_level
from src.wacc_engine import calculate_wacc


FINANCIAL_SECTOR_TERMS = {"bank", "banks", "insurance", "insurer", "financials", "asset manager"}


def calculate_dcf(input_data: ValuationInput) -> ValuationResult:
    cleaned = clean_historical_financials(input_data.history)
    forecast = build_forecast(cleaned, input_data.assumptions)
    wacc = calculate_wacc(input_data.market, cleaned.latest)
    return calculate_dcf_from_forecast(input_data, forecast, wacc.wacc)


def calculate_dcf_from_forecast(
    input_data: ValuationInput,
    forecast: list[ForecastYear],
    wacc: float,
    terminal_growth_rate: float | None = None,
) -> ValuationResult:
    cleaned = clean_historical_financials(input_data.history)
    wacc_result = calculate_wacc(input_data.market, cleaned.latest)
    wacc_result = wacc_result.__class__(
        cost_of_equity=wacc_result.cost_of_equity,
        after_tax_cost_of_debt=wacc_result.after_tax_cost_of_debt,
        equity_weight=wacc_result.equity_weight,
        debt_weight=wacc_result.debt_weight,
        wacc=wacc,
    )

    g = input_data.assumptions.terminal_growth_rate if terminal_growth_rate is None else terminal_growth_rate
    if wacc <= g:
        raise ValueError("WACC must be greater than terminal growth rate.")

    pv_fcff = [row.fcff / ((1 + wacc) ** index) for index, row in enumerate(forecast, start=1)]
    terminal_value = forecast[-1].fcff * (1 + g) / (wacc - g)
    pv_terminal_value = terminal_value / ((1 + wacc) ** len(forecast))
    enterprise_value = sum(pv_fcff) + pv_terminal_value

    latest = cleaned.latest
    equity_value = (
        enterprise_value
        - latest.debt
        + latest.cash
        - latest.minority_interest
        - latest.preferred_equity
        + latest.investments
    )
    fair_value_per_share = equity_value / latest.diluted_shares
    valuation_gap = fair_value_per_share / input_data.market.current_share_price - 1
    terminal_value_to_ev = pv_terminal_value / enterprise_value if enterprise_value else 0.0
    flags = validation_flags(input_data, forecast, wacc, g, terminal_value_to_ev)
    dq_flags = data_quality_flags(cleaned)
    score = confidence_score(input_data, cleaned.ratios["fcff"], terminal_value_to_ev, flags + dq_flags, wacc, g)
    level = confidence_level(score)
    recommendation = confidence_adjusted_recommendation(valuation_gap, level)
    limitations = limitation_statements(input_data, terminal_value_to_ev, flags + dq_flags)
    return ValuationResult(
        company=input_data.company,
        forecast=forecast,
        wacc=wacc_result,
        pv_fcff=pv_fcff,
        terminal_value=terminal_value,
        pv_terminal_value=pv_terminal_value,
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        fair_value_per_share=fair_value_per_share,
        valuation_gap=valuation_gap,
        recommendation=recommendation,
        confidence_score=score,
        confidence_level=level,
        terminal_value_to_ev=terminal_value_to_ev,
        limitations=limitations,
        flags=flags,
        data_quality_flags=dq_flags,
        metadata={"terminal_growth_rate": g},
    )


def validation_flags(
    input_data: ValuationInput,
    forecast: list[ForecastYear],
    wacc: float,
    terminal_growth_rate: float,
    terminal_value_to_ev: float,
) -> list[str]:
    flags: list[str] = []
    sector = input_data.company.sector.lower()
    company_type = input_data.company.company_type.lower()
    if any(term in sector or term in company_type for term in FINANCIAL_SECTOR_TERMS):
        flags.append("FCFF DCF is not suitable as the primary model for financial companies.")
    if terminal_value_to_ev > 0.85:
        flags.append("Terminal value exceeds 85% of enterprise value.")
    elif terminal_value_to_ev > 0.75:
        flags.append("Terminal value is above 75% of enterprise value.")
    if wacc - terminal_growth_rate < 0.02:
        flags.append("WACC minus terminal growth is below 2%, creating valuation instability.")
    if any(row.fcff < 0 for row in forecast):
        flags.append("Forecast FCFF is negative in at least one year.")
    if input_data.company.is_cyclical:
        flags.append("Company is marked cyclical; scenario analysis should be prioritised.")
    if input_data.company.high_share_based_compensation:
        flags.append("Stock-based compensation is material and should be reviewed separately.")
    if input_data.company.material_mna_or_one_offs:
        flags.append("M&A or one-off items may distort historical ratios.")
    return flags


def confidence_score(
    input_data: ValuationInput,
    historical_fcff: list[float | None],
    terminal_value_to_ev: float,
    flags: list[str],
    wacc: float,
    terminal_growth_rate: float,
) -> int:
    score = 50
    valid_fcff = [value for value in historical_fcff if value is not None]
    if valid_fcff and all(value > 0 for value in valid_fcff[-3:]):
        score += 20
    if len(input_data.history) >= 5:
        score += 10
    if terminal_value_to_ev < 0.70:
        score += 10
    if input_data.history[-1].debt < input_data.history[-1].cash + input_data.market.current_share_price * input_data.history[-1].diluted_shares:
        score += 10
    if input_data.company.is_cyclical:
        score -= 15
    if any(value is not None and value < 0 for value in historical_fcff):
        score -= 20
    if any("financial companies" in flag for flag in flags):
        score -= 25
    if input_data.company.high_share_based_compensation:
        score -= 10
    if wacc - terminal_growth_rate < 0.02:
        score -= 20
    if any("fewer than 5 years" in flag for flag in flags):
        score -= 15
    if terminal_value_to_ev > 0.80:
        score -= 10
    return max(0, min(100, score))


def limitation_statements(input_data: ValuationInput, terminal_value_to_ev: float, flags: list[str]) -> list[str]:
    company_type = input_data.company.company_type.lower()
    limitations = [
        f"Terminal value represents {terminal_value_to_ev:.1%} of enterprise value, so WACC and terminal growth are key model drivers.",
        "The framework uses public data and analyst assumptions; it is a decision-support model, not investment advice.",
    ]
    if "cyclical" in company_type or input_data.company.is_cyclical:
        limitations.append("For cyclical companies, current revenue and margins may not represent mid-cycle economics.")
    if "financial" in company_type or "bank" in input_data.company.sector.lower():
        limitations.append("FCFF is less meaningful for banks and insurers because debt is part of operating capital.")
    if "technology" in company_type or "platform" in company_type:
        limitations.append("For platform or technology companies, stock-based compensation, growth capex, and segment economics may require separate treatment.")
    if "early" in company_type or "high-growth" in company_type:
        limitations.append("High-growth or early-stage companies require scenario-weighted valuation because distant cash flows dominate value.")
    limitations.extend(flags)
    return list(dict.fromkeys(limitations))


def with_assumption_overrides(
    input_data: ValuationInput,
    revenue_growth_delta: float = 0.0,
    ebit_margin_delta: float = 0.0,
    wacc_delta: float = 0.0,
    terminal_growth_delta: float = 0.0,
) -> ValuationResult:
    cleaned = clean_historical_financials(input_data.history)
    assumptions = ForecastAssumptions(
        forecast_years=input_data.assumptions.forecast_years,
        revenue_growth=[max(-0.99, value + revenue_growth_delta) for value in input_data.assumptions.revenue_growth],
        ebit_margin=[max(-0.99, value + ebit_margin_delta) for value in input_data.assumptions.ebit_margin],
        tax_rate=input_data.assumptions.tax_rate,
        depreciation_amortisation_to_sales=input_data.assumptions.depreciation_amortisation_to_sales,
        capex_to_sales=input_data.assumptions.capex_to_sales,
        nwc_to_sales=input_data.assumptions.nwc_to_sales,
        terminal_growth_rate=input_data.assumptions.terminal_growth_rate,
    )
    forecast = build_forecast(cleaned, assumptions)
    base_wacc = calculate_wacc(input_data.market, cleaned.latest).wacc
    return calculate_dcf_from_forecast(
        input_data,
        forecast,
        base_wacc + wacc_delta,
        input_data.assumptions.terminal_growth_rate + terminal_growth_delta,
    )

