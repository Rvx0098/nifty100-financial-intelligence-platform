import sqlite3
import os

db_path = "n100.db"

print("Current Folder:")
print(os.getcwd())

print("\nDatabase Exists?")
print(os.path.exists(db_path))

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

tables = cursor.fetchall()

print("\nTables Found:")

for table in tables:
    print(table[0])

conn.close()