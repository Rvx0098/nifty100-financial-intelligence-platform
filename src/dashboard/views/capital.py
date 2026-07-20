import streamlit as st
import plotly.express as px
import pandas as pd

from src.dashboard.services.capital_service import (
    get_company_list,
    get_capital_allocation
)


def render():

    st.title("🌳 Capital Allocation")

    companies = get_company_list()

    company = st.selectbox(
        "Select Company",
        companies["id"]
    )

    df = get_capital_allocation(company)

    if df.empty:
        st.warning("No data found.")
        return

    row = df.iloc[0]

    assets = pd.DataFrame({
        "Category": [
            "Fixed Assets",
            "Investments",
            "CWIP",
            "Other Assets"
        ],
        "Value": [
            row["fixed_assets"],
            row["investments"],
            row["cwip"],
            row["other_asset"]
        ]
    })

    liabilities = pd.DataFrame({
        "Category": [
            "Equity",
            "Reserves",
            "Borrowings",
            "Other Liabilities"
        ],
        "Value": [
            row["equity_capital"],
            row["reserves"],
            row["borrowings"],
            row["other_liabilities"]
        ]
    })

    st.subheader("Assets")

    fig1 = px.treemap(
        assets,
        path=["Category"],
        values="Value"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader("Funding")

    fig2 = px.treemap(
        liabilities,
        path=["Category"],
        values="Value"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader("Balance Sheet Snapshot")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )