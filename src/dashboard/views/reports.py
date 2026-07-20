import streamlit as st

from src.dashboard.services.report_service import (
    get_company_list,
    get_report
)


def render():

    st.title("📄 Company Report")

    companies = get_company_list()

    company = st.selectbox(
        "Select Company",
        companies["id"]
    )

    df = get_report(company)

    if df.empty:
        st.warning("No report available.")
        return

    row = df.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "ROE",
        f"{row['return_on_equity_pct']:.2f}%"
    )

    col2.metric(
        "ROCE",
        f"{row['return_on_capital_employed_pct']:.2f}%"
    )

    col3.metric(
        "Quality Score",
        f"{row['composite_quality_score']:.2f}"
    )

    st.divider()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        "company_report.csv",
        "text/csv"
    )