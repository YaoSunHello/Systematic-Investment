# Model Validation Framework
## Fundamental Equity Valuation Model — FCFF DCF

**Role:** Independent model validator  
**Model under validation:** Public-data fundamental equity valuation model using Free Cash Flow to Firm Discounted Cash Flow (FCFF DCF)  
**Primary model outputs:** Fair value per share, valuation gap, model limitations, confidence score, and Buy/Hold/Sell recommendation  
**Validation objective:** Assess whether the model is conceptually sound, technically correct, empirically robust, transparent, and fit for investment decision support.

> **Important:** This validation framework is designed for model governance and research-quality review. It does not guarantee investment performance and should not be interpreted as investment advice.

---

## 1. Executive Summary

The valuation model under review uses an **FCFF DCF methodology** to estimate a company's intrinsic enterprise value, convert that into equity value, and compare the resulting fair value per share against the current market price.

From a model-validation perspective, the framework is directionally sound for **non-financial operating companies** with observable and forecastable cash flows. However, the robustness of the output depends heavily on:

- Forecast revenue growth assumptions
- EBIT margin assumptions
- Reinvestment assumptions, including capex and working capital
- WACC estimation
- Terminal value treatment
- Data quality and public-source consistency
- Sector suitability
- Recommendation thresholds
- Sensitivity to macro and company-specific shocks

The validation should therefore assess not only whether the model calculates correctly, but whether its outputs are:

1. **Economically reasonable**
2. **Technically reproducible**
3. **Transparent and explainable**
4. **Stable under plausible sensitivities**
5. **Appropriate for the company being valued**
6. **Governed with clear limitations and escalation rules**

---

## 2. Validation Scope

### 2.1 In Scope

| Area | Validation Question |
|---|---|
| Model design | Is FCFF DCF appropriate for the selected company? |
| Data | Are public inputs accurate, complete, and consistently mapped? |
| Forecast logic | Are revenue, margin, capex, tax, and working capital assumptions reasonable? |
| Discount rate | Is WACC calculated consistently with FCFF? |
| Terminal value | Is the terminal growth assumption economically defensible? |
| Valuation output | Is fair value per share calculated correctly? |
| Recommendation engine | Are Buy/Hold/Sell signals reasonable and not overconfident? |
| Limitations | Are company-specific weaknesses clearly disclosed? |
| Robustness | Does the conclusion survive sensitivity and stress testing? |
| Governance | Is the model documented, controlled, and monitored? |

### 2.2 Out of Scope

The validation does **not** guarantee that:

- The stock price will converge to the estimated fair value.
- The model's recommendation will outperform the market.
- Analyst assumptions will be correct.
- Public data is free from accounting limitations or reporting bias.
- FCFF DCF is the best methodology for every sector.

---

## 3. Conceptual Soundness Validation

### 3.1 Methodology Appropriateness

The model uses an **FCFF DCF** approach, valuing the enterprise by discounting future free cash flow to the firm using WACC.

The validator should confirm that:

- The model values the **enterprise**, not only the equity.
- FCFF is calculated before financing cash flows.
- FCFF is discounted using **WACC**, not cost of equity.
- Equity value is derived by adjusting enterprise value for debt, cash, minority interests, preferred equity, and other non-common-equity claims.
- Fair value per share is calculated using diluted shares outstanding.

### 3.2 Sector Suitability Gate

FCFF DCF is suitable for many operating companies, but it should not be applied mechanically across all sectors.

| Company Type | FCFF DCF Suitability | Validation Action |
|---|---:|---|
| Mature industrial company | High | Standard validation |
| Quality compounder | High | Check terminal value dominance |
| Technology platform | Medium | Check stock-based compensation, capex classification, and segment economics |
| Cyclical commodity company | Medium/Low | Require mid-cycle normalisation and scenarios |
| Bank or insurer | Low | Reject FCFF as primary model |
| Early-stage negative-FCF company | Low | Require scenario-weighted or alternative valuation |

### 3.3 Sector Suitability Rule

```text
If company sector is bank, insurer, or highly financialised business:
    FCFF DCF should not be used as the primary valuation model.
    Require alternative methodology, such as:
        - Dividend discount model
        - Excess return model
        - Price-to-book or ROE-based framework
```

---

## 4. Data Validation Framework

### 4.1 Data Lineage Validation

Each input should be traceable to a documented public source.

