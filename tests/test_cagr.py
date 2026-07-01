import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "analytics"))

from cagr import calculate_cagr


@pytest.mark.parametrize(
    "start_value,end_value,years,expected_value,expected_flag",
    [
        (100.0, 121.0, 2, 10.0, "NORMAL"),
        (100.0, 133.1, 3, 10.0, "NORMAL"),
        (100.0, 0.0, 2, None, "ZERO_BASE"),
        (100.0, -50.0, 2, None, "DECLINE_TO_LOSS"),
        (-100.0, 50.0, 2, None, "TURNAROUND"),
        (-100.0, -80.0, 2, None, "BOTH_NEGATIVE"),
        (100.0, 121.0, 0, None, "INSUFFICIENT_DATA"),
        (None, 121.0, 2, None, "INSUFFICIENT_DATA"),
    ],
)
def test_calculate_cagr_edge_cases(start_value, end_value, years, expected_value, expected_flag):
    value, flag = calculate_cagr(start_value, end_value, years)
    assert value == expected_value
    assert flag == expected_flag
