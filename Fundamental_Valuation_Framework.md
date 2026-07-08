# Technical Documentation: Public-Data Fundamental Equity Valuation Model

**Methodology selected:** Free Cash Flow to Firm Discounted Cash Flow — FCFF DCF  
**Investment philosophy:** Fundamental, intrinsic-value investing  
**Output:** Fair value per share, valuation gap, model limitations, and Buy/Hold/Sell recommendation  

> **Important:** This is a research framework, not investment advice. The model generates systematic valuation signals based on public information and assumptions. Final recommendations should be reviewed by an analyst.

---

## 1. Purpose of the Model

The objective is to build a repeatable equity valuation model that estimates the **fair value of a listed company** using publicly available financial and market data.

The model compares:

```text
Estimated Fair Value per Share
```

against:

```text
Current Market Price
```

to determine whether the company appears:

- Undervalued
- Fairly valued
- Overvalued

The model then produces a rule-based **Buy / Hold / Sell** recommendation.

This approach follows the fundamental investment principle that a stock’s market price can diverge from its intrinsic value. Fundamental analysis estimates the value of a security using company, industry, and economic information, then compares estimated value with market price.

---

## 2. Chosen Valuation Methodology

### 2.1 Selected Method: FCFF Discounted Cash Flow

The model uses a **Free Cash Flow to Firm DCF** methodology.

A DCF model estimates the present value of a company based on its expected future cash flows, discounted back at a rate reflecting their risk. The FCFF model values the entire enterprise, including both debt and equity holders.

```text
Enterprise Value = Σ [FCFF_t / (1 + WACC)^t] + [Terminal Value / (1 + WACC)^n]
```

Then:

```text
Equity Value = Enterprise Value - Net Debt - Minority Interest + Non-operating Assets
```

Finally:

```text
Fair Value per Share = Equity Value / Diluted Shares Outstanding
```

---

## 3. Why FCFF DCF Is Appropriate

FCFF DCF is selected because it is one of the core intrinsic valuation approaches used in fundamental equity research.

DCF is particularly suitable when:

- The company is a going concern.
- The company has positive or forecastable cash flows.
- Long-term business economics matter more than short-term market sentiment.
- The analyst wants to estimate intrinsic value from fundamentals rather than peer multiples.

---

## 4. Public Data Inputs

The model should rely only on publicly available information.

### 4.1 Company Financial Data

Required inputs:

| Data Item | Source Example | Purpose |
|---|---|---|
| Revenue | Annual report, 10-K, 20-F, company filings | Forecast sales growth |
| EBIT / operating income | Income statement | Operating profitability |
| Tax expense / effective tax rate | Income statement | NOPAT calculation |
| Depreciation & amortisation | Cash flow statement | Non-cash add-back |
| Capital expenditure | Cash flow statement | Reinvestment estimate |
| Working capital items | Balance sheet | Working capital forecast |
| Cash and equivalents | Balance sheet | Net debt calculation |
| Short-term and long-term debt | Balance sheet | Enterprise-to-equity bridge |
| Diluted shares outstanding | Annual report / financial data providers | Fair value per share |

### 4.2 Market Data

Required market inputs:

| Data Item | Source Example | Purpose |
|---|---|---|
| Current share price | Exchange, Yahoo Finance, Bloomberg, Refinitiv | Compare with fair value |
| Market capitalisation | Exchange / financial data provider | Cross-check |
| Beta | Yahoo Finance, Bloomberg, Refinitiv | Cost of equity |
| 10-year government yield | Treasury / central bank data | Risk-free rate |
| Equity risk premium | Damodaran / market assumptions | CAPM input |
| Credit spread or cost of debt | Bond yield, debt notes, rating data | WACC input |

---

## 5. Model Structure

The model contains seven main modules:

1. Historical financial cleaning
2. Forecast assumptions
3. Free cash flow to firm calculation
4. Discount rate / WACC
5. Terminal value
6. Equity value bridge
7. Recommendation engine

---

## 6. Module 1 — Historical Financial Cleaning

### 6.1 Objective

Convert raw public financial data into a clean historical financial dataset.

### 6.2 Required Historical Period

Use at least:

- **5 years** for mature companies
- **10 years** where available for cyclical or volatile companies

### 6.3 Key Historical Metrics

The model calculates:

```text
Revenue Growth_t = Revenue_t / Revenue_t-1 - 1

EBIT Margin_t = EBIT_t / Revenue_t

Effective Tax Rate_t = Tax Expense_t / Pre-tax Income_t

Capex / Sales_t = Capex_t / Revenue_t

D&A / Sales_t = D&A_t / Revenue_t

NWC / Sales_t = Net Working Capital_t / Revenue_t
```

These metrics form the basis for the forward forecast.

---

