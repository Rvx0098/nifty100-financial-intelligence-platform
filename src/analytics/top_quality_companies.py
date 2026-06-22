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
WHERE roe_percentage > 20
AND roce_percentage > 20
ORDER BY roe_percentage DESC
"""

df = pd.read_sql(
    query,
    conn
)

print("\nTop Quality Companies")
print("=" * 80)
print(df)

conn.close()