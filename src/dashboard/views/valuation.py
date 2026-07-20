import streamlit as st

from src.dashboard.services.valuation_service import (
    get_company_list,
    get_valuation
)


def valuation_label(pe):

    if pe == 0:
        return "Unknown"

    if pe < 15:
        return "🟢 Undervalued"

    if pe < 30:
        return "🟡 Fairly Valued"

    return "🔴 Expensive"


def render():

    st.title("💰 Valuation Engine")

    companies = get_company_list()

    company = st.selectbox(
        "Select Company",
        companies["id"]
    )

    df = get_valuation(company)

    if df.empty:
        st.warning("No valuation data.")
        return

    row = df.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Market Cap",
        f"₹ {row['market_cap_crore']:,.0f} Cr"
    )

    c2.metric(
        "P/E",
        f"{row['pe_ratio']:.2f}"
    )

    c3.metric(
        "P/B",
        f"{row['pb_ratio']:.2f}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "EV/EBITDA",
        f"{row['ev_ebitda']:.2f}"
    )

    c5.metric(
        "Dividend Yield",
        f"{row['dividend_yield_pct']:.2f}%"
    )

    c6.metric(
        "Quality Score",
        f"{row['composite_quality_score']:.2f}"
    )

    st.divider()

    st.subheader("Valuation Opinion")

    st.success(
        valuation_label(row["pe_ratio"])
    )

    st.subheader("Raw Financial Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )