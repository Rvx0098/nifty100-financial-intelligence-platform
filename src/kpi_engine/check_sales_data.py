import sqlite3
import pandas as pd

conn = sqlite3.connect("database/n100.db")

df = pd.read_sql("""
SELECT company_id, year, sales
FROM profitandloss
LIMIT 20
""", conn)

print(df)

conn.close()