diff --git a/security-analysis-1940/SKILL.md b/security-analysis-1940/SKILL.md
index 7bf1d26..a685bf2 100644
--- a/security-analysis-1940/SKILL.md
+++ b/security-analysis-1940/SKILL.md
@@ -1,17 +1,17 @@
 ---
 name: security-analysis-1940
-description: Analyze bonds, preferred shares, and common stocks using conservative security analysis for financial strength, valuation, margin of safety, risks, and memos.
+description: Apply Graham & Dodd's "Security Analysis" (1940) framework to bonds, preferred shares, and common stocks — financial-strength tests, earnings-coverage minimums, net-current-asset and earnings-power valuation, margin of safety, and downside scenarios, written up as a labelled investment memo. Use this whenever the user asks whether a bond or preferred is safe, whether a stock has a margin of safety, wants a security analyzed from a 10-K/annual report/filing, wants coverage ratios or a liquidation-value check run, or asks for an investment memo or credit-style writeup on a specific issuer — even if they don't name Graham, Dodd, or "security analysis" explicitly.
 ---
 
-# Security Analysis Workflow
+# Security Analysis Workflow (Graham & Dodd, 1940)
 
 ## Purpose
 
-Use this skill to conduct disciplined fundamental security analysis using the workflow and reference notes in this folder.
+Conduct disciplined fundamental security analysis using the actual tests, minimums, and reasoning from Graham & Dodd's *Security Analysis*, 2nd edition (1940) — not a generic memo dressed up with the book's name. Every reference file in this skill carries specific, citable content from the book (see `references/source-map.md`); consult them rather than reconstructing the framework from general knowledge.
 
-The goal is not to summarize a book. The goal is to support repeatable analysis of bonds, preferred shares, and common stocks by separating facts, calculations, assumptions, and analyst judgement.
+The goal is repeatable analysis of bonds, preferred shares, and common stocks that separates facts, calculations, assumptions, and analyst judgement.
 
-Do not treat historical rules as mechanically applicable to modern securities. Flag where accounting, legal, tax, industry, or market context requires current research.
+Graham & Dodd wrote for 1940s industrial and railroad capital structures. Their reasoning about safety, earning power, and margin of safety still holds, but several of their specific tests were built for a balance sheet and capital structure that many of today's securities do not have. **Do not apply the historical quantitative minimums as pass/fail thresholds for modern securities without adjustment.** See "Where the 1940 Framework Breaks" below — flag the breakpoint explicitly in the memo rather than silently applying or silently ignoring the historical test.
 
 ## Required Inputs
 
@@ -28,6 +28,17 @@ Request or identify, where available:
 
 If information is missing, continue only with supportable analysis, identify the limitation clearly, and do not invent financial data.
 
+## Where the 1940 Framework Breaks
+
+Name the breakpoint in the memo when it applies — do not just gesture at "modern context differs." These are the recurring, predictable places:
+
+- **Asset-value analysis on asset-light businesses.** Graham & Dodd's balance-sheet and net-current-asset tests (`references/valuation-methods.md`, `references/margin-of-safety.md`) assume tangible, separable assets. A software, platform, or brand-driven business may have little balance-sheet asset value relative to its earning power; NCAV and liquidation-value screens will understate it or be meaningless. Use earnings-power and cash-flow methods instead, and say why the asset test doesn't apply — see `references/equity-analysis.md`.
+- **Capitalized operating leases (IFRS 16 / ASC 842).** Modern balance sheets already capitalize most lease obligations as debt with an offsetting right-of-use asset. Graham & Dodd's fixed-charge coverage treated lease rentals as an off-balance-sheet charge to be added back (`references/fixed-income-analysis.md`). Check which convention the filing uses before adding lease expense a second time.
+- **Share-based compensation.** Treating SBC as a non-cash add-back (common modern practice) is the kind of earnings adjustment Graham & Dodd's income-account analysis explicitly warns against when it hides a recurring cost of the business (`references/financial-normalisation.md`). It dilutes shareholders every year it's granted; normalize it as a real cost unless there's a specific reason not to.
+- **Buybacks as the dividend substitute.** The dividend-factor and stock-equity-cushion reasoning in `references/equity-analysis.md` assumes dividends are the primary distribution. Many modern issuers distribute mainly through buybacks. Treat sustained buybacks as economically equivalent to a dividend for capital-return analysis, but note they are discretionary and reversible in a way a declared dividend is not.
+- **Preferred shares vs. modern hybrid/contingent capital.** The 1940 preferred-stock chapters (`references/equity-analysis.md`) describe industrial and utility preferred stock with discretionary but non-forfeitable dividends. Most preferred-like instruments an analyst meets today are bank AT1/contingent-convertible instruments with regulatory loss-absorption features (coupon cancellation at supervisory discretion, conversion or writedown at a trigger) that have no analogue in the book. The discretionary-dividend theory transfers; the loss-absorption mechanics do not — treat AT1 as its own instrument class and say so.
+- **Multi-year earnings averaging in a structurally growing or shrinking business.** The 7-to-10-year averaging period Graham & Dodd recommend for normalizing earnings (`references/equity-analysis.md`) assumes a business fluctuating around a stable trend. For a business with a genuine structural growth or decline rate, a long straight average understates or overstates current earning power — use a trend line or the most recent representative period instead, and say which you used and why.
+
 ## Procedure
 
 ### 1. Define the Question
@@ -36,7 +47,7 @@ Identify the security, security type, valuation date, currency, investor objecti
 
 ### 2. Separate Investment From Speculation
 
-Assess whether the conclusion depends mainly on demonstrable financial strength, sustainable earning power, asset protection, contractual claims, market expectations, uncertain future growth, or price momentum.
+Apply the book's own test (`references/analytical-principles.md`): does the conclusion, on thorough analysis, promise safety of principal and a satisfactory return? If so it is investment; if the case depends on the market's future opinion, price momentum, or a story about growth that isn't yet supported by the record, it is speculation — regardless of how strong or well-known the company is.
 
 Do not classify a security as an investment solely because its price has fallen.
 
@@ -50,44 +61,44 @@ Map claims in order of seniority:
 4. preferred shares
 5. common shares
 
-Identify all claims senior to the security under analysis and explain how they affect downside protection.
+Identify all claims senior to the security under analysis and explain how they affect downside protection. For a bond or preferred, remember Graham & Dodd's central claim: safety comes from the strength of the enterprise, not from the specific lien (`references/fixed-income-analysis.md`) — a mortgage on property that can't be sold at a fair price in a default is not protection.
 
 ### 4. Normalize Financial Information
 
-Review reported financials for non-recurring items, acquisition effects, accounting-policy changes, unusual working-capital movements, capitalized costs, exceptional gains or losses, and differences between accounting profit and cash generation.
+Review reported financials for non-recurring items, acquisition effects, accounting-policy changes, unusual working-capital movements, capitalized costs, exceptional gains or losses, share-based compensation, and differences between accounting profit and cash generation. See `references/financial-normalisation.md` for the specific devices the book flags for inflating or deflating per-share earnings.
 
 Show each adjustment separately. Preserve both reported and adjusted figures.
 
 ### 5. Assess Financial Strength
 
-Evaluate liquidity, leverage, maturity profile, interest coverage, fixed-charge coverage, asset coverage, cash-flow resilience, refinancing dependency, off-balance-sheet obligations, and contingent liabilities.
+Evaluate liquidity, leverage, maturity profile, interest coverage, fixed-charge coverage, asset coverage, cash-flow resilience, refinancing dependency, off-balance-sheet obligations, and contingent liabilities. For bonds and preferred shares, compute coverage on the **total-deductions (over-all) basis** — all fixed charges senior to and including the claim under analysis, never the security's charge in isolation — and compare against the book's minimums in `references/fixed-income-analysis.md`, naming them as a historical reference point rather than a current regulatory or statutory standard.
 
 Do not treat a single ratio as conclusive.
 
 ### 6. Estimate Sustainable Earning Power
 
