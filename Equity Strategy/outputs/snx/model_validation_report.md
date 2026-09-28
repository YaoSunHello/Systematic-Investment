# Model Validation Report

## Model Under Validation

- Company: Td Synnex Corp
- Ticker: SNX
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: 45
- Model risk rating: Very high model risk

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: 266.45 USD
- Current share price: 251.77 USD
- Valuation gap: 5.8%
- Recommendation: Moderate Buy / Accumulate
- Confidence: Medium (55/100)
- Terminal value / enterprise value: 72.1%
- WACC: 10.1%
- Terminal growth: 2.0%

## Required Limitation Disclosures

- Fair value with WACC +50bps: 251.23
- Fair value with terminal growth -50bps: 255.15
- Cyclical company: True
- Material stock-based compensation: False
- M&A or one-offs distort history: True

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
| base | 266.45 | 5.8% | Moderate Buy / Accumulate |
| recession | 12.76 | -94.9% | Sell |
| rates_inflation_shock | 66.58 | -73.6% | Sell |
| company_specific_shock | 4.35 | -98.3% | Sell |

## Validation Findings

### VAL-003 - Data
- Severity: Medium
- Issue: Revenue growth in 2022 is outside the normal validation range.; Diluted shares changed by more than 20% in 2022.
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
