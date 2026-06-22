import sqlite3
import pandas as pd

# Connect to REAL database
conn = sqlite3.connect("database/n100.db")

# Load Profit & Loss data
query = """
SELECT *
FROM profitandloss
"""

df = pd.read_sql(query, conn)

print(f"Rows Loaded: {len(df)}")

# Calculate expected operating profit
df["calculated_operating_profit"] = (
    df["sales"]
    - df["expenses"]
)

# Difference
df["profit_difference"] = (
    df["calculated_operating_profit"]
    - df["operating_profit"]
)

# Find suspicious rows
invalid_rows = df[
    abs(df["profit_difference"]) > 1
]

# Save report
invalid_rows.to_csv(
    "reports/income_statement_validation.csv",
    index=False
)

print(f"Invalid Rows Found: {len(invalid_rows)}")
print("Report Saved -> reports/income_statement_validation.csv")

conn.close()