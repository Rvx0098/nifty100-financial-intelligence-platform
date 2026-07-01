"""Populate the financial_ratios table with computed KPI values."""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_assets,
    return_on_capital_employed,
    return_on_equity,
)
from leverage import (
    asset_turnover,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage,
    interest_coverage_label,
    net_debt,
)
from cagr import calculate_cagr
from cashflow_kpis import (
    calculate_capex_intensity,
    calculate_cfo_quality_score,
    calculate_fcf_conversion,
    calculate_free_cash_flow,
    classify_capital_allocation_pattern,
)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / ".." / "database" / "n100.db"


def load_source_data(db_path: Path) -> pd.DataFrame:
    """Load the financial data needed to build the ratio dataset."""
    with sqlite3.connect(db_path) as conn:
        profit_df = pd.read_sql("SELECT * FROM profitandloss", conn)
        balance_df = pd.read_sql("SELECT * FROM balancesheet", conn)
        cashflow_df = pd.read_sql("SELECT * FROM cashflow", conn)

    merged = pd.merge(profit_df, balance_df, on=["company_id", "year"], how="left")
    merged = pd.merge(merged, cashflow_df, on=["company_id", "year"], how="left")
    return merged.sort_values(["company_id", "year"]).reset_index(drop=True)


def build_ratio_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the financial ratios and store them in a DataFrame."""
    ratio_df = df.copy()
    ratio_df["net_profit_margin_pct"] = ratio_df.apply(
        lambda row: net_profit_margin(row.get("net_profit", 0), row.get("sales", 0)), axis=1
    )
    ratio_df["operating_profit_margin_pct"] = ratio_df.apply(
        lambda row: operating_profit_margin(row.get("operating_profit", 0), row.get("sales", 0)), axis=1
    )
    ratio_df["return_on_equity_pct"] = ratio_df.apply(
        lambda row: return_on_equity(
            row.get("net_profit", 0), row.get("equity_capital", 0), row.get("reserves", 0)
        ), axis=1
    )
    ratio_df["return_on_assets_pct"] = ratio_df.apply(
        lambda row: return_on_assets(row.get("net_profit", 0), row.get("total_assets", 0)), axis=1
    )
    ratio_df["return_on_capital_employed_pct"] = ratio_df.apply(
        lambda row: return_on_capital_employed(
            row.get("operating_profit", 0), row.get("equity_capital", 0), row.get("reserves", 0), row.get("borrowings", 0)
        ), axis=1
    )
    ratio_df["debt_to_equity"] = ratio_df.apply(
        lambda row: debt_to_equity(row.get("borrowings", 0), row.get("equity_capital", 0), row.get("reserves", 0)), axis=1
    )
    ratio_df["interest_coverage"] = ratio_df.apply(
        lambda row: interest_coverage(row.get("operating_profit", 0), row.get("other_income", 0), row.get("interest", 0)), axis=1
    )
    ratio_df["asset_turnover"] = ratio_df.apply(
        lambda row: asset_turnover(row.get("sales", 0), row.get("total_assets", 0)), axis=1
    )
    ratio_df["net_debt"] = ratio_df.apply(
        lambda row: net_debt(row.get("borrowings", 0), row.get("investments", 0)), axis=1
    )
    ratio_df["high_leverage_flag"] = ratio_df["debt_to_equity"].apply(high_leverage_flag)
    ratio_df["interest_coverage_label"] = ratio_df["interest"].apply(interest_coverage_label)
    ratio_df["free_cash_flow_cr"] = ratio_df.apply(
        lambda row: calculate_free_cash_flow(row.get("operating_activity", 0), row.get("investing_activity", 0)), axis=1
    )
    ratio_df["capex_cr"] = ratio_df.apply(
        lambda row: calculate_capex_intensity(row.get("investing_activity", 0), row.get("sales", 0)), axis=1
    )
    ratio_df["earnings_per_share"] = ratio_df["eps"]
    ratio_df["book_value_per_share"] = ratio_df.apply(
        lambda row: (row.get("equity_capital", 0) + row.get("reserves", 0)) / max(1.0, row.get("face_value", 1.0)), axis=1
    )
    ratio_df["dividend_payout_ratio_pct"] = ratio_df["dividend_payout"]
    ratio_df["total_debt_cr"] = ratio_df["borrowings"]
    ratio_df["cash_from_operations_cr"] = ratio_df["operating_activity"]
    ratio_df["cfo_quality_score"] = ratio_df.apply(
        lambda row: calculate_cfo_quality_score(row.get("operating_activity", 0), row.get("net_profit", 0), row.get("investing_activity", 0)), axis=1
    )
    ratio_df["capital_allocation_pattern"] = ratio_df.apply(
        lambda row: classify_capital_allocation_pattern(
            row.get("operating_activity", 0),
            row.get("investing_activity", 0),
            row.get("financing_activity", 0),
        ), axis=1
    )
    return ratio_df


def write_ratio_table(ratio_df: pd.DataFrame, db_path: Path) -> None:
    """Write the computed ratios into the financial_ratios table."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM financial_ratios")
        ratio_df[[
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "capex_cr",
            "earnings_per_share",
            "book_value_per_share",
            "dividend_payout_ratio_pct",
            "total_debt_cr",
            "cash_from_operations_cr",
        ]].to_sql("financial_ratios", conn, if_exists="append", index=False)


def main() -> None:
    """Run the financial ratio population workflow."""
    source_df = load_source_data(DB_PATH)
    ratio_df = build_ratio_frame(source_df)
    write_ratio_table(ratio_df, DB_PATH)
    print(ratio_df[["company_id", "year", "net_profit_margin_pct", "return_on_equity_pct"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
