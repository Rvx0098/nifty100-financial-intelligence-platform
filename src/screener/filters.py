"""
Screener Filter Functions

Each function performs ONE filtering operation.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def filter_roe(
    df: pd.DataFrame,
    minimum: float,
) -> pd.DataFrame:
    """
    Filter companies having ROE
    greater than or equal to minimum.
    """

    return df[
        df["return_on_equity_pct"] >= minimum
    ].copy()

def filter_roce(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum ROCE."""
    return df[df["return_on_capital_employed_pct"] >= minimum].copy()


def filter_debt_to_equity(df: pd.DataFrame, maximum: float) -> pd.DataFrame:
    """Filter companies by maximum Debt-to-Equity ratio."""
    return df[df["debt_to_equity"] <= maximum].copy()


def filter_free_cash_flow(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum Free Cash Flow."""
    return df[df["free_cash_flow"] >= minimum].copy()


def filter_revenue_cagr(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum 5-year Revenue CAGR."""
    return df[df["revenue_cagr_5yr"] >= minimum].copy()


def filter_pat_cagr(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum 5-year PAT CAGR."""
    return df[df["pat_cagr_5yr"] >= minimum].copy()


def filter_eps_cagr(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum 5-year EPS CAGR."""
    return df[df["eps_cagr_5yr"] >= minimum].copy()


def filter_sales(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum sales."""
    return df[df["sales"] >= minimum].copy()


def filter_asset_turnover(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum asset turnover."""
    return df[df["asset_turnover"] >= minimum].copy()


def filter_interest_coverage(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """
    Filter companies by Interest Coverage.

    Companies labelled 'Debt Free' always pass.
    """
    mask = (
        (df["interest_coverage"] >= minimum)
        | (df["interest_coverage_label"] == "Debt Free")
    )
    return df[mask].copy()


def filter_pe(df: pd.DataFrame, maximum: float) -> pd.DataFrame:
    """Filter companies by maximum PE ratio."""
    return df[df["pe_ratio"] <= maximum].copy()


def filter_pb(df: pd.DataFrame, maximum: float) -> pd.DataFrame:
    """Filter companies by maximum PB ratio."""
    return df[df["pb_ratio"] <= maximum].copy()


def filter_dividend_yield(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum dividend yield."""
    return df[df["dividend_yield_pct"] >= minimum].copy()


def filter_dividend_payout(df: pd.DataFrame, maximum: float) -> pd.DataFrame:
    """Filter companies by maximum dividend payout ratio."""
    return df[df["dividend_payout_ratio_pct"] <= maximum].copy()


def filter_revenue_cagr_3yr(df: pd.DataFrame, minimum: float) -> pd.DataFrame:
    """Filter companies by minimum 3-year revenue CAGR."""
    return df[df["revenue_cagr_3yr"] >= minimum].copy()


def filter_debt_to_equity_improving(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder helper for debt-to-equity improvement analysis.

    The current dataset does not contain a year-over-year panel needed to
    calculate improvement reliably, so this helper intentionally preserves the
    current rows and leaves a TODO for future implementation.
    """

    logger.info("TODO: calculate year-over-year debt-to-equity improvement")
    return df.copy()