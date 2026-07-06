"""Preset screener implementations built on reusable filter helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.screener.filters import (
    filter_debt_to_equity,
    filter_debt_to_equity_improving,
    filter_dividend_payout,
    filter_dividend_yield,
    filter_free_cash_flow,
    filter_pat_cagr,
    filter_pb,
    filter_pe,
    filter_revenue_cagr,
    filter_revenue_cagr_3yr,
    filter_roe,
    filter_sales,
)


def _ensure_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the dataframe or an empty dataframe when needed."""

    if df is None or df.empty:
        return pd.DataFrame(columns=["company_id"])

    return df.copy()


def _rank_results(df: pd.DataFrame, sort_column: str | None = None, ascending: bool = False) -> pd.DataFrame:
    """Sort results by composite score when available, otherwise by the configured metric."""

    working = df.copy()
    if working.empty:
        return working

    if "composite_score" in working.columns:
        return working.sort_values(by="composite_score", ascending=False).reset_index(drop=True)

    if sort_column and sort_column in working.columns:
        return working.sort_values(by=sort_column, ascending=ascending).reset_index(drop=True)

    return working.reset_index(drop=True)


def quality_compounder(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies that look like high-quality compounders."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_roe(working, 15)
    filtered = filter_debt_to_equity(filtered, 1)
    filtered = filter_free_cash_flow(filtered, 0)
    filtered = filter_revenue_cagr(filtered, 10)

    return _rank_results(filtered, sort_column="return_on_equity_pct", ascending=False)


def value_pick(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies that appear undervalued on basic valuation metrics."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_pe(working, 20)
    filtered = filter_pb(filtered, 3)
    filtered = filter_debt_to_equity(filtered, 2)
    filtered = filter_dividend_yield(filtered, 1)

    return _rank_results(filtered, sort_column="pe_ratio", ascending=True)


def growth_accelerator(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies with strong growth and acceptable leverage."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_pat_cagr(working, 20)
    filtered = filter_revenue_cagr(filtered, 15)
    filtered = filter_debt_to_equity(filtered, 2)

    return _rank_results(filtered, sort_column="pat_cagr_5yr", ascending=False)


def dividend_champion(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies with strong dividend characteristics."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_dividend_yield(working, 2)
    filtered = filter_dividend_payout(filtered, 80)
    filtered = filter_free_cash_flow(filtered, 0)

    return _rank_results(filtered, sort_column="dividend_yield_pct", ascending=False)


def debt_free_bluechip(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies with zero debt, strong ROE, and large sales."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_debt_to_equity(working, 0)
    filtered = filter_roe(filtered, 12)
    filtered = filter_sales(filtered, 5000)

    return _rank_results(filtered, sort_column="market_cap_crore", ascending=False)


def turnaround_watch(df: pd.DataFrame) -> pd.DataFrame:
    """Return companies with improving revenue growth and positive cash flow."""

    working = _ensure_dataframe(df)
    if working.empty:
        return working

    filtered = filter_revenue_cagr_3yr(working, 10)
    filtered = filter_free_cash_flow(filtered, 0)
    filtered = filter_debt_to_equity_improving(filtered)

    return filtered.reset_index(drop=True)


def run_preset(dataframe: pd.DataFrame, preset_name: str) -> pd.DataFrame:
    """Dispatch to the requested preset screener."""

    preset_map: dict[str, Any] = {
        "quality_compounder": quality_compounder,
        "value_pick": value_pick,
        "growth_accelerator": growth_accelerator,
        "dividend_champion": dividend_champion,
        "debt_free_bluechip": debt_free_bluechip,
        "turnaround_watch": turnaround_watch,
    }

    if preset_name not in preset_map:
        raise ValueError(f"Unknown preset: {preset_name}")

    return preset_map[preset_name](dataframe)
