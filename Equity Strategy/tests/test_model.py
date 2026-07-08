import math
import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.data_loader import load_valuation_input
from src.dcf_engine import calculate_dcf
from src.financial_cleaner import clean_historical_financials
from src.forecast_engine import build_forecast
from src.recommendation import base_recommendation
from src.wacc_engine import calculate_wacc


def sample_input():
    return load_valuation_input(PROJECT_DIR / "data" / "raw" / "sample_company.json")


class ValuationModelTests(unittest.TestCase):
    def test_fcff_formula_first_forecast_year(self):
        data = sample_input()
        cleaned = clean_historical_financials(data.history)
        forecast = build_forecast(cleaned, data.assumptions)
        first = forecast[0]
        expected = (
            first.ebit * (1 - data.assumptions.tax_rate)
            + first.depreciation_amortisation
            - first.capex
            - first.change_in_nwc
        )
        self.assertTrue(math.isclose(first.fcff, expected, rel_tol=1e-12))

    def test_wacc_formula(self):
        data = sample_input()
        latest = data.history[-1]
        wacc = calculate_wacc(data.market, latest)
        equity_value = data.market.current_share_price * latest.diluted_shares
        debt_value = latest.debt
        expected_cost_of_equity = data.market.risk_free_rate + data.market.beta * data.market.equity_risk_premium
        expected_after_tax_debt = data.market.pre_tax_cost_of_debt * (1 - data.market.marginal_tax_rate)
        expected = (
            equity_value / (equity_value + debt_value) * expected_cost_of_equity
            + debt_value / (equity_value + debt_value) * expected_after_tax_debt
        )
        self.assertTrue(math.isclose(wacc.wacc, expected, rel_tol=1e-12))

    def test_recommendation_thresholds(self):
        self.assertEqual(base_recommendation(0.21), "Buy")
        self.assertEqual(base_recommendation(0.10), "Moderate Buy / Accumulate")
        self.assertEqual(base_recommendation(0.00), "Hold / Fairly Valued")
        self.assertEqual(base_recommendation(-0.10), "Reduce / Moderate Sell")
        self.assertEqual(base_recommendation(-0.21), "Sell")

    def test_end_to_end_valuation_runs(self):
        result = calculate_dcf(sample_input())
        self.assertGreater(result.enterprise_value, 0)
        self.assertGreater(result.equity_value, 0)
        self.assertGreater(result.fair_value_per_share, 0)
        self.assertGreater(result.wacc.wacc, result.metadata["terminal_growth_rate"])


if __name__ == "__main__":
    unittest.main()
