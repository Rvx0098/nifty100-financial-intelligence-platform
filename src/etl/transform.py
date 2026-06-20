import pandas as pd


def extract_year(df):

    if "year" not in df.columns:
        return df

    df["financial_year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    return df