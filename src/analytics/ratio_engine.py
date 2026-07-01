import sqlite3
import pandas as pd

# ==========================================
# Import Profitability Functions
# ==========================================

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_assets,
    return_on_capital_employed,
)

# ==========================================
# Import Leverage Functions
# ==========================================

from leverage import (
    debt_to_equity,
    interest_coverage,
    asset_turnover,
    net_debt,
    high_leverage_flag,
    interest_coverage_label,
)

# ==========================================
# Connect SQLite Database
# ==========================================

conn = sqlite3.connect("database/n100.db")

# ==========================================
# Load Profit & Loss
# ==========================================

profit_df = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

# ==========================================
# Load Balance Sheet
# ==========================================

balance_df = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

print(f"Profit & Loss Rows : {len(profit_df)}")
print(f"Balance Sheet Rows : {len(balance_df)}")

# ==========================================
# Merge Tables
# ==========================================

df = pd.merge(
    profit_df,
    balance_df,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

print(f"\nMerged Rows : {len(df)}")

# ==========================================
# PROFITABILITY RATIOS
# ==========================================

df["net_profit_margin_pct"] = df.apply(
    lambda row: net_profit_margin(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)

df["operating_profit_margin_pct"] = df.apply(
    lambda row: operating_profit_margin(
        row["operating_profit"],
        row["sales"]
    ),
    axis=1
)

df["return_on_equity_pct"] = df.apply(
    lambda row: return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

df["return_on_assets_pct"] = df.apply(
    lambda row: return_on_assets(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)

df["return_on_capital_employed_pct"] = df.apply(
    lambda row: return_on_capital_employed(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)

# ==========================================
# LEVERAGE RATIOS
# ==========================================

df["debt_to_equity"] = df.apply(
    lambda row: debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda row: interest_coverage(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda row: asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)

df["net_debt"] = df.apply(
    lambda row: net_debt(
        row["borrowings"],
        row["investments"]
    ),
    axis=1
)

df["high_leverage_flag"] = df["debt_to_equity"].apply(
    high_leverage_flag
)

df["interest_coverage_label"] = df["interest"].apply(
    interest_coverage_label
)

# ==========================================
# Preview
# ==========================================

print("\n========== FIRST 10 KPI ROWS ==========\n")

print(
    df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "return_on_assets_pct",
            "return_on_capital_employed_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "net_debt",
            "high_leverage_flag",
            "interest_coverage_label",
        ]
    ].head(10)
)

# ==========================================
# Save Report
# ==========================================

output_path = "reports/day09_ratio_engine.csv"

df.to_csv(
    output_path,
    index=False
)

print(f"\nReport Saved -> {output_path}")

# ==========================================
# Close Connection
# ==========================================

conn.close()

print("\nDay 09 Ratio Engine Completed Successfully!")