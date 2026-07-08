def base_recommendation(valuation_gap: float) -> str:
    if valuation_gap > 0.20:
        return "Buy"
    if valuation_gap >= 0.05:
        return "Moderate Buy / Accumulate"
    if valuation_gap >= -0.05:
        return "Hold / Fairly Valued"
    if valuation_gap >= -0.20:
        return "Reduce / Moderate Sell"
    return "Sell"


def confidence_adjusted_recommendation(valuation_gap: float, confidence_level: str) -> str:
    if confidence_level == "High" and valuation_gap > 0.15:
        return "Buy"
    if confidence_level == "Medium" and valuation_gap > 0.25:
        return "Buy"
    if confidence_level == "Low" and valuation_gap > 0.35:
        return "Speculative Buy / Analyst Review"
    if confidence_level == "Very Low" and valuation_gap > 0.20:
        return "No Automatic Buy / Analyst Review"
    return base_recommendation(valuation_gap)


def confidence_level(score: int) -> str:
    if score >= 75:
        return "High"
    if score >= 50:
        return "Medium"
    if score >= 30:
        return "Low"
    return "Very Low"

