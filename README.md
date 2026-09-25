1. Decide exactly what the Skill should do

Avoid the vague objective:

“Know everything in Security Analysis.”

Use a repeatable workflow instead:

“Analyse bonds, preference shares and ordinary shares using a Graham-and-Dodd-inspired process, separating investment from speculation, assessing asset coverage, earnings power, financial strength and margin of safety.”

For your own investment-risk work, I would give the Skill six functions:

Classify the security and analytical objective.
Normalise the company’s financial information.
Assess earnings quality and balance-sheet strength.
Value the security using several conservative methods.
Calculate the margin of safety.
Produce a structured investment memorandum with risks, missing information and sensitivity analysis.

That makes it an analytical Skill rather than a book-summary chatbot.

2. Create the folder structure

Create this structure locally:

Plain Text
security-analysis-1940/
├── SKILL.md
├── references/
│ ├── analytical-principles.md
│ ├── fixed-income-analysis.md
│ ├── equity-analysis.md
│ ├── financial-normalisation.md
│ ├── valuation-methods.md
│ ├── margin-of-safety.md
│ └── source-map.md
├── assets/
│ ├── security-analysis-template.md
│ └── investment-memo-template.md
└── scripts/
└── valuation_checks.py
Show less

Only SKILL.md is required. The other folders are optional but useful for keeping the main instruction file concise.

3. Convert the book into your own reference notes

Work through the book section by section and create your own concise notes. Do not make references/ a verbatim copy of the book.

For every relevant chapter, capture:

Markdown
# Topic
 
## Core principle
Explain the principle in your own words.
 
## Analytical purpose
What decision does this principle support?
 
## Required inputs
List the financial data required.
 
## Calculation or test
Describe the calculations and decision tests.
 
## Warning signs
List conditions requiring further investigation.
 
## Limitations
Explain when the principle may not apply reliably.
 
## Source map
Record the edition, chapter and page references for verification.
Show more lines

A useful source-map.md format would be:

Markdown
# Source Map
 
| Internal topic | Book section | Purpose |
|---|---|---|
| Investment versus speculation | Part/Chapter/Page | Security classification |
| Fixed-value investments | Part/Chapter/Page | Bond and preference-share analysis |
| Earnings normalisation | Part/Chapter/Page | Sustainable earnings assessment |
| Balance-sheet analysis | Part/Chapter/Page | Asset protection and solvency |
| Margin of safety | Part/Chapter/Page | Investment decision discipline |
``
Show more lines

Fill in the exact references from the copy you legally own. This preserves traceability without embedding unnecessary copyrighted text.

4. Create the main SKILL.md

Use the following as your starting file:

Markdown
---
name: security-analysis-1940
description: Analyse bonds, preference shares and ordinary shares using a conservative Graham-and-Dodd-inspired security analysis workflow. Use this skill when asked to assess financial strength, earnings quality, asset coverage, intrinsic value, downside protection, margin of safety or to produce a structured security analysis memorandum.
---
 
# Security Analysis Workflow
 
## Purpose
 
Conduct disciplined fundamental security analysis using the analytical
principles documented in the references folder.
 
Do not treat historical rules as mechanically applicable to modern securities.
Distinguish facts, calculations, assumptions and analyst judgement.
 
## Required inputs
 
Request or identify, where available:
 
- security type and capital-structure position
- financial statements and reporting periods
- market price and securities outstanding
- debt, cash and other senior claims
- interest, dividend and fixed-charge obligations
- historical revenue, profit and cash flow
- asset values and material accounting adjustments
- management guidance and relevant industry information
- investment horizon and required return
 
If information is missing, continue with the available information but clearly
identify the limitation. Never invent financial data.
 
## Analysis procedure
 
### Step 1: Define the analytical question
 
Identify:
 
- the security being analysed
- whether it is debt, preference equity or ordinary equity
- the investor's objective
- the valuation date
- the relevant currency
- the required output format
 
### Step 2: Separate investment from speculation
 
Assess whether the conclusion depends primarily on:
 
- demonstrable financial strength
- sustainable earning power
- asset protection
- contractual claims
- market expectations
- uncertain future growth
 
Do not label a security as an investment solely because its price has fallen.
 
### Step 3: Establish capital-structure priority
 
Map:
 
1. secured obligations
2. senior unsecured obligations
3. subordinated obligations
4. preference shares
5. ordinary shares
 
Identify the claims senior to the security under analysis.
 
### Step 4: Normalise financial information
 
Review the supplied financial statements for:
 
- non-recurring income and expenses
- acquisition-related items
- accounting-policy changes
- exceptional gains and losses
- unusual working-capital movements
- capitalised costs
- differences between profit and cash generation
- structural changes in the business
 
Show every adjustment separately. Preserve both reported and adjusted figures.
 
### Step 5: Analyse financial strength
 