-Use a representative operating history when supplied. Consider cyclicality, variability, customer or product concentration, maintenance capital expenditure, dilution, pension obligations, and structural changes in the business.
+Use a representative operating history when supplied — Graham & Dodd's own practice is a 7-to-10-year average, adjusted for genuine structural change (see "Where the 1940 Framework Breaks"). Consider cyclicality, variability, customer or product concentration, maintenance capital expenditure, dilution, pension obligations, and structural changes in the business.
 
-Explain why the selected earnings measure is representative.
+Explain why the selected earnings measure is representative — an average is only informative if the individual years cluster around it; an average of unrelated figures is not a measure of earning power (`references/equity-analysis.md`).
 
 ### 7. Value the Security
 
 Choose only methods appropriate to the security and available data:
 
-- asset-value analysis
+- asset-value / net-current-asset-value analysis
 - earnings-power valuation
 - discounted cash-flow analysis
 - yield and coverage analysis
 - recovery-value analysis
 - conservative comparable valuation
 
-For each method, show inputs, formula, assumptions, calculation, resulting value, and key limitations.
+For each method, show inputs, formula, assumptions, calculation, resulting value, and key limitations. Use `scripts/valuation_checks.py` for the coverage, net-debt, and enterprise-value arithmetic so the numbers are computed, not estimated in prose.
 
 ### 8. Assess Margin of Safety
 
 Compare conservative estimated value with observed market price. Report market price, central valuation, downside valuation, upside valuation, implied margin of safety, and assumptions responsible for the result.
 
-A valuation gap is not automatically a margin of safety. Explain the source and reliability of the protection.
+A valuation gap is not automatically a margin of safety (`references/margin-of-safety.md`). Explain the source and reliability of the protection — is it asset coverage, an earnings cushion over fixed charges, or simply that a DCF's central case comes in above price? The last one is the weakest and should be named as such.
 
 ### 9. Run Sensitivity and Downside Analysis
 
@@ -132,20 +143,25 @@ For each important conclusion, label whether it is a reported fact, calculated r
 
 Consult only the files needed for the task:
 
-- Use `references/analytical-principles.md` for investment versus speculation, evidence standards, and decision discipline.
-- Use `references/fixed-income-analysis.md` for bonds and other fixed claims.
-- Use `references/equity-analysis.md` for common-stock and preferred-stock analysis.
-- Use `references/financial-normalisation.md` for adjustments to reported financials.
-- Use `references/valuation-methods.md` for valuation approaches and formulas.
+- Use `references/analytical-principles.md` for investment versus speculation, the concept of intrinsic value, and decision discipline.
+- Use `references/fixed-income-analysis.md` for bonds and other fixed claims, including the historical coverage minimums and the total-deductions method.
+- Use `references/equity-analysis.md` for common-stock and preferred-stock theory, the earnings-record test, and the growth-company critique.
+- Use `references/financial-normalisation.md` for adjustments to reported financials and the specific devices used to distort per-share earnings.
+- Use `references/valuation-methods.md` for valuation approaches, including net-current-asset value and earnings-power valuation.
 - Use `references/margin-of-safety.md` for margin-of-safety interpretation and downside framing.
-- Use `references/source-map.md` to verify book-section support. If a principle is not mapped there, identify it as unsupported by source notes rather than inventing a citation.
+- Use `scripts/valuation_checks.py` for coverage, net-debt, and enterprise-value calculations.
+- Use `references/source-map.md` to verify book-section support before citing a chapter or page.
+
+## Citation Policy
+
+`references/source-map.md` lists the principles that carry a real edition/chapter/page citation from the 1940 second edition. When a memo states a principle that is mapped there, cite it plainly (e.g., "Graham & Dodd, Ch. VIII, p.128") — do not hedge language you can actually support. When a principle is *not* mapped there — including ordinary financial-analysis technique that doesn't come from this specific book — present it as standard analytical practice without a book citation, and do not invent a chapter or page number. Never manufacture a citation to sound more authoritative; an unsupported claim stated plainly as your own analysis is more honest than a fabricated reference.
 
 ## Guardrails
 
 - Never fabricate financial figures, quotations, citations, or book references.
 - Do not reproduce lengthy passages from copyrighted material.
 - Do not include confidential company, issuer, portfolio, client, or credential data in the reusable skill.
-- Do not present historical analytical conventions as current regulation.
+- Do not present historical analytical conventions (statutory minimums, legal-list rules, 1940s tax and accounting treatment) as current regulation.
 - Distinguish reported facts, calculations, assumptions, and judgement.
 - Flag legal, tax, accounting, and regulatory questions for qualified review.
 - Do not issue personalized investment advice.
diff --git a/security-analysis-1940/references/analytical-principles.md b/security-analysis-1940/references/analytical-principles.md
index c2e9224..2148f1d 100644
--- a/security-analysis-1940/references/analytical-principles.md
+++ b/security-analysis-1940/references/analytical-principles.md
@@ -1,24 +1,36 @@
 # Analytical Principles
 
+Source: Graham, Benjamin, and David L. Dodd. *Security Analysis: Principles and Technique*, 2nd ed. New York: McGraw-Hill, 1940. Citations below are to this edition unless noted. See `source-map.md`.
+
 ## Core Principle
 
 Security analysis should begin with a defined analytical question and an evidence standard. The analyst should distinguish investment conclusions supported by financial strength, earning power, asset protection, and contractual rights from speculative conclusions that depend mainly on favorable future market opinion.
 
-## Analytical Purpose
+## The Book's Own Test: Investment vs. Speculation
+
+Graham & Dodd tried several common distinctions — bonds vs. stocks, outright purchase vs. margin, permanent vs. temporary holding, income vs. profit — and rejected all of them as either too narrow or, in the "safety vs. risk" case, circular (a 1929 buyer of high-priced common stock also considered himself safe) (Ch. IV, pp.57–62). Their own definition, after that survey:
+
+> "An investment operation is one which, upon thorough analysis, promises safety of principal and a satisfactory return. Operations not meeting these requirements are speculative." (Ch. IV, p.63)
+
+Three things follow directly from this definition, and all three are places where analysts (then and now) go wrong:
+
+1. **It's an operation, not a security.** A stock or even a bond can have investment merit at one price and not another. There is no such thing as an "investment issue" in the absolute sense, independent of price (Ch. IV, p.63). A well-known, financially sound company bought at too high a price is a speculation, not an investment, regardless of its quality.
+2. **The safety must rest on standards, not on the outcome.** "Safety" judged only by whether the price later held up is circular — the cynic's definition that "an investment is a successful speculation" (Ch. IV, p.62). Safety has to be argued for in advance from the record and the balance sheet, not inferred afterward from the price action.
+3. **Thoroughness is a real, checkable standard, not a hedge word.** An "analysis" that recommends a stock at forty times its highest recorded earnings because of "excellent prospects" is not thorough by definition, no matter how much work went into the write-up (Ch. IV, p.64).
 
-Use these principles to classify the security, decide which analytical methods are appropriate, and prevent price movement or narrative appeal from replacing analysis.
+**Do not classify a security as an investment solely because its price has fallen** — a large decline can just as easily mean the original case never had a margin of safety, not that one now exists.
 
-## Required Inputs
+## The Concept of Intrinsic Value
 
