import sqlite3
import pandas as pd

DB_PATH = "database/n100.db"


def get_screener_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.id,
        c.company_name,

        s.broad_sector,

        fr.year,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.operating_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.free_cash_flow,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.composite_quality_score,

        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct,
        mc.market_cap_crore

    FROM financial_ratios fr

    INNER JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id

    LEFT JOIN market_cap mc
        ON fr.company_id = mc.company_id
        AND fr.year = mc.year

    WHERE fr.year = 'Mar 2024'
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def filter_companies(
    df,
    roe,
    debt,
    fcf,
    revenue,
    pat,
    opm,
    pe,
    pb,
    dividend,
    icr,
):

    data = df.copy()

    data = data.fillna(0)

    data = data[
        (data["return_on_equity_pct"] >= roe)
        &
        (data["debt_to_equity"] <= debt)
        &
        (data["free_cash_flow"] >= fcf)
        &
        (data["revenue_cagr_5yr"] >= revenue)
        &
        (data["pat_cagr_5yr"] >= pat)
        &
        (data["operating_margin_pct"] >= opm)
        &
        (data["pe_ratio"] <= pe)
        &
        (data["pb_ratio"] <= pb)
        &
        (data["dividend_yield_pct"] >= dividend)
        &
        (data["interest_coverage"] >= icr)
    ]

    return data.sort_values(
        "composite_quality_score",
        ascending=False
    )