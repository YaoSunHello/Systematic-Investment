from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.data_loader import write_json
from src.models import ValuationInput, ValuationResult
from src.sensitivity import revenue_margin_grid, stress_scenarios, wacc_terminal_growth_grid
from src.validation import validation_report_markdown


def _round_payload(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, list):
        return [_round_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: _round_payload(item) for key, item in value.items()}
    return value


def valuation_summary_payload(result: ValuationResult) -> dict[str, Any]:
    return _round_payload(
        {
            "company": asdict(result.company),
            "summary": {
                "valuation_method": "FCFF DCF",
                "current_share_price": result.metadata.get("current_share_price"),
                "fair_value_per_share": result.fair_value_per_share,
                "valuation_gap": result.valuation_gap,
                "recommendation": result.recommendation,
                "confidence_score": result.confidence_score,
                "confidence_level": result.confidence_level,
            },
            "valuation_breakdown": {
                "pv_explicit_fcff": sum(result.pv_fcff),
                "pv_terminal_value": result.pv_terminal_value,
                "enterprise_value": result.enterprise_value,
                "equity_value": result.equity_value,
                "terminal_value_to_ev": result.terminal_value_to_ev,
            },
            "wacc": asdict(result.wacc),
            "forecast": [asdict(row) for row in result.forecast],
            "limitations": result.limitations,
            "flags": result.flags,
            "data_quality_flags": result.data_quality_flags,
        }
    )


def summary_markdown(input_data: ValuationInput, result: ValuationResult) -> str:
    result.metadata["current_share_price"] = input_data.market.current_share_price
    assumptions = input_data.assumptions
    forecast_cagr = (
        result.forecast[-1].revenue / input_data.history[-1].revenue
    ) ** (1 / len(result.forecast)) - 1
    limitation_md = "\n".join(f"- {item}" for item in result.limitations)
    forecast_rows = "\n".join(
        f"| {row.year} | {row.revenue:.1f} | {row.ebit:.1f} | {row.fcff:.1f} |"
        for row in result.forecast
    )
    return f"""# Equity Valuation Summary

## Summary Output

- Company: {result.company.company_name}
- Ticker: {result.company.ticker}
- Currency: {result.company.currency}
- Valuation method: FCFF DCF
- Current share price: {input_data.market.current_share_price:.2f}
- Estimated fair value per share: {result.fair_value_per_share:.2f}
- Upside / downside: {result.valuation_gap:.1%}
- Recommendation: {result.recommendation}
- Confidence: {result.confidence_level} ({result.confidence_score}/100)

## Valuation Breakdown

- PV of explicit forecast FCFF: {sum(result.pv_fcff):.1f}
- PV of terminal value: {result.pv_terminal_value:.1f}
- Enterprise value: {result.enterprise_value:.1f}
- Equity value: {result.equity_value:.1f}
- Diluted shares outstanding: {input_data.history[-1].diluted_shares:.1f}
- Terminal value / enterprise value: {result.terminal_value_to_ev:.1%}

## Key Assumptions

- Forecast revenue CAGR: {forecast_cagr:.1%}
- Terminal growth rate: {assumptions.terminal_growth_rate:.1%}
- WACC: {result.wacc.wacc:.1%}
- Final-year EBIT margin: {assumptions.ebit_margin[-1]:.1%}
- Tax rate: {assumptions.tax_rate:.1%}
- Capex / sales: {assumptions.capex_to_sales:.1%}

## Forecast

| Year | Revenue | EBIT | FCFF |
|---:|---:|---:|---:|
{forecast_rows}

## Model Limitations

{limitation_md}
"""


def write_reports(input_data: ValuationInput, result: ValuationResult, output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    result.metadata["current_share_price"] = input_data.market.current_share_price
    write_json(output_path / "valuation_summary.json", valuation_summary_payload(result))
    write_json(output_path / "wacc_terminal_growth_sensitivity.json", {"grid": wacc_terminal_growth_grid(input_data)})
    write_json(output_path / "revenue_margin_sensitivity.json", {"grid": revenue_margin_grid(input_data)})
    write_json(output_path / "stress_scenarios.json", {"scenarios": stress_scenarios(input_data)})
    (output_path / "valuation_report.md").write_text(summary_markdown(input_data, result), encoding="utf-8")
    (output_path / "model_validation_report.md").write_text(
        validation_report_markdown(input_data, result),
        encoding="utf-8",
    )

