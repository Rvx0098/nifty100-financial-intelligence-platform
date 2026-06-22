import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

query = """
SELECT *
FROM profitandloss
"""

df = pd.read_sql(query, conn)

df["calculated_operating_profit"] = (
    df["sales"]
    - df["expenses"]
)

df["difference"] = (
    df["calculated_operating_profit"]
    - df["operating_profit"]
)

invalid_rows = df[
    abs(df["difference"]) > 1
]

print("\nFIRST 20 INVALID ROWS\n")

print(
    invalid_rows[
        [
            "company_id",
            "year",
            "sales",
            "expenses",
            "operating_profit",
            "difference"
        ]
    ].head(20)
)

conn.close()