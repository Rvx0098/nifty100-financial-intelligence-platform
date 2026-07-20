"""
N100 Financial Intelligence Platform
Dashboard Entry Point
"""

import streamlit as st

from src.dashboard.utils.db import get_companies
from src.dashboard.views import screener
from src.dashboard.views import valuation
from src.dashboard.views import peers
from src.dashboard.views import trends
from src.dashboard.views import sectors
from src.dashboard.views import capital
from src.dashboard.views import reports

# Home
from src.dashboard.services.home_service import (
    get_dashboard_kpis,
    get_sector_distribution,
    get_top_quality_companies,
)

import plotly.express as px

# Pages
from src.dashboard.views.profile import render as render_profile

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("N100 Financial Intelligence")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
    "🏠 Home",
    "🏢 Company Profile",
    "🔍 Screener",
    "👥 Peer Comparison",
    "📈 Trend Analysis",
    "🏭 Sector Analysis",
    "💰 Capital Allocation",
    "📄 Reports",
    "💰 Valuation Engine",
]
)

st.sidebar.markdown("---")

companies = get_companies()

st.sidebar.success("Database Connected")

st.sidebar.metric(
    "Companies",
    len(companies),
)

st.sidebar.metric(
    "Version",
    "Sprint 4",
)

# ---------------------------------------------------
# Router
# ---------------------------------------------------

if page == "🏠 Home":

    st.title("N100 Financial Intelligence Platform")

    kpis = get_dashboard_kpis()

    c1, c2, c3 = st.columns(3)

    c1.metric("Companies", kpis["companies"])
    c2.metric("Average ROE", f'{kpis["avg_roe"]}%')
    c3.metric("Average ROCE", f'{kpis["avg_roce"]}%')

    c4, c5, c6 = st.columns(3)

    c4.metric("Revenue CAGR", f'{kpis["avg_revenue_cagr"]}%')
    c5.metric("Debt Free", kpis["debt_free"])
    c6.metric("Average NPM", f'{kpis["avg_npm"]}%')

    left, right = st.columns([1.2, 1])

    sector = get_sector_distribution()

    fig = px.pie(
        sector,
        names="broad_sector",
        values="companies",
        hole=0.55,
    )

    left.plotly_chart(
        fig,
        use_container_width=True,
    )

    right.subheader("Top Quality Companies")

    right.dataframe(
        get_top_quality_companies(),
        use_container_width=True,
    )

elif page == "🏢 Company Profile":

    render_profile()

elif page == "🔍 Screener":
    screener.render()

elif page == "👥 Peer Comparison":
    peers.render()

elif page == "📈 Trend Analysis":
    trends.render()

elif page == "🏭 Sector Analysis":
    sectors.render()

elif page == "💰 Capital Allocation":
    capital.render()

elif page == "📄 Reports":
    reports.render()

elif page == "💰 Valuation Engine":
    valuation.render()