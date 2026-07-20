import streamlit as st
import plotly.express as px

from src.dashboard.services.sector_service import (
    get_sectors,
    get_sector_data
)


def render():

    st.title("🏭 Sector Analysis")

    sectors = get_sectors()

    sector = st.selectbox(
        "Select Sector",
        sectors["broad_sector"]
    )

    df = get_sector_data(sector)

    if df.empty:
        st.warning("No data found.")
        return

    fig = px.scatter(
        df,
        x="market_cap_crore",
        y="return_on_equity_pct",
        size="composite_quality_score",
        color="sub_sector",
        hover_name="company_name",
        title=f"{sector} Sector"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Sector Companies")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Average ROE",
        f"{df['return_on_equity_pct'].mean():.2f}%"
    )