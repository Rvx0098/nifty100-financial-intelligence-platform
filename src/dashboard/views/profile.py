import os
import streamlit as st

from src.dashboard.services.profile_service import (
    get_company_list,
    get_company_info,
    get_latest_ratios,
    get_market_data,
    get_pros_cons,
    get_documents,
)


def render():

    st.title("🏢 Company Profile")

    companies = get_company_list()

    if companies.empty:
        st.warning("No companies found.")
        return

    company = st.selectbox(
        "Select Company",
        companies["id"].tolist()
    )

    info = get_company_info(company)
    ratios = get_latest_ratios(company)
    market = get_market_data(company)
    pros_cons = get_pros_cons(company)
    documents = get_documents(company)

    # ------------------------------------
    # Tabs
    # ------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🏠 Overview",
            "📊 Financials",
            "📄 Reports",
            "👥 Peers"
        ]
    )

    # =====================================================
    # OVERVIEW
    # =====================================================
    with tab1:

        if info.empty:
            st.error("Company information not available.")
        else:

            company_info = info.iloc[0]

            col1, col2 = st.columns([1, 4])

            with col1:

                logo_path = os.path.join(
                    "assets",
                    "logos",
                    f"{company}.png"
                )

                if os.path.exists(logo_path):
                    st.image(logo_path, width=130)
                else:
                    st.write("🏢")

            with col2:

                st.subheader(company_info["company_name"])

                if (
                    "sector" in company_info
                    and str(company_info["sector"]) != "nan"
                ):
                    st.caption(f"Sector : {company_info['sector']}")

                if (
                    "industry" in company_info
                    and str(company_info["industry"]) != "nan"
                ):
                    st.caption(f"Industry : {company_info['industry']}")

                if (
                    "website" in company_info
                    and str(company_info["website"]).startswith("http")
                ):
                    st.link_button(
                        "🌐 Visit Website",
                        company_info["website"]
                    )

            st.divider()

            st.subheader("About Company")

            about = company_info.get(
                "about_company",
                "No description available."
            )

            st.write(about)

            st.divider()

            st.subheader("📈 Quick Snapshot")

            if not market.empty:

                m = market.iloc[0]

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "Market Cap",
                        f"₹{m['market_cap_crore']:,.0f} Cr"
                    )

                with c2:
                    st.metric(
                        "P/E Ratio",
                        m["pe_ratio"]
                    )

                with c3:
                    st.metric(
                        "P/B Ratio",
                        m["pb_ratio"]
                    )

                with c4:
                    st.metric(
                        "Dividend Yield",
                        f"{m['dividend_yield_pct']}%"
                    )

            st.divider()

            st.subheader("Strengths & Weaknesses")

            left, right = st.columns(2)

            with left:

                st.markdown("### 👍 Pros")

                if not pros_cons.empty:

                    for _, row in pros_cons.iterrows():

                        if str(row["pros"]) != "nan":
                            st.success(row["pros"])

                else:
                    st.info("No data available.")

            with right:

                st.markdown("### 👎 Cons")

                if not pros_cons.empty:

                    for _, row in pros_cons.iterrows():

                        if str(row["cons"]) != "nan":
                            st.error(row["cons"])

                else:
                    st.info("No data available.")

    # =====================================================
    # FINANCIALS
    # =====================================================
    with tab2:

        st.subheader("📊 Financial Ratios")

        if ratios.empty:
            st.warning("Financial ratios not available.")

        else:

            r = ratios.iloc[0]

            row1 = st.columns(5)

            row1[0].metric(
                "📈 ROE",
                f"{float(r['return_on_equity_pct']):.2f}%"
            )

            row1[1].metric(
                "🏆 ROCE",
                f"{float(r['return_on_capital_employed_pct']):.2f}%"
            )

            row1[2].metric(
                "💰 ROA",
                f"{float(r['return_on_assets_pct']):.2f}%"
            )

            row1[3].metric(
                "🏦 Debt / Equity",
                f"{float(r['debt_to_equity']):.2f}"
            )

            row1[4].metric(
                "⭐ Quality Score",
                f"{float(r['composite_quality_score']):.2f}"
            )

            st.divider()

            row2 = st.columns(5)

            if "operating_margin_pct" in r.index:
                row2[0].metric(
                    "Operating Margin",
                    f"{float(r['operating_margin_pct']):.2f}%"
                )

            if "net_profit_margin_pct" in r.index:
                row2[1].metric(
                    "Net Profit Margin",
                    f"{float(r['net_profit_margin_pct']):.2f}%"
                )

            if "current_ratio" in r.index:
                row2[2].metric(
                    "Current Ratio",
                    f"{float(r['current_ratio']):.2f}"
                )

            if "interest_coverage" in r.index:
                row2[3].metric(
                    "Interest Coverage",
                    f"{float(r['interest_coverage']):.2f}"
                )

            if "asset_turnover" in r.index:
                row2[4].metric(
                    "Asset Turnover",
                    f"{float(r['asset_turnover']):.2f}"
                )

        st.divider()

        st.subheader("💹 Market Data")

        if market.empty:

            st.warning("Market data not available.")

        else:

            m = market.iloc[0]

            market_row1 = st.columns(4)

            market_row1[0].metric(
                "Market Cap",
                f"₹{m['market_cap_crore']:,.0f} Cr"
            )

            market_row1[1].metric(
                "P/E Ratio",
                m["pe_ratio"]
            )

            market_row1[2].metric(
                "P/B Ratio",
                m["pb_ratio"]
            )

            market_row1[3].metric(
                "Dividend Yield",
                f"{m['dividend_yield_pct']}%"
            )

            st.divider()

            market_row2 = st.columns(4)

            if "book_value" in m.index:
                market_row2[0].metric(
                    "Book Value",
                    m["book_value"]
                )

            if "face_value" in m.index:
                market_row2[1].metric(
                    "Face Value",
                    m["face_value"]
                )

            if "current_price" in m.index:
                market_row2[2].metric(
                    "Current Price",
                    f"₹{m['current_price']}"
                )

            if "earnings_yield_pct" in m.index:
                market_row2[3].metric(
                    "Earnings Yield",
                    f"{m['earnings_yield_pct']}%"
                )                    
    # =====================================================
    # FINANCIALS
    # =====================================================
    with tab2:

        st.subheader("📊 Financial Ratios")

        if ratios.empty:
            st.warning("Financial ratios not available.")

        else:

            r = ratios.iloc[0]

            row1 = st.columns(5)

            row1[0].metric(
                "📈 ROE",
                f"{float(r['return_on_equity_pct']):.2f}%"
            )

            row1[1].metric(
                "🏆 ROCE",
                f"{float(r['return_on_capital_employed_pct']):.2f}%"
            )

            row1[2].metric(
                "💰 ROA",
                f"{float(r['return_on_assets_pct']):.2f}%"
            )

            row1[3].metric(
                "🏦 Debt / Equity",
                f"{float(r['debt_to_equity']):.2f}"
            )

            row1[4].metric(
                "⭐ Quality Score",
                f"{float(r['composite_quality_score']):.2f}"
            )

            st.divider()

            row2 = st.columns(5)

            if "operating_margin_pct" in r.index:
                row2[0].metric(
                    "Operating Margin",
                    f"{float(r['operating_margin_pct']):.2f}%"
                )

            if "net_profit_margin_pct" in r.index:
                row2[1].metric(
                    "Net Profit Margin",
                    f"{float(r['net_profit_margin_pct']):.2f}%"
                )

            if "current_ratio" in r.index:
                row2[2].metric(
                    "Current Ratio",
                    f"{float(r['current_ratio']):.2f}"
                )

            if "interest_coverage" in r.index:
                row2[3].metric(
                    "Interest Coverage",
                    f"{float(r['interest_coverage']):.2f}"
                )

            if "asset_turnover" in r.index:
                row2[4].metric(
                    "Asset Turnover",
                    f"{float(r['asset_turnover']):.2f}"
                )

        st.divider()

        st.subheader("💹 Market Data")

        if market.empty:

            st.warning("Market data not available.")

        else:

            m = market.iloc[0]

            market_row1 = st.columns(4)

            market_row1[0].metric(
                "Market Cap",
                f"₹{m['market_cap_crore']:,.0f} Cr"
            )

            market_row1[1].metric(
                "P/E Ratio",
                m["pe_ratio"]
            )

            market_row1[2].metric(
                "P/B Ratio",
                m["pb_ratio"]
            )

            market_row1[3].metric(
                "Dividend Yield",
                f"{m['dividend_yield_pct']}%"
            )

            st.divider()

            market_row2 = st.columns(4)

            if "book_value" in m.index:
                market_row2[0].metric(
                    "Book Value",
                    m["book_value"]
                )

            if "face_value" in m.index:
                market_row2[1].metric(
                    "Face Value",
                    m["face_value"]
                )

            if "current_price" in m.index:
                market_row2[2].metric(
                    "Current Price",
                    f"₹{m['current_price']}"
                )

            if "earnings_yield_pct" in m.index:
                market_row2[3].metric(
                    "Earnings Yield",
                    f"{m['earnings_yield_pct']}%"
                )                