-- security type
-- valuation date
-- price and relevant market terms
-- available financial statements
-- capital structure
-- investor objective and time horizon
-- available source notes
+Intrinsic value is "that value which is justified by the facts, e.g., the assets, earnings, dividends, definite prospects," as distinct from a market quotation shaped by manipulation or psychological excess (Ch. I, p.20). Graham & Dodd are explicit that this is a *useful but inexact* concept, not a precise number:
 
-## Tests
+> Security analysis "does not seek to determine exactly what is the intrinsic value of a given security. It needs only to establish either that the value is adequate... or else that the value is considerably higher or considerably lower than the market price." (Ch. I, p.22)
+
+Their own comparison: it is possible to tell by inspection that a woman is old enough to vote without knowing her exact age, or that a man is overweight without knowing his exact weight (Ch. I, p.22). **A conclusion that a security is cheap, dear, or adequately protected does not require a precise point-estimate of value — it requires enough confidence in the direction and the margin.** Analysts who insist on carrying a DCF to two decimal places are solving a harder and less reliable problem than the one that actually needs solving.
+
+The same chapter gives a cautionary example (J. I. Case Company, 1933): a ten-year average EPS of $9.50 that was "nothing more than an arithmetical resultant from 10 unrelated figures" — swinging from a $17 deficit to a $27 profit year to year — with "no convincing reason to believe" the average was representative of anything (Ch. I, pp.21–22). An average is only a measure of earning power when the individual years cluster around it; averaging noise produces a number that looks precise and means nothing. Apply this test before using any multi-year average in this skill's earnings-normalization or valuation steps.
+
+## Evidence Standard and Decision Discipline
 
 - Identify whether the thesis depends on assets, earnings, contractual payment, refinancing, growth, sentiment, or a combination.
 - State what evidence would disprove the thesis.
@@ -32,11 +44,8 @@ Use these principles to classify the security, decide which analytical methods a
 - no normalization of unusual earnings items
 - valuation rests on a single optimistic scenario
 - important data is missing but the conclusion is still definitive
+- an average is used as if it were representative without checking that the individual years support it (Ch. I, pp.21–22)
 
 ## Limitations
 
-Historical analytical conventions may not fit businesses with significant intangible assets, platform economics, regulated revenue models, unusual accounting, or rapidly changing competitive positions. Use current filings and market data when applying the framework.
-
-## Source Map
-
-Fill in exact edition, chapter, and page references in `source-map.md` from a legally acquired copy or your own authorized notes.
+Historical analytical conventions may not fit businesses with significant intangible assets, platform economics, regulated revenue models, unusual accounting, or rapidly changing competitive positions. Use current filings and market data when applying the framework. See `SKILL.md`, "Where the 1940 Framework Breaks," for the specific, recurring cases.
diff --git a/security-analysis-1940/references/equity-analysis.md b/security-analysis-1940/references/equity-analysis.md
index c28d635..505a3d4 100644
--- a/security-analysis-1940/references/equity-analysis.md
+++ b/security-analysis-1940/references/equity-analysis.md
@@ -1,47 +1,98 @@
 # Equity Analysis
 
+Source: Graham & Dodd, *Security Analysis*, 2nd ed. (1940), Chapters XIV–XV (preferred stocks) and XXVII–XXVIII, XXXVII (common stocks). See `source-map.md`.
+
 ## Core Principle
 
 For common and preferred shares, analysis should focus on sustainable earning power, balance-sheet strength, asset protection, dilution, capital allocation, and the relationship between conservative value and price.
 
-## Analytical Purpose
+## Preferred Stocks
+
+### The Discretionary-Dividend Problem
+
+Graham & Dodd's central point about preferred stock is structural, not a matter of degree: "payment of preferred dividends is entirely discretionary with the directors, whereas payment of bond interest is compulsory" (Ch. XIV, p.185). They explicitly reject the common simplification — "if the company is good, its preferred stock is as good as a bond; and if the company is bad, its bonds are as bad as a preferred stock" — because it ignores the wide middle ground of companies that *could* pay but choose to withhold the dividend "for the sake of the stockholders' future advantage," a decision the market routinely punishes with a price decline even when directors present it as prudent (Ch. XIV, p.185–186). **The legal right to omit a dividend without default, even when the company can afford to pay, is the real risk in preferred stock — treat it as a standing possibility, not a tail case.**
+
+This maps directly onto the modern instrument analysts are most likely to actually encounter: bank AT1 / contingent-convertible preferred and hybrid capital. The discretionary-suspension logic transfers cleanly (a coupon can be cancelled at supervisory discretion even when the bank can pay). The regulatory loss-absorption mechanics — conversion or writedown at a capital trigger — have no 1940s analogue and need separate, current analysis; see `SKILL.md`, "Where the 1940 Framework Breaks."
+
+### Sizing the Cushion: Minimum Coverage for Preferred vs. Bonds
+
+Because a preferred stockholder's claim is inferior to a bondholder's, Graham & Dodd require a *larger* earnings cushion for an investment-grade preferred than for an investment-grade bond of the same issuer class (Ch. XV, p.196):
+
+| Class of enterprise | Minimum coverage — bonds | Minimum coverage — preferred stock |
+|---|---:|---:|
+| Public utilities | 1.75× fixed charges | 2× fixed charges + preferred dividends |
+| Railroads | 2× fixed charges | 2.5× fixed charges + preferred dividends |
+| Industrials | 3× fixed charges | 4× fixed charges + preferred dividends |
+
+State these as 1940 benchmarks, not current standards (same caveat as `fixed-income-analysis.md`).
+
+### Compute Preferred Coverage on the Same Total-Deductions Basis
+
+The same error that afflicts junior-bond coverage afflicts preferred-dividend coverage, and Graham & Dodd give a worked correction (Ch. XV, pp.198–199): stating "earnings per share of preferred" in isolation, or dividing earnings by the preferred dividend alone, ignores the bond interest that ranks ahead of it. Their example (Colorado Fuel & Iron, 1929): interest charges covered 2.4×, but the customary practice of stating preferred-dividend coverage "alone" produced a separate, much larger 14.7× figure that implied — absurdly — that the preferred dividend was *safer* than the bond interest of the same company. The correct statement combines bond interest and preferred dividends into one **total fixed-charges-plus-preferred-dividends** figure and divides once. **Never accept a vendor or filing figure for "preferred dividend coverage" that doesn't include the bonds and any other preferred ranking ahead of the issue being analyzed.**
+
+The presence of funded debt ahead of a preferred issue does not by itself disqualify it — but it does raise the bar the combined coverage figure has to clear (Ch. XV, p.197).
+
+## Common Stocks
+
+### The Historical Failure Mode: New-Era Investing
+
+Graham & Dodd's critique of 1920s "new-era" common-stock investing is not a period piece — it is the clearest statement in the book of how a sound premise curdles into an unsound conclusion, and it recurs in every growth-stock cycle since, including AI-sector valuation. Their reconstruction of the 1928–29 logic (Ch. XXVIII, p.354):
+
+> "1. The value of a common stock depends on what it can earn in the future. 2. Good common stocks are those which have shown a rising trend of earnings. 3. Good common stocks will prove sound and profitable investments."
+
+Each statement is individually plausible; combined, they discard price as a variable entirely. If a stock can trade at 35x earnings instead of a "preboom" 10x, the new-era conclusion was never that the stock had become too expensive — only that "the standard of value had been raised" (Ch. XXVIII, p.355). Graham & Dodd's own diagnosis of the underlying error: the historical case for stocks (Edgar Lawrence Smith's 1924 finding that retained, reinvested earnings compound book value over time) is sound *only as long as the earnings yield paid for exceeds what a bond would pay* — a stock earning $10/share bought at 100 clears that bar; the same stock bought at 200 for $8 of earnings does not, because the buyer is now getting a bond-like return with none of a bond's seniority (Ch. XXVIII, pp.357–358). **This earnings-yield-vs-bond-yield comparison is a fast, book-grounded sanity check to run on any "quality growth" thesis before accepting the valuation.**
 
