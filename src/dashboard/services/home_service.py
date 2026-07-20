"""
Home Dashboard Service

Business logic for the Streamlit Home Dashboard.
"""

from __future__ import annotations

import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
)


def prepare_ratios() -> pd.DataFrame:
    """
    Prepare financial ratios and keep only the
    latest financial record for each company.
    """

    ratios = get_ratios().copy()
    companies = get_companies()

    # Keep only companies present in metadata table
    valid_ids = set(companies["id"])

    ratios = ratios[
        ratios["company_id"].isin(valid_ids)
    ].copy()

    # Extract numeric year
    ratios["financial_year"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    ratios["financial_year"] = pd.to_numeric(
        ratios["financial_year"],
        errors="coerce",
    )

    ratios = ratios.dropna(
        subset=["financial_year"]
    )

    ratios["financial_year"] = (
        ratios["financial_year"]
        .astype(int)
    )

    # Latest record first
    ratios = ratios.sort_values(
        ["company_id", "financial_year"],
        ascending=[True, False],
    )

    # Keep latest year only
    ratios = (
        ratios.drop_duplicates(
            subset="company_id",
            keep="first",
        )
        .reset_index(drop=True)
    )

    return ratios


def trimmed_mean(series: pd.Series) -> float:
    """
    Calculate trimmed mean after removing
    extreme 1% outliers.
    """

    s = series.dropna()

    if s.empty:
        return 0.0

    lower = s.quantile(0.05)
    upper = s.quantile(0.95)
    s = s[
        (s >= lower)
        & (s <= upper)
    ]

    if s.empty:
        return 0.0

    return round(s.median(), 2)


def get_dashboard_kpis() -> dict:
    """
    Calculate dashboard KPIs.
    """

    ratios = prepare_ratios()
    companies = get_companies()

    return {
        "companies": int(companies["id"].nunique()),

        "avg_roe": trimmed_mean(
            ratios["return_on_equity_pct"]
        ),

        "avg_roce": trimmed_mean(
            ratios["return_on_capital_employed_pct"]
        ),

        "avg_revenue_cagr": round(
            ratios["revenue_cagr_5yr"].mean(),
            2,
        ),

        "avg_npm": round(
            ratios["net_profit_margin_pct"].mean(),
            2,
        ),

        "debt_free": int(
            (ratios["debt_to_equity"] == 0).sum()
        ),
    }


def get_sector_distribution() -> pd.DataFrame:
    """
    Return sector distribution.
    """

    sectors = get_sectors()

    return (
        sectors.groupby("broad_sector")
        .size()
        .reset_index(name="companies")
        .sort_values(
            "companies",
            ascending=False,
        )
    )


def get_top_quality_companies() -> pd.DataFrame:
    """
    Return top 10 companies by quality score.
    """

    ratios = prepare_ratios()
    companies = get_companies()

    df = ratios.merge(
        companies[
            [
                "id",
                "company_name",
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    return (
        df.sort_values(
            "composite_quality_score",
            ascending=False,
        )[
            [
                "company_id",
                "company_name",
                "composite_quality_score",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
                "revenue_cagr_5yr",
            ]
        ]
        .head(10)
        .reset_index(drop=True)
    )