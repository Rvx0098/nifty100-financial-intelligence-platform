import sqlite3
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from visualization.radar_chart import (
    AXIS_DEFINITIONS,
    build_axis_labels,
    build_radar_series,
    create_radar_chart,
    generate_radar_charts,
    get_latest_company_metrics,
    load_radar_inputs,
    summarize_radar_generation,
)


def test_load_radar_inputs_reads_expected_tables():
    peer_percentiles, financial_ratios, companies = load_radar_inputs(ROOT / "database" / "n100.db")

    assert not peer_percentiles.empty
    assert not financial_ratios.empty
    assert not companies.empty
    assert {"company_id", "peer_group", "metric", "percentile_rank"}.issubset(peer_percentiles.columns)
    assert {"company_id", "year"}.issubset(financial_ratios.columns)
    assert {"id", "company_name"}.issubset(companies.columns)


def test_get_latest_company_metrics_returns_latest_snapshot_per_company():
    financial_ratios = pd.read_sql_query("SELECT * FROM financial_ratios", sqlite3.connect(ROOT / "database" / "n100.db"))

    latest = get_latest_company_metrics(financial_ratios)

    assert not latest.empty
    assert latest["company_id"].nunique() == latest.shape[0]
    assert {"company_id", "financial_year"}.issubset(latest.columns)


def test_build_radar_series_contains_all_requested_axes():
    peer_percentiles, financial_ratios, companies = load_radar_inputs(ROOT / "database" / "n100.db")
    series = build_radar_series("ABB", financial_ratios, peer_percentiles, companies)

    assert set(series.keys()) == {"company", "peer_average", "company_name", "peer_group", "company_values", "peer_values"}
    assert len(series["company_values"]) == len(AXIS_DEFINITIONS)
    assert len(series["peer_values"]) == len(AXIS_DEFINITIONS)


def test_build_radar_series_uses_nifty_average_when_peer_group_missing():
    peer_percentiles, financial_ratios, companies = load_radar_inputs(ROOT / "database" / "n100.db")
    series = build_radar_series("MISSING-COMPANY", financial_ratios, peer_percentiles, companies)

    assert series["peer_group"] == "Nifty100 average"
    assert all(isinstance(value, float) for value in series["peer_values"])


def test_create_radar_chart_writes_png_file(tmp_path):
    peer_percentiles, financial_ratios, companies = load_radar_inputs(ROOT / "database" / "n100.db")
    series = build_radar_series("ABB", financial_ratios, peer_percentiles, companies)
    output_path = tmp_path / "ABB_radar.png"

    result_path = create_radar_chart(series, output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generate_radar_charts_creates_expected_outputs(tmp_path):
    report_dir = tmp_path / "reports"
    chart_dir = tmp_path / "reports" / "radar_charts"
    summary = generate_radar_charts(
        db_path=ROOT / "database" / "n100.db",
        output_dir=chart_dir,
        reports_dir=report_dir,
    )

    assert summary["charts_generated"] == summary["company_count"]
    assert chart_dir.exists()
    assert (report_dir / "radar_summary.md").exists()
    assert len(list(chart_dir.glob("*_radar.png"))) == summary["charts_generated"]


def test_generate_radar_charts_reports_peer_groups_and_missing_groups(tmp_path):
    report_dir = tmp_path / "reports"
    summary = generate_radar_charts(
        db_path=ROOT / "database" / "n100.db",
        output_dir=tmp_path / "reports" / "radar_charts",
        reports_dir=report_dir,
    )

    assert summary["peer_groups"]
    assert isinstance(summary["companies_without_peer_group"], list)


def test_build_axis_labels_are_readable():
    labels = build_axis_labels()

    assert labels[0] == "ROE"
    assert labels[1] == "ROCE"
    assert labels[-1] == "Composite Score"


def test_summarize_radar_generation_contains_expected_sections():
    summary = summarize_radar_generation(charts_generated=10, peer_groups=["Banks"], companies_without_peer_group=["ABC"], execution_time_seconds=1.23)

    assert summary["charts_generated"] == 10
    assert summary["peer_groups"] == ["Banks"]
    assert summary["companies_without_peer_group"] == ["ABC"]
    assert summary["execution_time_seconds"] == 1.23


def test_generate_radar_charts_returns_execution_time_positive(tmp_path):
    summary = generate_radar_charts(
        db_path=ROOT / "database" / "n100.db",
        output_dir=tmp_path / "reports" / "radar_charts",
        reports_dir=tmp_path / "reports",
    )

    assert summary["execution_time_seconds"] >= 0
