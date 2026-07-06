import pandas as pd

from src.screener.scoring import (
    compute_cash_quality_score,
    compute_composite_score,
    compute_growth_score,
    compute_leverage_score,
    compute_profitability_score,
)


def make_scoring_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "company_id": "A",
                "return_on_equity_pct": 20,
                "return_on_capital_employed_pct": 18,
                "net_profit_margin_pct": 15,
                "free_cash_flow": 500,
                "cfo_quality_score": 80,
                "revenue_cagr_5yr": 12,
                "pat_cagr_5yr": 14,
                "debt_to_equity": 0.5,
                "interest_coverage": 6,
                "broad_sector": "Industrials",
            },
            {
                "company_id": "B",
                "return_on_equity_pct": 10,
                "return_on_capital_employed_pct": 8,
                "net_profit_margin_pct": 6,
                "free_cash_flow": -50,
                "cfo_quality_score": 30,
                "revenue_cagr_5yr": 8,
                "pat_cagr_5yr": 5,
                "debt_to_equity": 2.0,
                "interest_coverage": 1,
                "broad_sector": "Industrials",
            },
        ]
    )


def test_compute_profitability_score_returns_series():
    result = compute_profitability_score(make_scoring_df())

    assert isinstance(result, pd.Series)
    assert result.notna().all()


def test_compute_cash_quality_score_returns_series():
    result = compute_cash_quality_score(make_scoring_df())

    assert isinstance(result, pd.Series)
    assert result.notna().all()


def test_compute_growth_score_returns_series():
    result = compute_growth_score(make_scoring_df())

    assert isinstance(result, pd.Series)
    assert result.notna().all()


def test_compute_leverage_score_returns_series():
    result = compute_leverage_score(make_scoring_df())

    assert isinstance(result, pd.Series)
    assert result.notna().all()


def test_compute_composite_score_adds_expected_columns():
    result = compute_composite_score(make_scoring_df())

    assert "composite_score" in result.columns
    assert "sector_score" in result.columns
    assert "overall_score" in result.columns


def test_composite_scores_are_bounded_between_zero_and_hundred():
    result = compute_composite_score(make_scoring_df())

    assert result["composite_score"].between(0, 100).all()


def test_sector_scores_are_calculated_per_sector():
    result = compute_composite_score(make_scoring_df())

    assert result["sector_score"].notna().all()
