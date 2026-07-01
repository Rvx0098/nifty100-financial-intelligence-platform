"""Edge case analysis for Sprint 2 financial ratio outputs."""

from __future__ import annotations

import logging
from pathlib import Path
import sqlite3

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / ".." / "database" / "n100.db"
REPORTS_DIR = ROOT / ".." / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_inputs(db_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the financial data necessary for edge-case comparisons."""
    with sqlite3.connect(db_path) as conn:
        companies_df = pd.read_sql("SELECT id, company_name FROM companies", conn)
        sectors_df = pd.read_sql("SELECT company_id, broad_sector, sub_sector FROM sectors", conn)
        columns = [row[1] for row in conn.execute("PRAGMA table_info(financial_ratios)")]
        selected_columns = [
            column for column in ["company_id", "year", "return_on_equity_pct", "return_on_assets_pct", "return_on_capital_employed_pct"] if column in columns
        ]
        ratios_df = pd.read_sql(f"SELECT {', '.join(selected_columns)} FROM financial_ratios", conn)

    profitability_path = REPORTS_DIR / "profitability_ratios.csv"
    if profitability_path.exists():
        imported_df = pd.read_csv(profitability_path)
        imported_df = imported_df[["company_id", "year", "return_on_equity_pct", "return_on_capital_employed_pct"]].copy()
        imported_df = imported_df.rename(
            columns={
                "return_on_equity_pct": "imported_return_on_equity_pct",
                "return_on_capital_employed_pct": "imported_return_on_capital_employed_pct",
            }
        )
    else:
        imported_df = pd.DataFrame(
            columns=["company_id", "year", "imported_return_on_equity_pct", "imported_return_on_capital_employed_pct"]
        )

    return companies_df, sectors_df, ratios_df, imported_df


def classify_company(company_sector: str | None) -> str:
    """Return a financial-sector carve-out label for the company."""
    if company_sector is None:
        return "Other"
    sector_name = company_sector.lower()
    if any(keyword in sector_name for keyword in ("bank", "nbfc", "insurance", "finance", "financial")):
        return "Financial"
    return "Non-Financial"


def build_edge_case_report(
    companies_df: pd.DataFrame,
    sectors_df: pd.DataFrame,
    ratios_df: pd.DataFrame,
    imported_df: pd.DataFrame,
) -> pd.DataFrame:
    """Flag financial-sector edge cases and compare the computed ratios against current data."""
    merged = pd.merge(companies_df, sectors_df, left_on="id", right_on="company_id", how="left")
    merged = pd.merge(merged, ratios_df, left_on="id", right_on="company_id", how="left")
    merged = pd.merge(
        merged,
        imported_df,
        left_on=["id", "year"],
        right_on=["company_id", "year"],
        how="left",
        suffixes=(None, "_imported"),
    )
    merged["sector_classification"] = merged["broad_sector"].apply(classify_company)
    merged["roe_difference_pct"] = merged["return_on_equity_pct"] - merged["imported_return_on_equity_pct"]
    merged["roce_difference_pct"] = merged["return_on_capital_employed_pct"] - merged["imported_return_on_capital_employed_pct"]
    merged["issue_category"] = merged.apply(
        lambda row: "ROE/ROCE Difference"
        if pd.notna(row.get("roe_difference_pct")) or pd.notna(row.get("roce_difference_pct"))
        else "Missing Comparison",
        axis=1,
    )
    merged = merged[merged["sector_classification"] == "Financial"]
    available_columns = [
        column for column in [
            "id",
            "company_name",
            "broad_sector",
            "sector_classification",
            "year",
            "return_on_equity_pct",
            "imported_return_on_equity_pct",
            "roe_difference_pct",
            "return_on_capital_employed_pct",
            "imported_return_on_capital_employed_pct",
            "roce_difference_pct",
            "issue_category",
        ] if column in merged.columns
    ]
    return merged[available_columns]


def write_log(report_df: pd.DataFrame, reports_dir: Path) -> None:
    """Write a text log of edge-case findings."""
    log_path = reports_dir / "ratio_edge_cases.log"
    with log_path.open("w", encoding="utf-8") as handle:
        handle.write("Ratio Edge Case Review\n")
        handle.write("=====================\n")
        handle.write("Financial sector carve-outs: suppress leverage warnings for banks, NBFCs and insurers.\n")
        if report_df.empty:
            handle.write("No financial-sector edge cases identified.\n")
            return
        handle.write(f"Total financial sector records analyzed: {len(report_df):,}\n")
        issues = report_df[report_df["issue_category"] == "ROE/ROCE Difference"]
        handle.write(f"ROE/ROCE comparison rows: {len(issues):,}\n")
        handle.write("\nTop differences:\n")
        sample = issues.sort_values(by=["roe_difference_pct", "roce_difference_pct"], ascending=False).head(20)
        for _, row in sample.iterrows():
            handle.write(
                f"- {row['id']} | {row['company_name']} | {row['broad_sector']} | "
                f"ROE computed={row.get('return_on_equity_pct')} vs imported={row.get('imported_return_on_equity_pct')} | "
                f"ROCE computed={row.get('return_on_capital_employed_pct')} vs imported={row.get('imported_return_on_capital_employed_pct')}\n"
            )


def main() -> None:
    """Run the edge-case analysis and write the report log."""
    companies_df, sectors_df, ratios_df, imported_df = load_inputs(DB_PATH)
    report_df = build_edge_case_report(companies_df, sectors_df, ratios_df, imported_df)
    write_log(report_df, REPORTS_DIR)
    logger.info("edge case report written to %s", REPORTS_DIR / "ratio_edge_cases.log")


if __name__ == "__main__":
    main()
