import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/n100.db"
)

query = """
SELECT
    company_name,
    roe_percentage,
    roce_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10
"""

df = pd.read_sql(
    query,
    conn
)

print(df)

conn.close()