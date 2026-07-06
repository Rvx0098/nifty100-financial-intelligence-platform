import pandas as pd

from src.screener.presets import (
    debt_free_bluechip,
    dividend_champion,
    growth_accelerator,
    quality_compounder,
    run_preset,
    turnaround_watch,
    value_pick,
)


def make_sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "company_id": "A",
                "return_on_equity_pct": 16,
                "debt_to_equity": 0.8,
                "free_cash_flow": 10,
                "revenue_cagr_5yr": 12,
                "pe_ratio": 18,
                "pb_ratio": 2.4,
                "dividend_yield_pct": 1.6,
                "pat_cagr_5yr": 25,
                "sales": 6000,
                "market_cap_crore": 5000,
                "dividend_payout_ratio_pct": 60,
                "revenue_cagr_3yr": 12,
            },
            {
                "company_id": "B",
                "return_on_equity_pct": 20,
                "debt_to_equity": 0.5,
                "free_cash_flow": 3,
                "revenue_cagr_5yr": 11,
                "pe_ratio": 22,
                "pb_ratio": 3.2,
                "dividend_yield_pct": 2.2,
                "pat_cagr_5yr": 18,
                "sales": 4500,
                "market_cap_crore": 7000,
                "dividend_payout_ratio_pct": 75,
                "revenue_cagr_3yr": 8,
            },
            {
                "company_id": "C",
                "return_on_equity_pct": 14,
                "debt_to_equity": 0.2,
                "free_cash_flow": 8,
                "revenue_cagr_5yr": 15,
                "pe_ratio": 16,
                "pb_ratio": 2.0,
                "dividend_yield_pct": 3.0,
                "pat_cagr_5yr": 22,
                "sales": 8000,
                "market_cap_crore": 9000,
                "dividend_payout_ratio_pct": 50,
                "revenue_cagr_3yr": 15,
            },
            {
                "company_id": "D",
                "return_on_equity_pct": 18,
                "debt_to_equity": 1.2,
                "free_cash_flow": 0,
                "revenue_cagr_5yr": 10,
                "pe_ratio": 15,
                "pb_ratio": 1.8,
                "dividend_yield_pct": 0.5,
                "pat_cagr_5yr": 30,
                "sales": 5200,
                "market_cap_crore": 10000,
                "dividend_payout_ratio_pct": 90,
                "revenue_cagr_3yr": 11,
            },
        ]
    )


def test_quality_compounder_filters_and_sorts():
    result = quality_compounder(make_sample_df())

    assert list(result["company_id"]) == ["B", "A"]


def test_quality_compounder_boundary_value_is_included():
    df = make_sample_df().copy()
    df.loc[df["company_id"] == "B", "return_on_equity_pct"] = 15
    result = quality_compounder(df)

    assert "B" in result["company_id"].tolist()


def test_value_pick_filters_and_sorts_by_lowest_pe():
    result = value_pick(make_sample_df())

    assert list(result["company_id"]) == ["C", "A"]


def test_growth_accelerator_filters_and_sorts_by_pat_cagr():
    result = growth_accelerator(make_sample_df())

    assert list(result["company_id"]) == ["C"]


def test_dividend_champion_filters_and_sorts_by_yield():
    result = dividend_champion(make_sample_df())

    assert list(result["company_id"]) == ["C", "B"]


def test_debt_free_bluechip_filters_and_sorts_by_market_cap():
    df = make_sample_df().copy()
    df.loc[df["company_id"] == "C", "debt_to_equity"] = 0
    result = debt_free_bluechip(df)

    assert list(result["company_id"]) == ["C"]


def test_turnaround_watch_keeps_candidates_with_todo_placeholder():
    result = turnaround_watch(make_sample_df())

    assert list(result["company_id"]) == ["A", "C", "D"]


def test_run_preset_dispatches_known_preset():
    result = run_preset(make_sample_df(), "quality_compounder")

    assert not result.empty


def test_run_preset_raises_for_invalid_preset():
    try:
        run_preset(make_sample_df(), "unknown_preset")
    except ValueError as exc:
        assert "Unknown preset" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid preset")


def test_empty_dataframe_returns_empty_for_any_preset():
    empty = pd.DataFrame(columns=["company_id"])

    result = quality_compounder(empty)

    assert result.empty


def test_threshold_edge_case_for_dividend_payout():
    df = make_sample_df().copy()
    df.loc[df["company_id"] == "B", "dividend_payout_ratio_pct"] = 80
    result = dividend_champion(df)

    assert "B" in result["company_id"].tolist()


def test_threshold_edge_case_for_debt_to_equity():
    df = make_sample_df().copy()
    df.loc[df["company_id"] == "A", "debt_to_equity"] = 1.0
    result = quality_compounder(df)

    assert "A" in result["company_id"].tolist()
