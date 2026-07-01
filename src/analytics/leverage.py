"""
Sprint 2


Leverage & Efficiency KPIs

Only mathematical functions.
No SQL.
No CSV.
"""

from typing import Optional


def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:

    equity = equity_capital + reserves

    # Debt free company
    if borrowings == 0:
        return 0.0

    # Invalid denominator
    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )


def interest_coverage(
    operating_profit: float,
    other_income: float,
    interest: float
) -> Optional[float]:

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def asset_turnover(
    sales: float,
    total_assets: float
) -> Optional[float]:

    if total_assets <= 0:
        return None

    return round(
        sales / total_assets,
        2
    )


def net_debt(
    borrowings: float,
    investments: float
):

    return round(
        borrowings - investments,
        2
    )


def high_leverage_flag(
    debt_to_equity_ratio: Optional[float]
) -> bool:

    if debt_to_equity_ratio is None:
        return False

    return debt_to_equity_ratio > 5


def interest_coverage_label(
    interest: float
) -> str:

    if interest == 0:
        return "Debt Free"

    return ""