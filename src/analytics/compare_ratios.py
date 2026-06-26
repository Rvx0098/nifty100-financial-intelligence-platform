import sqlite3
import pandas as pd

print("Starting comparison...")

conn = sqlite3.connect("database/n100.db")

try:
    db_ratios = pd.read_sql("""
    SELECT
        company_id,
        year,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct
    FROM financial_ratios
    LIMIT 10
    """, conn)

    computed = pd.read_csv("reports/profitability_ratios.csv")

    computed = computed[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct"
        ]
    ].head(10)

    print("\n========== DATABASE ==========")
    print(db_ratios)

    print("\n========== COMPUTED ==========")
    print(computed)

except Exception as e:
    print("\nERROR:")
    print(e)

finally:
    conn.close()