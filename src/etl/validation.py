import sqlite3
import pandas as pd

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    "database/n100.db"
)

print("=" * 70)
print("N100 FINANCIAL INTELLIGENCE PLATFORM")
print("DATA QUALITY VALIDATION REPORT")
print("=" * 70)

# ==========================================
# RULE 1
# MISSING COMPANY IDS
# ==========================================

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "sectors"
]

print("\nRULE 1: Missing Company IDs")
print("-" * 70)

for table in tables:

    query = f"""
    SELECT COUNT(*) AS missing_count
    FROM {table}
    WHERE company_id IS NULL
    """

    result = pd.read_sql(
        query,
        conn
    )

    count = result.iloc[0, 0]

    print(
        f"{table:<20} Missing Company IDs: {count}"
    )

# ==========================================
# RULE 2
# MISSING YEARS
# ==========================================

year_tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap"
]

print("\nRULE 2: Missing Years")
print("-" * 70)

for table in year_tables:

    query = f"""
    SELECT COUNT(*) AS missing_years
    FROM {table}
    WHERE year IS NULL
    """

    result = pd.read_sql(
        query,
        conn
    )

    count = result.iloc[0, 0]

    print(
        f"{table:<20} Missing Years: {count}"
    )

# ==========================================
# RULE 3
# DUPLICATE COMPANY-YEAR RECORDS
# ==========================================

print("\nRULE 3: Duplicate Company-Year Records")
print("-" * 70)

duplicate_tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap"
]

for table in duplicate_tables:

    query = f"""
    SELECT
        company_id,
        year,
        COUNT(*) AS record_count
    FROM {table}
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
    """

    result = pd.read_sql(
        query,
        conn
    )

    duplicate_count = len(result)

    print(
        f"{table:<20} Duplicate Groups: {duplicate_count}"
    )

# ==========================================
# RULE 4
# BALANCE SHEET VALIDATION
# ==========================================

print("\nRULE 4: Balance Sheet Validation")
print("-" * 70)

query = """
SELECT
    company_id,
    year,
    total_assets,
    total_liabilities
FROM balancesheet
"""

balance_df = pd.read_sql(
    query,
    conn
)

balance_df["difference"] = (
    balance_df["total_assets"]
    - balance_df["total_liabilities"]
)

print("\nBalance Sheet Difference Statistics")

print(
    balance_df["difference"].describe()
)

# ==========================================
# RULE 5
# COMPANY COVERAGE CHECK
# ==========================================

print("\nRULE 5: Company Coverage")
print("-" * 70)

query = """
SELECT COUNT(DISTINCT company_id)
FROM profitandloss
"""

coverage = pd.read_sql(
    query,
    conn
)

company_count = coverage.iloc[0, 0]

print(
    f"Unique Companies in P&L Dataset: {company_count}"
)

# ==========================================
# SUMMARY
# ==========================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

conn.close()

