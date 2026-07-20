import streamlit as st

from src.dashboard.services.screener_service import (
    get_screener_data,
    filter_companies,
)


def render():

    st.title("🔍 Stock Screener")

    df = get_screener_data()
    st.write("Rows Loaded:", len(df))

    st.sidebar.header("Filters")

    roe = st.sidebar.slider(
        "Minimum ROE (%)",
        0.0,
        50.0,
        15.0,
    )

    debt = st.sidebar.slider(
        "Maximum Debt / Equity",
        0.0,
        5.0,
        1.0,
    )

    fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    float(df["free_cash_flow"].min()),
    float(df["free_cash_flow"].max()),
    float(df["free_cash_flow"].min()),
)

    revenue = st.sidebar.slider(
        "Minimum Revenue CAGR %",
        -20.0,
        50.0,
        5.0,
    )

    pat = st.sidebar.slider(
        "Minimum PAT CAGR %",
        -20.0,
        50.0,
        5.0,
    )

    opm = st.sidebar.slider(
        "Minimum Operating Margin %",
        0.0,
        80.0,
        15.0,
    )

    pe = st.sidebar.slider(
        "Maximum PE",
        0.0,
        150.0,
        40.0,
    )

    pb = st.sidebar.slider(
        "Maximum PB",
        0.0,
        30.0,
        8.0,
    )

    dividend = st.sidebar.slider(
        "Minimum Dividend Yield %",
        0.0,
        10.0,
        0.0,
    )

    icr = st.sidebar.slider(
        "Minimum Interest Coverage",
        0.0,
        100.0,
        2.0,
    )

    filtered = filter_companies(
        df,
        roe,
        debt,
        fcf,
        revenue,
        pat,
        opm,
        pe,
        pb,
        dividend,
        icr,
    )

    st.subheader(f"Matching Companies : {len(filtered)}")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "screener_output.csv",
        "text/csv",
    )