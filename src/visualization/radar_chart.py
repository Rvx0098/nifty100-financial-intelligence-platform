"""Generate radar charts for company peer comparison."""

from __future__ import annotations

import logging
import re
import sqlite3
import time
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

AXIS_DEFINITIONS: tuple[tuple[str, str], ...] = (
    ("return_on_equity_pct", "ROE"),
    ("return_on_capital_employed_pct", "ROCE"),
    ("net_profit_margin_pct", "Net Profit Margin"),
    ("debt_to_equity", "Debt To Equity"),
    ("interest_coverage", "Interest Coverage"),
    ("revenue_cagr_5yr", "Revenue CAGR 5Y"),
    ("pat_cagr_5yr", "PAT CAGR 5Y"),
    ("composite_quality_score", "Composite Score"),
)

DEFAULT_PEER_GROUP = "Nifty100 average"


def load_radar_inputs(db_path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the peer percentile, ratio, and company tables from SQLite."""

    db_path = Path(db_path)
    logger.info("Loading radar chart inputs from %s", db_path)
    with sqlite3.connect(db_path) as conn:
        peer_percentiles = pd.read_sql_query("SELECT * FROM peer_percentiles", conn)
        financial_ratios = pd.read_sql_query("SELECT * FROM financial_ratios", conn)
        companies = pd.read_sql_query("SELECT * FROM companies", conn)

    return peer_percentiles, financial_ratios, companies


def _normalize_financial_year(value: Any) -> int | None:
    """Convert mixed year values to a comparable integer year."""

    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)

    text = str(value).strip()
    if not text:
        return None

    if text.isdigit():
        return int(text)

    for token in ("Dec", "Mar", "Jun", "Sep"):
        if token in text:
            digits = [part for part in text.split() if part.isdigit()]
            if digits:
                return int(digits[-1])

    try:
        return int(text)
    except ValueError:
        return None


def get_latest_company_metrics(financial_ratios: pd.DataFrame) -> pd.DataFrame:
    """Return the most recent financial ratio snapshot per company."""

    if financial_ratios.empty:
        return pd.DataFrame(columns=["company_id", "financial_year", *[metric for metric, _ in AXIS_DEFINITIONS]])

    working = financial_ratios.copy()
    company_column = "company_id" if "company_id" in working.columns else "id"
    year_column = "year" if "year" in working.columns else "financial_year"
    working = working[[company_column, year_column, *[metric for metric, _ in AXIS_DEFINITIONS]]].copy()
    working = working.rename(columns={company_column: "company_id", year_column: "year"})
    working["financial_year"] = working["year"].apply(_normalize_financial_year)

    working = working.dropna(subset=["company_id", "financial_year"])
    if working.empty:
        return pd.DataFrame(columns=["company_id", "financial_year", *[metric for metric, _ in AXIS_DEFINITIONS]])

    working = working.sort_values(["company_id", "financial_year"], ascending=[True, True])
    latest_by_company = working.groupby("company_id", as_index=False).tail(1)
    return latest_by_company.reset_index(drop=True)


def build_axis_labels() -> list[str]:
    """Build readable axis labels for the radar chart."""

    return [label for _, label in AXIS_DEFINITIONS]


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _percentile_rank(values: pd.Series) -> pd.Series:
    numeric_values = _safe_numeric(values)
    valid = numeric_values.notna()
    if not valid.any():
        return pd.Series([50.0] * len(values), index=values.index, dtype=float)

    ranked = numeric_values[valid].rank(pct=True, method="average") * 100
    result = pd.Series(50.0, index=values.index, dtype=float)
    result.loc[valid.index[valid]] = ranked.to_numpy()
    return result


def _coerce_axis_value(metric: str, company_id: str, peer_group: str, latest_metrics: pd.DataFrame, peer_percentiles: pd.DataFrame) -> float:
    if metric == "composite_quality_score":
        if not latest_metrics.empty and metric in latest_metrics.columns:
            row = latest_metrics.loc[latest_metrics["company_id"] == company_id]
            if not row.empty:
                value = _safe_numeric(row.iloc[0][metric]).item()
                if pd.notna(value):
                    return float(value)

        return 50.0

    percentiles = peer_percentiles.loc[peer_percentiles["company_id"] == company_id]
    if not percentiles.empty:
        metric_rows = percentiles.loc[percentiles["metric"] == metric]
        if not metric_rows.empty:
            rank_value = _safe_numeric(metric_rows.iloc[0]["percentile_rank"])
            if pd.notna(rank_value):
                return float(rank_value)

    if not latest_metrics.empty and metric in latest_metrics.columns:
        row = latest_metrics.loc[latest_metrics["company_id"] == company_id]
        if not row.empty:
            value = _safe_numeric(row.iloc[0][metric]).item()
            if pd.notna(value):
                return float(value)

    return 50.0


def _peer_average_value(metric: str, peer_group: str, peer_percentiles: pd.DataFrame, latest_metrics: pd.DataFrame) -> float:
    if metric == "composite_quality_score":
        if latest_metrics.empty or "composite_quality_score" not in latest_metrics.columns:
            return 50.0

        group_values = latest_metrics.loc[latest_metrics["company_id"].isin(latest_metrics["company_id"])]
        if group_values.empty:
            return 50.0

        values = _safe_numeric(group_values["composite_quality_score"])
        valid = values.dropna()
        if valid.empty:
            return 50.0
        return float(valid.mean())

    if peer_group == DEFAULT_PEER_GROUP:
        filtered = peer_percentiles.loc[peer_percentiles["metric"] == metric]
    else:
        filtered = peer_percentiles.loc[(peer_percentiles["peer_group"] == peer_group) & (peer_percentiles["metric"] == metric)]

    if filtered.empty:
        return 50.0

    ranks = _safe_numeric(filtered["percentile_rank"])
    valid = ranks.dropna()
    if valid.empty:
        return 50.0
    return float(valid.mean())


def build_radar_series(
    company_id: str,
    financial_ratios: pd.DataFrame,
    peer_percentiles: pd.DataFrame,
    companies: pd.DataFrame,
) -> dict[str, Any]:
    """Build company and peer-average values for a radar chart."""

    latest_metrics = get_latest_company_metrics(financial_ratios)
    company_name = company_id
    if not companies.empty:
        id_column = "id" if "id" in companies.columns else "company_id"
        name_column = "company_name" if "company_name" in companies.columns else "company"
        company_row = companies.loc[companies[id_column].astype(str) == str(company_id)]
        if not company_row.empty and name_column in company_row.columns:
            company_name = str(company_row.iloc[0][name_column])

    peer_group = DEFAULT_PEER_GROUP
    if not peer_percentiles.empty:
        filtered = peer_percentiles.loc[peer_percentiles["company_id"] == company_id]
        if not filtered.empty and "peer_group" in filtered.columns and filtered["peer_group"].notna().any():
            peer_group = str(filtered.iloc[0]["peer_group"])

    if peer_group == "nan":
        peer_group = DEFAULT_PEER_GROUP

    company_values: list[float] = []
    peer_values: list[float] = []
    for metric_name, _ in AXIS_DEFINITIONS:
        company_value = _coerce_axis_value(metric_name, company_id, peer_group, latest_metrics, peer_percentiles)
        peer_value = _peer_average_value(metric_name, peer_group, peer_percentiles, latest_metrics)
        company_values.append(float(company_value))
        peer_values.append(float(peer_value))

    return {
        "company": company_id,
        "peer_average": peer_group,
        "company_name": company_name,
        "peer_group": peer_group,
        "company_values": company_values,
        "peer_values": peer_values,
    }


def create_radar_chart(series: dict[str, Any], output_path: str | Path) -> Path:
    """Create and save a radar chart image for one company."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = build_axis_labels()
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    company_values = series["company_values"] + series["company_values"][:1]
    peer_values = series["peer_values"] + series["peer_values"][:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0", "25", "50", "75", "100"], fontsize=8)
    ax.set_rlabel_position(90)

    ax.plot(angles, company_values, color="#1f77b4", linewidth=1.8, marker="o", label=series["company_name"])
    ax.fill(angles, company_values, color="#1f77b4", alpha=0.15)

    ax.plot(angles, peer_values, color="#ff7f0e", linewidth=1.8, marker="o", label=series["peer_group"])
    ax.fill(angles, peer_values, color="#ff7f0e", alpha=0.10)

    ax.set_title(f"{series['company_name']} vs {series['peer_group']}", pad=25, fontsize=12)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.10))

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output_path