## 7. Module 2 — Forecast Assumptions

### 7.1 Forecast Horizon

Base case forecast horizon:

```text
5 years
```

A 5-year explicit forecast period is commonly used because it balances near-term forecast visibility with long-term uncertainty.

### 7.2 Revenue Forecast

Revenue can be forecast using:

```text
Revenue_t = Revenue_t-1 × (1 + g_t)
```

Where:

```text
g_t = assumed revenue growth rate
```

Recommended approach:

| Company Type | Revenue Forecast Method |
|---|---|
| Mature large-cap | Historical average adjusted for consensus growth |
| High-growth company | Fade growth rate toward industry / GDP growth |
| Cyclical company | Normalised mid-cycle revenue |
| Commodity company | Scenario-based revenue using commodity price assumptions |
| Bank / insurer | Do not use standard FCFF DCF; use excess return or dividend model instead |

### 7.3 Margin Forecast

Operating margin is forecast using:

```text
EBIT_t = Revenue_t × EBIT Margin_t
```

Margin assumptions should reflect:

- Historical EBIT margin
- Industry structure
- Competitive advantage
- Cost inflation
- Operating leverage
- Mean reversion

### 7.4 Tax Rate Forecast

```text
NOPAT_t = EBIT_t × (1 - Tax Rate_t)
```

Use the normalised effective tax rate unless major tax changes are known.

### 7.5 Reinvestment Forecast

Capital expenditure:

```text
Capex_t = Revenue_t × Capex / Sales_t
```

Depreciation and amortisation:

```text
D&A_t = Revenue_t × D&A / Sales_t
```

Change in net working capital:

```text
ΔNWC_t = NWC_t - NWC_t-1
```

---

## 8. Module 3 — Free Cash Flow to Firm Calculation

The model calculates FCFF as:

```text
FCFF_t = EBIT_t × (1 - Tax Rate_t) + D&A_t - Capex_t - ΔNWC_t
```

Where:

- `EBIT × (1 - T)` is after-tax operating profit.
- `D&A` is added back because it is non-cash.
- `Capex` is deducted because it is required investment.
- Working capital investment is deducted because it consumes cash.

---

## 9. Module 4 — Discount Rate / WACC

### 9.1 WACC Formula

The model discounts FCFF using WACC:

```text
WACC = [E / (D + E)] × Cost of Equity + [D / (D + E)] × Cost of Debt × (1 - Tax Rate)
```

Where:

- `E` = market value of equity
- `D` = market value of debt
- `Cost of Equity` = required return by equity holders
- `Cost of Debt` = pre-tax borrowing cost
- `T` = marginal tax rate

### 9.2 Cost of Equity

Use CAPM:

```text
Cost of Equity = Risk-free Rate + Beta × Equity Risk Premium
```

### 9.3 Cost of Debt

Preferred hierarchy:

1. Yield to maturity on traded company bonds
2. Interest expense / average debt
3. Credit-rating-based spread over government yield

### 9.4 Important Consistency Rule

Because this is an FCFF model, cash flows must be discounted using **WACC**, not cost of equity.

In other words:

```text
FCFF → discount using WACC
FCFE → discount using cost of equity
```

---

## 10. Module 5 — Terminal Value

The model uses a Gordon Growth terminal value:

```text
Terminal Value = FCFF_n+1 / (WACC - g)
```

Where:

```text
FCFF_n+1 = FCFF_n × (1 + g)
```

And:

- `g` = terminal growth rate
- `g` should be lower than or equal to long-run nominal GDP growth
- `WACC > g` must always hold

Recommended base case:

| Market | Terminal Growth Assumption |
|---|---:|
| US large-cap | 2.0%–3.0% |
| UK large-cap | 1.5%–2.5% |
| Europe large-cap | 1.5%–2.5% |
| Emerging market company | 3.0%–5.0%, depending on inflation and currency |

---

## 11. Module 6 — Equity Value Bridge

After calculating enterprise value:

```text
Enterprise Value = PV(Explicit FCFF) + PV(Terminal Value)
```

Then:

```text
Equity Value = Enterprise Value - Total Debt + Cash - Minority Interest - Preferred Equity + Investments
```

Then:

```text
Fair Value per Share = Equity Value / Diluted Shares
```

---

## 12. Module 7 — Recommendation Engine

The model compares fair value per share with the current market price.

```text
Valuation Gap = (Fair Value - Current Price) / Current Price
```

### 12.1 Recommendation Rules

| Valuation Gap | Signal |
|---:|---|
| Greater than +20% | Buy |
| +5% to +20% | Moderate Buy / Accumulate |
| -5% to +5% | Hold / Fairly Valued |
| -20% to -5% | Reduce / Moderate Sell |
| Less than -20% | Sell |

