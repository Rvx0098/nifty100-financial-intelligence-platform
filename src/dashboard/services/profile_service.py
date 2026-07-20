import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT.parent / "database" / "n100.db"


def get_connection():
    """Create a database connection."""
    return sqlite3.connect(DB_PATH)


def get_company_list():
    """
    Returns all companies sorted alphabetically.
    """

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    companies = pd.read_sql(query, conn)

    conn.close()

    return companies

def get_company_info(company_id):
    """
    Returns basic information for one company.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM companies
    WHERE id = ?
    """

    company = pd.read_sql(
        query,
        conn,
        params=[company_id]
    )

    conn.close()

    return company

def get_latest_ratios(company_id):
    """
    Returns the latest financial ratios of a company.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    AND return_on_equity_pct IS NOT NULL
    ORDER BY year DESC
    LIMIT 1
    """

    ratios = pd.read_sql(
        query,
        conn,
        params=[company_id]
    )

    conn.close()

    return ratios

def get_market_data(company_id):
    """
    Returns the latest market information for a company.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM market_cap
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    market = pd.read_sql(
        query,
        conn,
        params=[company_id]
    )

    conn.close()

    return market

def get_pros_cons(company_id):
    """
    Returns the strengths and weaknesses of a company.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM prosandcons
    WHERE company_id = ?
    """

    pros_cons = pd.read_sql(
        query,
        conn,
        params=[company_id]
    )

    conn.close()

    return pros_cons

def get_documents(company_id):
    """
    Returns all available company documents.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM documents
    WHERE company_id = ?
    ORDER BY year DESC
    """

    documents = pd.read_sql(
        query,
        conn,
        params=[company_id]
    )

    conn.close()

    return documents