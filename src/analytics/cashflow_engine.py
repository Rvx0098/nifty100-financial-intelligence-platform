"""Generate cash flow KPI reports for the N100 Financial Intelligence Platform."""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd

from cashflow_kpis import (
    calculate_capex_intensity,
    calculate_cfo_quality_score,
    calculate_fcf_conversion,
    calculate_free_cash_flow,
    classify_capital_allocation_pattern,
    classify_cfo_quality_label,
)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / ".." / "database" / "n100.db"
REPORTS_DIR = ROOT / ".." / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_cashflow_data(db_path: Path) -> pd.DataFrame:
    """Load the cash flow data together with profit and balance sheet rows."""
    with sqlite3.connect(db_path) as conn:
        profit_df = pd.read_sql("SELECT company_id, year, net_profit, sales, operating_profit FROM profitandloss", conn)
        balance_df = pd.read_sql("SELECT company_id, year, borrowings, investments FROM balancesheet", conn)
        cashflow_df = pd.read_sql("SELECT company_id, year, operating_activity, investing_activity, financing_activity FROM cashflow", conn)
    merged = pd.merge(profit_df, balance_df, on=["company_id", "year"], how="left")
    return pd.merge(merged, cashflow_df, on=["company_id", "year"], how="left")


def build_cashflow_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute free cash flow and related capital allocation KPIs."""
    result_df = df.copy()
    result_df["free_cash_flow"] = result_df.apply(
        lambda row: calculate_free_cash_flow(row.get("operating_activity", 0), row.get("investing_activity", 0)), axis=1
    )
    result_df["fcf_conversion"] = result_df.apply(
        lambda row: calculate_fcf_conversion(row.get("free_cash_flow", 0), row.get("operating_profit", 0)), axis=1
    )
    result_df["capex_intensity"] = result_df.apply(
        lambda row: calculate_capex_intensity(row.get("investing_activity", 0), row.get("sales", 0)), axis=1
    )
    result_df["cfo_quality_score"] = result_df.apply(
        lambda row: calculate_cfo_quality_score(
            row.get("operating_activity", 0), row.get("net_profit", 0), row.get("investing_activity", 0)
        ), axis=1
    )
    result_df["cfo_quality_label"] = result_df.apply(
        lambda row: classify_cfo_quality_label(row.get("operating_activity", 0), row.get("net_profit", 0)), axis=1
    )
    result_df["capital_allocation_pattern"] = result_df.apply(
        lambda row: classify_capital_allocation_pattern(
            row.get("operating_activity", 0),
            row.get("investing_activity", 0),
            row.get("financing_activity", 0),
            row.get("sales", 0),
            row.get("net_profit", 0),
        ), axis=1
    )
    return result_df


def save_report(result_df: pd.DataFrame, reports_dir: Path) -> None:
    """Persist the cash flow KPI report as a CSV file."""
    result_df[[
        "company_id",
        "year",
        "free_cash_flow",
        "fcf_conversion",
        "capex_intensity",
        "cfo_quality_score",
        "cfo_quality_label",
        "capital_allocation_pattern",
    ]].to_csv(reports_dir / "capital_allocation.csv", index=False)


def main() -> None:
    """Run the cash flow KPI pipeline and write the report."""
    df = load_cashflow_data(DB_PATH)
    result_df = build_cashflow_kpis(df)
    save_report(result_df, REPORTS_DIR)
    print(result_df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