### 12.2 Margin of Safety

For a fundamental investment process, a margin of safety is useful because DCF outputs are sensitive to assumptions.

Recommended rule:

```text
Buy only if Fair Value ≥ Market Price × 1.20
```

That means the company must be at least **20% undervalued** before receiving a clear Buy signal.

---

## 13. End-to-End Model Workflow

### Step 1 — Input Ticker

Example:

```text
Ticker: AAPL
Exchange: NASDAQ
Currency: USD
```

### Step 2 — Pull Public Data

Required data:

```text
Income statement
Balance sheet
Cash flow statement
Current share price
Shares outstanding
Beta
Risk-free rate
Equity risk premium
Debt and cash balance
```

### Step 3 — Clean Historical Financials

Standardise:

```text
Revenue
EBIT
Tax rate
D&A
Capex
Net working capital
Debt
Cash
Shares
```

### Step 4 — Build Forecast

Forecast:

```text
Revenue growth
EBIT margin
Tax rate
D&A
Capex
Working capital
FCFF
```

### Step 5 — Estimate WACC

Calculate:

```text
Cost of equity
After-tax cost of debt
Capital structure weights
WACC
```

### Step 6 — Calculate Enterprise Value

Calculate:

```text
PV of explicit FCFF
PV of terminal value
Enterprise value
```

### Step 7 — Convert to Equity Value

Adjust for:

```text
Cash
Debt
Minority interest
Preferred equity
Investments
```

### Step 8 — Calculate Fair Value per Share

```text
Equity value / diluted shares outstanding
```

### Step 9 — Generate Recommendation

Compare:

```text
Fair value per share vs current market price
```

Return:

```text
Buy / Hold / Sell
```

---

## 14. Model Output Template

For each company, the model should return the following result.

### 14.1 Summary Output

```text
Company: [Company Name]
Ticker: [Ticker]
Currency: [Currency]
Valuation Method: FCFF DCF
Current Share Price: [X]
Estimated Fair Value per Share: [Y]
Upside / Downside: [Z%]
Recommendation: [Buy / Hold / Sell]
Confidence Level: [High / Medium / Low]
```

### 14.2 Valuation Breakdown

```text
PV of Explicit Forecast FCFF: [X]
PV of Terminal Value: [Y]
Enterprise Value: [Z]
Net Debt: [A]
Equity Value: [B]
Diluted Shares Outstanding: [C]
Fair Value per Share: [D]
```

### 14.3 Key Assumptions

```text
Forecast Revenue CAGR: [X%]
Terminal Growth Rate: [Y%]
WACC: [Z%]
Normalised EBIT Margin: [A%]
Tax Rate: [B%]
Capex / Sales: [C%]
```

### 14.4 Recommendation Logic

```text
Fair Value per Share: [Y]
Current Market Price: [X]
Valuation Gap: [(Y - X) / X]

If Valuation Gap > 20%:
    Recommendation = Buy
elif Valuation Gap between 5% and 20%:
    Recommendation = Moderate Buy
elif Valuation Gap between -5% and 5%:
    Recommendation = Hold
elif Valuation Gap between -20% and -5%:
    Recommendation = Reduce
else:
    Recommendation = Sell
```

---

## 15. Sensitivity Analysis

Because DCF is assumption-sensitive, the model should include a sensitivity matrix.

### 15.1 WACC vs Terminal Growth Sensitivity

| WACC / Terminal Growth | 1.5% | 2.0% | 2.5% | 3.0% |
|---:|---:|---:|---:|---:|
| 7.0% | Fair value | Fair value | Fair value | Fair value |
| 8.0% | Fair value | Fair value | Fair value | Fair value |
| 9.0% | Fair value | Fair value | Fair value | Fair value |
| 10.0% | Fair value | Fair value | Fair value | Fair value |

### 15.2 Revenue Growth vs Margin Sensitivity

| Revenue CAGR / EBIT Margin | Low Margin | Base Margin | High Margin |
|---|---:|---:|---:|
| Low Growth | Fair value | Fair value | Fair value |
| Base Growth | Fair value | Fair value | Fair value |
| High Growth | Fair value | Fair value | Fair value |

---

## 16. Company-Specific Limitation Framework

The model should automatically generate limitations depending on the chosen company type.

### 16.1 Mature Quality Compounder

Examples: Microsoft, LVMH, Visa, Nestlé

Main limitations:

- Terminal value may dominate total valuation.
- Small changes in WACC or terminal growth can materially affect fair value.
- Market may already price in quality, brand strength, and competitive advantage.
- Accounting earnings may not fully capture intangible asset creation.

### 16.2 Cyclical Company

Examples: miners, energy producers, autos, semiconductors

Main limitations:

