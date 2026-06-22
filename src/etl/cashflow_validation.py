import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("database/n100.db")

# Load cashflow table
query = """
SELECT *
FROM cashflow
"""

df = pd.read_sql(query, conn)

print(f"Rows Loaded: {len(df)}")

# Calculate expected cash flow
df["calculated_net_cash_flow"] = (
    df["operating_activity"]
    +
    df["investing_activity"]
    +
    df["financing_activity"]
)

# Difference
df["cashflow_difference"] = (
    df["calculated_net_cash_flow"]
    -
    df["net_cash_flow"]
)

# Invalid rows
invalid_rows = df[
    abs(df["cashflow_difference"]) > 1
]

# Save report
invalid_rows.to_csv(
    "reports/cashflow_validation.csv",
    index=False
)

print(f"Invalid Rows Found: {len(invalid_rows)}")
print("Report Saved -> reports/cashflow_validation.csv")

conn.close()