import sqlite3
import pandas as pd

DB_PATH = "database/n100.db"


def get_sectors():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT DISTINCT broad_sector
    FROM sectors
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_sector_data(sector):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.company_name,

        s.sub_sector,

        mc.market_cap_crore,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.revenue_cagr_5yr,
        fr.composite_quality_score

    FROM sectors s

    INNER JOIN companies c
        ON s.company_id = c.id

    INNER JOIN financial_ratios fr
        ON s.company_id = fr.company_id

    LEFT JOIN market_cap mc
        ON s.company_id = mc.company_id
        AND mc.year = CAST(SUBSTR(fr.year,-4) AS INTEGER)

    WHERE
        s.broad_sector=?
        AND fr.year='Mar 2024'
    """

    df = pd.read_sql(
        query,
        conn,
        params=(sector,)
    )

    conn.close()

    return df.fillna(0)