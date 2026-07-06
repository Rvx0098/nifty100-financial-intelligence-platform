"""Composite scoring utilities for the screener engine."""

from __future__ import annotations

import logging

import pandas as pd

from src.screener.normalization import normalize_series, winsorize_series

logger = logging.getLogger(__name__)


def _ensure_numeric(series: pd.Series) -> pd.Series:
    """Return a numeric series with NaN values preserved."""

    return pd.to_numeric(series, errors="coerce")


def compute_profitability_score(df: pd.DataFrame) -> pd.Series:
    """Compute a profitability score from ROE, ROCE, and net profit margin."""

    roe = winsorize_series(_ensure_numeric(df["return_on_equity_pct"]))
    roce = winsorize_series(_ensure_numeric(df["return_on_capital_employed_pct"]))
    net_margin = winsorize_series(_ensure_numeric(df["net_profit_margin_pct"]))

    roe_score = normalize_series(roe)
    roce_score = normalize_series(roce)
    margin_score = normalize_series(net_margin)

    return (
        roe_score * 0.15
        + roce_score * 0.10
        + margin_score * 0.10
    )


def compute_cash_quality_score(df: pd.DataFrame) -> pd.Series:
    """Compute a cash quality score from free cash flow and CFO quality metrics."""

    fcf = winsorize_series(_ensure_numeric(df["free_cash_flow"]))
    cfo_quality = winsorize_series(_ensure_numeric(df["cfo_quality_score"]))
    positive_fcf = _ensure_numeric(df["free_cash_flow"]).gt(0).astype(float)

    fcf_score = normalize_series(fcf)
    cfo_score = normalize_series(cfo_quality)

    return (
        fcf_score * 0.15
        + cfo_score * 0.10
        + positive_fcf * 0.05
    )


def compute_growth_score(df: pd.DataFrame) -> pd.Series:
    """Compute a growth score from revenue and PAT CAGR metrics."""

    revenue_cagr = winsorize_series(_ensure_numeric(df["revenue_cagr_5yr"]))
    pat_cagr = winsorize_series(_ensure_numeric(df["pat_cagr_5yr"]))

    revenue_score = normalize_series(revenue_cagr)
    pat_score = normalize_series(pat_cagr)

    return revenue_score * 0.10 + pat_score * 0.10


def compute_leverage_score(df: pd.DataFrame) -> pd.Series:
    """Compute a leverage score while inverting debt-to-equity and using interest coverage."""

    debt_to_equity = winsorize_series(_ensure_numeric(df["debt_to_equity"]))
    interest_coverage = winsorize_series(_ensure_numeric(df["interest_coverage"]))

    debt_score = normalize_series(1 / (1 + debt_to_equity))
    coverage_score = normalize_series(interest_coverage)

    return debt_score * 0.10 + coverage_score * 0.05


def compute_composite_score(df: pd.DataFrame) -> pd.DataFrame:
    """Return the composite quality score and a sector-relative score."""

    if df.empty:
        return df.copy()

    profitability = compute_profitability_score(df)
    cash_quality = compute_cash_quality_score(df)
    growth = compute_growth_score(df)
    leverage = compute_leverage_score(df)

    overall_score = (
        profitability
        + cash_quality
        + growth
        + leverage
    )

    working = df.copy()
    working["composite_score"] = overall_score.clip(0, 100)

    if "broad_sector" in working.columns:
        sector_scores: list[float] = []
        for _, sector_df in working.groupby("broad_sector", dropna=False):
            sector_values = sector_df["composite_score"].astype(float)
            sector_ranked = normalize_series(sector_values)
            sector_scores.extend(sector_ranked.tolist())

        working["sector_score"] = sector_scores
    else:
        working["sector_score"] = pd.NA

    working["overall_score"] = working["composite_score"]
    return working
