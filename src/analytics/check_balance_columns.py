import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

df = pd.read_sql("""
SELECT *
FROM balancesheet
LIMIT 5
""", conn)

print("\nColumns:\n")
print(df.columns.tolist())

print("\nFirst 5 Rows:\n")
print(df)

conn.close()