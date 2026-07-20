"""Populate the financial_ratios table with computed Sprint 2 KPIs."""

from __future__ import annotations

import logging
from pathlib import Path
import sqlite3
from typing import Any

import pandas as pd

from cagr import calculate_cagr
from cashflow_kpis import (
    calculate_capex_intensity,
    calculate_cfo_quality_score,
    calculate_fcf_conversion,
    calculate_free_cash_flow,
)
from leverage import (
    asset_turnover,
    debt_to_equity,
    interest_coverage,
    net_debt,
)
from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_assets,
    return_on_capital_employed,
    return_on_equity,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / ".." / "database" / "n100.db"
REPORTS_DIR = ROOT / ".." / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Add the extra columns required by the population workflow if they do not exist."""
    existing_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(financial_ratios)")
    }
    for column_name, column_type in {
        "operating_margin_pct": "REAL",
        "return_on_assets_pct": "REAL",
        "return_on_capital_employed_pct": "REAL",
        "free_cash_flow": "REAL",
        "fcf_conversion": "REAL",
        "capex_intensity": "REAL",
        "cfo_quality_score": "REAL",
        "composite_quality_score": "REAL",
        "net_debt": "REAL",
        "revenue_cagr_3yr": "REAL",
        "revenue_cagr_5yr": "REAL",
        "revenue_cagr_10yr": "REAL",
        "pat_cagr_3yr": "REAL",
        "pat_cagr_5yr": "REAL",
        "pat_cagr_10yr": "REAL",
        "eps_cagr_3yr": "REAL",
        "eps_cagr_5yr": "REAL",
        "eps_cagr_10yr": "REAL",
    }.items():
        if column_name not in existing_columns:
            conn.execute(f"ALTER TABLE financial_ratios ADD COLUMN {column_name} {column_type}")


def load_input_data(db_path: Path) -> pd.DataFrame:
    """Load the core financial statement tables needed for population."""
    with sqlite3.connect(db_path) as conn:
        profit_df = pd.read_sql(
            "SELECT company_id, year, sales, operating_profit, other_income, interest, net_profit, eps, dividend_payout FROM profitandloss",
            conn,
        )
        balance_df = pd.read_sql(
            "SELECT company_id, year, equity_capital, reserves, borrowings, total_assets, investments FROM balancesheet",
            conn,
        )
        cashflow_df = pd.read_sql(
            "SELECT company_id, year, operating_activity, investing_activity, financing_activity FROM cashflow",
            conn,
        )

    profit_df = profit_df.drop_duplicates(subset=["company_id", "year"], keep="first")
    balance_df = balance_df.drop_duplicates(subset=["company_id", "year"], keep="first")
    cashflow_df = cashflow_df.drop_duplicates(subset=["company_id", "year"], keep="first")

    merged = pd.merge(profit_df, balance_df, on=["company_id", "year"], how="left")
    merged = pd.merge(merged, cashflow_df, on=["company_id", "year"], how="left")
    merged = merged.drop_duplicates(subset=["company_id", "year"], keep="first")
    return merged.sort_values(["company_id", "year"]).reset_index(drop=True)


def compute_cagr_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute 3-, 5- and 10-year CAGR values for revenue, PAT and EPS."""
    working_df = df.copy()
    working_df["financial_year"] = pd.to_numeric(
        working_df["year"].astype(str).str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )
    working_df = working_df.dropna(subset=["financial_year"]).copy()
    working_df["financial_year"] = working_df["financial_year"].astype(int)

    rows: list[dict[str, Any]] = []
    for company_id, group in working_df.groupby("company_id", sort=True):
        group = group.sort_values("financial_year").reset_index(drop=True)
        for _, current in group.iterrows():
            current_year = int(current["financial_year"])
            row = {
                "company_id": company_id,
                "year": current["year"],
            }
            for horizon in (3, 5, 10):
                prior_year = current_year - horizon
                prior = group[group["financial_year"] == prior_year]
                if prior.empty:
                    row[f"revenue_cagr_{horizon}yr"] = None
                    row[f"pat_cagr_{horizon}yr"] = None
                    row[f"eps_cagr_{horizon}yr"] = None
                    continue
                prior = prior.iloc[0]
                revenue_value, _ = calculate_cagr(float(prior["sales"]), float(current["sales"]), horizon)
                pat_value, _ = calculate_cagr(float(prior["net_profit"]), float(current["net_profit"]), horizon)
                eps_value, _ = calculate_cagr(float(prior["eps"]), float(current["eps"]), horizon)
                row[f"revenue_cagr_{horizon}yr"] = revenue_value
                row[f"pat_cagr_{horizon}yr"] = pat_value
                row[f"eps_cagr_{horizon}yr"] = eps_value
            rows.append(row)
    return pd.DataFrame(rows)