| Input | Required Evidence |
|---|---|
| Revenue | Annual report, 10-K, 20-F, or company filing |
| EBIT / operating income | Income statement |
| D&A | Cash flow statement or notes |
| Capex | Cash flow statement |
| Working capital | Balance sheet |
| Debt | Balance sheet and debt notes |
| Cash | Balance sheet |
| Tax rate | Income statement and tax footnote |
| Diluted shares | Annual report or market data provider |
| Current market price | Exchange or public market data provider |
| Beta | Market data provider or documented sector proxy |
| Risk-free rate | Government bond yield consistent with valuation currency |
| Equity risk premium | Published market assumption with source and date |

### 4.2 Data Completeness Checks

The model should not produce an unconstrained recommendation if critical inputs are missing.

```text
Revenue exists for at least 5 historical years.
EBIT exists for at least 5 historical years.
D&A exists or can be reasonably estimated.
Capex exists.
Debt and cash balances exist.
Diluted shares outstanding exist.
Current market price exists.
Beta exists or a sector beta proxy is documented.
Risk-free rate exists.
Equity risk premium exists.
```

### 4.3 Data Consistency Checks

```text
Revenue should be positive.
Cash should not be negative.
Debt should not be negative.
Capex should be treated consistently as a cash outflow.
D&A should generally be positive.
Diluted shares should be positive.
Enterprise value bridge should reconcile.
Historical EBIT margin should be within plausible industry range.
```

### 4.4 Restatement and Accounting Consistency Checks

The validator should assess whether historical data is comparable over time.

Potential issues include:

- Accounting standard changes
- Major M&A or disposals
- Discontinued operations
- One-off restructuring charges
- Pandemic-period distortions
- FX translation effects
- Share splits
- Fiscal-year changes

### 4.5 Automated Data Flags

```text
If revenue growth > 50% or < -30%:
    Flag possible acquisition, disposal, accounting issue, or data error.

If EBIT margin changes by more than 10 percentage points:
    Flag possible one-off event or business mix shift.

If shares outstanding change by more than 20%:
    Flag possible buyback, issuance, or split adjustment.
```

---

## 5. Forecast Assumption Validation

Forecast assumptions are the largest source of model risk. The validator should challenge whether the assumptions are economically defensible rather than mechanically extrapolated.

### 5.1 Revenue Growth Validation

#### Key Validation Questions

```text
Is forecast growth consistent with historical growth?
Is it consistent with industry growth?
Does it fade toward a sustainable long-term rate?
Is it realistic relative to GDP, inflation, and market share?
Does the company's scale support the assumed growth?
```

#### Diagnostic Tests

| Test | Validation Logic |
|---|---|
| Historical comparison | Compare forecast growth with 3-year, 5-year, and 10-year CAGR |
| Industry comparison | Benchmark against listed peers and industry outlook |
| Fade test | High growth should gradually fade toward terminal growth |
| Market-share test | Forecast should not imply unrealistic market share gains |
| Macro consistency | Long-term growth should not greatly exceed nominal GDP without justification |

#### Red Flags

```text
Forecast growth materially exceeds historical growth without explanation.
Long-term growth materially exceeds industry growth.
No fade-down is applied for a high-growth company.
Revenue doubles or triples without corresponding reinvestment.
Terminal growth exceeds sustainable long-run nominal GDP.
```

---

### 5.2 Margin Validation

#### Key Validation Questions

```text
Are EBIT margins based on history, peers, and business economics?
Does the model assume excessive margin expansion?
Are margins consistent with competitive dynamics?
Are inflation and input-cost pressures considered?
```

#### Diagnostic Tests

| Test | Validation Logic |
|---|---|
| Historical margin range | Forecast margin should sit within a justified historical range |
| Peer benchmark | Compare forecast margin with direct peers |
| Mean reversion | Cyclical peak margins should normalise |
| Operating leverage | Margin expansion should be linked to scale economics |
| Cost pressure test | Assess sensitivity to wage, commodity, and FX pressures |

#### Red Flags

```text
Forecast margin exceeds historical maximum.
Forecast margin exceeds best-in-class peers without justification.
Margin expansion occurs without scale or cost explanation.
A cyclical company is valued using peak margins.
No downside margin scenario is included.
```

---

### 5.3 Reinvestment Validation

#### Capex Validation

```text
If revenue growth is high but capex/sales falls:
    Flag potential inconsistency.

If capex is below depreciation for many years:
    Flag possible underinvestment unless the business is demonstrably asset-light.
```

#### Working Capital Validation

```text
If revenue grows materially but working capital investment is zero:
    Flag inconsistency.

If working capital turns permanently improve without explanation:
    Flag aggressive assumption.
```

