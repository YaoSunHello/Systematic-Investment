# Model Validation Report

## Model Under Validation

- Company: Example Quality Compounder plc
- Ticker: EXM
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 90
- Model risk rating: Low model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 78.71 USD
- Current share price: 54.00 USD
- Valuation gap: 45.8%
- Recommendation: Buy
- Confidence: High (90/100)
- Terminal value / enterprise value: 74.2%
- WACC: 9.2%
- Terminal growth: 2.5%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 73.14
- Fair value with terminal growth -50bps: 74.38
- Cyclical company: False
- Material stock-based compensation: False
- M&A or one-offs distort history: False

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 78.71 | 45.8% | Buy |
| recession | 44.76 | -17.1% | Reduce / Moderate Sell |
| rates_inflation_shock | 56.29 | 4.2% | Hold / Fairly Valued |
| company_specific_shock | 53.64 | -0.7% | Hold / Fairly Valued |

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
