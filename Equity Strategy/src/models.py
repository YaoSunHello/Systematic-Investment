from dataclasses import dataclass, field
from typing import Any


Number = int | float


@dataclass(frozen=True)
class HistoricalYear:
    year: int
    revenue: float
    ebit: float
    tax_expense: float
    pretax_income: float
    depreciation_amortisation: float
    capex: float
    net_working_capital: float
    debt: float
    cash: float
    diluted_shares: float
    minority_interest: float = 0.0
    preferred_equity: float = 0.0
    investments: float = 0.0


@dataclass(frozen=True)
class MarketInputs:
    current_share_price: float
    beta: float
    risk_free_rate: float
    equity_risk_premium: float
    pre_tax_cost_of_debt: float
    marginal_tax_rate: float
    market_cap: float | None = None


@dataclass(frozen=True)
class ForecastAssumptions:
    forecast_years: int
    revenue_growth: list[float]
    ebit_margin: list[float]
    tax_rate: float
    depreciation_amortisation_to_sales: float
    capex_to_sales: float
    nwc_to_sales: float
    terminal_growth_rate: float


@dataclass(frozen=True)
class CompanyProfile:
    company_name: str
    ticker: str
    exchange: str
    currency: str
    sector: str
    company_type: str
    is_cyclical: bool = False
    high_share_based_compensation: bool = False
    material_mna_or_one_offs: bool = False
    data_sources: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ValuationInput:
    company: CompanyProfile
    history: list[HistoricalYear]
    market: MarketInputs
    assumptions: ForecastAssumptions


@dataclass(frozen=True)
class CleanedFinancials:
    history: list[HistoricalYear]
    ratios: dict[str, list[float | None]]
    latest: HistoricalYear


@dataclass(frozen=True)
class ForecastYear:
    year: int
    revenue: float
    ebit: float
    nopat: float
    depreciation_amortisation: float
    capex: float
    net_working_capital: float
    change_in_nwc: float
    fcff: float


@dataclass(frozen=True)
class WaccResult:
    cost_of_equity: float
    after_tax_cost_of_debt: float
    equity_weight: float
    debt_weight: float
    wacc: float


@dataclass(frozen=True)
class ValuationResult:
    company: CompanyProfile
    forecast: list[ForecastYear]
    wacc: WaccResult
    pv_fcff: list[float]
    terminal_value: float
    pv_terminal_value: float
    enterprise_value: float
    equity_value: float
    fair_value_per_share: float
    valuation_gap: float
    recommendation: str
    confidence_score: int
    confidence_level: str
    terminal_value_to_ev: float
    limitations: list[str]
    flags: list[str]
    data_quality_flags: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