#### Reinvestment Efficiency Test

A useful diagnostic ratio is:

```text
Sales to Invested Capital = Revenue / Invested Capital
```

If forecast growth requires materially less invested capital than history, the model should provide a clear explanation.

---

## 6. WACC Validation

WACC is a key driver of fair value. Because FCFF represents cash flow available to both debt and equity providers, it should be discounted using WACC.

### 6.1 Cost of Equity Validation

The model uses CAPM:

```text
Cost of Equity = Risk-free Rate + Beta × Equity Risk Premium
```

#### Validation Checks

```text
Risk-free rate should match the valuation currency.
Beta should reflect the company's business risk.
Equity risk premium should be documented with source and date.
Levered and unlevered beta treatment should be consistent.
Country risk premium should be added where relevant.
```

#### Red Flags

```text
Using a US Treasury yield for non-USD cash flows without justification.
Using stale beta.
Ignoring country risk for emerging-market revenue exposure.
Using raw beta for a company with unstable leverage.
Using ERP without source or date.
```

---

### 6.2 Cost of Debt Validation

Preferred hierarchy:

```text
1. Yield to maturity on traded company debt.
2. Credit spread based on credit rating.
3. Interest expense / average debt.
```

#### Red Flags

```text
Cost of debt below the risk-free rate.
Cost of debt based only on historical coupon when rates have changed.
No adjustment for floating-rate debt.
No adjustment for distressed credit risk.
```

---

### 6.3 Capital Structure Validation

The model should use market-value weights where possible.

```text
WACC = [E / (D + E)] × Ke + [D / (D + E)] × Kd × (1 - Tax Rate)
```

#### Validation Tests

```text
Equity weight uses market capitalisation.
Debt weight uses market value or book value if market value is unavailable.
Cash is not incorrectly included as negative debt in WACC weighting.
Tax shield is applied only to debt cost.
Preferred equity, leases, and minority interest are treated consistently.
```

---

## 7. Terminal Value Validation

Terminal value is often the largest component of a DCF valuation. The model should explicitly measure terminal value dependence.

### 7.1 Gordon Growth Formula

```text
Terminal Value = FCFF(n+1) / (WACC - g)
```

Mandatory validation rules:

```text
WACC must be greater than terminal growth.
Terminal growth must be economically sustainable.
Terminal value should be separately disclosed.
Terminal value as a percentage of enterprise value should be flagged.
```

### 7.2 Terminal Value Dominance Test

| Terminal Value / Enterprise Value | Interpretation |
|---:|---|
| < 60% | Acceptable |
| 60%–75% | Normal but sensitive |
| 75%–85% | High dependence on terminal assumptions |
| > 85% | Serious model-risk flag |

### 7.3 Terminal Growth Validation

```text
If terminal growth > long-run nominal GDP:
    Flag aggressive terminal assumption.

If WACC - terminal growth < 2%:
    Flag high valuation instability.
```

---

## 8. Calculation and Implementation Validation

This section validates the technical implementation.

### 8.1 Core Formula Checks

```text
Revenue_t = Revenue_t-1 × (1 + Growth_t)

EBIT_t = Revenue_t × EBIT Margin_t

NOPAT_t = EBIT_t × (1 - Tax Rate_t)

FCFF_t = NOPAT_t + D&A_t - Capex_t - Change in NWC_t

PV_FCFF_t = FCFF_t / (1 + WACC)^t

Terminal Value = FCFF_n × (1 + g) / (WACC - g)

PV_Terminal Value = Terminal Value / (1 + WACC)^n

Enterprise Value = Sum(PV_FCFF) + PV_Terminal Value

Equity Value = Enterprise Value - Debt + Cash - Minority Interest - Preferred Equity + Investments

Fair Value per Share = Equity Value / Diluted Shares
```

### 8.2 Independent Rebuild Test

The validator should rebuild the valuation outside the production model.

```text
Original model: production implementation
Validator model: independent spreadsheet or Python implementation
Tolerance: fair value difference < 0.5%
```

If the valuation differs by more than 0.5%, the discrepancy should be investigated and documented.

---

## 9. Sensitivity and Stress Testing

DCF outputs are sensitive to long-term assumptions. The validation should test whether the recommendation remains stable under plausible changes.

### 9.1 Core Sensitivity Tests

The model should produce sensitivity matrices for:

```text
WACC vs terminal growth
Revenue CAGR vs EBIT margin
Capex/sales vs revenue growth
Tax rate vs WACC
Working capital intensity vs margin
```