-Use this reference to select equity-appropriate valuation methods and to avoid applying debt-style protection tests or asset-value rules mechanically.
+By contrast, the sound canons Graham & Dodd endorse — echoing, then updating, the original (pre-1927) investment-trust discipline of buying in depressions, diversifying widely, and searching out undervalued issues through actual research (Ch. XXVIII, p.355) — reduce to three elements for a common-stock investment program (Ch. XXVIII, p.362):
+
+1. Treat it as a **group operation** — diversification is depended on to produce a favorable average result, because no single common stock's future is knowable with bond-like confidence.
+2. Select individual issues with the **same qualitative and quantitative rigor** used for fixed-value investments.
+3. Put **more weight on the future outlook** than bond selection requires — common stock is inherently a claim on the future, not just a test of survival.
+
+### The Growth-Company Trap
+
+Chapter XXVIII's critique of "growth companies" (a term Graham & Dodd date to the 1930s) is directly applicable to any current growth-stock or AI-sector thesis (Ch. XXVIII, pp.365–366). Their argument has three parts:
+
+1. **The label is defined by a short, favorable track record**, not by durable economics — "how many cycles are needed" before a company's earnings-through-cycles pattern is proven, rather than lucky?
+2. **Companies follow a life cycle**: struggle, then a period of persistent growth, then "supermaturity" — a slackening of expansion or even a loss of leadership. A very long run of increasing earnings can mean a business is *approaching* its saturation point, not confirming it will keep growing.
+3. This creates a **real dilemma, not a solvable one**: a newer company with a short growth record risks being a temporary fluke; an older one with a long growth record risks being near the top of its own curve. There is no shortcut past business judgement about where a specific company sits in its own cycle — the record alone can't answer it.
+
+**Use this explicitly when analyzing any business whose investment case rests on "the growth continues."** Ask, and answer in the memo: where is this business in its own life cycle, and what would falling off the "growth company" list actually look like here?
+
+### Earning Power: What Makes an Average Meaningful
+
+"The concept of earning power... combines a statement of actual earnings, shown over a period of years, with a reasonable expectation that these will be approximated in the future" (Ch. XXXVII, p.506). The multi-year record exists to average out the business cycle — but only if the individual years actually cluster around the average. Graham & Dodd's own paired example: a company whose ten annual results stay within a narrow band of its average has a real "indicated earning power"; a company whose ten results are wildly scattered has only "an abstraction from... widely varying figures," with no basis for expecting the average to recur (Ch. XXXVII, p.507).
+
+The controlling principle for combining the quantitative record with everything else known about the business:
+
+> "Quantitative data are useful only to the extent that they are supported by a qualitative survey of the enterprise." (Ch. XXXVII, p.508)
+
+A stable-looking earnings history is not sufficient on its own — the nature of the business has to independently support an expectation of continued stability. See `SKILL.md`, "Where the 1940 Framework Breaks," on adjusting the averaging period for a business with genuine structural growth or decline rather than cyclical noise around a flat trend.
+
+### Where Asset-Value Methods Stop Being Useful
+
+Asset-based methods (see `valuation-methods.md`) are most informative for businesses whose value sits on the balance sheet — manufacturing, real estate, financial assets. They are progressively less informative as value shifts to software, networks, brands, data, talent, or other intangible sources not fully captured (or not captured at all) as balance-sheet assets. In these cases, emphasize unit economics, durability of the earning power, reinvestment economics, and downside cash-flow scenarios instead of asset coverage.
 
 ## Required Inputs
 
-- historical financial statements
+- historical financial statements (7–10 years where available, per the earning-power averaging period above)
 - share count and dilution data
 - debt, cash, preferred equity, and minority interest
 - segment performance and business mix
 - normalized earnings and cash flow
-- dividend terms for preferred shares
+- dividend (and buyback) terms
 - market price and valuation date
 
-## Calculations Or Tests
-
-- normalized earnings and earnings variability
-- free cash flow after maintenance capital expenditure
-- return on capital and reinvestment quality
-- balance-sheet resilience
-- preferred dividend coverage where applicable
-- earnings-power value
-- conservative comparable valuation
-- asset-value or liquidation-value cross-check where relevant
-
 ## Warning Signs
 
 - earnings depend on peak-cycle conditions
 - reported profit does not convert to cash
 - high leverage weakens equity optionality
 - dilution is material and recurring
-- intangible-heavy asset base is valued mechanically
+- intangible-heavy asset base is valued mechanically (see "Where Asset-Value Methods Stop Being Useful," above)
 - management guidance is treated as fact
+- a "growth company" thesis is accepted without asking where the business sits in its own life cycle
+- preferred-dividend coverage is quoted without combining it with senior fixed charges
 
 ## Limitations
 
-Asset-based methods may be less informative for businesses whose value comes from software, networks, brands, data, talent, or other intangible sources. In these cases, emphasize unit economics, durability, reinvestment economics, and downside cash-flow scenarios.
-
-## Source Map
-
-Record exact book-section support in `source-map.md`.
+Asset-based methods may be less informative for businesses whose value comes from intangible sources. In these cases, emphasize unit economics, durability, reinvestment economics, and downside cash-flow scenarios.
diff --git a/security-analysis-1940/references/financial-normalisation.md b/security-analysis-1940/references/financial-normalisation.md
index f0bd54b..9d99a8c 100644
--- a/security-analysis-1940/references/financial-normalisation.md
+++ b/security-analysis-1940/references/financial-normalisation.md
@@ -1,29 +1,43 @@
 # Financial Normalization
 
+Source: Graham & Dodd, *Security Analysis*, 2nd ed. (1940), Chapter XXXI. See `source-map.md`.
+
 ## Core Principle
 
 Reported financial results often need adjustment before they can support an investment conclusion. Normalization should make earnings and cash flow more representative without hiding unfavorable facts.
 
-## Analytical Purpose
+## Don't Let Earnings Alone Carry the Analysis
+
+Graham & Dodd open their income-account chapter with a direct warning against exactly the failure mode that normalization exercises tend to fall into: treating the (adjusted) earnings number as if it were the whole analysis. They describe the ordinary business owner's habit of checking both the income statement *and* the balance sheet against each other as a "double check on intrinsic values" (Ch. XXXI, p.401), and warn that relying on earnings alone has four specific costs (Ch. XXXI, p.402):
+
+1. It discards a familiar, cross-checkable frame of reference (how any real business is actually judged) for a narrower one.
+2. It replaces a **twofold test** (earnings and assets) with a single, less dependable one.
+3. Earnings move faster and more erratically than balance sheets, so relying on earnings alone injects instability into the valuation that isn't really there in the underlying business.
+4. Earnings statements are more easily shaped through legitimate accounting choices than balance sheets are.
+
+**Practical implication for this skill: a normalization exercise is not complete when the adjusted earnings figure is defensible. It is complete when the adjusted earnings figure has been checked against the balance sheet** — does the company's asset base and capital structure corroborate the earning power the income statement implies, or contradict it?
+
+## The Formula Behind Most Mispricing
 
-Use normalization to separate recurring economics from unusual, non-recurring, accounting-driven, or structurally changed items.
+Graham & Dodd reduce ordinary market practice — the thing normalization exists to see past — to one formula: **price = current earnings per share × a "quality coefficient"** that is itself driven mostly by the recent earnings trend (Ch. XXXI, p.402–403). The circularity is the point: the multiple applied to earnings is largely *derived from* the same earnings series being multiplied, so a business whose reported EPS has been pushed up (by any of the devices below) gets rewarded twice — once directly through the higher EPS, and again through a higher multiple justified by the resulting "trend."
 
