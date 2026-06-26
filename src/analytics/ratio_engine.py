import sqlite3
import pandas as pd

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_assets,
    return_on_capital_employed,
)

# -------------------------------------------------
# Connect Database
# -------------------------------------------------

conn = sqlite3.connect("database/n100.db")

# -------------------------------------------------
# Load Tables
# -------------------------------------------------

profit_df = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance_df = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

# -------------------------------------------------
# Merge Tables
# -------------------------------------------------

df = pd.merge(
    profit_df,
    balance_df,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

print(f"Merged Rows : {len(df)}")

# -------------------------------------------------
# KPI Calculations
# -------------------------------------------------

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

# -------------------------------------------------
# Preview Results
# -------------------------------------------------

print("\nFirst 10 KPI Rows:\n")

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
        ]
    ].head(10)
)

# -------------------------------------------------
# Save Report
# -------------------------------------------------

df.to_csv(
    "reports/profitability_ratios.csv",
    index=False
)

print("\nReport Saved -> reports/profitability_ratios.csv")

conn.close()