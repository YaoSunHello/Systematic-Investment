from src.dcf_engine import with_assumption_overrides
from src.models import ValuationInput


def wacc_terminal_growth_grid(
    input_data: ValuationInput,
    wacc_deltas: list[float] | None = None,
    terminal_growth_deltas: list[float] | None = None,
) -> list[dict[str, float | str]]:
    wacc_deltas = wacc_deltas or [-0.01, -0.005, 0.0, 0.005, 0.01]
    terminal_growth_deltas = terminal_growth_deltas or [-0.01, -0.005, 0.0, 0.005, 0.01]
    rows: list[dict[str, float | str]] = []
    for wacc_delta in wacc_deltas:
        for growth_delta in terminal_growth_deltas:
            try:
                result = with_assumption_overrides(
                    input_data,
                    wacc_delta=wacc_delta,
                    terminal_growth_delta=growth_delta,
                )
                rows.append(
                    {
                        "wacc_delta": wacc_delta,
                        "terminal_growth_delta": growth_delta,
                        "fair_value_per_share": result.fair_value_per_share,
                        "recommendation": result.recommendation,
                    }
                )
            except ValueError as exc:
                rows.append(
                    {
                        "wacc_delta": wacc_delta,
                        "terminal_growth_delta": growth_delta,
                        "fair_value_per_share": "invalid",
                        "recommendation": str(exc),
                    }
                )
    return rows


def revenue_margin_grid(
    input_data: ValuationInput,
    revenue_growth_deltas: list[float] | None = None,
    ebit_margin_deltas: list[float] | None = None,
) -> list[dict[str, float | str]]:
    revenue_growth_deltas = revenue_growth_deltas or [-0.02, 0.0, 0.02]
    ebit_margin_deltas = ebit_margin_deltas or [-0.02, 0.0, 0.02]
    rows: list[dict[str, float | str]] = []
    for growth_delta in revenue_growth_deltas:
        for margin_delta in ebit_margin_deltas:
            result = with_assumption_overrides(
                input_data,
                revenue_growth_delta=growth_delta,
                ebit_margin_delta=margin_delta,
            )
            rows.append(
                {
                    "revenue_growth_delta": growth_delta,
                    "ebit_margin_delta": margin_delta,
                    "fair_value_per_share": result.fair_value_per_share,
                    "recommendation": result.recommendation,
                }
            )
    return rows


def stress_scenarios(input_data: ValuationInput) -> list[dict[str, float | str]]:
    shocks = {
        "base": {},
        "recession": {
            "revenue_growth_delta": -0.05,
            "ebit_margin_delta": -0.03,
            "wacc_delta": 0.015,
            "terminal_growth_delta": -0.005,
        },
        "rates_inflation_shock": {
            "ebit_margin_delta": -0.02,
            "wacc_delta": 0.015,
            "terminal_growth_delta": -0.005,
        },
        "company_specific_shock": {
            "revenue_growth_delta": -0.03,
            "ebit_margin_delta": -0.03,
            "wacc_delta": 0.01,
        },
    }
    output: list[dict[str, float | str]] = []
    for name, params in shocks.items():
        result = with_assumption_overrides(input_data, **params)
        output.append(
            {
                "scenario": name,
                "fair_value_per_share": result.fair_value_per_share,
                "valuation_gap": result.valuation_gap,
                "recommendation": result.recommendation,
                "confidence_level": result.confidence_level,
            }
        )
    return output