-## Required Inputs
+## Four Devices That Distort Reported Per-Share Earnings
 
-- income statements for multiple periods
-- cash-flow statements
-- balance sheets
-- notes to accounts
-- segment disclosures
-- acquisition and restructuring details
-- management adjustments, if supplied
+Graham & Dodd's own list of where reported EPS becomes "subject... to arbitrary determination and manipulation" (Ch. XXXI, p.403):
 
-## Adjustments To Consider
+1. **Allocating items to surplus (equity) instead of income, or vice versa** — moving a charge or gain below the income statement (or the reverse) to shape the reported trend. Modern analogue: "adjusted" or "non-GAAP" earnings that routinely exclude recurring charges (restructuring "every year," stock-based compensation) as if they were one-time.
+2. **Over- or understating amortization and other reserve charges** — the depreciation/amortization policy itself is a lever on reported earnings, not a neutral fact.
+3. **Varying the capital structure between senior securities and common stock** — issuing preferred or debt instead of common (or vice versa) changes reported common EPS independent of any change in the underlying business.
+4. **The use made of large capital funds not employed in the business** — idle cash or investments held off to the side can make return-on-capital or per-share metrics look better or worse depending how they're classified.
+
+Use this list as a checklist when reviewing why reported EPS differs from what the underlying operating trend would suggest — not just whether an adjustment exists, but which of these four mechanisms produced it.
+
+## Adjustments to Consider
 
 - non-recurring gains or losses
 - restructuring charges
 - acquisition, integration, and divestiture effects
-- stock-based compensation
+- stock-based compensation (see `SKILL.md`, "Where the 1940 Framework Breaks" — treat as a real recurring cost, not a routine non-cash add-back)
 - capitalized costs
 - unusual working-capital movements
 - impairments and reversals
@@ -49,11 +63,8 @@ For every adjustment, show:
 - management adjustments are accepted without challenge
 - negative adjustments are omitted
 - short history is treated as through-cycle evidence
+- adjusted EPS is not cross-checked against the balance sheet (Ch. XXXI, pp.401–402)
 
 ## Limitations
 
 Normalization is judgemental. Keep an audit trail and present reported and adjusted numbers side by side.
-
-## Source Map
-
-Record exact book-section support in `source-map.md`.
diff --git a/security-analysis-1940/references/fixed-income-analysis.md b/security-analysis-1940/references/fixed-income-analysis.md
index 0f9a4ac..4f19b72 100644
--- a/security-analysis-1940/references/fixed-income-analysis.md
+++ b/security-analysis-1940/references/fixed-income-analysis.md
@@ -1,12 +1,66 @@
 # Fixed-Income Analysis
 
+Source: Graham & Dodd, *Security Analysis*, 2nd ed. (1940), Chapters VI–VIII. See `source-map.md`.
+
 ## Core Principle
 
 For bonds and other fixed claims, the analyst should prioritize contractual claims, fixed-charge coverage, asset protection, seniority, maturity profile, refinancing risk, and recovery value.
 
-## Analytical Purpose
+## The Four Principles of Fixed-Value Selection
+
+Graham & Dodd's selection framework for bonds and high-grade preferred stock rests on four principles (Ch. VI, p.80):
+
+> "I. Safety is measured not by specific lien or other contractual rights, but by the ability of the issuer to meet all of its obligations. II. This ability should be measured under conditions of depression rather than prosperity. III. Deficient safety cannot be compensated for by an abnormally high coupon rate. IV. The selection of all bonds for investment should be subject to rules of exclusion and to specific quantitative tests..."
+
+### I. Safety Is the Enterprise, Not the Lien
+
+This is the load-bearing idea in the chapter, and it is still the single most useful corrective to how people intuitively think about bond safety. A bond is popularly seen as a claim against *property*; Graham & Dodd argue it should be seen as a claim against a *business* (Ch. VI, p.80). Their reasoning: a mortgage lien fails to protect in practice for three reasons (Ch. VI, pp.80–83):
+
+1. Pledged property (a rail line, a factory, a power plant) is usually worth far less once the business that used it has failed — the collateral's value is itself dependent on the earning power of the enterprise, not independent of it.
+2. Courts are reluctant to let bondholders foreclose and take possession if the property might be worth more than the claim — in practice bondholders are pushed into a reorganization, not a payout.
+3. Even a strong first-mortgage position takes years to resolve in receivership, during which the market price of the bond is depressed regardless of the eventual recovery.
+
+The corollary: since specific lien is a weak protection, its *absence* is also a minor matter. A debenture (unsecured bond) of a strong company is a sounder investment than a mortgage bond of a weak one (Ch. VI, p.83). **When assessing a bond, weight the issuer's ability to pay far above the nominal security package.** Collateral matters at the margin, primarily by affecting recovery in a default that has already happened — it is not a substitute for issuer quality.
+
+Because the chief emphasis is avoiding loss rather than seeking gain, bond selection is "primarily a negative art" — the penalty for wrongly rejecting a sound bond is near zero, while the penalty for wrongly accepting an unsound one is not. Graham & Dodd apply Walter Bagehot's observation to commercial bankers directly to bond selection: "If there is a difficulty or a doubt the security should be declined" (Ch. VI, p.79, quoting Bagehot, *Lombard Street*, 1892).
+
+### II. Test Under Depression, Not Prosperity
+
+No industry is depression-proof — only more or less stable. Graham & Dodd's own example: utilities suffer smaller earnings shrinkage than steel producers, but a small decline can still be fatal if the company is financed to the limit of prosperity earnings (Ch. VII, pp.91–92). This gives a direct, usable rule: **the required margin of safety should scale with the instability of the industry** — a stable business can carry more debt relative to its normal earning power; an unstable one needs a larger earnings cushion for the same debt load (Ch. VII, p.92).
+
+### III. Yield Does Not Buy Safety
+
+A high coupon is compensation for risk already present, not a substitute for the underlying safety analysis. Do not let an attractive yield relax the coverage and seniority tests.
+
+### IV. Apply Specific, Quantitative Tests
+
+Graham & Dodd propose extending the logic of savings-bank legal-list statutes (which existed to protect depositors) to bond selection generally, while explicitly rejecting the statutes' blanket exclusions by industry as too crude — "a considerable narrowing... is in fact demanded," but *individual strength should compensate for a class's supposed weakness* rather than excluding whole categories (Ch. VIII, p.109). Applied today: don't reject a sector wholesale (e.g. "no industrials") — require a stronger individual exhibit from issuers in weaker classes.
 
