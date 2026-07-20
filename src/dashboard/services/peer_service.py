import sqlite3
import pandas as pd

DB_PATH = "database/n100.db"


def get_peer_groups():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT DISTINCT peer_group_name
    FROM peer_groups
    ORDER BY peer_group_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_peer_comparison(group_name):

    conn = sqlite3.connect(DB_PATH)

    query = """
SELECT

    c.company_name,
    pg.is_benchmark,

    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.operating_margin_pct,
    fr.debt_to_equity,
    fr.interest_coverage,
    fr.revenue_cagr_5yr,
    fr.composite_quality_score,

    mc.pe_ratio,
    mc.pb_ratio

FROM peer_groups pg

INNER JOIN companies c
    ON pg.company_id = c.id

INNER JOIN financial_ratios fr
    ON pg.company_id = fr.company_id

LEFT JOIN market_cap mc
    ON pg.company_id = mc.company_id
    AND mc.year = CAST(SUBSTR(fr.year, -4) AS INTEGER)

WHERE
    pg.peer_group_name = ?
    AND fr.year = 'Mar 2024'

ORDER BY
    pg.is_benchmark DESC,
    c.company_name
"""

    df = pd.read_sql(
        query,
        conn,
        params=(group_name,)
    )

    conn.close()

    return df.fillna(0)