def summarize_radar_generation(
    charts_generated: int,
    peer_groups: list[str],
    companies_without_peer_group: list[str],
    execution_time_seconds: float,
) -> dict[str, Any]:
    """Create a structured summary payload for the radar chart run."""

    return {
        "charts_generated": charts_generated,
        "company_count": charts_generated,
        "peer_groups": peer_groups,
        "companies_without_peer_group": companies_without_peer_group,
        "execution_time_seconds": round(float(execution_time_seconds), 3),
    }


def generate_radar_charts(
    db_path: str | Path = "database/n100.db",
    output_dir: str | Path | None = None,
    reports_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Generate one radar chart per company and write a summary report."""

    start_time = time.perf_counter()
    db_path = Path(db_path)
    output_dir = Path(output_dir or Path("reports/radar_charts"))
    reports_dir = Path(reports_dir or Path("reports"))
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    peer_percentiles, financial_ratios, companies = load_radar_inputs(db_path)
    id_column = "id" if "id" in companies.columns else "company_id"
    company_ids = sorted(companies[id_column].dropna().astype(str).unique().tolist())

    peer_groups: set[str] = set()
    companies_without_peer_group: list[str] = []
    generated_files: list[Path] = []

    for company_id in company_ids:
        series = build_radar_series(company_id, financial_ratios, peer_percentiles, companies)
        sanitized_company = re.sub(r"[^A-Za-z0-9]+", "_", company_id).strip("_")
        chart_name = f"{sanitized_company or 'company'}_radar.png"
        chart_path = output_dir / chart_name
        create_radar_chart(series, chart_path)
        generated_files.append(chart_path)

        if series["peer_group"] == DEFAULT_PEER_GROUP:
            companies_without_peer_group.append(company_id)
        else:
            peer_groups.add(series["peer_group"])

    execution_time = time.perf_counter() - start_time
    summary = summarize_radar_generation(
        charts_generated=len(generated_files),
        peer_groups=sorted(peer_groups),
        companies_without_peer_group=companies_without_peer_group,
        execution_time_seconds=execution_time,
    )

    summary_path = reports_dir / "radar_summary.md"
    summary_path.write_text(
        "\n".join(
            [
                "# Radar Chart Summary",
                "",
                f"- Charts Generated: {summary['charts_generated']}",
                f"- Peer Groups: {', '.join(summary['peer_groups']) if summary['peer_groups'] else 'None'}",
                f"- Companies Without Peer Group: {', '.join(summary['companies_without_peer_group']) if summary['companies_without_peer_group'] else 'None'}",
                f"- Execution Time: {summary['execution_time_seconds']}s",
            ]
        ),
        encoding="utf-8",
    )
    logger.info("Radar charts generated: %s", summary["charts_generated"])
    return summary