-Use this reference when assessing whether a fixed-income security has adequate downside protection and whether its promised payments are supported by issuer resources.
+## Computing Earnings Coverage: Three Methods, One Correct
+
+This is the most common technical error in coverage analysis, then and now, and it is fully specified in the book (Ch. VIII, pp.126–128):
+
+- **Prior-deductions method (wrong):** deduct only the charges senior to the bond being analyzed, then divide the remainder by that bond's own interest. This makes junior debt look *better covered* than senior debt from the same issuer, which is absurd — Graham & Dodd's own numeric example: a company earning $1.4mm with $500k senior interest and $300k junior interest shows senior coverage of 2.8x and junior coverage of "3x" under this method, implying the junior bond is safer.
+- **Cumulative-deductions method (partial):** compute each tranche's coverage using its own and all senior charges combined (junior coverage = earnings ÷ (senior + junior charges) = 1.75x in the example above). Better, and used by some legal-list statutes, but still lets a senior tranche's coverage be calculated in isolation.
+- **Total-deductions / "over-all" method (correct, and the one this skill uses):** compute coverage as available earnings ÷ **all** fixed charges of the issuer, and apply that same ratio to every tranche, senior or junior. In the example, both the "first 5s" and the "debenture 6s" are stated as covered 1.75x. The logic: insolvency triggered by a junior default drags down the senior claim too, so the issuer's *aggregate* capacity to service *all* fixed charges is what protects any single tranche (Ch. VIII, pp.127–128).
+
+**Always compute and report the total-deductions coverage ratio.** A prior-deductions or per-tranche number pulled from an offering circular or a data vendor should be treated as marketing, not analysis, unless it's been rebuilt on this basis.
+
+## Historical Minimum Coverage (1940, Not a Current Standard)
+
+Graham & Dodd's own recommended minimums for total fixed-charge coverage, by issuer class (Ch. VIII, p.128):
+
+| Class of enterprise | Minimum coverage of total fixed charges |
+|---|---:|
+| Public utilities | 1.75× |
+| Railroads | 2× |
+| Industrials | 3× |
+
+State these explicitly as **1940 recommendations for a 1940s capital-structure and interest-rate environment**, never as a current regulatory or rating-agency standard. They are useful as a sense of relative stringency by issuer class (industrials need more cushion than utilities, consistent with Principle II) and as a historical benchmark, not as a pass/fail test for a modern credit.
+
+## The Averaging Period
+
+A single year's coverage — or even the requirement (used by some 1940s statutes) that the minimum be met in most of the last five or six years — rewards buying bonds at the top of a cycle and selling at the bottom (Ch. VIII, p.129). Graham & Dodd's own preference: a **seven-year average**, shortened to exclude clearly abnormal years where that produces a fairer picture, or lengthened to ten or twelve years if the seven-year window itself falls mostly in a severe depression (Ch. VIII, p.129). For a deficit year that would otherwise drag the average to an unrepresentative negative number, they suggest counting it as **zero rather than the actual negative figure** when the deficit is clearly abnormal (Ch. VIII, p.130) — flag this adjustment explicitly if used; it is a real judgement call, not a neutral default.
 
 ## Required Inputs
 
@@ -14,33 +68,20 @@ Use this reference when assessing whether a fixed-income security has adequate d
 - coupon, maturity, call protection, covenants, and collateral
 - issuer income statement, balance sheet, and cash-flow statement
 - debt maturity schedule
-- interest expense and other fixed charges
+- interest expense and other fixed charges (including capitalized leases — see `SKILL.md`, "Where the 1940 Framework Breaks")
 - asset values and senior claims
 - market price and yield
 
-## Calculations Or Tests
-
-- interest coverage
-- fixed-charge coverage
-- leverage and net leverage
-- asset coverage for the claim under analysis
-- maturity wall and refinancing dependency
-- recovery-value analysis under downside scenarios
-- covenant headroom where covenants are available
-
 ## Warning Signs
 
+- coverage quoted on a prior-deductions or single-tranche basis rather than total-deductions
 - weak or declining coverage
 - large near-term maturities without clear refinancing capacity
 - structurally senior claims at subsidiaries
-- asset values dependent on optimistic marks
+- asset values dependent on optimistic marks, or collateral treated as protection independent of issuer strength
 - covenant erosion or limited creditor protections
 - material off-balance-sheet obligations
 
 ## Limitations
 
 Legal priority, covenant interpretation, collateral enforceability, and restructuring outcomes require current document review and may require qualified legal input.
-
-## Source Map
-
-Record exact book-section support in `source-map.md`.
diff --git a/security-analysis-1940/references/margin-of-safety.md b/security-analysis-1940/references/margin-of-safety.md
index 690568e..18846db 100644
--- a/security-analysis-1940/references/margin-of-safety.md
+++ b/security-analysis-1940/references/margin-of-safety.md
@@ -1,12 +1,16 @@
 # Margin Of Safety
 
+Source: Graham & Dodd, *Security Analysis*, 2nd ed. (1940), Chapters VII, VIII, XLIII, LII. See `source-map.md`.
+
 ## Core Principle
 
 Margin of safety is the protection between conservative estimated value and market price, supported by identifiable asset, earnings, coverage, or contractual evidence. It is not simply the difference between an optimistic valuation and price.
 
-## Analytical Purpose
+## Two Distinct Uses in the Book — Don't Collapse Them
+
+Most analysts today use "margin of safety" loosely to mean "price below estimated intrinsic value." That is a real and legitimate use, but it is worth knowing that the 1940 text's own primary, technical use of the term is narrower and more mechanical: **the earnings cushion above fixed charges**, expressed as a coverage ratio. Graham & Dodd note that some authorities (Moody's *Manual of Investments*, pre-1930) defined it explicitly: if interest is covered *x* times, the margin of safety is (x − 1)/x expressed as a percentage — e.g. interest covered 1.75× implies a margin of safety of 43% (Ch. VIII, p.129, footnote). This is the sense the book uses most often in the bond and preferred-stock chapters (`fixed-income-analysis.md`, `equity-analysis.md`): **how much can earnings shrink before fixed charges stop being covered.**
 
-Use margin-of-safety analysis to evaluate whether downside risk is compensated and whether the conclusion remains supportable under adverse scenarios.
+The second, broader use — familiar from later popularizations of the book — is closer to what this skill's `SKILL.md` procedure calls "margin of safety": the gap between a conservative estimate of value and the price paid, for *any* security type including common stock. Both uses are legitimate and both appear in the book; **state which one you mean in a memo**, since a bond's coverage-based margin of safety and a stock's price-vs-value margin of safety are answering different questions and aren't directly comparable.
 
 ## Required Inputs
 
@@ -19,13 +23,31 @@ Use margin-of-safety analysis to evaluate whether downside risk is compensated a
 
 ## Calculation
 
-Basic formula:
+For a bond or preferred stock (coverage-based, Ch. VIII, p.129):
+
+```text
+margin_of_safety = (coverage_ratio - 1) / coverage_ratio
+```
+
+For a security valued against a conservative estimate of intrinsic value (price-based):
 
 ```text
 margin_of_safety = (intrinsic_value - market_price) / intrinsic_value
 ```
 
