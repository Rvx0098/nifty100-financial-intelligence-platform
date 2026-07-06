import pandas as pd

from src.screener.engine import _select_latest_snapshot, load_financial_data, run_screener


def test_select_latest_snapshot_keeps_latest_row_per_company():
    df = pd.DataFrame(
        [
            {"company_id": "A", "financial_year": 2022},
            {"company_id": "A", "financial_year": 2023},
            {"company_id": "B", "financial_year": 2021},
        ]
    )

    result = _select_latest_snapshot(df)

    assert list(result["company_id"]) == ["A", "B"]
    assert result.loc[result["company_id"] == "A", "financial_year"].iloc[0] == 2023


def test_load_financial_data_returns_expected_columns():
    df = load_financial_data()

    assert "sales" in df.columns
    assert "market_cap_crore" in df.columns
    assert "broad_sector" in df.columns


def test_run_screener_returns_dataframe_for_valid_preset():
    result = run_screener("quality_compounder")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
