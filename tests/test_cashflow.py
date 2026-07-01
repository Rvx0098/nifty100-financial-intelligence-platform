import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from cashflow_kpis import (
    calculate_capex_intensity,
    calculate_cfo_quality_score,
    calculate_fcf_conversion,
    calculate_free_cash_flow,
    classify_capital_allocation_pattern,
)


def test_calculate_free_cash_flow():
    assert calculate_free_cash_flow(120.0, 30.0) == 90.0


def test_calculate_free_cash_flow_negative():
    assert calculate_free_cash_flow(20.0, 50.0) == -30.0


def test_calculate_fcf_conversion():
    assert calculate_fcf_conversion(100.0, 50.0) == 200.0


def test_calculate_fcf_conversion_with_zero_profit():
    assert calculate_fcf_conversion(100.0, 0.0) is None


def test_calculate_capex_intensity():
    assert calculate_capex_intensity(20.0, 100.0) == 20.0


def test_calculate_capex_intensity_zero_sales():
    assert calculate_capex_intensity(20.0, 0.0) is None


def test_calculate_cfo_quality_score():
    assert calculate_cfo_quality_score(120.0, 100.0, 10.0) == 100.0


def test_classify_capital_allocation_pattern():
    assert classify_capital_allocation_pattern(100.0, 120.0, -20.0) == "(+, -, -)"
    assert classify_capital_allocation_pattern(100.0, 120.0, 20.0) == "(+, +, +)"
    assert classify_capital_allocation_pattern(-100.0, -120.0, 20.0) == "(-, -, +)"
    assert classify_capital_allocation_pattern(100.0, -120.0, 20.0) == "(+, -, +)"
