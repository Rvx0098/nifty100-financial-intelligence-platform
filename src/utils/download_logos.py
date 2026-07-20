import os
import sqlite3
import pandas as pd
import requests

# -----------------------------
# Find database automatically
# -----------------------------
possible_dbs = [
    "database/n100.db",
    "database/nifty100.db",
    "data/database/n100.db",
    "data/database/nifty100.db",
]

DB_PATH = None

for db in possible_dbs:
    if os.path.exists(db):
        DB_PATH = db
        break

if DB_PATH is None:
    raise FileNotFoundError(
        "Couldn't find the SQLite database. Check the database folder."
    )

print(f"Using database: {DB_PATH}")

# -----------------------------
# Logo folder
# -----------------------------
LOGO_FOLDER = "assets/logos"
os.makedirs(LOGO_FOLDER, exist_ok=True)

# -----------------------------
# Read companies
# -----------------------------
conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT id, website FROM companies",
    conn
)

conn.close()

print(f"Found {len(companies)} companies")

# -----------------------------
# Download logos
# -----------------------------
for _, row in companies.iterrows():

    company = row["id"]
    website = str(row["website"])

    if not website.startswith("http"):
        continue

    domain = (
        website.replace("https://", "")
        .replace("http://", "")
        .split("/")[0]
    )

    url = f"https://www.google.com/s2/favicons?sz=256&domain={domain}"

    try:

        r = requests.get(url, timeout=10)

        if r.status_code == 200:

            with open(
                f"{LOGO_FOLDER}/{company}.png",
                "wb"
            ) as f:
                f.write(r.content)

            print(f"✓ {company}")

    except Exception as e:
        print(company, e)

print("\nDone!")