Evaluate:
 
- liquidity
- leverage
- debt maturity profile
- fixed-charge coverage
- interest coverage
- asset coverage
- cash-flow resilience
- refinancing dependency
- off-balance-sheet or contingent obligations
 
Do not treat a single ratio as conclusive.
 
### Step 6: Estimate sustainable earning power
 
Use a sufficiently representative history where supplied.
 
Consider:
 
- through-cycle earnings
- cyclicality
- variability
- dependence on favourable market conditions
- customer or product concentration
- maintenance capital expenditure
- dilution
- pension and other long-term obligations
 
Explain why the selected earnings measure is representative.
 
### Step 7: Value the security
 
Select methods appropriate to the security and available data:
 
- asset-value analysis
- earnings-power valuation
- discounted cash-flow analysis
- yield and coverage analysis
- recovery-value analysis
- conservative comparable valuation
 
Do not force every method onto every security.
 
For each method, show:
 
- inputs
- formula
- assumptions
- calculation
- resulting value
- principal limitations
 
### Step 8: Assess margin of safety
 
Compare conservative estimated value with the observed market price.
 
Report:
 
- market price
- central valuation
- downside valuation
- upside valuation
- implied margin of safety
- assumptions responsible for the result
 
A valuation difference is not automatically a margin of safety. Explain the
source and reliability of the protection.
 
### Step 9: Conduct sensitivity and downside analysis
 
Test the variables most capable of invalidating the conclusion, including:
 
- revenue
- operating margin
- normalised earnings
- discount rate
- exit multiple
- interest expense
- refinancing cost
- asset recovery value
 
Use clearly labelled scenarios rather than pretending to provide a precise
point estimate.
 
### Step 10: Produce the conclusion
 
Classify the conclusion as:
 
- potentially suitable for further investigation
- insufficient information
- valuation dependent
- financially weak
- speculative
- outside the analyst's circle of competence
 
Do not issue personalised investment advice.
 
## Output format
 
Produce these sections:
 
1. Executive conclusion
2. Security and capital structure
3. Financial-strength assessment
4. Earnings-quality adjustments
5. Sustainable earning power
6. Valuation methods
7. Margin-of-safety assessment
8. Downside and sensitivity analysis
9. Key risks and disconfirming evidence
10. Missing information
11. Source and assumption register
 
For every important conclusion, distinguish:
 
- reported fact
- calculated result
- assumption
- analyst judgement
 
## Reference routing
 
Consult the relevant file when needed:
 
- `references/analytical-principles.md`
- `references/fixed-income-analysis.md`
- `references/equity-analysis.md`
- `references/financial-normalisation.md`
- `references/valuation-methods.md`
- `references/margin-of-safety.md`
 
Use `assets/investment-memo-template.md` for full company analyses.
Use `assets/security-analysis-template.md` for shorter reviews.
 
## Guardrails
 
- Never fabricate financial figures, quotations or book references.
- Do not present historical analytical conventions as current regulation.
- Flag accounting, legal, tax and market information requiring current research.
- Treat outputs as research support rather than personalised investment advice.
- Do not reproduce lengthy passages from copyrighted material.
Show more lines

The YAML description is particularly important because Claude uses it to determine when the Skill should be invoked. Official guidance recommends a specific description explaining both what the Skill does and when it should be used.

5. Add an investment memorandum template

Create assets/investment-memo-template.md:

Markdown
# Security Analysis Memorandum
 
## 1. Executive conclusion
 
## 2. Analytical scope
- Security:
- Security type:
- Valuation date:
- Market price:
- Currency:
- Investor objective:
 
## 3. Business and security description
 
## 4. Capital structure
| Claim | Amount | Priority | Key terms |
 
## 5. Financial strength
| Measure | Reported | Adjusted | Interpretation |
 
## 6. Earnings normalisation
| Item | Reported effect | Adjustment | Rationale |
 
## 7. Sustainable earning power
 
## 8. Valuation
| Method | Value | Key assumptions | Limitations |
 
## 9. Margin of safety
- Conservative value:
- Market price:
- Estimated margin of safety:
- Source of downside protection:
 
## 10. Sensitivity analysis
 
## 11. Principal risks
 
## 12. Disconfirming evidence
 
## 13. Missing information
 
## 14. Assumptions and sources
Show more lines
6. Add simple calculation support

The optional scripts/valuation_checks.py can standardise calculations:

Python
def margin_of_safety(intrinsic_value: float, market_price: float) -> float:
if intrinsic_value <= 0:
raise ValueError("Intrinsic value must be positive.")
return (intrinsic_value - market_price) / intrinsic_value
 
 
def interest_coverage(operating_profit: float, interest_expense: float) -> float:
if interest_expense <= 0:
raise ValueError("Interest expense must be positive.")
return operating_profit / interest_expense
 
 
def net_debt(total_debt: float, cash: float) -> float:
return total_debt - cash
 
 
def enterprise_value(
market_capitalisation: float,
total_debt: float,
cash: float,
preference_equity: float = 0.0,
minority_interest: float = 0.0,
) -> float:
return (
market_capitalisation
+ total_debt
+ preference_equity
+ minority_interest
- cash
)
Show more lines

