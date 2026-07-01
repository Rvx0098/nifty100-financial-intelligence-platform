import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from populate_financial_ratios import (
    build_population_frame,
    compute_cagr_metrics,
    load_input_data,
)


def test_load_input_data_returns_company_year_pairs():
    db_path = ROOT / "database" / "n100.db"
    input_df = load_input_data(db_path)
    duplicate_rows = (
        input_df.groupby(["company_id", "year"]).size().reset_index(name="count").query("count > 1")
    )
    assert duplicate_rows.empty


def test_compute_cagr_metrics_produces_one_row_per_company_year():
    db_path = ROOT / "database" / "n100.db"
    input_df = load_input_data(db_path)
    cagr_df = compute_cagr_metrics(input_df)
    assert set(["company_id", "year"]).issubset(cagr_df.columns)
    assert cagr_df.duplicated(["company_id", "year"]).sum() == 0
    expected_columns = {
        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "revenue_cagr_10yr",
        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "pat_cagr_10yr",
        "eps_cagr_3yr",
        "eps_cagr_5yr",
        "eps_cagr_10yr",
    }
    assert expected_columns.issubset(cagr_df.columns)


def test_build_population_frame_contains_required_kpis():
    db_path = ROOT / "database" / "n100.db"
    input_df = load_input_data(db_path)
    population_df = build_population_frame(input_df)
    expected_columns = {
        "net_profit_margin_pct",
        "operating_margin_pct",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "net_debt",
        "free_cash_flow",
        "fcf_conversion",
        "capex_intensity",
        "cfo_quality_score",
        "composite_quality_score",
    }
    assert expected_columns.issubset(population_df.columns)
    assert population_df.shape[0] == input_df.shape[0]


def test_population_merge_with_cagr_keeps_all_rows():
    db_path = ROOT / "database" / "n100.db"
    input_df = load_input_data(db_path)
    population_df = build_population_frame(input_df)
    cagr_df = compute_cagr_metrics(input_df)
    merged = population_df.merge(cagr_df, on=["company_id", "year"], how="left")
    assert merged.shape[0] == population_df.shape[0]
    assert "revenue_cagr_3yr" in merged.columns
    assert "eps_cagr_10yr" in merged.columns
