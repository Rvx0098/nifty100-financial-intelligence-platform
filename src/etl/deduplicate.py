import pandas as pd

from src.etl.extract import load_all_datasets

datasets = load_all_datasets()

for name, df in datasets.items():

    before = len(df)

    df_clean = df.drop_duplicates()

    after = len(df_clean)

    removed = before - after

    print(
        f"{name:<25}"
        f" Before: {before:<5}"
        f" After: {after:<5}"
        f" Removed: {removed}"
    )