### 9.2 WACC / Terminal Growth Sensitivity Grid

| Fair Value Sensitivity | g - 1.0% | g - 0.5% | Base g | g + 0.5% | g + 1.0% |
|---|---:|---:|---:|---:|---:|
| WACC - 1.0% | Value | Value | Value | Value | Value |
| WACC - 0.5% | Value | Value | Value | Value | Value |
| Base WACC | Value | Value | Value | Value | Value |
| WACC + 0.5% | Value | Value | Value | Value | Value |
| WACC + 1.0% | Value | Value | Value | Value | Value |

### 9.3 Recommendation Stability Test

```text
Base case recommendation: Buy

If WACC + 0.5% changes recommendation to Hold:
    Model confidence = Medium

If WACC + 0.5% changes recommendation to Sell:
    Model confidence = Low
```

### 9.4 Stress Scenarios

| Scenario | Shock Design |
|---|---|
| Recession case | Revenue falls, margin compresses, working capital worsens |
| Inflation/rates shock | WACC rises, cost pressures reduce margin |
| Company-specific shock | Revenue growth slows, capex rises, competitive pressure increases |

Example stress design:

```text
Revenue growth: -5 percentage points versus base case
EBIT margin: -300 basis points versus base case
WACC: +150 basis points versus base case
Terminal growth: -50 basis points versus base case
```

---

## 10. Challenger Model Validation

The validator should compare the FCFF DCF output with alternative valuation approaches.

### 10.1 Challenger Models

| Challenger Model | Purpose |
|---|---|
| EV/EBITDA peer multiple | Market-relative valuation cross-check |
| P/E peer multiple | Earnings-based relative valuation |
| Dividend discount model | Useful for mature dividend-paying companies |
| Sum-of-the-parts | Useful for diversified or multi-segment companies |
| Asset-based valuation | Useful for asset-heavy firms |
| Scenario-weighted DCF | Useful for cyclicals and uncertain growth companies |

### 10.2 Challenger Validation Rule

```text
If FCFF DCF fair value differs from peer multiple valuation by more than 30%:
    Require explanation.

If FCFF DCF gives Buy but relative valuation shows a substantial premium:
    Flag for analyst review.

If FCFF DCF gives Sell but peer valuation and market-implied assumptions look reasonable:
    Flag for assumption review.
```

---

## 11. Back-Testing Framework

Back-testing assesses whether historical model signals would have shown useful predictive behaviour.

### 11.1 Back-Test Design

For each historical valuation date:

```text
1. Use only information publicly available at that date.
2. Generate fair value estimate.
3. Generate model recommendation.
4. Track subsequent share-price return.
5. Compare against benchmark and sector peers.
```

### 11.2 Recommended Horizons

| Horizon | Purpose |
|---|---|
| 3 months | Short-term signal stability |
| 6 months | Medium-term price reaction |
| 12 months | Fundamental valuation convergence |
| 24 months | Long-term intrinsic-value test |

### 11.3 Back-Test Metrics

| Metric | Interpretation |
|---|---|
| Hit rate | Percentage of Buy calls outperforming benchmark |
| Average excess return | Magnitude of outperformance |
| Drawdown after Buy call | Downside risk after signal |
| False positive rate | Buy signals that underperform materially |
| False negative rate | Sell signals that outperform materially |
| Recommendation turnover | Stability of model signals |
| Information coefficient | Rank correlation between upside and future return |

### 11.4 Look-Ahead Bias Controls

```text
No future financial statements are used.
No later restated data is used unless restatement handling is documented.
Market prices are taken from the valuation date.
Consensus inputs, if used, are point-in-time.
Risk-free rates and equity risk premia are point-in-time.
```

---

## 12. Recommendation Engine Validation

### 12.1 Base Recommendation Rules

| Valuation Gap | Recommendation |
|---:|---|
| > +20% | Buy |
| +5% to +20% | Moderate Buy / Accumulate |
| -5% to +5% | Hold / Fairly Valued |
| -20% to -5% | Reduce / Moderate Sell |
| < -20% | Sell |

### 12.2 Validator Challenge

A fixed 20% Buy threshold may be too aggressive for unstable companies and too conservative for very robust companies. The required margin of safety should vary by model confidence.

### 12.3 Recommended Confidence-Adjusted Rule

| Model Confidence | Required Upside for Buy |
|---|---:|
| High | > 15% |
| Medium | > 25% |
| Low | > 35% |
| Very Low | No automatic Buy allowed |

