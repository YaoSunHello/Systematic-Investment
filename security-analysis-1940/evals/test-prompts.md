# Skill Evaluation Prompts

## Test 1: Missing Data

Prompt:

```text
Analyze this company using the Security Analysis framework.
I only have the latest income statement and current share price.
```

Expected behavior:

- perform only supportable analysis
- identify missing balance-sheet, cash-flow, capital-structure, and historical information
- avoid fabricating figures
- avoid definitive valuation

## Test 2: Bond Analysis

Prompt:

```text
Assess whether this corporate bond has adequate downside protection.
Use the attached issuer financial statements and bond terms.
```

Expected behavior:

- prioritize seniority, fixed charges, coverage, maturity profile, covenants, and recovery
- avoid an equity-only valuation framework
- identify missing legal or covenant details

## Test 3: Normalization

Prompt:

```text
Normalize the company's earnings and explain every adjustment.
```

Expected behavior:

- separate reported numbers from adjustments
- flag judgemental adjustments
- retain an audit trail
- preserve reported and adjusted figures

## Test 4: Challenging The Thesis

Prompt:

```text
Here is my valuation model. Identify evidence that could invalidate my investment conclusion.
```

Expected behavior:

- actively search for disconfirming evidence
- identify sensitivity to assumptions
- avoid simply endorsing the thesis

## Test 5: Modern Application

Prompt:

```text
Apply the framework to a software company with significant intangible assets.
```

Expected behavior:

- recognize where asset-based historical methods are less informative
- avoid mechanically applying industrial-company rules
- explain limitations and use more relevant economic evidence
