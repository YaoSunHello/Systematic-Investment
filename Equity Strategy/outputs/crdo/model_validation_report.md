# Model Validation Report

## Model Under Validation

- Company: Credo Technology Group Holding Ltd
- Ticker: CRDO
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 30
- Model risk rating: Very high model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 75.40 USD
- Current share price: 257.79 USD
- Valuation gap: -70.8%
- Recommendation: Sell
- Confidence: Low (40/100)
- Terminal value / enterprise value: 73.4%
- WACC: 13.1%
- Terminal growth: 3.5%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 71.56
- Fair value with terminal growth -50bps: 72.65
- Cyclical company: False
- Material stock-based compensation: True
- M&A or one-offs distort history: False

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 75.40 | -70.8% | Sell |
| recession | 51.39 | -80.1% | Sell |
| rates_inflation_shock | 59.34 | -77.0% | Sell |
| company_specific_shock | 58.02 | -77.5% | Sell |

## Validation Findings

### VAL-003 - Data
- Severity: Medium
- Issue: Revenue growth in 2023 is outside the normal validation range.; Revenue growth in 2025 is outside the normal validation range.; Revenue growth in 2026 is outside the normal validation range.; EBIT margin changed by more than 10 percentage points in 2025.; EBIT margin changed by more than 10 percentage points in 2026.; Diluted shares changed by more than 20% in 2023.
- Impact: Input issues may distort fair value and model confidence.
- Recommendation: Resolve data lineage and mapping issues before production use.
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