```text
If model confidence = High and upside > 15%:
    Buy

If model confidence = Medium and upside > 25%:
    Buy

If model confidence = Low and upside > 35%:
    Speculative Buy / Analyst Review

If model confidence = Very Low:
    No automatic Buy recommendation
```

---

## 13. Model Limitation Validation

The model should generate company-specific limitations rather than generic disclaimers.

### 13.1 Weak vs Strong Limitation Language

Weak limitation:

```text
The model is sensitive to assumptions.
```

Stronger limitation:

```text
For this company, 82% of enterprise value comes from terminal value.
A 50bps increase in WACC reduces fair value by 18%.
Therefore, the Buy recommendation is highly dependent on long-term discount-rate assumptions.
```

### 13.2 Required Limitation Outputs

For each company, the model should disclose:

```text
Terminal value as % of enterprise value.
Sensitivity of fair value to +50bps WACC.
Sensitivity of fair value to -50bps terminal growth.
Historical FCFF volatility.
Whether the company is cyclical.
Whether the company has negative FCFF.
Whether the sector is suitable for FCFF DCF.
Whether stock-based compensation is material.
Whether M&A or one-offs distort history.
```

---

## 14. Model Risk Rating Framework

### 14.1 Model Risk Score Components

| Component | Weight |
|---|---:|
| Methodology suitability | 20% |
| Data quality | 15% |
| Assumption reasonableness | 20% |
| Sensitivity robustness | 15% |
| Challenger-model agreement | 10% |
| Back-test performance | 10% |
| Governance quality | 10% |

### 14.2 Model Risk Rating

| Score | Rating | Interpretation |
|---:|---|---|
| 85–100 | Low model risk | Suitable for regular research use |
| 70–85 | Moderate model risk | Use with normal analyst review |
| 50–70 | High model risk | Use only as supporting tool |
| < 50 | Very high model risk | Do not rely on recommendation output |

---

## 15. Validation Test Plan

### 15.1 Minimum Required Tests

```text
Test 1: Confirm FCFF formula implementation.
Test 2: Confirm WACC formula implementation.
Test 3: Confirm WACC > terminal growth.
Test 4: Recalculate fair value independently.
Test 5: Validate data mapping from public source.
Test 6: Test sensitivity to WACC and terminal growth.
Test 7: Test valuation under recession scenario.
Test 8: Compare DCF output to peer multiples.
Test 9: Check recommendation stability.
Test 10: Review company-specific model limitations.
```

### 15.2 Acceptance Criteria

| Test Area | Pass Criteria |
|---|---|
| Formula accuracy | Independent valuation within 0.5% |
| Data quality | No critical missing inputs |
| WACC logic | FCFF discounted using WACC only |
| Terminal value | WACC > g and terminal value share disclosed |
| Sensitivity | Recommendation stable under reasonable shocks, or confidence downgraded |
| Sector suitability | Unsuitable sectors flagged |
| Challenger model | Large differences explained |
| Recommendation | Signal consistent with valuation gap and confidence score |

---

## 16. Validation Findings Template

```text
Finding ID: VAL-001
Severity: High / Medium / Low
Area: WACC / Data / Forecast / Recommendation / Governance

Issue:
    Description of the validation issue.

Impact:
    How this affects fair value, recommendation, or confidence.

Evidence:
    Specific test result or model output.

Recommendation:
    Required remediation.

Owner:
    Model developer / analyst / data owner.

Target Date:
    Remediation deadline.

Status:
    Open / In progress / Closed.
```

---

## 17. Example Validation Findings

### Finding 1 — Terminal Value Dominance

```text
Severity: High

Issue:
Terminal value represents 88% of enterprise value.

Impact:
Fair value is highly dependent on WACC and terminal growth assumptions.
The Buy recommendation may not be robust.

Recommendation:
Downgrade model confidence to Low.
Add WACC/g sensitivity matrix.
Require analyst override before issuing Buy recommendation.
```

### Finding 2 — Aggressive Margin Expansion

```text
Severity: Medium

Issue:
Forecast EBIT margin rises from 18% historically to 27% by year five,
above the company's historical maximum and peer median.

Impact:
Fair value may be overstated.

Recommendation:
Require justification for operating leverage assumption or reduce base-case margin.
```

### Finding 3 — Sector Misapplication

```text
Severity: High

Issue:
The model was applied to a bank using FCFF.

Impact:
FCFF is not appropriate because debt is part of the operating model of financial institutions.

Recommendation:
Reject FCFF valuation and use excess return, dividend discount, or P/B framework.
```

