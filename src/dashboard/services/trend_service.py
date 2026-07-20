import sqlite3
import pandas as pd

DB_PATH = "database/n100.db"


def get_company_list():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
    """, conn)

    conn.close()

    return df


def get_company_trends(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        year,
        return_on_equity_pct,
        return_on_capital_employed_pct,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        earnings_per_share

    FROM financial_ratios

    WHERE company_id=?

    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna(0)