import sqlite3
import pandas as pd

DB_PATH = "database/n100.db"


def get_company_list():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT id, company_name
        FROM companies
        ORDER BY company_name
    """, conn)

    conn.close()

    return df


def get_report(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.company_name,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.operating_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.composite_quality_score,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,
        mc.dividend_yield_pct

    FROM companies c

    INNER JOIN financial_ratios fr
        ON c.id = fr.company_id

    LEFT JOIN market_cap mc
        ON c.id = mc.company_id
        AND mc.year = CAST(SUBSTR(fr.year, -4) AS INTEGER)

    WHERE
        c.id = ?
        AND fr.year = 'Mar 2024'
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna(0)