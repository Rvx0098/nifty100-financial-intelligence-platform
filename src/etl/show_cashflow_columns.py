import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

query = """
SELECT *
FROM cashflow
LIMIT 5
"""

df = pd.read_sql(query, conn)

print("\nCOLUMNS:\n")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:\n")
print(df.head())

conn.close()