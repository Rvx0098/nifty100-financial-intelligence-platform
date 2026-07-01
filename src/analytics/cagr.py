"""Production-grade CAGR calculations for the N100 Financial Intelligence Platform."""

from __future__ import annotations

from typing import Optional, Tuple


def calculate_cagr(
    start_value: Optional[float],
    end_value: Optional[float],
    years: int,
) -> Tuple[Optional[float], str]:
    """Calculate CAGR and classify edge cases for a start/end pair.

    The function returns both a numeric CAGR value and a descriptive flag so the
    analytics pipeline can distinguish normal growth from common edge cases.
    """
    if years is None or years <= 0:
        return None, "INSUFFICIENT_DATA"

    if start_value is None or end_value is None:
        return None, "INSUFFICIENT_DATA"

    if start_value == 0 and end_value == 0:
        return None, "ZERO_BASE"

    if start_value == 0 and end_value > 0:
        return None, "ZERO_BASE"

    if start_value == 0 and end_value < 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value >= 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    if end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value > 0 and end_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0 and start_value < end_value:
        value = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(value, 2), "NORMAL"

    if start_value > 0 and end_value > 0 and start_value > end_value:
        value = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(value, 2), "DECLINE"

    return None, "INSUFFICIENT_DATA"