- Current earnings may be above or below mid-cycle levels.
- Revenue and margins are highly sensitive to commodity prices, demand cycles, or inventory cycles.
- A single base-case DCF may overstate precision.
- Scenario analysis is more important than point estimate valuation.

### 16.3 Financial Company

Examples: banks, insurers, asset managers

Main limitations:

- FCFF is less meaningful for banks and insurers because debt is part of operating capital.
- Regulatory capital requirements drive distributable cash flow.
- Dividend discount model, excess return model, or price-to-book framework may be more appropriate.
- Interest rate assumptions can dominate valuation.

### 16.4 High-Growth / Early-Stage Company

Examples: unprofitable software, biotech, electric vehicle startups

Main limitations:

- Near-term free cash flow may be negative.
- Valuation depends heavily on distant terminal assumptions.
- Forecast uncertainty is high.
- DCF should be supplemented with scenario-weighted valuation.

### 16.5 Platform / Technology Company

Examples: Alphabet, Meta, Amazon, Tencent

Main limitations:

- Reported capex may include growth investment rather than maintenance investment.
- Stock-based compensation treatment can materially affect free cash flow.
- Regulatory and antitrust risks may not be captured in base-case cash flows.
- Segment-level sum-of-the-parts valuation may be more informative.

---

## 17. Model Governance

### 17.1 Data Quality Checks

Before producing a recommendation, the model should validate:

```text
Revenue is positive.
EBIT is available.
Cash flow statement exists.
Capex is available.
Debt and cash balances are available.
Diluted share count is available.
WACC > terminal growth rate.
Terminal value is not more than 80% of enterprise value unless flagged.
Historical financial data covers at least 5 years.
```

### 17.2 Valuation Quality Score

The model should assign a confidence score.

| Condition | Score Impact |
|---|---:|
| Positive and stable FCFF | +20 |
| Revenue history above 5 years | +10 |
| EBIT margin stable | +10 |
| Low leverage | +10 |
| Terminal value below 70% of EV | +10 |
| High cyclicality | -15 |
| Negative FCFF | -20 |
| Financial company using FCFF | -25 |
| High share-based compensation | -10 |
| WACC close to terminal growth | -20 |

Suggested interpretation:

| Score | Confidence |
|---:|---|
| 75–100 | High |
| 50–75 | Medium |
| Below 50 | Low |

---

## 18. Recommended Implementation Design

### 18.1 Model Components

1. Data ingestion layer
2. Financial statement cleaner
3. Historical ratio calculator
4. Forecast engine
5. WACC engine
6. DCF valuation engine
7. Sensitivity engine
8. Recommendation engine
9. Limitation generator
10. Output report generator

### 18.2 Suggested Python Package Structure

```text
equity_valuation_model/
│
├── config/
│   └── assumptions.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data_loader.py
│   ├── financial_cleaner.py
│   ├── forecast_engine.py
│   ├── wacc_engine.py
│   ├── dcf_engine.py
│   ├── sensitivity.py
│   ├── recommendation.py
│   └── report_generator.py
│
├── outputs/
│   ├── valuation_summary.xlsx
│   └── valuation_report.pdf
│
└── main.py
```

---

## 19. Recommendation Output Example

```text
Company: Example plc
Ticker: EXM LN
Current Share Price: £10.00
Estimated Fair Value per Share: £12.80
Valuation Gap: +28.0%
Recommendation: Buy
Confidence: Medium
```

**Investment View:**  
The model estimates that the company is trading below intrinsic value. The positive valuation gap is mainly driven by resilient forecast free cash flow, stable operating margins, and moderate leverage.

**Key Risks:**  
The valuation is sensitive to terminal growth and WACC assumptions. If long-term revenue growth slows below the base-case assumption, the fair value estimate would fall materially.

---

## 20. Final Recommendation Logic

The model’s decision rule is:

```text
If Fair Value materially exceeds Market Price:
    Buy

If Fair Value is close to Market Price:
    Hold

If Fair Value is materially below Market Price:
    Sell
```

With thresholds:

```text
Buy: upside > 20%
Moderate Buy: upside between 5% and 20%
Hold: valuation gap between -5% and +5%
Reduce: downside between -5% and -20%
Sell: downside > 20%
```

---

## 21. Summary

This technical design uses an **FCFF DCF model** as the core intrinsic valuation engine. It is suitable for fundamental equity research because it values a company based on its future operating cash flows rather than short-term market sentiment.

The model produces:

- Fair value per share
- Upside / downside versus market price
- Buy / Hold / Sell recommendation
- Sensitivity analysis
- Company-specific model limitations
- Confidence score

The key strength of the model is that it is transparent, repeatable, and based on public information. The key weakness is that DCF valuation is highly sensitive to forecast assumptions, especially WACC, terminal growth, and long-term margin assumptions.
