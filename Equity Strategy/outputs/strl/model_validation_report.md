# Model Validation Report

## Model Under Validation

- Company: Sterling Infrastructure, Inc.
- Ticker: STRL
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 75
- Model risk rating: Moderate model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 234.86 USD
- Current share price: 682.29 USD
- Valuation gap: -65.6%
- Recommendation: Sell
- Confidence: High (75/100)
- Terminal value / enterprise value: 74.6%
- WACC: 10.0%
- Terminal growth: 3.0%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 218.94
- Fair value with terminal growth -50bps: 222.60
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: False

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 234.86 | -65.6% | Sell |
| recession | 123.86 | -81.8% | Sell |
| rates_inflation_shock | 164.12 | -75.9% | Sell |
| company_specific_shock | 149.75 | -78.1% | Sell |

## Validation Findings

### VAL-000 - Overall
- Severity: Low
- Issue: No high-severity validation exceptions from automated checks.
- Impact: Model can be used as a research support tool with stated limitations.
- Recommendation: Keep analyst review, sensitivity analysis, and source documentation mandatory.
- Status: Open


## Validator Checklist

- [x] FCFF formula implemented as NOPAT + D&A - capex - change in NWC.
- [x] WACC uses CAPM cost of equity and after-tax cost of debt.
- [x] WACC must be greater than terminal growth.
- [x] Enterprise value converts to equity value through debt, cash, minority interest, preferred equity, and investments.
- [x] Recommendation uses valuation gap and confidence-adjusted margin of safety.
- [x] Terminal value dependence, sensitivity, stress tests, and limitations are disclosed.

## Final Opinion

Approved with limitations. The model is usable for research support where source data and assumptions are reviewed by an analyst. Automatic Buy recommendations should be blocked or escalated when confidence is low, sector suitability is poor, or terminal value dominates enterprise value.