---

## 18. Ongoing Monitoring Framework

### 18.1 Monitoring Triggers

The model should be revalidated if:

```text
Company releases new annual results.
Company issues a profit warning.
Company announces a major acquisition or disposal.
Interest rates move by more than 100bps.
Beta changes materially.
WACC changes by more than 100bps.
Recommendation changes from Sell to Buy or Buy to Sell.
Model methodology changes.
Data provider changes.
```

### 18.2 Periodic Review Frequency

| Review Type | Frequency |
|---|---|
| Data refresh check | Quarterly |
| Assumption review | Quarterly |
| Full model validation | Annually |
| Back-test review | Annually |
| Methodology review | Every 2 years or after major model change |

---

## 19. Validator's Final Opinion Framework

The final validation opinion should use four categories.

| Opinion | Meaning |
|---|---|
| Approved | Model is fit for purpose |
| Approved with limitations | Model is usable, but key weaknesses must be disclosed |
| Conditional approval | Model can only be used after remediation |
| Rejected | Model is not fit for purpose |

### Example Final Opinion

```text
Validation Opinion: Approved with Limitations

The FCFF DCF model is conceptually sound for non-financial operating companies.
The valuation mechanics are appropriate and consistent with standard intrinsic valuation theory.

However, the model is materially sensitive to WACC, terminal growth, and margin assumptions.
Recommendations should not be used mechanically.
For companies where terminal value exceeds 80% of enterprise value, confidence should be downgraded and analyst review should be mandatory.

The model should not be used as the primary valuation method for banks, insurers, or companies with persistently negative free cash flow.
```

---

## 20. Practical Validator Checklist

### Conceptual

```text
[ ] Is FCFF DCF appropriate for this company?
[ ] Are cash flows and discount rate matched correctly?
[ ] Is the company a financial institution?
[ ] Is the company too early-stage for DCF?
```

### Data

```text
[ ] Are all public data sources documented?
[ ] Are financial statements mapped correctly?
[ ] Are exceptional items adjusted?
[ ] Are share counts and market price current?
```

### Assumptions

```text
[ ] Is revenue growth realistic?
[ ] Is margin expansion justified?
[ ] Is capex sufficient to support growth?
[ ] Is working capital treatment reasonable?
[ ] Is terminal growth sustainable?
```

### WACC

```text
[ ] Is risk-free rate currency-consistent?
[ ] Is beta reasonable?
[ ] Is ERP documented?
[ ] Is cost of debt realistic?
[ ] Is capital structure based on market values?
```

### Output

```text
[ ] Is fair value per share correctly calculated?
[ ] Is upside/downside correctly calculated?
[ ] Is recommendation threshold applied correctly?
[ ] Is confidence score reasonable?
[ ] Are limitations company-specific?
```

### Robustness

```text
[ ] Has WACC/g sensitivity been performed?
[ ] Has stress testing been performed?
[ ] Has a challenger model been used?
[ ] Has recommendation stability been checked?
[ ] Has back-testing been performed?
```

---

## 21. Recommended Enhancements Before Production Use

### 21.1 Dynamic Margin of Safety

Replace the fixed 20% Buy threshold with a confidence-adjusted threshold.

```text
High confidence: Buy if upside > 15%
Medium confidence: Buy if upside > 25%
Low confidence: Buy if upside > 35%
Very low confidence: No automatic Buy
```

### 21.2 Terminal Value Risk Flag

```text
If Terminal Value / Enterprise Value > 80%:
    Automatically downgrade confidence.
```

### 21.3 Sector Suitability Gate

```text
If company is a bank, insurer, or highly financialised business:
    Block FCFF recommendation.
```

### 21.4 Challenger Valuation Requirement

```text
DCF output must be compared against at least one relative valuation method.
If divergence > 30%, require analyst explanation.
```

---

## 22. Final Validation Framework Summary

The validation framework should answer five core questions:

```text
1. Is the methodology appropriate?
2. Is the data reliable?
3. Are the assumptions reasonable?
4. Are the calculations correct?
5. Is the recommendation robust?
```

A model should only receive approval if:

```text
The valuation logic is conceptually sound.
The data is complete and traceable.
The assumptions are economically defensible.
The fair value calculation is independently reproducible.
The recommendation remains reasonable under sensitivity and stress testing.
The limitations are clearly disclosed.
```

In short, the model can be a useful fundamental research tool, but it should be treated as a **decision-support model**, not an automatic stock-picking engine.
