"""
Financial Ratio Functions

Sprint 2
Day 08

These functions only perform calculations.
No database operations should be written here.
"""

from typing import Optional


def net_profit_margin(
    net_profit: float,
    sales: float
) -> Optional[float]:

    if sales <= 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:

    if sales <= 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:

    if total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


def return_on_capital_employed(
    operating_profit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:

    capital = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital <= 0:
        return None

    return round(
        (operating_profit / capital) * 100,
        2
    )