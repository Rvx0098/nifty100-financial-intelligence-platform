import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/n100.db"
)

query = """
SELECT *
FROM profitandloss
WHERE company_id = 'ADANIPORTS'
AND year = 'Mar 2024'
"""

df = pd.read_sql(
    query,
    conn
)

print(df.T)

conn.close()