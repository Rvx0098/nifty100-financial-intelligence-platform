import pandas as pd


def normalize_company_id(df):

    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

    return df


def extract_financial_year(df):

    if "year" not in df.columns:
        return df

    df["financial_year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    return df