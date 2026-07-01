"""Cash flow KPI calculations for the N100 Financial Intelligence Platform."""

from __future__ import annotations

from typing import Optional


def calculate_free_cash_flow(
    operating_cash_flow: float,
    capex: float,
) -> float:
    """Return free cash flow as operating cash flow minus capital expenditure."""
    return round(operating_cash_flow - capex, 2)


def calculate_fcf_conversion(
    free_cash_flow: float,
    operating_profit: float,
) -> Optional[float]:
    """Return free cash flow conversion as a percentage of operating profit."""
    if operating_profit == 0:
        return None
    return round((free_cash_flow / operating_profit) * 100, 2)


def calculate_capex_intensity(
    capex: float,
    sales: float,
) -> Optional[float]:
    """Return capital expenditure intensity as a percentage of sales."""
    if sales == 0:
        return None
    return round(abs(capex) / sales * 100, 2)


def calculate_cfo_quality_score(
    operating_cash_flow: float,
    net_income: float,
    capex: float,
) -> float:
    """Return a simplified CFO quality score based on cash conversion."""
    if net_income == 0:
        return 0.0
    ratio = operating_cash_flow / net_income
    return round(max(0.0, min(100.0, ratio * 100)), 2)


def classify_cfo_quality_label(
    operating_cash_flow: float,
    net_income: float,
) -> str:
    """Classify CFO quality into simple business labels."""
    if net_income == 0:
        return "Accrual Risk"
    ratio = operating_cash_flow / net_income
    if ratio >= 1.0:
        return "High Quality"
    if ratio >= 0.5:
        return "Moderate"
    return "Accrual Risk"


def classify_capital_allocation_pattern(
    operating_cash_flow: float,
    capex: float,
    financing_cash_flow: float,
    sales: float | None = None,
    net_profit: float | None = None,
) -> str:
    """Classify capital allocation behaviour using cash flow sign patterns."""
    if sales is not None and net_profit is not None and (sales <= 0 or net_profit <= 0):
        return "Pre-Revenue"

    ocf_sign = "+" if operating_cash_flow >= 0 else "-"
    fin_sign = "+" if financing_cash_flow >= 0 else "-"
    combined_sign = "+" if capex * financing_cash_flow >= 0 else "-"

    return f"({ocf_sign}, {combined_sign}, {fin_sign})"
