# Equity Strategy Implementation Notes

This folder implements the prompt log request:

1. Create a new `Equity Strategy` folder.
2. Develop the public-data fundamental equity valuation framework from `Fundamental_Valuation_Framework.md`.
3. Generate model-validation documentation using `Model_Validation_Framework_FCFF_DCF (1).md`.

## Delivered Modules

- `src/data_loader.py`: loads JSON valuation inputs.
- `src/financial_cleaner.py`: cleans historical financials and calculates ratios.
- `src/forecast_engine.py`: builds revenue, EBIT, NOPAT, reinvestment, and FCFF forecasts.
- `src/wacc_engine.py`: calculates CAPM cost of equity, after-tax cost of debt, and WACC.
- `src/dcf_engine.py`: calculates enterprise value, equity value, fair value per share, confidence, limitations, and recommendation.
- `src/sensitivity.py`: produces WACC/g, revenue/margin, and stress-test outputs.
- `src/validation.py`: creates validation findings, risk ratings, and model-validation report text.
- `src/report_generator.py`: writes Markdown and JSON reports.
- `main.py`: command-line runner.

## Run

```bash
python3 "Equity Strategy/main.py"
```

Outputs are written to `Equity Strategy/outputs/`.

## Input Format

The current implementation uses a documented JSON input file in `data/raw/sample_company.json`. This keeps the first version deterministic and avoids hidden dependencies on live market-data APIs. Public-source ingestion can be added later behind the same input schema.