def build_population_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Build the financial ratio population dataset with the requested KPIs."""
    result_df = df.copy()
    result_df["net_profit_margin_pct"] = result_df.apply(
        lambda row: net_profit_margin(row.get("net_profit", 0), row.get("sales", 0)), axis=1
    )
    result_df["operating_margin_pct"] = result_df.apply(
        lambda row: operating_profit_margin(row.get("operating_profit", 0), row.get("sales", 0)), axis=1
    )
    result_df["return_on_equity_pct"] = result_df.apply(
        lambda row: return_on_equity(row.get("net_profit", 0), row.get("equity_capital", 0), row.get("reserves", 0)), axis=1
    )
    result_df["return_on_assets_pct"] = result_df.apply(
        lambda row: return_on_assets(row.get("net_profit", 0), row.get("total_assets", 0)), axis=1
    )
    result_df["return_on_capital_employed_pct"] = result_df.apply(
        lambda row: return_on_capital_employed(row.get("operating_profit", 0), row.get("equity_capital", 0), row.get("reserves", 0), row.get("borrowings", 0)), axis=1
    )
    result_df["debt_to_equity"] = result_df.apply(
        lambda row: debt_to_equity(row.get("borrowings", 0), row.get("equity_capital", 0), row.get("reserves", 0)), axis=1
    )
    result_df["interest_coverage"] = result_df.apply(
        lambda row: interest_coverage(row.get("operating_profit", 0), row.get("other_income", 0), row.get("interest", 0)), axis=1
    )
    result_df["asset_turnover"] = result_df.apply(
        lambda row: asset_turnover(row.get("sales", 0), row.get("total_assets", 0)), axis=1
    )
    result_df["net_debt"] = result_df.apply(
        lambda row: net_debt(row.get("borrowings", 0), row.get("investments", 0)), axis=1
    )
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
        lambda row: calculate_cfo_quality_score(row.get("operating_activity", 0), row.get("net_profit", 0), row.get("investing_activity", 0)), axis=1
    )
       # ---------------------------------------------------------
    # Composite Quality Score (0-100)
    # ---------------------------------------------------------

    def percentile_rank(series: pd.Series, ascending: bool = True) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce")

        if ascending:
            return numeric.rank(method="average", pct=True) * 100

        return (1 - numeric.rank(method="average", pct=True)) * 100

    result_df["roe_rank"] = percentile_rank(
        result_df["return_on_equity_pct"]
    )

    result_df["roce_rank"] = percentile_rank(
        result_df["return_on_capital_employed_pct"]
    )

    result_df["roa_rank"] = percentile_rank(
        result_df["return_on_assets_pct"]
    )

    result_df["npm_rank"] = percentile_rank(
        result_df["net_profit_margin_pct"]
    )

    result_df["cfo_rank"] = percentile_rank(
        result_df["cfo_quality_score"]
    )

    result_df["asset_turnover_rank"] = percentile_rank(
        result_df["asset_turnover"]
    )

    result_df["interest_coverage_rank"] = percentile_rank(
        result_df["interest_coverage"]
    )

    # Lower Debt-to-Equity is better
    result_df["debt_rank"] = percentile_rank(
        result_df["debt_to_equity"],
        ascending=False,
    )

   

    result_df["composite_quality_score"] = (
    result_df[
        [
            "roe_rank",
            "roce_rank",
            "roa_rank",
            "npm_rank",
            "cfo_rank",
            "asset_turnover_rank",
            "interest_coverage_rank",
            "debt_rank",
        ]
    ]
    .mean(axis=1)
    .round(2)
)

    return result_df

def write_population_table(population_df: pd.DataFrame, db_path: Path) -> int:
    """Write the computed ratios into the financial_ratios table and return the row count."""
    with sqlite3.connect(db_path) as conn:
        ensure_schema(conn)
        conn.execute("DELETE FROM financial_ratios")
        population_df[[
            "company_id",
            "year",
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
            "revenue_cagr_3yr",
            "revenue_cagr_5yr",
            "revenue_cagr_10yr",
            "pat_cagr_3yr",
            "pat_cagr_5yr",
            "pat_cagr_10yr",
            "eps_cagr_3yr",
            "eps_cagr_5yr",
            "eps_cagr_10yr",
        ]].to_sql("financial_ratios", conn, if_exists="append", index=False)
        count = conn.execute("SELECT COUNT(*) FROM financial_ratios").fetchone()[0]
    return int(count)


def write_report(count: int, reports_dir: Path) -> None:
    """Write the database population report markdown file."""
    report_path = reports_dir / "database_population_report.md"
    columns = [
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
        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "revenue_cagr_10yr",
        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "pat_cagr_10yr",
        "eps_cagr_3yr",
        "eps_cagr_5yr",
        "eps_cagr_10yr",
    ]
    report_path.write_text(
        "# Database Population Report\n\n"
        "## Objective\n"
        "Populate the financial_ratios table with computed Sprint 2 KPI values.\n\n"
        "## Formula\n"
        "- Profitability and leverage ratios are calculated using the existing analytics modules.\n"
        "- Cash flow metrics use operating, investing and financing activity flows.\n\n"
        "## Business Meaning\n"
        "- These metrics support screening, valuation and quality analysis.\n\n"
        "## Implementation\n"
        "- The workflow loads profit-and-loss, balance-sheet and cash-flow data.\n"
        "- Calculated metrics are written to the financial_ratios table.\n\n"
        "## Validation\n"
        "- A row count check confirms the table has been populated.\n"
        f"- Total rows in financial_ratios: {count}\n"
        f"- Total columns populated: {len(columns)}\n\n"
        "## Output Summary\n"
        f"- The database now contains {len(columns)} Sprint 2 KPI columns in financial_ratios.\n"
        "- All CAGR columns are present and any missing values are null-filled for unmatched horizons.\n",
        encoding="utf-8",
    )


def main() -> None:
    """Execute the financial ratio population workflow."""
    input_df = load_input_data(DB_PATH)
    population_df = build_population_frame(input_df)
    cagr_df = compute_cagr_metrics(input_df)
    population_df = population_df.merge(
        cagr_df,
        on=["company_id", "year"],
        how="left",
    )
    for column_name in [
        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "revenue_cagr_10yr",
        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "pat_cagr_10yr",
        "eps_cagr_3yr",
        "eps_cagr_5yr",
        "eps_cagr_10yr",
    ]:
        if column_name not in population_df.columns:
            population_df[column_name] = None
    count = write_population_table(population_df, DB_PATH)
    write_report(count, REPORTS_DIR)
    logger.info("financial_ratios row count: %s", count)
    print(f"Rows written: {count}")


if __name__ == "__main__":
    main()