Keep formulas transparent and require Claude to show inputs rather than returning unexplained outputs.

7. Test the Skill with realistic prompts

Create a small evaluation set:

Test 1: Missing data
Plain Text
Analyse this company using the Security Analysis framework.
I only have the latest income statement and current share price.
Show more lines

Expected behaviour:

performs only supportable analysis;
identifies missing balance-sheet and historical information;
does not fabricate figures;
avoids a definitive valuation.
Test 2: Bond analysis
Plain Text
Assess whether this corporate bond has adequate downside protection.
Use the attached issuer financial statements and bond terms.
Show more lines

Expected behaviour:

prioritises fixed charges, capital structure, coverage and recovery;
does not use an equity-only valuation framework.
Test 3: Normalisation
Plain Text
Normalise the company's earnings and explain every adjustment.
Show more lines

Expected behaviour:

separates reported numbers from adjustments;
flags judgemental adjustments;
retains an audit trail.
Test 4: Challenging the thesis
Plain Text
Here is my valuation model. Identify evidence that could invalidate my
investment conclusion.
Show more lines

Expected behaviour:

actively searches for disconfirming evidence;
identifies sensitivity to assumptions;
avoids simply endorsing the user’s thesis.
Test 5: Modern application
Plain Text
Apply the framework to a software company with significant intangible assets.
Show more lines

Expected behaviour:

recognises where asset-based historical methods are less informative;
does not mechanically apply industrial-company rules;
explains the limitations.

Anthropic’s published Skill-creator process recommends drafting the Skill, developing test prompts, evaluating the outputs qualitatively and quantitatively, and then iterating.

8. Package and upload it

Package the folder itself, normally as:

Plain Text
security-analysis-1940.zip
Show more lines

Before packaging, check:

the top-level folder is security-analysis-1940;
it contains SKILL.md;
the YAML name is also security-analysis-1940;
all referenced files exist;
filenames use consistent capitalisation;
there are no confidential company files or credentials;
you are permitted to use every included source.

Custom Skills can be provided as a directory containing SKILL.md and supporting files, and uploaded as a ZIP archive or as individual files where the relevant Claude product supports custom Skills.

9. Use this prompt with Claude’s Skill Creator

Claude’s official Skills page indicates that the Skill Creator can generate the folder structure, format SKILL.md and bundle resources.

Paste this into Claude together with your own notes, not an unauthorised book copy:

Plain Text
Create a custom Claude Skill called "security-analysis-1940".
 
Its purpose is to conduct conservative, evidence-based analysis of bonds,
preference shares and ordinary shares using a Graham-and-Dodd-inspired
framework.
 
The Skill must:
 
1. classify the security before choosing an analytical method;
2. map the security's position in the capital structure;
3. distinguish investment from speculation;
4. normalise reported financial information;
5. analyse financial strength, fixed-charge coverage and asset protection;
6. estimate sustainable earning power;
7. apply only valuation methods appropriate to the security;
8. calculate and explain the margin of safety;
9. run downside and sensitivity analysis;
10. identify missing information and disconfirming evidence;
11. distinguish facts, calculations, assumptions and analyst judgement;
12. never fabricate financial data or book quotations;
13. produce a structured security-analysis memorandum;
14. treat outputs as research support, not personalised investment advice.
 
Keep SKILL.md concise and place detailed material in references.
Create separate reference files for analytical principles, fixed-income
analysis, equity analysis, financial normalisation, valuation methods and
margin of safety.
 
Create reusable short-form and full investment-memorandum templates.
Include test prompts covering missing data, bond analysis, earnings
normalisation, thesis challenge and analysis of an intangible-heavy company.
 
Use only the source notes I provide. Do not reproduce lengthy passages from
the original book. When a principle cannot be traced to my notes, identify it
as unsupported rather than inventing a citation.
Show more lines
Important copyright and governance point

Use a copy you acquired lawfully and convert it into your own analytical notes and workflows. Do not distribute a Skill containing a full scanned book, extensive verbatim extracts or a substitute reconstruction of the text. For an internal investment workflow, also keep proprietary portfolio data, issuer materials and company analysis outside the distributable core Skill unless your organisation has approved their inclusion.

This approach also fits your existing Claude usage: you have previously positioned Claude as a research and engineering assistant that turns analytical methods into transparent code, documentation and reusable workflows. AI Application (AutoRecovered) describes the same pattern of supplying requirements, supporting materials and iterative guidance rather than relying on a single broad prompt.
