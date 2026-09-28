# Model Validation Report

## Model Under Validation

- Company: Microchip Technology Inc
- Ticker: MCHP
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 65
- Model risk rating: High model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 44.69 USD
- Current share price: 88.59 USD
- Valuation gap: -49.6%
- Recommendation: Sell
- Confidence: High (75/100)
- Terminal value / enterprise value: 73.5%
- WACC: 10.7%
- Terminal growth: 2.5%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 41.35
- Fair value with terminal growth -50bps: 42.21
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: True

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 44.69 | -49.6% | Sell |
| recession | 24.43 | -72.4% | Sell |
| rates_inflation_shock | 31.86 | -64.0% | Sell |
| company_specific_shock | 30.45 | -65.6% | Sell |

## Validation Findings

### VAL-003 - Data
- Severity: Medium
- Issue: Revenue growth in 2025 is outside the normal validation range.; EBIT margin changed by more than 10 percentage points in 2025.
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
