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


def get_capital_allocation(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        year,

        fixed_assets,
        investments,
        cwip,
        other_asset,

        equity_capital,
        reserves,
        borrowings,
        other_liabilities

    FROM balancesheet

    WHERE company_id=?
    AND year='Mar 2024'
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna(0)