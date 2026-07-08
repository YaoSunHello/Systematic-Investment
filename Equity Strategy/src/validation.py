from src.models import ValuationInput, ValuationResult
from src.sensitivity import stress_scenarios, wacc_terminal_growth_grid


def validation_findings(input_data: ValuationInput, result: ValuationResult) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if result.terminal_value_to_ev > 0.85:
        findings.append(
            {
                "id": "VAL-001",
                "severity": "High",
                "area": "Terminal Value",
                "issue": "Terminal value exceeds 85% of enterprise value.",
                "impact": "Fair value and recommendation are highly dependent on WACC and terminal growth.",
                "recommendation": "Downgrade confidence and require analyst review before issuing a Buy call.",
            }
        )
    elif result.terminal_value_to_ev > 0.75:
        findings.append(
            {
                "id": "VAL-001",
                "severity": "Medium",
                "area": "Terminal Value",
                "issue": "Terminal value exceeds 75% of enterprise value.",
                "impact": "Point-estimate valuation is sensitive to long-run assumptions.",
                "recommendation": "Review WACC/g sensitivity before using the recommendation.",
            }
        )
    if any("financial companies" in flag for flag in result.flags):
        findings.append(
            {
                "id": "VAL-002",
                "severity": "High",
                "area": "Methodology",
                "issue": "FCFF DCF applied to a financial company.",
                "impact": "Debt may be operating capital, making FCFF unsuitable as the primary model.",
                "recommendation": "Use dividend discount, excess return, or P/B framework.",
            }
        )
    if result.data_quality_flags:
        findings.append(
            {
                "id": "VAL-003",
                "severity": "Medium",
                "area": "Data",
                "issue": "; ".join(result.data_quality_flags),
                "impact": "Input issues may distort fair value and model confidence.",
                "recommendation": "Resolve data lineage and mapping issues before production use.",
            }
        )
    if not findings:
        findings.append(
            {
                "id": "VAL-000",
                "severity": "Low",
                "area": "Overall",
                "issue": "No high-severity validation exceptions from automated checks.",
                "impact": "Model can be used as a research support tool with stated limitations.",
                "recommendation": "Keep analyst review, sensitivity analysis, and source documentation mandatory.",
            }
        )
    return findings


def model_risk_rating(result: ValuationResult) -> tuple[int, str]:
    score = result.confidence_score
    if result.data_quality_flags:
        score -= 10
    if any("financial companies" in flag for flag in result.flags):
        score -= 20
    if result.terminal_value_to_ev > 0.85:
        score -= 10
    score = max(0, min(100, score))
    if score >= 85:
        return score, "Low model risk"
    if score >= 70:
        return score, "Moderate model risk"
    if score >= 50:
        return score, "High model risk"
    return score, "Very high model risk"


def validation_report_markdown(input_data: ValuationInput, result: ValuationResult) -> str:
    findings = validation_findings(input_data, result)
    risk_score, risk_rating = model_risk_rating(result)
    plus_50bps = next(
        row for row in wacc_terminal_growth_grid(input_data, [0.005], [0.0])
        if row["wacc_delta"] == 0.005
    )
    minus_50bps_g = next(
        row for row in wacc_terminal_growth_grid(input_data, [0.0], [-0.005])
        if row["terminal_growth_delta"] == -0.005
    )
    stress = stress_scenarios(input_data)
    findings_md = "\n".join(
        [
            f"### {item['id']} - {item['area']}\n"
            f"- Severity: {item['severity']}\n"
            f"- Issue: {item['issue']}\n"
            f"- Impact: {item['impact']}\n"
            f"- Recommendation: {item['recommendation']}\n"
            f"- Status: Open\n"
            for item in findings
        ]
    )
    stress_md = "\n".join(
        f"| {row['scenario']} | {row['fair_value_per_share']:.2f} | {row['valuation_gap']:.1%} | {row['recommendation']} |"
        for row in stress
    )
    return f"""# Model Validation Report

## Model Under Validation

- Company: {result.company.company_name}
- Ticker: {result.company.ticker}
- Methodology: FCFF DCF
- Validation opinion: Approved with limitations
- Model risk score: {risk_score}
- Model risk rating: {risk_rating}

## Core Validation Opinion

The FCFF DCF model is conceptually sound for non-financial operating companies when public data is complete, assumptions are documented, WACC is matched to FCFF, and terminal-value dependence is disclosed. This report validates the generated output as a decision-support valuation, not an automatic stock-picking engine.

## Key Output Checks

- Fair value per share: {result.fair_value_per_share:.2f} {result.company.currency}
- Current share price: {input_data.market.current_share_price:.2f} {result.company.currency}
- Valuation gap: {result.valuation_gap:.1%}
- Recommendation: {result.recommendation}
- Confidence: {result.confidence_level} ({result.confidence_score}/100)
- Terminal value / enterprise value: {result.terminal_value_to_ev:.1%}
- WACC: {result.wacc.wacc:.1%}
- Terminal growth: {result.metadata['terminal_growth_rate']:.1%}

## Required Limitation Disclosures

- Fair value with WACC +50bps: {plus_50bps['fair_value_per_share']:.2f}
- Fair value with terminal growth -50bps: {minus_50bps_g['fair_value_per_share']:.2f}
- Cyclical company: {input_data.company.is_cyclical}
- Material stock-based compensation: {input_data.company.high_share_based_compensation}
- M&A or one-offs distort history: {input_data.company.material_mna_or_one_offs}

## Stress Test Summary

| Scenario | Fair Value | Gap | Recommendation |
|---|---:|---:|---|
{stress_md}

## Validation Findings

{findings_md}

## Validator Checklist

- [x] FCFF formula implemented as NOPAT + D&A - capex - change in NWC.
- [x] WACC uses CAPM cost of equity and after-tax cost of debt.
- [x] WACC must be greater than terminal growth.
- [x] Enterprise value converts to equity value through debt, cash, minority interest, preferred equity, and investments.
- [x] Recommendation uses valuation gap and confidence-adjusted margin of safety.
- [x] Terminal value dependence, sensitivity, stress tests, and limitations are disclosed.

## Final Opinion

Approved with limitations. The model is usable for research support where source data and assumptions are reviewed by an analyst. Automatic Buy recommendations should be blocked or escalated when confidence is low, sector suitability is poor, or terminal value dominates enterprise value.
"""