-Use only when intrinsic value is positive and supported by evidence. Explain whether the calculated margin reflects asset protection, earning power, contractual payments, or market multiple assumptions.
+Use the price-based formula only when intrinsic value is positive and supported by evidence. Explain whether the calculated margin reflects asset protection, earning power, contractual payments, or market multiple assumptions.
+
+## The Required Margin Scales with Instability
+
+Graham & Dodd's depression-basis principle (`fixed-income-analysis.md`, Principle II) gives a direct rule for sizing the required margin: **the more unstable the business, the larger the earnings cushion needed to protect the same claim** (Ch. VII, p.92). A stable utility can be financed closer to its normal earning power than a cyclical industrial can, for the same nominal safety. Apply this before accepting a coverage ratio as "enough" — the bar should move with the issuer's own volatility, not sit at a single fixed number across issuer types (which is also why the book's historical minimums differ by class — see `fixed-income-analysis.md`).
+
+## Net-Current-Asset Value as a Margin-of-Safety Source
+
+For common stocks with a meaningful current-asset base, a price below net current asset value (`valuation-methods.md`) is a specific, book-grounded source of margin of safety: it implies the market price is below what a conservative liquidation of current assets alone — after paying every liability in full — would return, with the entire earning power and fixed-asset base thrown in for nothing (Ch. XLIII, pp.578–581). This is one of the strongest, most literal margins of safety the book describes, precisely because it depends on the least optimistic assumptions. It is also narrow in applicability — see `equity-analysis.md` on asset-light businesses.
+
+## What Analysis Protects Against That Forecasting Doesn't
+
+Graham & Dodd's closing distinction between security analysis and market/chart analysis is a useful framing for why margin of safety matters at all: both disciplines work with historical data that is suggestive but not conclusive about the future — "the past earnings of a company supply a useful indication of its future earnings — useful, but not infallible." The difference is that "the securities analyst can protect himself by a margin of safety that is denied to the market analyst" (Ch. LII, p.716). A market forecaster who is wrong has no cushion; an analyst who bought with an adequate margin of safety can be wrong about the exact future and still come out protected. **This is the justification for insisting on a margin at all, not just a favorable central case.**
 
 ## Warning Signs
 
@@ -34,11 +56,9 @@ Use only when intrinsic value is positive and supported by evidence. Explain whe
 - margin exists only after excluding recurring costs
 - senior claims absorb most downside value
 - market price is stale or illiquid
+- a bond's coverage-based margin and a stock's price-based margin are conflated or compared directly
+- the required margin is held constant across issuers of very different earnings stability (Ch. VII, p.92)
 
 ## Limitations
 
 Margin-of-safety calculations are sensitive to the reliability of the value estimate. Present ranges and scenario outcomes instead of implying false precision.
-
-## Source Map
-
-Record exact book-section support in `source-map.md`.
diff --git a/security-analysis-1940/references/source-map.md b/security-analysis-1940/references/source-map.md
index ab91a3e..fa2beb9 100644
--- a/security-analysis-1940/references/source-map.md
+++ b/security-analysis-1940/references/source-map.md
@@ -1,13 +1,47 @@
 # Source Map
 
-Use this file to connect internal skill guidance to your own authorized notes from a legally acquired source. Do not paste lengthy copyrighted passages here.
-
-| Internal topic | Book section | Purpose | Notes status |
-|---|---|---|---|
-| Investment versus speculation | TBD | Security classification | Add edition, chapter, and page |
-| Fixed-value investments | TBD | Bond and preferred-share analysis | Add edition, chapter, and page |
-| Earnings normalization | TBD | Sustainable earnings assessment | Add edition, chapter, and page |
-| Balance-sheet analysis | TBD | Asset protection and solvency | Add edition, chapter, and page |
-| Margin of safety | TBD | Investment decision discipline | Add edition, chapter, and page |
-| Common-stock valuation | TBD | Equity valuation discipline | Add edition, chapter, and page |
-| Disconfirming evidence | TBD | Thesis challenge | Add edition, chapter, and page |
+All page citations below are to the printed page numbers of Graham, Benjamin, and David L. Dodd, *Security Analysis: Principles and Technique*, 2nd ed. (New York: McGraw-Hill, 1940) — verified directly against the book's own chapter headings and running page numbers, not estimated. If you add a new principle to a reference file, verify its chapter and page against the source text the same way before adding a row here; if you can't verify it, don't add it — cite it in the memo as standard practice instead (see `SKILL.md`, "Citation Policy").
+
+| Internal topic | Book location | Used in |
+|---|---|---|
+| Three functions of analysis; intrinsic value defined; "adequate, not exact" doctrine | Ch. I, pp.17–22 | `analytical-principles.md` |
+| J. I. Case ten-year-average example (average of unrelated figures ≠ earning power) | Ch. I, pp.21–22 | `analytical-principles.md` |
+| Distinctions commonly drawn between investment and speculation (five criteria, all rejected) | Ch. IV, pp.57–62 | `analytical-principles.md` |
+| "An investment operation is one which, upon thorough analysis, promises safety of principal and a satisfactory return..." | Ch. IV, p.63 | `analytical-principles.md` |
+| Investment is price-dependent, not an absolute property of an issue; thoroughness standard | Ch. IV, pp.63–64 | `analytical-principles.md` |
+| Four principles of fixed-value selection (safety = ability to pay, not lien; depression basis; coupon ≠ safety; quantitative tests) | Ch. VI, p.80 | `fixed-income-analysis.md` |
+| Enterprise vs. property claim; three reasons a mortgage lien fails to protect in practice | Ch. VI, pp.80–83 | `fixed-income-analysis.md` |
+| Bagehot ("If there is a difficulty or a doubt the security should be declined"); bond selection as a negative art | Ch. VI, p.79 (quoting Bagehot, *Lombard Street*, 1892) | `fixed-income-analysis.md` |
+| No industry is depression-proof; required margin scales with industry instability | Ch. VII, pp.91–92 | `fixed-income-analysis.md`, `margin-of-safety.md` |
+| Savings-bank statutes as a starting point; individual strength should compensate for class weakness rather than blanket exclusion | Ch. VIII, p.109 | `fixed-income-analysis.md` |
+| Three methods of computing earnings coverage (prior-deductions, cumulative-deductions, total-deductions/"over-all"), with worked numeric example | Ch. VIII, pp.126–128 | `fixed-income-analysis.md` |
+| Recommended minimum total-fixed-charge coverage by issuer class (utilities 1.75×, railroads 2×, industrials 3×) | Ch. VIII, p.128 | `fixed-income-analysis.md` |
+| Old margin-of-safety definition (Moody's, pre-1930): (coverage − 1)/coverage | Ch. VIII, p.129, footnote | `margin-of-safety.md` |
+| Recommended earnings-averaging period (7 years, adjustable), and deficit-years-as-zero convention | Ch. VIII, pp.129–130 | `fixed-income-analysis.md` |
+| Preferred stock's discretionary (non-compulsory) dividend as the core structural risk; rejection of the "good company ⇒ preferred as safe as bond" fallacy | Ch. XIV, pp.184–186 | `equity-analysis.md` |
+| Minimum average-earnings coverage for investment preferred stock, by issuer class (utilities 2×, railroads 2.5×, industrials 4×, fixed charges + preferred dividends) | Ch. XV, p.196 | `equity-analysis.md` |
+| Funded debt ahead of a preferred does not automatically disqualify it, but raises the required coverage | Ch. XV, p.197 | `equity-analysis.md` |
+| Total-deductions basis required for preferred coverage; Colorado Fuel & Iron worked example of the "preferred dividend earned per share" fallacy | Ch. XV, pp.198–199 | `equity-analysis.md` |
+| Three "new-era" (1928–29) canons of common-stock investment, and their fallacy | Ch. XXVIII, p.354 | `equity-analysis.md` |
+| Original (pre-1927) investment-trust canons: buy in depression, diversify, seek undervalued issues via research | Ch. XXVIII, p.355 | `equity-analysis.md` |
+| Price disconnected from value under new-era logic ("the standard of value had been raised") | Ch. XXVIII, p.355 | `equity-analysis.md` |
+| Edgar Lawrence Smith's compounding-book-value argument, and why it breaks down once price exceeds the earnings-yield-over-bond-yield threshold | Ch. XXVIII, pp.357–358 | `equity-analysis.md` |
+| Three-element sound canon for common-stock investment (group operation; qualitative+quantitative selection; greater weight on outlook) | Ch. XXVIII, p.362 | `equity-analysis.md` |
+| Growth-company definition problem, business life-cycle argument (struggle → growth → "supermaturity"), and the resulting selection dilemma | Ch. XXVIII, pp.365–366 | `equity-analysis.md` |
+| Definition of "earning power" as a multi-year record plus a reasonable expectation of recurrence | Ch. XXXVII, p.506 | `equity-analysis.md` |
+| S. H. Kress vs. Hudson Motors example: an average is only meaningful if individual years cluster around it | Ch. XXXVII, p.507 | `equity-analysis.md` |
+| "Quantitative data are useful only to the extent that they are supported by a qualitative survey of the enterprise" | Ch. XXXVII, p.508 | `equity-analysis.md` |
+| Twofold test (earnings + balance sheet) vs. sole reliance on earnings; four costs of ignoring the balance sheet | Ch. XXXI, pp.401–402 | `financial-normalisation.md` |
+| Wall Street formula: price = current EPS × quality coefficient (itself earnings-trend-driven); circularity critique | Ch. XXXI, pp.402–403 | `financial-normalisation.md`, `valuation-methods.md` |
+| Four devices for distorting reported per-share earnings | Ch. XXXI, p.403 | `financial-normalisation.md` |
+| Net-current-asset value: definition, three theses, and the realizability schedule for liquidation (cash 100%, receivables 80%, inventory 66⅔%, fixed/misc. ~15%) | Ch. XLIII, pp.578–579 | `valuation-methods.md`, `margin-of-safety.md` |
+| Historical incidence of NYSE industrials trading below net current asset value (>40% in 1932; 20.5% in early 1938) | Ch. XLIII, p.581 | `valuation-methods.md` |
+| Security analysis vs. market/chart analysis: "the securities analyst can protect himself by a margin of safety that is denied to the market analyst" | Ch. LII, p.716 | `margin-of-safety.md` |
+
+## Not Yet Mapped
+
+The following topics are referenced in this skill's procedure but do not yet have a verified book citation. Treat them as standard analytical practice in memos, without a book citation, until someone maps them against the text the same way as above:
+
+- discounted cash-flow mechanics (not covered by the 1940 text in the form used today)
+- conservative-comparables / peer-multiple technique
+- modern lease-capitalization, share-based-compensation, and AT1/contingent-capital treatment (deliberately out of scope for book citation — see `SKILL.md`, "Where the 1940 Framework Breaks")
diff --git a/security-analysis-1940/references/valuation-methods.md b/security-analysis-1940/references/valuation-methods.md
index a5c1b49..fc158e9 100644
--- a/security-analysis-1940/references/valuation-methods.md
+++ b/security-analysis-1940/references/valuation-methods.md
@@ -1,36 +1,51 @@
 # Valuation Methods
 
+Source: Graham & Dodd, *Security Analysis*, 2nd ed. (1940), Chapters I, XXXI, XLIII. See `source-map.md`. DCF and conservative-comparables technique below is standard modern practice, not drawn from the book — see the note at the end of each section.
+
 ## Core Principle
 
 Valuation should use methods appropriate to the security, the issuer, and the available data. Avoid forcing every method onto every case.
 
 ## Analytical Purpose
 
-Use multiple conservative methods to triangulate value, reveal dependency on assumptions, and distinguish robust downside protection from optimistic upside.
+Use multiple conservative methods to triangulate value, reveal dependency on assumptions, and distinguish robust downside protection from optimistic upside. Graham & Dodd's own framing of what a valuation needs to accomplish: not a precise number, but enough confidence to say the value is *adequate* to protect the claim, or *considerably* above or below the market price (Ch. I, p.22 — see `analytical-principles.md`).
+
+## Net-Current-Asset-Value Analysis (Book-Grounded)
+
+This is the book's own primary asset-value method, and it is a genuinely mechanical, low-judgement test — which is also its limitation. **Net current assets = current assets − all liabilities (including any debt and preferred equity ranking ahead of the common)**, with no credit given for fixed assets at all (Ch. XLIII, pp.578–581).
+
+The method rests on a specific, conservative realizability schedule for balance-sheet assets in a liquidation, which Graham & Dodd give explicitly (Ch. XLIII, p.579):
 
-## Common Methods
+| Asset type | % of book value realizable (rough average) |
+|---|---:|
+| Cash and marketable securities | 100% |
+| Receivables (net of reserves) | 80% (range 75–90%) |
+| Inventory (lower of cost or market) | 66⅔% (range 60–75%) |
+| Fixed and miscellaneous assets (real estate, plant, equipment, intangibles) | ~15% (range 1–50%) |
 
-### Asset-Value Analysis
+The **first rule**: liabilities are real and are deducted at full face value; only the assets are subject to a haircut (Ch. XLIII, p.579).
 
-Estimate value from balance-sheet assets after conservative adjustments for asset quality, recoverability, senior claims, and liquidation friction.
+Graham & Dodd's own historical finding using this test: **over 40% of NYSE industrial companies traded below their net current asset value at some point in 1932**, and 20.5% again in early 1938 — including a meaningful number trading below their cash-asset value alone (Ch. XLIII, p.581). A stock priced below net current asset value is, by this test, being valued by the market at less than what a conservative liquidation of the current assets alone (after paying every liability in full) would return — which the book treats as *prima facie* illogical rather than proof of undervaluation (there may be a reason, such as cash burn, that the market is right).
 
-### Earnings-Power Valuation
+**Use this as a floor/screen, not a target price**, and only where the balance sheet actually carries meaningful current assets relative to the business. It is close to useless for an asset-light or intangible-heavy business — see `equity-analysis.md`, "Where Asset-Value Methods Stop Being Useful."
 
-Estimate value from normalized, sustainable earnings using a conservative capitalization rate or multiple supported by business quality and risk.
+## Earnings-Power Valuation
 
-### Discounted Cash Flow
+Estimate value from normalized, sustainable earnings (see `financial-normalisation.md` and `equity-analysis.md` for how Graham & Dodd define a representative earnings measure) using a conservative capitalization rate or multiple supported by business quality and risk. The book's own critique of the naive version of this method — price as current EPS times a "quality coefficient" driven by the earnings trend itself (Ch. XXXI, pp.402–403) — is the reason to anchor the multiple or capitalization rate to something outside the earnings series being capitalized (a required-return standard, a sector base rate, bond yields), not to a trend extrapolated from the same numbers being valued.
 
-Use when cash-flow drivers can be modeled with reasonable support. Show revenue, margin, reinvestment, discount-rate, terminal-value, and dilution assumptions.
+## Discounted Cash Flow (Standard Modern Practice)
 
-### Yield And Coverage Analysis
+Use when cash-flow drivers can be modeled with reasonable support. Show revenue, margin, reinvestment, discount-rate, terminal-value, and dilution assumptions. Not a method described in the 1940 text — apply Graham & Dodd's general discipline (conservatism, explicit assumptions, distrust of any single point estimate) to it, but do not attribute the DCF mechanics themselves to the book.
 
-Use for bonds and preferred shares to assess promised payments, coverage, downside protection, and compensation for risk.
+## Yield and Coverage Analysis (Book-Grounded)
 
-### Recovery-Value Analysis
+Use for bonds and preferred shares to assess promised payments, coverage, downside protection, and compensation for risk. See `fixed-income-analysis.md` and `equity-analysis.md` for the specific coverage tests and historical minimums.
 
-Use for stressed credits or leveraged capital structures. Estimate recoverable value by priority of claims and downside enterprise value or asset value.
+## Recovery-Value Analysis (Book-Grounded, Distress Context)
 
-### Conservative Comparables
+Use for stressed credits or leveraged capital structures. Estimate recoverable value by priority of claims and downside enterprise value or asset value, using the same realizability schedule as net-current-asset-value analysis above for the underlying assets, adjusted for the specific security type and industry.
+
+## Conservative Comparables (Standard Modern Practice)
 
 Use market multiples only as a cross-check. Adjust for growth, leverage, margins, accounting quality, cyclicality, and business mix.
 
@@ -50,7 +65,5 @@ Use market multiples only as a cross-check. Adjust for growth, leverage, margins
 - peer multiples ignore leverage or quality differences
 - asset value ignores senior claims or liquidation costs
 - DCF assumptions are not tied to historical evidence
-
-## Source Map
-
-Record exact book-section support in `source-map.md`.
+- an earnings multiple is justified by reference to the same earnings trend it's being applied to (Ch. XXXI, pp.402–403)
+- net-current-asset-value is applied to a business with little balance-sheet asset value relative to its earning power
