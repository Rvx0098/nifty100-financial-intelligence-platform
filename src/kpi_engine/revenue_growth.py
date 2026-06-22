"""
Revenue Growth KPI calculations and analysis module.

This module provides functions to calculate revenue growth metrics,
trends, and year-over-year comparisons.
"""


def calculate_revenue_growth(current_revenue, previous_revenue):
    """
    Calculate revenue growth rate.
    
    Args:
        current_revenue: Current period revenue
        previous_revenue: Previous period revenue
        
    Returns:
        float: Revenue growth rate as percentage
    """
    if previous_revenue == 0:
        return None
    return ((current_revenue - previous_revenue) / previous_revenue) * 100


def calculate_cagr(ending_value, beginning_value, num_years):
    """
    Calculate Compound Annual Growth Rate (CAGR).
    
    Args:
        ending_value: Final value
        beginning_value: Initial value
        num_years: Number of years
        
    Returns:
        float: CAGR as percentage
    """
    if beginning_value <= 0 or num_years <= 0:
        return None
    return ((ending_value / beginning_value) ** (1 / num_years) - 1) * 100
