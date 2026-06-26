import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

try:
    df = pd.read_sql(
        "SELECT * FROM financial_ratios LIMIT 5",
        conn
    )

    print("\nColumns:\n")
    print(df.columns.tolist())

    print("\nSample Rows:\n")
    print(df)

except Exception as e:
    print(e)

conn.close()