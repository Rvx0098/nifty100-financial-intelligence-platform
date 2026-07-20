import streamlit as st
import plotly.express as px

from src.dashboard.services.peer_service import (
    get_peer_groups,
    get_peer_comparison
)


def render():

    st.title("👥 Peer Comparison")

    groups = get_peer_groups()

    group = st.selectbox(
        "Peer Group",
        groups["peer_group_name"]
    )

    df = get_peer_comparison(group)

    st.subheader(f"{group} ({len(df)} Companies)")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    fig = px.bar(
        df.sort_values(
            "composite_quality_score",
            ascending=False
        ),
        x="company_name",
        y="composite_quality_score",
        color="is_benchmark",
        title="Composite Quality Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )