# Equity Strategy

Public-data FCFF DCF equity valuation framework.

The model estimates enterprise value from forecast free cash flow to firm, converts enterprise value to equity value, calculates fair value per share, and generates a confidence-adjusted Buy/Hold/Sell recommendation. It also produces validation documentation covering data quality, terminal value dependence, sensitivity testing, stress testing, and model-risk findings.

## Quick Start

```bash
python3 main.py
```

From the repository root:

```bash
python3 "Equity Strategy/main.py"
```

## Reports

Generated files:

- `outputs/valuation_report.md`
- `outputs/model_validation_report.md`
- `outputs/valuation_summary.json`
- `outputs/wacc_terminal_growth_sensitivity.json`
- `outputs/revenue_margin_sensitivity.json`
- `outputs/stress_scenarios.json`

## Scope

This is a research framework, not investment advice. FCFF DCF is suitable mainly for non-financial operating companies with observable and forecastable cash flows. Banks, insurers, and highly financialised businesses should use dividend discount, excess return, or price-to-book frameworks instead.

