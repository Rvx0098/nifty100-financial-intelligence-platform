"""
Database utility functions for the Streamlit dashboard.
"""

from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = ROOT / "database" / "n100.db"


@st.cache_data(ttl=600)
def get_connection():
    return sqlite3.connect(DATABASE_PATH)


@st.cache_data(ttl=600)
def get_companies():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            """
            SELECT *
            FROM companies
            ORDER BY company_name
            """,
            conn,
        )


@st.cache_data(ttl=600)
def get_ratios():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM financial_ratios",
            conn,
        )


@st.cache_data(ttl=600)
def get_profit_loss():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM profitandloss",
            conn,
        )


@st.cache_data(ttl=600)
def get_balance_sheet():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM balancesheet",
            conn,
        )


@st.cache_data(ttl=600)
def get_cashflow():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM cashflow",
            conn,
        )


@st.cache_data(ttl=600)
def get_market_cap():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM market_cap",
            conn,
        )


@st.cache_data(ttl=600)
def get_sectors():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM sectors",
            conn,
        )


@st.cache_data(ttl=600)
def get_peer_groups():
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM peer_groups",
            conn,
        )