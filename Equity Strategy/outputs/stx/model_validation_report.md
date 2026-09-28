# Model Validation Report

## Model Under Validation

- Company: Seagate Technology Holdings plc
- Ticker: STX
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 75
- Model risk rating: Moderate model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 117.01 USD
- Current share price: 910.34 USD
- Valuation gap: -87.1%
- Recommendation: Sell
- Confidence: High (85/100)
- Terminal value / enterprise value: 67.3%
- WACC: 10.0%
- Terminal growth: 2.0%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 109.12
- Fair value with terminal growth -50bps: 111.20
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: False

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 117.01 | -87.1% | Sell |
| recession | 59.89 | -93.4% | Sell |
| rates_inflation_shock | 81.20 | -91.1% | Sell |
| company_specific_shock | 73.55 | -91.9% | Sell |

## Validation Findings

### VAL-003 - Data
- Severity: Medium
- Issue: Revenue growth in 2023 is outside the normal validation range.; EBIT margin changed by more than 10 percentage points in 2023.; EBIT margin changed by more than 10 percentage points in 2024.; EBIT margin changed by more than 10 percentage points in 2025.
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
