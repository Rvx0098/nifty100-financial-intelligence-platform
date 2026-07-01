import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from ratios import net_profit_margin, operating_profit_margin, return_on_assets, return_on_capital_employed, return_on_equity


def test_net_profit_margin():
    assert net_profit_margin(50.0, 200.0) == 25.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(50.0, 0.0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(40.0, 200.0) == 20.0


def test_return_on_equity():
    assert return_on_equity(30.0, 100.0, 50.0) == 20.0


def test_return_on_equity_zero_equity():
    assert return_on_equity(30.0, 0.0, 0.0) is None


def test_return_on_assets():
    assert return_on_assets(30.0, 150.0) == 20.0


def test_return_on_capital_employed():
    assert return_on_capital_employed(40.0, 100.0, 50.0, 50.0) == 20.0
