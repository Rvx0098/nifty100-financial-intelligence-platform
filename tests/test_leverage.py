import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from leverage import asset_turnover, debt_to_equity, high_leverage_flag, interest_coverage, interest_coverage_label, net_debt


def test_debt_to_equity():
    assert debt_to_equity(50.0, 100.0, 50.0) == 0.33


def test_debt_to_equity_zero_borrowings():
    assert debt_to_equity(0.0, 100.0, 50.0) == 0.0


def test_interest_coverage():
    assert interest_coverage(100.0, 20.0, 10.0) == 12.0


def test_interest_coverage_zero_interest():
    assert interest_coverage(100.0, 20.0, 0.0) is None


def test_asset_turnover():
    assert asset_turnover(200.0, 100.0) == 2.0


def test_net_debt():
    assert net_debt(80.0, 20.0) == 60.0


def test_high_leverage_flag():
    assert high_leverage_flag(6.0) is True
    assert high_leverage_flag(4.0) is False


def test_interest_coverage_label():
    assert interest_coverage_label(0.0) == "Debt Free"
    assert interest_coverage_label(10.0) == ""
