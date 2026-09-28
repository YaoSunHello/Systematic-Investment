---
name: advanced-portfolio-management
description: "Apply Paleologo-style active equity portfolio management: size ideas, decompose factor risk, hedge exposures, attribute PnL, manage drawdowns, and set leverage."
---

# Advanced Portfolio Management

## Purpose

Use this skill to help a fundamental equity analyst or portfolio manager turn investment ideas into a risk-aware, resilient active portfolio. The skill is based on Giuseppe A. Paleologo's *Advanced Portfolio Management: A Quant's Guide for Fundamental Investors* and should be used as an operating workflow, not as a book-summary generator.

The local source book is in `Active Portfolio Management/`. The uploaded PDF appears to be image-scanned, so do not invent page-level citations or direct quotations unless the user provides OCR text or notes. Keep outputs paraphrased and analytical.

## Core Operating Principles

- Start from the PM's edge: the names, events, themes, or valuation views where the investor claims skill.
- Hedge or constrain the rest: market, country, industry, beta, volatility, momentum, crowdedness, short-interest, and valuation-factor exposures should be intentional, not accidental.
- Size ideas from signal strength, expected return, risk, correlation, liquidity, horizon, and implementation cost.
- Distinguish factor PnL from idiosyncratic PnL before judging stock selection or timing.
- Prefer transparent heuristics before optimization; use optimization when constraints or scale make heuristics insufficient.
- Review outcomes with a learning loop: selection, sizing, timing, trade execution, and risk-budget use.
- Treat leverage, drawdown controls, and tail-risk policies as business-survival decisions, not just return enhancers.

## Standard Workflow

1. Define the portfolio problem.
   Identify mandate, universe, benchmark or absolute-return target, long/short rules, gross and net exposure limits, liquidity constraints, time horizon, and available data.

2. Inventory the alpha.
   List each idea with direction, expected return or conviction, horizon, catalyst, thesis category, confidence, liquidity, borrow/financing concerns, and what would falsify it.

3. Map risk exposures.
   Decompose the book across market, country, industry, beta, volatility, momentum, valuation, size, short interest, crowdedness or active-manager-holdings proxies, and custom thematic factors.

4. Size positions.
   Use risk-based sizing when expected returns are uncertain; use expected-return sizing only when forecasts are calibrated. Flag concentrated single-name, single-factor, and single-theme risks.

5. Separate alpha from environment.
   Identify which returns are intended stock-specific bets and which are passive exposure to the trading or macro environment. Recommend hedges or constraints for unintended exposures.

6. Attribute performance.
   Break PnL into factor and idiosyncratic components, then analyze idiosyncratic PnL through selection, sizing, timing, diversification, event handling, and trading costs.

7. Stress the portfolio.
   Test factor shocks, correlation spikes, liquidity withdrawal, borrow recalls, crowded unwind, event gaps, stop-loss behavior, and leverage reduction.

8. Decide and document.
   State actions as maintain, resize, hedge, diversify, exit, or research further. Separate measured facts, model assumptions, judgement, and open data gaps.

## References

Read only what is needed:

- `references/framework.md` for the book-based analytical map and recurring portfolio questions.
- `references/deliverables.md` for memo, dashboard, and review formats.

## Guardrails

- Do not provide personalized financial advice.
- Do not fabricate holdings, returns, factor exposures, borrow costs, transaction costs, or model outputs.
- Do not treat factor models as truth; they are useful decompositions with estimation error, missing variables, and regime sensitivity.
- Do not optimize a portfolio without explaining objective function, constraints, covariance assumptions, forecast assumptions, and turnover/liquidity treatment.
- Do not copy long passages from the copyrighted book into outputs or skill resources.
