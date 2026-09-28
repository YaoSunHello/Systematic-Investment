# Model Validation Report

## Model Under Validation

- Company: Western Digital Corp
- Ticker: WDC
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 35
- Model risk rating: Very high model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 89.28 USD
- Current share price: 582.59 USD
- Valuation gap: -84.7%
- Recommendation: Sell
- Confidence: Low (45/100)
- Terminal value / enterprise value: 63.8%
- WACC: 11.7%
- Terminal growth: 2.5%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 84.37
- Fair value with terminal growth -50bps: 85.82
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: True

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 89.28 | -84.7% | Sell |
| recession | 52.98 | -90.9% | Sell |
| rates_inflation_shock | 66.92 | -88.5% | Sell |
| company_specific_shock | 62.06 | -89.3% | Sell |

## Validation Findings

### VAL-003 - Data
- Severity: Medium
- Issue: Revenue growth in 2023 is outside the normal validation range.; Revenue growth in 2025 is outside the normal validation range.; EBIT margin changed by more than 10 percentage points in 2023.; EBIT margin changed by more than 10 percentage points in 2025.
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
