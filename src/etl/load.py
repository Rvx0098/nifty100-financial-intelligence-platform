import sqlite3

from src.etl.extract import load_all_datasets

DATABASE_PATH = "database/n100.db"


def create_database():

    print("=" * 60)
    print("N100 Financial Intelligence Platform")
    print("Database Loading Started")
    print("=" * 60)

    conn = sqlite3.connect(DATABASE_PATH)

    datasets = load_all_datasets()

    total_rows = 0

    for name, df in datasets.items():

        table_name = (
            name.replace(".xlsx", "")
            .lower()
        )

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        rows = len(df)
        total_rows += rows

        print(
            f"✓ Loaded {table_name:<20} | {rows:>5} rows"
        )

    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"Total Tables Loaded : {len(datasets)}")
    print(f"Total Rows Loaded   : {total_rows}")
    print("Database Created Successfully")
    print("=" * 60)


if __name__ == "__main__":
    create_database()