"""Transparent calculation helpers for security-analysis workflows."""

from __future__ import annotations


def margin_of_safety(intrinsic_value: float, market_price: float) -> float:
    """Return margin of safety as a decimal percentage of intrinsic value."""
    if intrinsic_value <= 0:
        raise ValueError("Intrinsic value must be positive.")
    return (intrinsic_value - market_price) / intrinsic_value


def interest_coverage(operating_profit: float, interest_expense: float) -> float:
    """Return operating profit divided by interest expense."""
    if interest_expense <= 0:
        raise ValueError("Interest expense must be positive.")
    return operating_profit / interest_expense


def fixed_charge_coverage(
    operating_profit: float,
    interest_expense: float,
    lease_expense: float = 0.0,
    preferred_dividends: float = 0.0,
) -> float:
    """Return coverage of recurring fixed charges."""
    fixed_charges = interest_expense + lease_expense + preferred_dividends
    if fixed_charges <= 0:
        raise ValueError("Fixed charges must be positive.")
    return operating_profit / fixed_charges


def net_debt(total_debt: float, cash: float) -> float:
    """Return debt minus cash."""
    return total_debt - cash


def enterprise_value(
    market_capitalization: float,
    total_debt: float,
    cash: float,
    preferred_equity: float = 0.0,
    minority_interest: float = 0.0,
) -> float:
    """Return enterprise value from equity value and non-common claims."""
    return (
        market_capitalization
        + total_debt
        + preferred_equity
        + minority_interest
        - cash
    )
