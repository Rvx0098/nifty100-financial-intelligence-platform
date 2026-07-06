import pandas as pd

from src.screener.normalization import normalize_series, winsorize_series


def test_winsorize_series_caps_outliers():
    series = pd.Series([1, 2, 3, 100])
    result = winsorize_series(series)

    assert result.iloc[3] <= series.quantile(0.9)
    assert result.iloc[0] >= series.quantile(0.1)


def test_winsorize_series_handles_empty():
    result = winsorize_series(pd.Series([], dtype=float))

    assert result.empty


def test_normalize_series_scales_to_100_range():
    series = pd.Series([0, 50, 100])
    result = normalize_series(series)

    assert result.iloc[0] == 0.0
    assert result.iloc[2] == 100.0


def test_normalize_series_handles_constant_values():
    result = normalize_series(pd.Series([5, 5, 5]))

    assert result.iloc[0] == 50.0


def test_normalize_series_handles_nan():
    result = normalize_series(pd.Series([1, None, 3]))

    assert result.isna().sum() == 1
