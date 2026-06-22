import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

query = """
SELECT *
FROM cashflow
"""

df = pd.read_sql(query, conn)

df["calculated_net_cash_flow"] = (
    df["operating_activity"]
    + df["investing_activity"]
    + df["financing_activity"]
)

df["cashflow_difference"] = (
    df["calculated_net_cash_flow"]
    - df["net_cash_flow"]
)

invalid_rows = df[
    abs(df["cashflow_difference"]) > 1
]

print("\nFAILED ROWS:\n")
print(invalid_rows)

conn.close()