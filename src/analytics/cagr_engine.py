"""Generate CAGR reports from the SQLite financial statements database."""

from __future__ import annotations

import logging
from pathlib import Path
import sqlite3
from typing import Any

import pandas as pd

from cagr import calculate_cagr

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / ".." / "database" / "n100.db"
REPORTS_DIR = ROOT / ".." / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_financial_data(db_path: Path) -> pd.DataFrame:
    """Load the relevant financial statement data from SQLite."""
    with sqlite3.connect(db_path) as conn:
        profit_df = pd.read_sql(
            "SELECT company_id, year, sales, net_profit, eps FROM profitandloss",
            conn,
        )
    profit_df = profit_df[profit_df["year"] != "TTM"].copy()
    profit_df["financial_year"] = profit_df["year"].str.extract(r"(\d{4})").astype(int)
    return profit_df.sort_values(["company_id", "financial_year"]).reset_index(drop=True)


def build_cagr_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue, PAT and EPS CAGR values for 3, 5 and 10-year horizons."""
    rows: list[dict[str, Any]] = []
    for company_id, group in df.groupby("company_id", sort=True):
        group = group.reset_index(drop=True)
        for _, current in group.iterrows():
            current_year = int(current["financial_year"])
            for horizon in (3, 5, 10):
                prior_year = current_year - horizon
                prior = group[group["financial_year"] == prior_year]
                if prior.empty:
                    continue
                prior = prior.iloc[0]
                revenue_value, revenue_flag = calculate_cagr(
                    float(prior["sales"]), float(current["sales"]), horizon
                )
                pat_value, pat_flag = calculate_cagr(
                    float(prior["net_profit"]), float(current["net_profit"]), horizon
                )
                eps_value, eps_flag = calculate_cagr(
                    float(prior["eps"]), float(current["eps"]), horizon
                )
                rows.append(
                    {
                        "company_id": company_id,
                        "year": current["year"],
                        "horizon_years": horizon,
                        "revenue_cagr_value": revenue_value,
                        "revenue_cagr_flag": revenue_flag,
                        "pat_cagr_value": pat_value,
                        "pat_cagr_flag": pat_flag,
                        "eps_cagr_value": eps_value,
                        "eps_cagr_flag": eps_flag,
                    }
                )
    return pd.DataFrame(rows)


def save_reports(result_df: pd.DataFrame, reports_dir: Path) -> None:
    """Persist CAGR outputs into CSV files for downstream reporting."""
    revenue = result_df[[
        "company_id",
        "year",
        "horizon_years",
        "revenue_cagr_value",
        "revenue_cagr_flag",
    ]].copy()
    pat = result_df[[
        "company_id",
        "year",
        "horizon_years",
        "pat_cagr_value",
        "pat_cagr_flag",
    ]].copy()
    eps = result_df[[
        "company_id",
        "year",
        "horizon_years",
        "eps_cagr_value",
        "eps_cagr_flag",
    ]].copy()
    edge_cases = result_df[
        result_df["revenue_cagr_flag"].ne("NORMAL")
        | result_df["pat_cagr_flag"].ne("NORMAL")
        | result_df["eps_cagr_flag"].ne("NORMAL")
    ].copy()

    revenue.to_csv(reports_dir / "revenue_cagr.csv", index=False)
    pat.to_csv(reports_dir / "pat_cagr.csv", index=False)
    eps.to_csv(reports_dir / "eps_cagr.csv", index=False)
    edge_cases.to_csv(reports_dir / "cagr_edge_cases.csv", index=False)


def main() -> None:
    """Run the CAGR pipeline and write all requested reports."""
    df = load_financial_data(DB_PATH)
    result_df = build_cagr_rows(df)
    save_reports(result_df, REPORTS_DIR)
    logger.info("CAGR reports written to %s", REPORTS_DIR)
    print(result_df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
