import pandas as pd

from src.screener.filters import (
    filter_roe,
    filter_debt_to_equity,
)


def test_filter_roe():
    df = pd.DataFrame(
        {
            "company": ["A", "B", "C"],
            "return_on_equity_pct": [10, 18, 25],
        }
    )

    result = filter_roe(df, 15)

    assert list(result["company"]) == ["B", "C"]


def test_filter_debt_to_equity():
    df = pd.DataFrame(
        {
            "company": ["A", "B", "C"],
            "debt_to_equity": [0.2, 1.5, 0.8],
        }
    )

    result = filter_debt_to_equity(df, 1.0)

    assert list(result["company"]) == ["A", "C"]