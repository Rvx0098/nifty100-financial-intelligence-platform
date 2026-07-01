import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from populate_financial_ratios import build_population_frame, load_input_data


def test_build_population_frame_returns_columns():
    data_path = ROOT / "database" / "n100.db"
    raw_df = load_input_data(data_path)
    result_df = build_population_frame(raw_df)
    expected_columns = {
        "net_profit_margin_pct",
        "operating_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "net_debt",
        "free_cash_flow",
        "fcf_conversion",
        "capex_intensity",
        "cfo_quality_score",
        "composite_quality_score",
    }
    assert expected_columns.issubset(result_df.columns)
