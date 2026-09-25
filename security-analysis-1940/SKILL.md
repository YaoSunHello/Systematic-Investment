---
name: security-analysis-1940
description: Analyze bonds, preferred shares, and common stocks using conservative security analysis for financial strength, valuation, margin of safety, risks, and memos.
---

# Security Analysis Workflow

## Purpose

Use this skill to conduct disciplined fundamental security analysis using the workflow and reference notes in this folder.

The goal is not to summarize a book. The goal is to support repeatable analysis of bonds, preferred shares, and common stocks by separating facts, calculations, assumptions, and analyst judgement.

Do not treat historical rules as mechanically applicable to modern securities. Flag where accounting, legal, tax, industry, or market context requires current research.

## Required Inputs

Request or identify, where available:

- security type and capital-structure position
- issuer or company financial statements and reporting periods
- market price, shares outstanding, debt, cash, and other senior claims
- interest, dividend, lease, and fixed-charge obligations
- historical revenue, profit, cash flow, and capital expenditure
- asset values and material accounting adjustments
- management guidance, segment information, and industry context
- investment horizon, required return, and valuation date

If information is missing, continue only with supportable analysis, identify the limitation clearly, and do not invent financial data.

## Procedure

### 1. Define the Question

Identify the security, security type, valuation date, currency, investor objective, available information, and required output format.

### 2. Separate Investment From Speculation

Assess whether the conclusion depends mainly on demonstrable financial strength, sustainable earning power, asset protection, contractual claims, market expectations, uncertain future growth, or price momentum.

Do not classify a security as an investment solely because its price has fallen.

### 3. Map Capital-Structure Priority

Map claims in order of seniority:

1. secured obligations
2. senior unsecured obligations
3. subordinated obligations
4. preferred shares
5. common shares

Identify all claims senior to the security under analysis and explain how they affect downside protection.

### 4. Normalize Financial Information

Review reported financials for non-recurring items, acquisition effects, accounting-policy changes, unusual working-capital movements, capitalized costs, exceptional gains or losses, and differences between accounting profit and cash generation.

Show each adjustment separately. Preserve both reported and adjusted figures.

### 5. Assess Financial Strength

Evaluate liquidity, leverage, maturity profile, interest coverage, fixed-charge coverage, asset coverage, cash-flow resilience, refinancing dependency, off-balance-sheet obligations, and contingent liabilities.

Do not treat a single ratio as conclusive.

### 6. Estimate Sustainable Earning Power

Use a representative operating history when supplied. Consider cyclicality, variability, customer or product concentration, maintenance capital expenditure, dilution, pension obligations, and structural changes in the business.

Explain why the selected earnings measure is representative.

### 7. Value the Security

Choose only methods appropriate to the security and available data:

- asset-value analysis
- earnings-power valuation
- discounted cash-flow analysis
- yield and coverage analysis
- recovery-value analysis
- conservative comparable valuation

For each method, show inputs, formula, assumptions, calculation, resulting value, and key limitations.

### 8. Assess Margin of Safety

Compare conservative estimated value with observed market price. Report market price, central valuation, downside valuation, upside valuation, implied margin of safety, and assumptions responsible for the result.

A valuation gap is not automatically a margin of safety. Explain the source and reliability of the protection.

### 9. Run Sensitivity and Downside Analysis

Test variables most likely to invalidate the conclusion, including revenue, margins, normalized earnings, discount rate, exit multiple, interest expense, refinancing cost, and asset recovery value.

Use clear scenarios rather than false precision.

### 10. Conclude

Classify the conclusion as one of:

- potentially suitable for further investigation
- insufficient information
- valuation dependent
- financially weak
- speculative
- outside the analyst's circle of competence

Treat the output as research support, not personalized investment advice.

## Output Format

For full analyses, use `assets/investment-memo-template.md`. For shorter reviews, use `assets/security-analysis-template.md`.

Include these sections:

1. executive conclusion
2. security and capital structure
3. financial-strength assessment
4. earnings-quality adjustments
5. sustainable earning power
6. valuation methods
7. margin-of-safety assessment
8. downside and sensitivity analysis
9. key risks and disconfirming evidence
10. missing information
11. source and assumption register

For each important conclusion, label whether it is a reported fact, calculated result, assumption, or analyst judgement.

## Reference Routing

Consult only the files needed for the task:

- Use `references/analytical-principles.md` for investment versus speculation, evidence standards, and decision discipline.
- Use `references/fixed-income-analysis.md` for bonds and other fixed claims.
- Use `references/equity-analysis.md` for common-stock and preferred-stock analysis.
- Use `references/financial-normalisation.md` for adjustments to reported financials.
- Use `references/valuation-methods.md` for valuation approaches and formulas.
- Use `references/margin-of-safety.md` for margin-of-safety interpretation and downside framing.
- Use `references/source-map.md` to verify book-section support. If a principle is not mapped there, identify it as unsupported by source notes rather than inventing a citation.

## Guardrails

- Never fabricate financial figures, quotations, citations, or book references.
- Do not reproduce lengthy passages from copyrighted material.
- Do not include confidential company, issuer, portfolio, client, or credential data in the reusable skill.
- Do not present historical analytical conventions as current regulation.
- Distinguish reported facts, calculations, assumptions, and judgement.
- Flag legal, tax, accounting, and regulatory questions for qualified review.
- Do not issue personalized investment advice.
