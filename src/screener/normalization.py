"""Normalization helpers for screener scoring."""

from __future__ import annotations

import pandas as pd


def winsorize_series(series: pd.Series, lower: float = 0.1, upper: float = 0.9) -> pd.Series:
    """Cap outliers using the specified percentile bounds."""

    working = series.astype(float).copy()
    if working.dropna().empty:
        return working

    lower_bound = working.quantile(lower)
    upper_bound = working.quantile(upper)
    capped = working.copy()
    capped = capped.clip(lower_bound, upper_bound)
    return capped


def normalize_series(series: pd.Series) -> pd.Series:
    """Scale a numeric series to the 0-100 range while handling NaN and constants."""

    working = series.astype(float).copy()
    if working.dropna().empty:
        return pd.Series(pd.NA, index=series.index, dtype="Float64")

    cleaned = working.dropna()
    if cleaned.nunique(dropna=True) <= 1:
        return pd.Series(50.0, index=series.index, dtype="float64")

    minimum = cleaned.min()
    maximum = cleaned.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(50.0, index=series.index, dtype="float64")

    normalized = (working - minimum) / (maximum - minimum) * 100.0
    return normalized.where(working.notna(), pd.NA)
