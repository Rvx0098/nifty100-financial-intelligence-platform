import streamlit as st
import plotly.express as px

from src.dashboard.services.trend_service import (
    get_company_list,
    get_company_trends,
)


def render():

    st.title("📈 Trend Analysis")

    companies = get_company_list()

    company = st.selectbox(
        "Select Company",
        companies["id"]
    )

    df = get_company_trends(company)

    if df.empty:

        st.warning("No data available.")

        return

    metric = st.selectbox(
        "Metric",
        [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "earnings_per_share",
        ]
    )

    fig = px.line(
        df,
        x="year",
        y=metric,
        markers=True,
        title=metric.replace("_", " ").title()
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )