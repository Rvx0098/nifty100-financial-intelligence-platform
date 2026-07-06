"""
Screener Engine

Loads financial data from SQLite,
merges required tables,
and loads screener configuration.
"""

from __future__ import annotations

import logging
import re
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.screener.presets import run_preset
from src.screener.scoring import compute_composite_score

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = ROOT / "database" / "n100.db"
CONFIG_PATH = ROOT / "config" / "screener_config.yaml"
REPORTS_PATH = ROOT / "reports"


def _normalize_financial_year(values: pd.Series) -> pd.Series:
    """Normalize mixed year values into either integers or 'TTM'."""

    normalized: list[Any] = []

    for value in values:
        if pd.isna(value):
            normalized.append(pd.NA)
            continue

        if isinstance(value, str):
            text = value.strip()
        else:
            text = str(value).strip()

        if not text:
            normalized.append(pd.NA)
            continue

        if text.upper() == "TTM":
            normalized.append("TTM")
            continue

        match = re.search(r"(\d{4})", text)
        if match:
            normalized.append(int(match.group(1)))
            continue

        try:
            normalized.append(int(float(text)))
        except ValueError:
            normalized.append(text)

    return pd.Series(normalized, index=values.index, dtype="object")


def _prepare_year_key(df: pd.DataFrame) -> pd.DataFrame:
    """Add a reusable financial_year key for joining across tables."""

    prepared = df.copy()

    if "financial_year" in prepared.columns:
        prepared["financial_year"] = _normalize_financial_year(prepared["financial_year"])
    elif "year" in prepared.columns:
        prepared["financial_year"] = _normalize_financial_year(prepared["year"])
    else:
        raise KeyError("Expected a year column to normalize for the screener merge")

    return prepared


def _select_latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Keep the latest available company snapshot before running presets."""

    working = df.copy()
    if working.empty:
        return working

    if "financial_year" not in working.columns:
        raise KeyError("Expected financial_year to select the latest company snapshot")

    year_sort = []
    for value in working["financial_year"]:
        if pd.isna(value) or value == "TTM":
            year_sort.append(float("nan"))
            continue

        try:
            year_sort.append(int(value))
        except (TypeError, ValueError):
            year_sort.append(float("nan"))

    working = working.assign(_year_sort=year_sort)
    working = working.sort_values(
        by=["company_id", "_year_sort", "financial_year"],
        ascending=[True, False, False],
        na_position="last",
    )
    latest_df = working.drop_duplicates(subset=["company_id"], keep="first")
    return latest_df.drop(columns=["_year_sort"]).reset_index(drop=True)


def _log_dividend_filter_summary(df: pd.DataFrame) -> None:
    """Log descriptive statistics for the dividend-related screener filters."""

    columns = ["dividend_yield_pct", "dividend_payout_ratio_pct", "free_cash_flow"]
    available = [column for column in columns if column in df.columns]

    if not available:
        logger.warning("Dividend-related columns are missing from the screener dataframe")
        return

    summary = df[available].describe(include="all")
    logger.info("Dividend filter summary:\n%s", summary.to_string())

    if "dividend_yield_pct" in df.columns:
        dividend_yield = df["dividend_yield_pct"].dropna()
        if dividend_yield.empty or (dividend_yield >= 2).sum() == 0:
            logger.warning(
                "Dividend yield threshold >= 2 may return no companies because the current distribution has no qualifying values."
            )

    if "dividend_payout_ratio_pct" in df.columns:
        payout = df["dividend_payout_ratio_pct"].dropna()
        if payout.empty or (payout <= 80).sum() == 0:
            logger.warning(
                "Dividend payout threshold <= 80 may return no companies because the current distribution has no qualifying values."
            )

    if "free_cash_flow" in df.columns:
        fcf = df["free_cash_flow"].dropna()
        if fcf.empty or (fcf > 0).sum() == 0:
            logger.warning(
                "Free cash flow threshold > 0 may return no companies because the current distribution has no positive values."
            )


def load_financial_data() -> pd.DataFrame:
    """Load and merge screener financial data using a normalized year key."""

    logger.info("Loading database...")

    with sqlite3.connect(DATABASE_PATH) as conn:
        ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        market_cap = pd.read_sql("SELECT * FROM market_cap", conn)
        profitandloss = pd.read_sql(
            "SELECT company_id, year, sales, net_profit FROM profitandloss",
            conn,
        )
        sectors = pd.read_sql(
            "SELECT company_id, broad_sector FROM sectors",
            conn,
        )

    ratios = _prepare_year_key(ratios)
    market_cap = _prepare_year_key(market_cap)
    profitandloss = _prepare_year_key(profitandloss)

    logger.info("Rows loaded from financial_ratios: %s", len(ratios))
    logger.info("Rows loaded from market_cap: %s", len(market_cap))
    logger.info("Rows loaded from profitandloss: %s", len(profitandloss))

    market_cap_for_merge = market_cap.rename(columns={"year": "market_cap_year"})
    profitandloss_for_merge = profitandloss.rename(columns={"year": "profitandloss_year"})

    logger.info("Merging ratios, profitandloss, and market cap on company_id and financial_year")
    df = ratios.merge(
        profitandloss_for_merge,
        on=["company_id", "financial_year"],
        how="left",
    )
    df = df.merge(
        market_cap_for_merge,
        on=["company_id", "financial_year"],
        how="left",
    )
    df = df.merge(sectors, on="company_id", how="left")

    _log_dividend_filter_summary(df)

    if "market_cap_crore" in df.columns:
        missing_market_cap_rows = int(df["market_cap_crore"].isna().sum())
    else:
        missing_market_cap_rows = 0

    if "broad_sector" in df.columns:
        missing_sector_rows = int(df["broad_sector"].isna().sum())
    else:
        missing_sector_rows = 0

    if "sales" in df.columns:
        missing_sales_rows = int(df["sales"].isna().sum())
    else:
        missing_sales_rows = 0

    print("\nScreener Merge Validation")
    print("-" * 40)
    print("Rows Loaded:", len(ratios))
    print("Rows After Merge:", len(df))
    print("Unique Companies:", df["company_id"].nunique())
    print("Duplicate Company-Year Count:", int(df.duplicated(subset=["company_id", "financial_year"], keep=False).sum()))
    print("Missing Market Cap Rows:", missing_market_cap_rows)
    print("Missing Sector Rows:", missing_sector_rows)
    print("Missing Sales Rows:", missing_sales_rows)

    if missing_market_cap_rows:
        logger.warning(
            "Many market cap rows are unmatched because market_cap is only available for a narrower year window than financial_ratios."
        )

    duplicate_keys = df.duplicated(subset=["company_id", "financial_year"], keep=False)
    if duplicate_keys.any():
        logger.warning(
            "Duplicate company-year combinations detected: %s",
            int(duplicate_keys.sum()),
        )
    else:
        logger.info("No duplicate company-year combinations detected")

    return df


def write_top_companies(df: pd.DataFrame, preset_name: str) -> None:
    """Export the top 20 ranked companies for the active preset."""

    output_path = REPORTS_PATH / "top20_quality_companies.csv"
    if df.empty:
        pd.DataFrame(columns=["Company", "Composite Score", "ROE", "ROCE", "FCF", "Revenue CAGR", "PAT CAGR", "Debt To Equity"]).to_csv(output_path, index=False)
        return

    columns_to_keep = [
        ("company_id", "Company"),
        ("composite_score", "Composite Score"),
        ("return_on_equity_pct", "ROE"),
        ("return_on_capital_employed_pct", "ROCE"),
        ("free_cash_flow", "FCF"),
        ("revenue_cagr_5yr", "Revenue CAGR"),
        ("pat_cagr_5yr", "PAT CAGR"),
        ("debt_to_equity", "Debt To Equity"),
    ]

    available = [source for source, _ in columns_to_keep if source in df.columns]
    rename_map = {source: target for source, target in columns_to_keep if source in df.columns}
    export_df = df.loc[:, available].copy()
    export_df = export_df.rename(columns=rename_map)
    export_df = export_df.rename(columns={"Company": "Company"})
    export_df = export_df.head(20)
    export_df.to_csv(output_path, index=False)
    logger.info("Exported top 20 ranked companies to %s", output_path)


def load_config() -> dict[str, Any]:
    """
    Load screener configuration.
    """

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_PATH}"
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def show_database_summary(df: pd.DataFrame) -> None:
    """
    Display dataset summary.
    """

    logger.info("Rows       : %s", len(df))
    logger.info("Columns    : %s", len(df.columns))
    logger.info("Companies  : %s", df["company_id"].nunique())


def run_screener(preset_name: str) -> pd.DataFrame:
    """Run a named preset screener over the loaded financial dataset."""

    logger.info("Running preset: %s", preset_name)

    df = load_financial_data()
    config = load_config()

    if not isinstance(config, dict):
        raise TypeError("Screener config must be a dictionary")

    if preset_name not in config:
        raise ValueError(f"Unknown preset: {preset_name}")

    latest_df = _select_latest_snapshot(df)
    scored_df = compute_composite_score(latest_df)
    scored_df = scored_df.sort_values(by="composite_score", ascending=False).reset_index(drop=True)
    write_top_companies(scored_df, preset_name)
    result = run_preset(scored_df, preset_name)

    show_database_summary(result)

    print(f"\nPreset Name: {preset_name}")
    print(f"Rows Returned: {len(result)}")
    print(f"Unique Companies: {result['company_id'].nunique()}")
    print("Execution Time: completed")

    return result


def main() -> None:

    df = load_financial_data()

    config = load_config()

    show_database_summary(df)

    print("\nAvailable Screeners\n")

    for screener in config:
        print("-", screener)


if __name__ == "__main__":
    main()