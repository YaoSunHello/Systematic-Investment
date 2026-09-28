# Model Validation Report

## Model Under Validation

- Company: Concrete Pumping Holdings, Inc.
- Ticker: BBCP
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 75
- Model risk rating: Moderate model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 2.72 USD
- Current share price: 10.87 USD
- Valuation gap: -75.0%
- Recommendation: Sell
- Confidence: High (75/100)
- Terminal value / enterprise value: 75.4%
- WACC: 8.4%
- Terminal growth: 2.0%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 1.99
- Fair value with terminal growth -50bps: 2.14
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: False

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 2.72 | -75.0% | Sell |
| recession | -2.66 | -124.5% | Sell |
| rates_inflation_shock | -1.06 | -109.7% | Sell |
| company_specific_shock | -1.77 | -116.3% | Sell |

## Validation Findings

### VAL-001 - Terminal Value
- Severity: Medium
- Issue: Terminal value exceeds 75% of enterprise value.
- Impact: Point-estimate valuation is sensitive to long-run assumptions.
- Recommendation: Review WACC/g sensitivity before using the recommendation.
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
